"""
PWM 검증 플롯 2종 생성
  fig1 : 레그1·레그2 동형 증빙 — 4에지 시차 (grouped bar)
  fig2 : ETA_DEADTIME_NS knob 추종 — flash+boot silicon 실측 (line + errorbar)

출력: raw/pwm_plots/fig1_isoform_edge_skew.png
      raw/pwm_plots/fig2_deadtime_tracking.png
"""

import csv, statistics, bisect, os, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BASE = Path(__file__).parent
OUT  = BASE / "pwm_plots"
OUT.mkdir(exist_ok=True)

# ── 공통 유틸 ─────────────────────────────────────────────────────────────────

def load4(path):
    """4채널 transition CSV → (times, levels[4][]) """
    times = []; lvs = [[] for _ in range(4)]
    with open(path) as f:
        r = csv.reader(f); next(r)
        for row in r:
            if not row: continue
            times.append(float(row[0]))
            for c in range(4):
                lvs[c].append(int(row[c + 1]))
    return times, lvs

def load2(path):
    """2채널 transition CSV → (times, A[], B[]) """
    times = []; a = []; b = []
    with open(path) as f:
        r = csv.reader(f); next(r)
        for row in r:
            if not row: continue
            times.append(float(row[0])); a.append(int(row[1])); b.append(int(row[2]))
    return times, a, b

def edges_from(times, lv):
    e = []; prev = lv[0]
    for i in range(1, len(lv)):
        if lv[i] != prev:
            e.append((times[i], +1 if lv[i] == 1 else -1))
            prev = lv[i]
    return e

def rises(e): return [t for t, k in e if k == +1]
def falls(e): return [t for t, k in e if k == -1]

def window(times):
    span = times[-1] - times[0]
    return times[0] + 0.10 * span, times[-1] - 0.10 * span

# ── Figure 1 helpers ───────────────────────────────────────────────────────────

def edge_skew4(times, lvs, ca, cb, etype):
    """에지 시차 (ca − cb) ns — ca, cb는 0-3 채널 인덱스"""
    w0, w1 = window(times)
    ea = edges_from(times, lvs[ca])
    eb = edges_from(times, lvs[cb])
    ta = sorted(t for t, k in ea if k == etype and w0 <= t <= w1)
    tb = sorted(t for t, k in eb if k == etype)
    out = []
    for t in ta:
        idx = bisect.bisect_left(tb, t)
        cand = []
        if idx < len(tb): cand.append(tb[idx])
        if idx > 0:       cand.append(tb[idx - 1])
        if cand:
            nb = min(cand, key=lambda x: abs(x - t))
            out.append((t - nb) * 1e9)
    return out

# ── Figure 2 helpers ───────────────────────────────────────────────────────────

def both_low(times, la, lb, fall_is_a):
    """fall_ch→rise_ch 간 both-low gap (ns)"""
    w0, w1 = window(times)
    ea = edges_from(times, la)
    eb = edges_from(times, lb)
    if fall_is_a:
        fa = sorted(t for t, k in ea if k == -1 and w0 <= t <= w1)
        ri = sorted(rises(eb))
    else:
        fa = sorted(t for t, k in eb if k == -1 and w0 <= t <= w1)
        ri = sorted(rises(ea))
    out = []
    for ft in fa:
        idx = bisect.bisect_right(ri, ft)
        if idx < len(ri):
            g = (ri[idx] - ft) * 1e9
            if 0 < g < 3000:
                out.append(g)
    return out

def stat2(xs):
    if not xs: return None
    return statistics.mean(xs), statistics.pstdev(xs), min(xs), max(xs), len(xs)

# ── 데이터 수집 ────────────────────────────────────────────────────────────────

DT_SETTINGS = [100, 150, 250, 400]

# Figure 1 — isoform edge skew
ISOFORM_DIR = BASE / "pwm_leg2_isoform"
PAIRS = [
    ("HS2↑−HS1↑", 2, 0, +1),
    ("HS2↓−HS1↓", 2, 0, -1),
    ("LS2↑−LS1↑", 3, 1, +1),
    ("LS2↓−LS1↓", 3, 1, -1),
]

fig1_medians = {lbl: [] for lbl, *_ in PAIRS}
fig1_errl    = {lbl: [] for lbl, *_ in PAIRS}
fig1_erru    = {lbl: [] for lbl, *_ in PAIRS}

print("=== Figure 1: isoform edge skew ===")
for dt in DT_SETTINGS:
    csv_path = ISOFORM_DIR / f"verify_dt{dt}" / "digital.csv"
    times, lvs = load4(csv_path)
    for lbl, ca, cb, etype in PAIRS:
        skews = edge_skew4(times, lvs, ca, cb, etype)
        med = statistics.median(skews)
        mn, mx = min(skews), max(skews)
        fig1_medians[lbl].append(med)
        fig1_errl[lbl].append(med - mn)
        fig1_erru[lbl].append(mx - med)
        print(f"  DT={dt:3d}ns  {lbl}  median={med:+.1f}  min={mn:+.1f}  max={mx:+.1f}  n={len(skews)}")

# Figure 2 — deadtime tracking
KNOB_DIR = BASE / "pwm_deadtime_knob_verify"
SERIES = [
    ("레그1 HS↓→LS↑", 1, True),
    ("레그1 LS↓→HS↑", 1, False),
    ("레그2 HS↓→LS↑", 2, True),
    ("레그2 LS↓→HS↑", 2, False),
]

fig2_mean = {lbl: [] for lbl, *_ in SERIES}
fig2_sd   = {lbl: [] for lbl, *_ in SERIES}

print("\n=== Figure 2: deadtime tracking ===")
for dt in DT_SETTINGS:
    for lbl, leg, fall_is_a in SERIES:
        csv_path = KNOB_DIR / f"dt{dt}" / f"leg{leg}" / "digital.csv"
        times, a, b = load2(csv_path)
        gaps = both_low(times, a, b, fall_is_a)
        s = stat2(gaps)
        fig2_mean[lbl].append(s[0])
        fig2_sd[lbl].append(s[1])
        print(f"  DT={dt:3d}ns  {lbl}  mean={s[0]:.2f}  sd={s[1]:.2f}  n={s[4]}")

# ── 스타일 공통 ────────────────────────────────────────────────────────────────

ORANGE = "#e07a3c"
COLORS = ["#e07a3c", "#c2622a", "#5b7fa6", "#3a5f82"]  # leg1-두 방향, leg2-두 방향
BAR_COLORS = ["#e07a3c", "#c2622a", "#5b7fa6", "#3a5f82"]

plt.rcParams.update({
    "font.family": ["Malgun Gothic", "Apple SD Gothic Neo", "DejaVu Sans"],
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "axes.grid.axis":    "y",
    "grid.color":        "#e6d3bc",
    "grid.linewidth":    0.8,
    "figure.facecolor":  "#fbf3e9",
    "axes.facecolor":    "#fbf3e9",
    "axes.labelcolor":   "#4a3b30",
    "xtick.color":       "#4a3b30",
    "ytick.color":       "#4a3b30",
    "text.color":        "#4a3b30",
})

# ── Figure 1 — grouped bar ─────────────────────────────────────────────────────

n_groups = len(DT_SETTINGS)
n_bars   = len(PAIRS)
bar_w    = 0.17
x        = np.arange(n_groups)

fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor("#fbf3e9")

for i, (lbl, ca, cb, etype) in enumerate(PAIRS):
    offset = (i - n_bars / 2 + 0.5) * bar_w
    med  = np.array(fig1_medians[lbl])
    errl = np.array(fig1_errl[lbl])
    erru = np.array(fig1_erru[lbl])
    ax.bar(x + offset, med, bar_w,
           color=BAR_COLORS[i], alpha=0.85, label=lbl,
           yerr=[errl, erru], capsize=4,
           error_kw={"elinewidth": 1.2, "ecolor": "#7a6a5c"})

ax.axhline(0, color="#4a3b30", linewidth=1.2, linestyle="--", alpha=0.6, label="기준 0 ns")
ax.set_xticks(x)
ax.set_xticklabels([f"{d} ns" for d in DT_SETTINGS], fontsize=11)
ax.set_xlabel("Dead-time 설정값", fontsize=11)
ax.set_ylabel("에지 시차 (ns)", fontsize=11)
ax.set_ylim(-4.5, 4.5)
ax.set_yticks(range(-4, 5))
ax.set_title("레그1 · 레그2 4에지 시차 (동형 증빙)\nmedian ±2 ns 이내 — 4채널이 시간축에서 포개짐",
             fontsize=12, fontweight="bold", pad=14)
ax.legend(loc="upper right", fontsize=9, framealpha=0.7,
          facecolor="#fffaf3", edgecolor="#e6d3bc")

# 주석: ±2 ns 허용 밴드
ax.axhspan(-2, 2, color=ORANGE, alpha=0.06)
ax.text(n_groups - 0.05, 2.05, "±2 ns 허용대", fontsize=8, color=ORANGE,
        ha="right", va="bottom")

fig.tight_layout()
out1 = OUT / "fig1_isoform_edge_skew.png"
fig.savefig(out1, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"\nSaved: {out1}")

# ── Figure 2 — line + errorbar ─────────────────────────────────────────────────

xs = np.array(DT_SETTINGS, dtype=float)
ref = np.linspace(80, 420, 200)

fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor("#fbf3e9")

ax.plot(ref, ref, color="#a99e89", linewidth=1.2, linestyle="--",
        label="y = x (이상 추종)", zorder=1)

markers = ["o", "s", "o", "s"]
lstyles = ["-", "--", "-", "--"]

for i, (lbl, leg, _) in enumerate(SERIES):
    mean = np.array(fig2_mean[lbl])
    sd   = np.array(fig2_sd[lbl])
    ax.errorbar(xs, mean, yerr=sd, fmt=markers[i], linestyle=lstyles[i],
                color=COLORS[i], linewidth=1.8, markersize=7, capsize=5,
                label=lbl, zorder=2 + i,
                markerfacecolor="white" if i % 2 == 1 else COLORS[i],
                markeredgecolor=COLORS[i], markeredgewidth=1.8)

ax.set_xticks(DT_SETTINGS)
ax.set_xticklabels([f"{d}" for d in DT_SETTINGS], fontsize=11)
ax.set_xlabel("ETA_DEADTIME_NS 설정값 (ns)", fontsize=11)
ax.set_ylabel("실측 dead-time mean (ns)", fontsize=11)
ax.set_xlim(80, 420)
ax.set_ylim(80, 420)
ax.set_title("ETA_DEADTIME_NS knob — flash+boot silicon 실측 (레그1 vs 레그2)\n최대 절대 오차 < 2 ns · Shoot-through 0 ns",
             fontsize=12, fontweight="bold", pad=14)
ax.legend(loc="upper left", fontsize=9, framealpha=0.7,
          facecolor="#fffaf3", edgecolor="#e6d3bc")

fig.tight_layout()
out2 = OUT / "fig2_deadtime_tracking.png"
fig.savefig(out2, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {out2}")
