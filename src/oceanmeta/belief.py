"""Ensemble belief over a gridded ocean field (log10 chlorophyll), updated by a serial
ensemble adjustment Kalman filter (Anderson 2001) with Gaspari-Cohn localization."""
import numpy as np


def gaussian_random_fields(n, ny, nx, length, rng):
    """n unit-variance stationary Gaussian fields with squared-exponential covariance
    exp(-r^2 / (2 length^2)), length in cells. FFT on a grid padded by 3 lengths."""
    pad = int(np.ceil(3 * length))
    Ny, Nx = ny + 2 * pad, nx + 2 * pad
    ky = np.fft.fftfreq(Ny)[:, None]
    kx = np.fft.rfftfreq(Nx)[None, :]
    spec = np.exp(-2 * (np.pi * length) ** 2 * (kx ** 2 + ky ** 2))
    amp = np.sqrt(spec)
    noise = rng.standard_normal((n, Ny, Nx))
    f = np.fft.irfft2(np.fft.rfft2(noise) * amp, s=(Ny, Nx))
    f = f[:, pad:pad + ny, pad:pad + nx]
    f /= f.reshape(n, -1).std(axis=1).mean()
    return f


def gaspari_cohn(r):
    """Gaspari-Cohn fifth-order taper; r = distance / half-width, zero beyond r = 2."""
    r = np.abs(r)
    out = np.zeros_like(r)
    a = r <= 1
    b = (r > 1) & (r < 2)
    ra = r[a]
    out[a] = -0.25 * ra**5 + 0.5 * ra**4 + 0.625 * ra**3 - 5 / 3 * ra**2 + 1
    rb = r[b]
    out[b] = rb**5 / 12 - 0.5 * rb**4 + 0.625 * rb**3 + 5 / 3 * rb**2 - 5 * rb + 4 - 2 / (3 * rb)
    return out


class EnsembleBelief:
    """members: (N, ny, nx) array of plausible fields. Land cells hold NaN-free filler and are
    never observed or planned through (mask)."""

    def __init__(self, members, mask, loc_halfwidth, inflation=1.0):
        self.X = np.ascontiguousarray(members, dtype=np.float64)
        self.N, self.ny, self.nx = self.X.shape
        self.mask = mask
        self.c = loc_halfwidth
        self.inflation = inflation
        yy, xx = np.mgrid[0:self.ny, 0:self.nx]
        self._yy, self._xx = yy, xx

    @classmethod
    def from_prior(cls, mean, sd, length, n, mask, rng, loc_factor=2.0):
        pert = gaussian_random_fields(n, *mean.shape, length, rng)
        sd = np.broadcast_to(sd, mean.shape)
        X = mean[None] + sd[None] * pert
        return cls(X, mask, loc_halfwidth=loc_factor * length)

    def mean(self):
        return self.X.mean(axis=0)

    def std(self):
        return self.X.std(axis=0, ddof=1)

    def loc_row(self, iy, ix):
        r = np.hypot(self._yy - iy, self._xx - ix) / self.c
        return gaspari_cohn(r)

    def update(self, iy, ix, y, r, loc=None):
        """Assimilate one observation y of cell (iy, ix) with error variance r."""
        hx = self.X[:, iy, ix].copy()
        mu = hx.mean()
        var = hx.var(ddof=1)
        if var <= 1e-12:
            return
        post_var = 1.0 / (1.0 / var + 1.0 / r)
        post_mu = post_var * (mu / var + y / r)
        alpha = np.sqrt(post_var / var)
        dy = post_mu + alpha * (hx - mu) - hx
        Xa = self.X - self.X.mean(axis=0)
        cov = np.tensordot(hx - mu, Xa, axes=(0, 0)) / (self.N - 1)
        if loc is None:
            loc = self.loc_row(iy, ix)
        beta = cov / var * loc
        self.X += dy[:, None, None] * beta[None]

    def update_many(self, cells, values, r):
        for (iy, ix), y in zip(cells, values):
            self.update(iy, ix, y, r)
        if self.inflation != 1.0:
            m = self.X.mean(axis=0)
            self.X = m + self.inflation * (self.X - m)

    def copy(self):
        b = EnsembleBelief.__new__(EnsembleBelief)
        b.__dict__.update(self.__dict__)
        b.X = self.X.copy()
        return b
