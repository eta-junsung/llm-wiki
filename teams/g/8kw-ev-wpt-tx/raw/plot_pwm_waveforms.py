"""
PWM 파형 줌 플롯 2종 생성
  fig3 : Dead-time 파형 줌 (4 rows x 4 cols) — both-LOW 구간 음영
  fig4 : Isoform 파형 줌 (2 rows x 4 cols) — Leg1 vs Leg2 직접 비교

출력: raw/pwm_plots/fig3_deadtime_waveforms.png
      raw/pwm_plots/fig4_isoform_waveforms.png
"""

import csv, bisect, statistics, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).parent
OUT  = BASE / "pwm_plots"
OUT.mkdir(exist_ok=True)

# ── CSV 로드 ──────────────────────────────────────────────────────────────────

def load2(path):
    times, la, lb = [], [], []
    with open(path) as f:
        r = csv.reader(f); next(r)
        for row in r:
            if not row: continue
            times.append(float(row[0])); la.append(int(row[1])); lb.append(int(row[2]))
    return times, la, lb

def load4(path):
    times = []; lvs = [[], [], [], []]
    with open(path) as f:
        r = csv.reader(f); next(r)
        for row in r:
            if not row: continue
            times.append(float(row[0]))
            for c in range(4): lvs[c].append(int(row[c + 1]))
    return times, lvs

def ch_trans(times, levels_list):
    """levels_list: single channel's level array → [(time, level)] transition list"""
    result = [(times[0], levels_list[0])]
    prev = levels_list[0]
    for i in range(1, len(times)):
        v = levels_list[i]
        if v != prev:
            result.append((times[i], v))
            prev = v
    return result

# ── 스텝 파형 재구성 ─────────────────────────────────────────────────────────

def make_step(trans, t0, t1, t_ref=None):
    """trans: [(time_s, level)] → (xs_ns_relative, ys) step arrays over [t0, t1].
    xs are relative to t_ref (defaults to t0 so x=0 at zoom window start)."""
    if t_ref is None:
        t_ref = t0
    level = trans[0][1]
    for t, v in trans:
        if t <= t0:
            level = v
    def ns(t): return (t - t_ref) * 1e9
    xs = [ns(t0)]; ys = [float(level)]
    for t, v in trans:
        if t0 < t <= t1:
            xs.append(ns(t)); ys.append(ys[-1])
            xs.append(ns(t)); ys.append(float(v))
    xs.append(ns(t1)); ys.append(ys[-1])
    return np.array(xs), np.array(ys)

# ── 커뮤테이션 이벤트 탐색 ────────────────────────────────────────────────────

def find_gap_events(trans_fall_ch, trans_rise_ch, w0, w1):
    """fall_ch 하강 → rise_ch 상승 이벤트 목록 반환 [(t_fall, t_rise)]"""
    falls = [t for t, v in trans_fall_ch if v == 0 and w0 <= t <= w1]
    rises = sorted(t for t, v in trans_rise_ch if v == 1)
    out = []
    for tf in falls:
        idx = bisect.bisect_right(rises, tf)
        if idx < len(rises):
            tr = rises[idx]
            g = (tr - tf) * 1e9
            if 0 < g < 3000:
                out.append((tf, tr))
    return out

def pick_event(events, n=8):
    if not events:
        return None
    return events[min(n, len(events) - 1)]

# ── 패널 그리기 ───────────────────────────────────────────────────────────────

# 신호 y 배치: HS 위, LS 아래, 간격으로 구분
HS_BASE = 0.60; HS_H = 0.75   # HS LOW=HS_BASE, HIGH=HS_BASE+HS_H
LS_BASE = -0.40; LS_H = 0.75  # LS LOW=LS_BASE, HIGH=LS_BASE+LS_H

def draw_dt_panel(ax, t_fall, t_rise, tr_hs, tr_ls,
                  dt_set, mean_gap,
                  hs_color, ls_color,
                  hs_lbl, ls_lbl, pin_hs, pin_ls):
    half_win_s = max(dt_set * 3.5e-9, 350e-9)
    t0 = t_fall - half_win_s
    t1 = t_rise + half_win_s

    xs_hs, ys_raw_hs = make_step(tr_hs, t0, t1, t_ref=t0)
    xs_ls, ys_raw_ls = make_step(tr_ls, t0, t1, t_ref=t0)

    ys_hs = ys_raw_hs * HS_H + HS_BASE
    ys_ls = ys_raw_ls * LS_H + LS_BASE

    # 상대 좌표 (t0 기준 0)
    t0_ns = 0.0
    t1_ns = (t1 - t0) * 1e9
    tf_ns = (t_fall - t0) * 1e9
    tr_ns = (t_rise - t0) * 1e9

    ax.plot(xs_hs, ys_hs, color=hs_color, linewidth=2.2, solid_capstyle="round")
    ax.plot(xs_ls, ys_ls, color=ls_color, linewidth=2.2, solid_capstyle="round")

    # both-LOW 음영
    ax.axvspan(tf_ns, tr_ns, color="#fef08a", alpha=0.75, zorder=0)

    # 양방향 화살표 + 주석
    y_ann = (HS_BASE + LS_BASE + LS_H) / 2 + 0.05
    ax.annotate("", xy=(tr_ns, y_ann), xytext=(tf_ns, y_ann),
                arrowprops=dict(arrowstyle="<->", color="#222", lw=1.3))
    ax.text((tf_ns + tr_ns) / 2, y_ann + 0.10,
            f"~{dt_set} ns\n(meas {mean_gap:.0f} ns)",
            ha="center", va="bottom", fontsize=7.5, fontweight="bold",
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", pad=1))

    # 신호 레이블 (왼쪽)
    ax.text(t0_ns - (t1_ns - t0_ns) * 0.02, HS_BASE + HS_H * 0.5,
            f"{hs_lbl}\n{pin_hs}", ha="right", va="center",
            fontsize=7, color=hs_color, fontweight="bold", linespacing=1.3)
    ax.text(t0_ns - (t1_ns - t0_ns) * 0.02, LS_BASE + LS_H * 0.5,
            f"{ls_lbl}\n{pin_ls}", ha="right", va="center",
            fontsize=7, color=ls_color, fontweight="bold", linespacing=1.3)

    ax.set_xlim(t0_ns, t1_ns)
    ax.set_ylim(-0.65, 1.55)
    ax.set_xlabel("time [ns]", fontsize=8)
    ax.yaxis.set_visible(False)
    for spine in ("left", "top", "right"): ax.spines[spine].set_visible(False)
    ax.tick_params(axis="x", labelsize=8)
    ax.xaxis.grid(True, color="#ddd", linewidth=0.6)

# ── Figure 3 — Dead-time 파형 줌 (4 rows × 4 cols) ─────────────────────────

DT_SETTINGS = [100, 150, 250, 400]
KNOB_DIR    = BASE / "pwm_deadtime_knob_verify"

# rows: (leg, fall_is_hs, row_label, hs_color, ls_color, hs_lbl, ls_lbl, pin_hs, pin_ls)
ROWS = [
    (1, False, "Leg1  LS↓→HS↑", "#8b0000", "#1a2a6c",
     "PWM_HS1", "PWM_LS1", "J4.39", "J4.40"),
    (1, True,  "Leg1  HS↓→LS↑", "#8b0000", "#1a2a6c",
     "PWM_HS1", "PWM_LS1", "J4.39", "J4.40"),
    (2, False, "Leg2  LS↓→HS↑", "#c2622a", "#2a9d8f",
     "PWM_HS2", "PWM_LS2", "J6.52", "J6.51"),
    (2, True,  "Leg2  HS↓→LS↑", "#c2622a", "#2a9d8f",
     "PWM_HS2", "PWM_LS2", "J6.52", "J6.51"),
]

plt.rcParams.update({
    "font.family": ["Malgun Gothic", "DejaVu Sans"],
    "figure.facecolor": "#f8f4ee",
    "axes.facecolor":   "#f8f4ee",
})

fig3, axes3 = plt.subplots(4, 4, figsize=(15, 11),
                            gridspec_kw={"hspace": 0.55, "wspace": 0.12})
fig3.patch.set_facecolor("#f8f4ee")
fig3.suptitle("Dead-time zoom @ commutation (both-LOW gap shaded)  leg x build = 4x4",
              fontsize=13, fontweight="bold", y=0.98)

# column headers
for ci, dt in enumerate(DT_SETTINGS):
    axes3[0, ci].set_title(f"{dt} ns build", fontsize=10, fontweight="bold", pad=8)

# row labels
for ri, row_info in enumerate(ROWS):
    axes3[ri, 0].set_ylabel(row_info[2], fontsize=9, fontweight="bold", labelpad=8)

print("=== Figure 3: deadtime waveforms ===")
for ri, (leg, fall_is_hs, row_lbl,
         hs_col, ls_col, hs_lbl, ls_lbl, pin_hs, pin_ls) in enumerate(ROWS):
    for ci, dt in enumerate(DT_SETTINGS):
        path = KNOB_DIR / f"dt{dt}" / f"leg{leg}" / "digital.csv"
        times, la, lb = load2(path)  # la=HS(CH0), lb=LS(CH1)

        span = times[-1] - times[0]
        w0 = times[0] + 0.15 * span
        w1 = times[-1] - 0.15 * span

        tr_hs = ch_trans(times, la)
        tr_ls = ch_trans(times, lb)

        if fall_is_hs:
            # HS 하강 → LS 상승
            events = find_gap_events(tr_hs, tr_ls, w0, w1)
        else:
            # LS 하강 → HS 상승
            events = find_gap_events(tr_ls, tr_hs, w0, w1)

        ev = pick_event(events, n=8)
        if ev is None:
            print(f"  [WARN] no event: leg{leg} dt{dt} {'HS-fall' if fall_is_hs else 'LS-fall'}")
            axes3[ri, ci].axis("off"); continue

        t_fall, t_rise = ev
        mean_gap = statistics.mean((tr - tf) * 1e9 for tf, tr in events[:100])
        print(f"  leg{leg} dt={dt:3d}ns {'HS↓→LS↑' if fall_is_hs else 'LS↓→HS↑'}: "
              f"gap={( t_rise - t_fall)*1e9:.1f}ns  mean={mean_gap:.1f}ns  events={len(events)}")

        draw_dt_panel(axes3[ri, ci], t_fall, t_rise, tr_hs, tr_ls,
                      dt, mean_gap,
                      hs_col, ls_col, hs_lbl, ls_lbl, pin_hs, pin_ls)

out3 = OUT / "fig3_deadtime_waveforms.png"
fig3.savefig(out3, dpi=150, bbox_inches="tight")
plt.close(fig3)
print(f"\nSaved: {out3}")

# ── Figure 4 — Isoform 오버레이 (150 ns 단일 케이스, 4채널 1 axes) ───────────

ISOFORM_DIR = BASE / "pwm_leg2_isoform"

# ── 메트릭 헬퍼 ──────────────────────────────────────────────────────────────

def tr_edges(trans):
    """ch_trans 결과 → [(time, +1 or -1)] 에지 목록"""
    out = []
    for i in range(1, len(trans)):
        t, v = trans[i]
        out.append((t, +1 if v == 1 else -1))
    return out

def iso_edge_skew(edges_a, edges_b, etype, w0, w1):
    """에지 타입(+1/-1) 기준 a→b 시차 목록 [ns]. (a_time - b_time)"""
    ea = sorted(t for t, e in edges_a if e == etype and w0 <= t <= w1)
    eb = sorted(t for t, e in edges_b if e == etype)
    out = []
    for ta in ea:
        idx = bisect.bisect_left(eb, ta)
        cands = []
        if idx < len(eb): cands.append(eb[idx])
        if idx > 0:       cands.append(eb[idx - 1])
        if cands:
            nb = min(cands, key=lambda x: abs(x - ta))
            out.append((ta - nb) * 1e9)
    return out

def iso_high_times(edges, w0, w1):
    """채널의 high 구간 길이 목록 [ns]"""
    out = []
    rises = sorted(t for t, e in edges if e == +1)
    falls = sorted(t for t, e in edges if e == -1)
    for rt in rises:
        if not (w0 <= rt <= w1): continue
        idx = bisect.bisect_right(falls, rt)
        if idx < len(falls):
            out.append((falls[idx] - rt) * 1e9)
    return out

def iso_shoot_through(edges_a, edges_b, w0, w1):
    """양 채널 동시 HIGH 누적 시간 [ns]"""
    evs = sorted([(t, 0, e) for t, e in edges_a] + [(t, 1, e) for t, e in edges_b])
    sa = sb = 0; ov = 0.0; last = None
    for t, ch, e in evs:
        if last is not None and sa and sb and w0 <= last <= w1:
            ov += t - last
        if ch == 0: sa = 1 if e == +1 else 0
        else:       sb = 1 if e == +1 else 0
        last = t
    return ov * 1e9

def skew_stats(lst):
    if not lst: return None
    return statistics.median(lst), min(lst), max(lst)

# ── 데이터 로드 ───────────────────────────────────────────────────────────────

print("\n=== Figure 4: isoform overlay (150 ns) ===")
path4 = ISOFORM_DIR / "verify_dt150" / "digital.csv"
times4, lvs4 = load4(path4)  # CH0=HS1, CH1=LS1, CH2=HS2, CH3=LS2

span4 = times4[-1] - times4[0]
w0_4  = times4[0] + 0.10 * span4
w1_4  = times4[-1] - 0.10 * span4

tr4 = [ch_trans(times4, lvs4[c]) for c in range(4)]
ed4 = [tr_edges(tr4[c]) for c in range(4)]  # edges per channel

# ── B1: 4 에지 시차 ───────────────────────────────────────────────────────────
skew_labels = [
    ("HS2↑ − HS1↑", 2, 0, +1),
    ("HS2↓ − HS1↓", 2, 0, -1),
    ("LS2↑ − LS1↑", 3, 1, +1),
    ("LS2↓ − LS1↓", 3, 1, -1),
]
b1_results = []
for lbl, ca, cb, et in skew_labels:
    lst = iso_edge_skew(ed4[ca], ed4[cb], et, w0_4, w1_4)
    st = skew_stats(lst)
    b1_results.append((lbl, st))
    if st:
        print(f"  B1 {lbl}: median={st[0]:+.1f}  min={st[1]:+.1f}  max={st[2]:+.1f}  n={len(lst)}")

# ── B2: high-time 일치 ────────────────────────────────────────────────────────
ht = [iso_high_times(ed4[c], w0_4, w1_4) for c in range(4)]
hs1_med = statistics.median(ht[0]) if ht[0] else 0
hs2_med = statistics.median(ht[2]) if ht[2] else 0
ls1_med = statistics.median(ht[1]) if ht[1] else 0
ls2_med = statistics.median(ht[3]) if ht[3] else 0
b2_hs_diff = hs2_med - hs1_med
b2_ls_diff = ls2_med - ls1_med
print(f"  B2 HS high-time: HS1={hs1_med:.1f}ns  HS2={hs2_med:.1f}ns  diff={b2_hs_diff:+.1f}ns")
print(f"  B2 LS high-time: LS1={ls1_med:.1f}ns  LS2={ls2_med:.1f}ns  diff={b2_ls_diff:+.1f}ns")

# ── Shoot-through ─────────────────────────────────────────────────────────────
st_leg1 = iso_shoot_through(ed4[0], ed4[1], w0_4, w1_4)
st_leg2 = iso_shoot_through(ed4[2], ed4[3], w0_4, w1_4)
print(f"  Shoot-through: Leg1={st_leg1:.3f}ns  Leg2={st_leg2:.3f}ns")

# ── 줌 창 선택 (HS1↓→LS1↑) ───────────────────────────────────────────────────
events4 = find_gap_events(tr4[0], tr4[1], w0_4, w1_4)
if not events4:
    events4 = find_gap_events(tr4[1], tr4[0], w0_4, w1_4)
ev4 = pick_event(events4, n=8)
if ev4 is None:
    print("  [WARN] no isoform event — skipping fig4")
else:
    t_fall4, t_rise4 = ev4
    half_win = max(150 * 3.5e-9, 350e-9)
    t0_z = t_fall4 - half_win
    t1_z = t_rise4 + half_win
    win_ns = (t1_z - t0_z) * 1e9

    # ── 그림 구성: 1 axes(파형) + textbox(메트릭) ─────────────────────────────
    fig4 = plt.figure(figsize=(13, 5.5))
    fig4.patch.set_facecolor("#f8f4ee")
    fig4.suptitle("Leg1 vs Leg2 isoform — 4채널 오버레이  DT=150 ns",
                  fontsize=13, fontweight="bold", y=0.97)

    # axes 비율: 파형 75%, 메트릭 25%
    ax_wave = fig4.add_axes([0.10, 0.14, 0.60, 0.72])
    ax_wave.set_facecolor("#f8f4ee")

    CH_STYLE = [
        (0, "#8b0000", "PWM_HS1", "J4.39", HS_BASE, HS_H),
        (1, "#1a2a6c", "PWM_LS1", "J4.40", LS_BASE, LS_H),
        (2, "#c2622a", "PWM_HS2", "J6.52", HS_BASE, HS_H),
        (3, "#2a9d8f", "PWM_LS2", "J6.51", LS_BASE, LS_H),
    ]
    lw_order = [2.2, 2.2, 1.4, 1.4]  # Leg1 굵게, Leg2 가늘게(오버레이 시인성)
    zorders   = [3, 3, 2, 2]

    for i, (ch, col, lbl, pin, base, h) in enumerate(CH_STYLE):
        xs, ys_raw = make_step(tr4[ch], t0_z, t1_z, t_ref=t0_z)
        ys = ys_raw * h + base
        ax_wave.plot(xs, ys, color=col, linewidth=lw_order[i],
                     solid_capstyle="round", zorder=zorders[i],
                     label=f"{lbl} ({pin})")

    # both-LOW 음영 (Leg1 기준)
    tf_rel = (t_fall4 - t0_z) * 1e9
    tr_rel = (t_rise4 - t0_z) * 1e9
    ax_wave.axvspan(tf_rel, tr_rel, color="#fef08a", alpha=0.75, zorder=0)

    # DT 화살표
    y_ann = (HS_BASE + LS_BASE + LS_H) / 2 + 0.05
    ax_wave.annotate("", xy=(tr_rel, y_ann), xytext=(tf_rel, y_ann),
                     arrowprops=dict(arrowstyle="<->", color="#444", lw=1.2))
    ax_wave.text((tf_rel + tr_rel) / 2, y_ann + 0.10, "~150 ns DT",
                 ha="center", va="bottom", fontsize=8, fontweight="bold",
                 bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", pad=1))

    ax_wave.set_xlim(0, win_ns)
    ax_wave.set_ylim(-0.65, 1.55)
    ax_wave.set_xlabel("time [ns]", fontsize=9)
    ax_wave.yaxis.set_visible(False)
    for sp in ("left", "top", "right"): ax_wave.spines[sp].set_visible(False)
    ax_wave.tick_params(axis="x", labelsize=8)
    ax_wave.xaxis.grid(True, color="#ddd", linewidth=0.6)
    ax_wave.legend(loc="upper right", fontsize=8, framealpha=0.85,
                   edgecolor="#ccc", ncol=2)

    # ── 메트릭 텍스트 박스 ────────────────────────────────────────────────────
    ax_txt = fig4.add_axes([0.73, 0.10, 0.25, 0.80])
    ax_txt.axis("off")
    ax_txt.set_facecolor("#f8f4ee")

    def _sf(st):
        if st is None: return "—"
        return f"{st[0]:+.1f}  [{st[1]:+.1f} / {st[2]:+.1f}]"

    b1_lines = [f"  {lbl}:\n    {_sf(st)} ns" for lbl, st in b1_results]

    ok = lambda v: "✓" if abs(v) <= 2.0 else "!"
    b1_ok = all(st is not None and abs(st[0]) <= 2.0 for _, st in b1_results)
    b2_ok = abs(b2_hs_diff) <= 10 and abs(b2_ls_diff) <= 10

    box_text = (
        "── B1  Edge skew  (median [min/max]) ──\n"
        + "\n".join(b1_lines) + "\n\n"
        "── B2  High-time match ──\n"
        f"  HS1 {hs1_med:.0f} ns  vs  HS2 {hs2_med:.0f} ns\n"
        f"    diff = {b2_hs_diff:+.1f} ns  {ok(b2_hs_diff)}\n"
        f"  LS1 {ls1_med:.0f} ns  vs  LS2 {ls2_med:.0f} ns\n"
        f"    diff = {b2_ls_diff:+.1f} ns  {ok(b2_ls_diff)}\n\n"
        "── Shoot-through ──\n"
        f"  Leg1: {st_leg1:.0f} ns  {'✓' if st_leg1 == 0 else '!'}\n"
        f"  Leg2: {st_leg2:.0f} ns  {'✓' if st_leg2 == 0 else '!'}"
    )

    ax_txt.text(0.03, 0.97, box_text,
                transform=ax_txt.transAxes, ha="left", va="top",
                fontsize=8.0, family="monospace",
                bbox=dict(facecolor="white", edgecolor="#aaa", alpha=0.92,
                          pad=6, boxstyle="round,pad=0.5"))

    out4 = OUT / "fig4_isoform_waveforms.png"
    fig4.savefig(out4, dpi=150, bbox_inches="tight")
    plt.close(fig4)
    print(f"Saved: {out4}")
