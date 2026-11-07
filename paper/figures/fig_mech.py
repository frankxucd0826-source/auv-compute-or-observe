"""Figure 5: why one-step metareasoning loses and what rehearsal does instead (148 test missions,
main truth model). (a) share of 20-minute intervals with the high-performance computer on and
(b) share spent stopped, for one-step metareasoning (values computation on the searched imagined
oceans), the same controller valuing on held-out oceans, and rehearsal; (c) which strategy rehearsal
picks, by vehicle.
Data: results/rev2_summary.json
"""
import json
import sys

import style as S
from style import plt

sys.path.insert(0, str(S.ROOT / "paper"))
from terms import VEHICLE  # noqa: E402

S.setup()
R = json.load(open(S.ROOT / "results" / "rev2_summary.json", encoding="utf-8"))["main"]["sat+"]
_dp = S.ROOT / "results" / "rev2_diag_summary.json"
DIAG = json.load(open(_dp, encoding="utf-8")) if _dp.exists() else {}
V = ["weak", "moderate", "strong", "efficient"]
fig, ax = plt.subplots(1, 3, figsize=(S.TEXTW, 62 * S.MM), gridspec_kw=dict(width_ratios=[1, 1, 1.25]))
fig.subplots_adjust(left=0.115, right=0.965, top=0.78 if DIAG else 0.83, bottom=0.25, wspace=0.12)
ys = list(range(len(V)))
for k, (key, title) in enumerate((("think", "(a) 开着高功耗芯片的时段占比"), ("stopped", "(b) 停下漂流的时段占比"))):
    a = ax[k]
    for y, v in zip(ys, V):
        r = R.get(v, {})
        pts = [(r.get("meta_shares"), S.META, "o"), (r.get("double_shares"), S.META_HELD, "o"),
               (r.get("rehearsal_shares"), S.REHEARSAL, "D")]
        xs = [p[key] * 100 for p, _, _ in pts if p]
        if len(xs) > 1:
            a.plot([min(xs), max(xs)], [y, y], color="#CED4DA", lw=2.2, zorder=1)
        for p, c, mk in pts:
            if p:
                a.plot(p[key] * 100, y, mk, ms=6.8 if mk == "o" else 6.2, color=c, mec="white", mew=0.8, zorder=3)
        # one change at a time (slow and moderate computers): valuation only / decision rule only
        dg = DIAG.get(v, {})
        for name, c, mk in (("double-noguard", S.META_HELD, "s"), ("rational-guard", S.META, "^")):
            if name in dg and key in dg[name]:
                a.plot(dg[name][key] * 100, y + 0.22, mk, ms=5.2, color="white", mec=c, mew=1.3, zorder=3)
    a.set_xlim(-4, 104)
    a.set_xticks([0, 25, 50, 75, 100], ["0", "25%", "50%", "75%", "100%"])
    a.set_ylim(len(V) - 0.5, -0.5)
    a.set_yticks(ys, [VEHICLE[v] for v in V] if k == 0 else [])
    a.tick_params(axis="y", length=0)
    a.grid(axis="y", visible=False)
    S.caption(a, title, y=-0.20)
h = [ax[0].plot([], [], "o", ms=6.5, color=S.META, label="单步元推理")[0],
     ax[0].plot([], [], "o", ms=6.5, color=S.META_HELD, label="单步元推理（留出估值）")[0],
     ax[0].plot([], [], "D", ms=6, color=S.REHEARSAL, label="出发前预演（本文）")[0]]
if DIAG:
    h += [ax[0].plot([], [], "s", ms=5.2, color="white", mec=S.META_HELD, mew=1.3, label="只改为留出估值")[0],
          ax[0].plot([], [], "^", ms=5.2, color="white", mec=S.META, mew=1.3, label="只加保守的切换规则")[0]]
fig.legend(handles=h, loc="upper center", ncol=3, bbox_to_anchor=(0.36, 1.03), fontsize=7.6, columnspacing=1.0,
           handletextpad=0.3)
# (c) what rehearsal picks
a = ax[2]
order = [("go", "一直走", S.GO), ("think 1 in 3", "三段深想一段", S.THINK3), ("think", "一直深想", S.THINK),
         ("stop", "停下类策略", S.STOP)]
for y, v in zip(ys, V):
    ch = dict(R.get(v, {}).get("choice") or {})
    ch["stop"] = ch.pop("stop and think 1 in 3", 0) + ch.pop("stop and resample 1 in 3", 0)
    left = 0.0
    for key, lab, c in order:
        w = ch.get(key, 0.0) * 100
        a.barh(y, w, left=left, color=c, height=0.62, edgecolor="white", lw=0.8)
        if w >= 9:
            a.text(left + w / 2, y, f"{w:.0f}%", ha="center", va="center", fontsize=7.4,
                   color="white" if key in ("go", "think", "stop") else S.INK)
        left += w
a.set_xlim(0, 100)
a.set_xticks([0, 50, 100], ["0", "50%", "100%"])
a.set_ylim(len(V) - 0.5, -0.5)
a.set_yticks(ys, [])
a.grid(False)
for sp in ("left", "bottom"):
    a.spines[sp].set_visible(False)
a.tick_params(length=0)
hh = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in order]
a.legend(hh, [lab for _, lab, _ in order], loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=7.4,
         handlelength=1.0, columnspacing=0.8, handletextpad=0.3, borderaxespad=0.2)
S.caption(a, "(c) 出发前预演选出的策略", y=-0.20)
S.save(fig, "fig_mech")
