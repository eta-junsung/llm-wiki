import csv, statistics, bisect

PATH = r"C:\Users\echog\eta\projects\g\8kw-ev-wpt-tx\verify_dt150\digital.csv"
CH = {0:"HS1", 1:"LS1", 2:"HS2", 3:"LS2"}

times=[]; levels=[]
with open(PATH) as f:
    r=csv.reader(f); next(r)
    for row in r:
        times.append(float(row[0]))
        levels.append([int(row[1]),int(row[2]),int(row[3]),int(row[4])])

edges={c:[] for c in range(4)}
prev=None
for t,v in zip(times,levels):
    if prev is None: prev=v; continue
    for c in range(4):
        if v[c]!=prev[c]:
            edges[c].append((t, +1 if v[c]==1 else -1))
    prev=v

t0=times[0]; t1=times[-1]; span=t1-t0
w0=t0+0.10*span; w1=t1-0.10*span
def in_win(t): return w0<=t<=w1
ns=1e9
def rises(c): return [t for (t,e) in edges[c] if e==+1]
def falls(c): return [t for (t,e) in edges[c] if e==-1]

def high_times(c):
    es=sorted(edges[c]); out=[]; i=0
    while i<len(es)-1:
        t,e=es[i]
        if e==+1:
            j=i+1
            while j<len(es) and es[j][1]!=-1: j+=1
            if j<len(es):
                rt=t; ft=es[j][0]
                if in_win(rt) and in_win(ft): out.append((ft-rt)*ns)
                i=j
            else: break
        else: i+=1
    return out

def low_gaps(fall_ch, rise_ch):
    fa=sorted(falls(fall_ch)); ri=sorted(rises(rise_ch)); out=[]
    for ft in fa:
        idx=bisect.bisect_right(ri, ft)
        if idx<len(ri):
            rt=ri[idx]; g=(rt-ft)*ns
            if 0<g<3000 and in_win(ft) and in_win(rt): out.append(g)
    return out

def overlap_high(ca, cb):
    # shoot-through: time both channels high simultaneously
    es=[]
    for c in (ca,cb):
        for (t,e) in edges[c]: es.append((t,c,e))
    es.sort()
    sa=sb=0; ov=0.0; last=None
    for (t,c,e) in es:
        if last is not None and sa and sb and in_win(last):
            ov += (t-last)
        if c==ca: sa = 1 if e==+1 else 0
        else: sb = 1 if e==+1 else 0
        last=t
    return ov*ns

def edge_skew(ca, cb, etype):
    # match each edge of given type on ca to nearest on cb, report skew (ca - cb) ns
    ea=sorted([t for (t,e) in edges[ca] if e==etype])
    eb=sorted([t for (t,e) in edges[cb] if e==etype])
    out=[]
    for t in ea:
        if not in_win(t): continue
        idx=bisect.bisect_left(eb, t)
        cand=[]
        if idx<len(eb): cand.append(eb[idx])
        if idx>0: cand.append(eb[idx-1])
        if cand:
            nb=min(cand, key=lambda x: abs(x-t))
            out.append((t-nb)*ns)
    return out

def stats(lst):
    if not lst: return None
    return (statistics.median(lst), min(lst), max(lst), len(lst))
def fmt(s):
    if s is None: return "  (none)"
    return f"median {s[0]:8.2f}  min {s[1]:8.2f}  max {s[2]:8.2f}  n={s[3]}"

print(f"capture span = {span*1e6:.1f} us, stable window = middle 80%")
print(f"edge counts: HS1={len(edges[0])} LS1={len(edges[1])} HS2={len(edges[2])} LS2={len(edges[3])}")
print()
print("=== A. Leg2 dead-time (DT_COUNTS=30, expect ~150ns each) ===")
sa1=stats(low_gaps(2,3)); sa2=stats(low_gaps(3,2))
print(f"A1 HS2->LS2 gap : {fmt(sa1)}")
print(f"A2 LS2->HS2 gap : {fmt(sa2)}")
if sa1 and sa2:
    print(f"   bidir diff(median)={abs(sa1[0]-sa2[0]):.2f}ns  sum={sa1[0]+sa2[0]:.2f}ns (expect ~300)")
print(f"A3 leg2 shoot-through (HS2&LS2 both high) = {overlap_high(2,3):.3f} ns total")
print()
print("=== C. Leg1 dead-time (regression, expect ~150ns each) ===")
sc1=stats(low_gaps(0,1)); sc2=stats(low_gaps(1,0))
print(f"C1 HS1->LS1 gap : {fmt(sc1)}")
print(f"C2 LS1->HS1 gap : {fmt(sc2)}")
if sc1 and sc2:
    print(f"   leg1 sum={sc1[0]+sc2[0]:.2f}ns")
print(f"   leg1 shoot-through (HS1&LS1) = {overlap_high(0,1):.3f} ns total")
print()
print("=== B2/C high-time (expect 5730ns) ===")
for c in range(4):
    print(f"{CH[c]} high : {fmt(stats(high_times(c)))}")
print()
print("=== B1 leg-to-leg edge skew (HS2-HS1, LS2-LS1; expect <~2ns) ===")
for (lbl,ca,cb,et) in [("HS2.rise - HS1.rise",2,0,+1),("HS2.fall - HS1.fall",2,0,-1),
                       ("LS2.rise - LS1.rise",3,1,+1),("LS2.fall - LS1.fall",3,1,-1)]:
    print(f"{lbl} : {fmt(stats(edge_skew(ca,cb,et)))}")
