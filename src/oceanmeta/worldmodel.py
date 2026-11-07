"""A latent world model of the East China Sea surface learned from satellite data.

Each daily frame (log10 chlorophyll, sea surface temperature, land mask) is cut into 8 x 8
pixel tokens and encoded by a small vision transformer. A predictor transformer reads the
tokens of the three most recent available days (some tokens dropped, like clouds) and
predicts the tokens of a day 1-3 days ahead. Training follows the joint-embedding predictive
architecture (JEPA): the predicted tokens are matched to the tokens a slowly updated (EMA)
copy of the encoder gives the real future frame, so the model learns what is predictable
without having to reproduce pixel noise. A light decoder turns the predicted tokens into a
forecast mean and standard deviation of log10 chlorophyll, which become the vehicle's prior.
"""
import copy
import math

import torch
import torch.nn as nn
import torch.nn.functional as F

P = 8            # token size in pixels
HIST = 3         # number of past frames read
C_IN = 3         # channels per frame: log10 chl, SST anomaly, ocean mask


class Block(nn.Module):
    def __init__(self, d, heads, mlp=4.0, drop=0.0):
        super().__init__()
        self.n1 = nn.LayerNorm(d)
        self.att = nn.MultiheadAttention(d, heads, dropout=drop, batch_first=True)
        self.n2 = nn.LayerNorm(d)
        self.mlp = nn.Sequential(nn.Linear(d, int(d * mlp)), nn.GELU(), nn.Linear(int(d * mlp), d))

    def forward(self, x):
        h = self.n1(x)
        x = x + self.att(h, h, h, need_weights=False)[0]
        return x + self.mlp(self.n2(x))


def sincos_2d(n_side, d):
    """Fixed 2-D sine-cosine position codes for an n_side x n_side token grid."""
    y, x = torch.meshgrid(torch.arange(n_side), torch.arange(n_side), indexing="ij")
    omega = 1.0 / (10000 ** (torch.arange(d // 4) / (d // 4)))
    out = []
    for g in (y.flatten(), x.flatten()):
        a = g[:, None].float() * omega[None]
        out += [torch.sin(a), torch.cos(a)]
    return torch.cat(out, 1)


class Encoder(nn.Module):
    def __init__(self, img=64, d=192, depth=6, heads=6):
        super().__init__()
        self.n_side = img // P
        self.embed = nn.Conv2d(C_IN, d, P, P)
        self.register_buffer("pos", sincos_2d(self.n_side, d)[None], persistent=False)
        self.blocks = nn.ModuleList([Block(d, heads) for _ in range(depth)])
        self.norm = nn.LayerNorm(d)

    def forward(self, frame, keep=None):
        """frame: (B, C_IN, H, W) -> tokens (B, T, d). keep: (B, T) bool, tokens to encode."""
        x = self.embed(frame).flatten(2).transpose(1, 2) + self.pos
        if keep is not None:
            x = x[keep].view(x.shape[0], -1, x.shape[-1])
        for b in self.blocks:
            x = b(x)
        return self.norm(x)


class Predictor(nn.Module):
    def __init__(self, n_side=8, d=192, dp=192, depth=6, heads=6, max_lead=3):
        super().__init__()
        self.inp = nn.Linear(d, dp)
        self.register_buffer("pos", sincos_2d(n_side, dp)[None], persistent=False)
        self.time = nn.Embedding(HIST, dp)          # which past frame a token comes from
        self.lead = nn.Embedding(max_lead + 1, dp)  # how far ahead the query asks
        self.query = nn.Parameter(torch.zeros(1, 1, dp))
        self.blocks = nn.ModuleList([Block(dp, heads) for _ in range(depth)])
        self.norm = nn.LayerNorm(dp)
        self.out = nn.Linear(dp, d)
        nn.init.normal_(self.query, std=0.02)

    def forward(self, ctx, ctx_pos, ctx_time, lead):
        """ctx: (B, Tc, d) context tokens, ctx_pos: (B, Tc) token index, ctx_time: (B, Tc),
        lead: (B,) days ahead. Returns predicted tokens for the whole future frame (B, T, d)."""
        B = ctx.shape[0]
        T = self.pos.shape[1]
        pos = self.pos.expand(B, -1, -1)
        c = self.inp(ctx) + torch.gather(pos, 1, ctx_pos[..., None].expand(-1, -1, pos.shape[-1])) \
            + self.time(ctx_time)
        q = self.query.expand(B, T, -1) + pos + self.lead(lead)[:, None]
        x = torch.cat([c, q], 1)
        for b in self.blocks:
            x = b(x)
        return self.out(self.norm(x[:, -T:]))


class Decoder(nn.Module):
    """Predicted tokens -> forecast mean and log standard deviation, 8 x 8 pixels per token."""

    def __init__(self, d=192, n_side=8):
        super().__init__()
        self.n_side = n_side
        self.mlp = nn.Sequential(nn.Linear(d, d), nn.GELU(), nn.Linear(d, 2 * P * P))

    def forward(self, tok, last_chl):
        B = tok.shape[0]
        y = self.mlp(tok).view(B, self.n_side, self.n_side, 2, P, P)
        y = y.permute(0, 3, 1, 4, 2, 5).reshape(B, 2, self.n_side * P, self.n_side * P)
        mean = last_chl + y[:, 0]          # forecast the change from the latest map
        log_sd = y[:, 1].clamp(-4, 1.5)
        return mean, log_sd


class WorldModel(nn.Module):
    def __init__(self, img=64, d=192, depth=6, heads=6, ema=0.996):
        super().__init__()
        self.enc = Encoder(img, d, depth, heads)
        self.target_enc = copy.deepcopy(self.enc)
        for p in self.target_enc.parameters():
            p.requires_grad = False
        self.pred = Predictor(img // P, d, d, depth, heads)
        self.dec = Decoder(d, img // P)
        self.ema = ema

    @torch.no_grad()
    def update_target(self):
        for pt, p in zip(self.target_enc.parameters(), self.enc.parameters()):
            pt.mul_(self.ema).add_(p.detach(), alpha=1 - self.ema)

    def context(self, frames, drop=0.0):
        """frames: (B, HIST, C_IN, H, W). Encode each frame, drop a fraction of tokens."""
        B = frames.shape[0]
        toks, pos, tim = [], [], []
        T = self.enc.n_side ** 2
        n_keep = T - int(drop * T)
        for h in range(HIST):
            if drop > 0:
                perm = torch.rand(B, T, device=frames.device).argsort(1)[:, :n_keep]
                keep = torch.zeros(B, T, dtype=torch.bool, device=frames.device)
                keep.scatter_(1, perm, True)
                idx = keep.nonzero()[:, 1].view(B, n_keep)
            else:
                keep = None
                idx = torch.arange(T, device=frames.device).expand(B, -1)
            toks.append(self.enc(frames[:, h], keep))
            pos.append(idx)
            tim.append(torch.full_like(idx, h))
        return torch.cat(toks, 1), torch.cat(pos, 1), torch.cat(tim, 1)

    def forward(self, frames, lead, drop=0.0):
        ctx, pos, tim = self.context(frames, drop)
        pred = self.pred(ctx, pos, tim, lead)
        mean, log_sd = self.dec(pred, frames[:, -1, 0])
        return pred, mean, log_sd

    def loss(self, frames, target_frame, lead, drop=0.25, w_latent=1.0):
        """JEPA latent loss + Gaussian negative log-likelihood of the decoded forecast on
        ocean pixels of the target day."""
        pred, mean, log_sd = self(frames, lead, drop)
        with torch.no_grad():
            tgt = self.target_enc(target_frame)
            tgt = F.layer_norm(tgt, tgt.shape[-1:])
        l_lat = F.smooth_l1_loss(F.layer_norm(pred, pred.shape[-1:]), tgt)
        y = target_frame[:, 0]
        ocean = target_frame[:, 2] > 0.5
        nll = (log_sd + 0.5 * ((y - mean) / log_sd.exp()) ** 2)[ocean].mean()
        return w_latent * l_lat + nll, dict(latent=l_lat.item(), nll=nll.item())
