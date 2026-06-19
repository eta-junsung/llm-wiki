import csv

PATH = r"C:\Users\echog\eta\projects\g\8kw-ev-wpt-tx\verify_dt100\digital.csv"

# transition rows: Time, ch0..ch3 levels
rows = []
with open(PATH, newline="") as f:
    r = csv.reader(f)
    header = next(r)
    for line in r:
        if not line: continue
        t = float(line[0])
        lv = [int(line[1]), int(line[2]), int(line[3]), int(line[4])]
        rows.append((t, lv))

# channel names
CH = {0:"HS1",1:"LS1",2:"HS2",3:"LS2"}

# Build per-channel edge lists by detecting level changes between consecutive transition rows.
# Each transition row gives the NEW level set at time t. Compare to previous to find which ch changed.
prev = None
edges = {0:[],1:[],2:[],3:[]}  # list of (time, 'rise'/'fall')
for t, lv in rows:
    if prev is None:
        prev = lv
        prevt = t
        continue
    for c in range(4):
        if lv[c] != prev[c]:
            edges[c].append((t, 'rise' if lv[c]==1 else 'fall'))
    prev = lv
    prevt = t

tot_t = rows[-1][0] - rows[0][0]
print(f"# rows={len(rows)} span={tot_t*1e6:.2f}us")
for c in range(4):
    nr = sum(1 for _,k in edges[c] if k=='rise')
    nf = sum(1 for _,k in edges[c] if k=='fall')
    print(f"  {CH[c]}: rises={nr} falls={nf}")

# Restrict to middle 80% window
t0 = rows[0][0]; t1 = rows[-1][0]
lo = t0 + 0.10*(t1-t0)
hi = t0 + 0.90*(t1-t0)
def inwin(t): return lo <= t <= hi

ns = 1e9

# ---- High-time per channel (rise->next fall) in middle window ----
def high_times(c):
    es = edges[c]
    hts = []
    for i in range(len(es)-1):
        if es[i][1]=='rise' and es[i+1][1]=='fall':
            if inwin(es[i][0]):
                hts.append((es[i+1][0]-es[i][0])*ns)
    return hts

def stats(xs):
    if not xs: return None
    xs = sorted(xs)
    n=len(xs)
    med = xs[n//2] if n%2 else (xs[n//2-1]+xs[n//2])/2
    return (min(xs), med, max(xs), n)

print("\n## High-time (ns) [min/median/max, n]")
ht = {}
for c in range(4):
    s = stats(high_times(c))
    ht[c]=s
    if s: print(f"  {CH[c]}: min={s[0]:.1f} med={s[1]:.1f} max={s[2]:.1f} n={s[3]}")

# ---- Dead-time leg2: both-low gaps ----
# Merge edges of HS2(2) and LS2(3) into one timeline tracking both levels.
def both_low_gaps(ch_hs, ch_ls):
    # build merged event timeline with running levels
    ev = []
    for t,k in edges[ch_hs]: ev.append((t,'hs',k))
    for t,k in edges[ch_ls]: ev.append((t,'ls',k))
    ev.sort()
    # initial levels from first row
    hs = rows[0][1][ch_hs]; ls = rows[0][1][ch_ls]
    # We'll find intervals where both==0, and classify by which signal falls first
    # Track: when both go low, note the transition that caused entry (the falling edge),
    # and exit caused by a rising edge.
    gaps_hs_to_ls = []  # HS fell first then LS rises (HS->LS deadband)
    gaps_ls_to_hs = []
    shoot = 0
    last_low_start = None
    entered_by = None  # which fell to cause both-low
    cur_hs, cur_ls = hs, ls
    for t,sig,k in ev:
        if sig=='hs': cur_hs = 1 if k=='rise' else 0
        else: cur_ls = 1 if k=='rise' else 0
        # detect both high (shoot-through)
        if cur_hs==1 and cur_ls==1:
            shoot += 1
        # entering both-low
        if cur_hs==0 and cur_ls==0:
            if last_low_start is None:
                last_low_start = t
                entered_by = sig  # the signal that just fell
        else:
            if last_low_start is not None:
                gap = (t - last_low_start)*ns
                # exit caused by a rise. classify by entered_by:
                # if HS fell to enter -> this is the HS-off then LS-on band = HS->LS
                if entered_by=='hs':
                    gaps_hs_to_ls.append(gap)
                else:
                    gaps_ls_to_hs.append(gap)
                last_low_start = None
                entered_by=None
    return gaps_hs_to_ls, gaps_ls_to_hs, shoot

print("\n## Leg2 dead-time (both-LOW gaps, ns)")
g_hl, g_lh, sh2 = both_low_gaps(2,3)
g_hl = [g for g in g_hl if True]
def filt(gs):
    # keep only in window-ish (already small). report stats
    return stats(gs)
# restrict to window
def both_low_gaps_win(ch_hs, ch_ls):
    a,b,s = both_low_gaps(ch_hs,ch_ls)
    return a,b,s
print(f"  A1 HS2->LS2 both-low: {stats(g_hl)}")
print(f"  A2 LS2->HS2 both-low: {stats(g_lh)}")
print(f"  A3 leg2 shoot-through(both-HIGH) events = {sh2}")

print("\n## Leg1 dead-time (both-LOW gaps, ns)")
g1_hl, g1_lh, sh1 = both_low_gaps(0,1)
print(f"  HS1->LS1 both-low: {stats(g1_hl)}")
print(f"  LS1->HS1 both-low: {stats(g1_lh)}")
print(f"  leg1 shoot-through(both-HIGH) events = {sh1}")

# ---- B1: 4-edge inter-leg skew. Pair nearest edges of same type between leg1 and leg2 ----
def edge_times(c, kind):
    return [t for t,k in edges[c] if k==kind and inwin(t)]

def pairwise_skew(la, lb):
    # for each edge in la, nearest in lb, abs diff
    diffs=[]
    for t in la:
        best = min(lb, key=lambda x: abs(x-t)) if lb else None
        if best is not None:
            diffs.append(abs(best-t)*ns)
    return diffs

print("\n## B1 inter-leg edge skew (ns) [min/median/max, n]")
pairs = [
    ("HS2.rise vs HS1.rise", edge_times(2,'rise'), edge_times(0,'rise')),
    ("HS2.fall vs HS1.fall", edge_times(2,'fall'), edge_times(0,'fall')),
    ("LS2.rise vs LS1.rise", edge_times(3,'rise'), edge_times(1,'rise')),
    ("LS2.fall vs LS1.fall", edge_times(3,'fall'), edge_times(1,'fall')),
]
for name, a, b in pairs:
    d = pairwise_skew(a,b)
    print(f"  {name}: {stats(d)}")

# ---- B2 high-time leg agreement (median diff) ----
print("\n## B2 high-time leg agreement (median ns)")
if ht[2] and ht[0]:
    print(f"  HS1 med={ht[0][1]:.1f} vs HS2 med={ht[2][1]:.1f}  diff={abs(ht[0][1]-ht[2][1]):.1f}")
if ht[3] and ht[1]:
    print(f"  LS1 med={ht[1][1]:.1f} vs LS2 med={ht[3][1]:.1f}  diff={abs(ht[1][1]-ht[3][1]):.1f}")

# ---- B4 pulse-width spread ----
print("\n## B4 high-time spread (max-min, ns)")
for c in range(4):
    if ht[c]:
        print(f"  {CH[c]}: spread={ht[c][2]-ht[c][0]:.1f}")

# period check
def period(c):
    rs = [t for t,k in edges[c] if k=='rise' and inwin(t)]
    if len(rs)<2: return None
    ps = [(rs[i+1]-rs[i])*ns for i in range(len(rs)-1)]
    return stats(ps)
print("\n## Period (ns) HS1 rises")
print(f"  {period(0)}")
