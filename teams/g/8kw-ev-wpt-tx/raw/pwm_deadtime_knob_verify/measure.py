import csv, statistics, bisect, sys

def load(path):
    times=[]; a=[]; b=[]
    with open(path) as f:
        r=csv.reader(f); hdr=next(r)
        for row in r:
            if not row: continue
            times.append(float(row[0])); a.append(int(row[1])); b.append(int(row[2]))
    return hdr, times, a, b

def edges(times, lv):
    # transition CSV: each row is new level. derive rise/fall for this channel
    e=[]; prev=lv[0]
    for i in range(1,len(lv)):
        if lv[i]!=prev:
            e.append((times[i], +1 if lv[i]==1 else -1))
            prev=lv[i]
    return e

def rises(e): return [t for t,k in e if k==+1]
def falls(e): return [t for t,k in e if k==-1]

def both_low(fall_ch_e, rise_ch_e, w0, w1):
    # fall of channel X -> next rise of channel Y, both LOW between => dead-time entering via X fall
    fa=sorted(falls(fall_ch_e)); ri=sorted(rises(rise_ch_e)); out=[]
    for ft in fa:
        if not (w0<=ft<=w1): continue
        idx=bisect.bisect_right(ri, ft)
        if idx<len(ri):
            g=(ri[idx]-ft)*1e9
            if 0<g<3000: out.append(g)
    return out

def st(xs):
    if not xs: return None
    return (statistics.mean(xs), statistics.pstdev(xs), min(xs), max(xs), len(xs))
def fmt(s):
    if s is None: return "(none)"
    return f"mean={s[0]:7.2f} sd={s[1]:5.2f} min={s[2]:6.1f} max={s[3]:6.1f} n={s[4]}"

def analyze(path, chA_name, chB_name, label):
    hdr, t, A, B = load(path)
    eA=edges(t,A); eB=edges(t,B)
    span=t[-1]-t[0]; w0=t[0]+0.10*span; w1=t[-1]-0.10*span
    print(f"=== {label} ({hdr[1]}={chA_name}, {hdr[2]}={chB_name}) span={span*1e3:.1f}ms rows={len(t)}")
    # high times sanity
    print(f"  {chA_name} edges={len(eA)}  {chB_name} edges={len(eB)}")
    # A-down -> B-up
    d1=both_low(eA, eB, w0, w1)   # A falls, B rises
    d2=both_low(eB, eA, w0, w1)   # B falls, A rises
    print(f"  {chA_name}-down->{chB_name}-up both-LOW : {fmt(st(d1))}")
    print(f"  {chB_name}-down->{chA_name}-up both-LOW : {fmt(st(d2))}")
    s1=st(d1); s2=st(d2)
    if s1 and s2:
        print(f"  bidir asymmetry (mean diff) = {abs(s1[0]-s2[0]):.2f} ns")
    # shoot-through check: both HIGH simultaneously
    es=sorted([(tt,'A',k) for tt,k in eA]+[(tt,'B',k) for tt,k in eB])
    sa=A[0]; sb=B[0]; ov=0.0; last=None; cnt=0
    for tt,c,k in es:
        if last is not None and sa==1 and sb==1 and w0<=last<=w1:
            ov+=(tt-last); 
        if c=='A': sa=1 if k==+1 else 0
        else: sb=1 if k==+1 else 0
        last=tt
    print(f"  shoot-through (both HIGH) total = {ov*1e9:.2f} ns")
    return s1, s2

print("\n##### LEG1 #####")
analyze(r"C:\Users\echog\eta\projects\g\8kw-ev-wpt-tx\dt100\leg1_raw\digital.csv","HS1","LS1","LEG1")
print("\n##### LEG2 #####")
analyze(r"C:\Users\echog\eta\projects\g\8kw-ev-wpt-tx\dt100\leg2_raw\digital.csv","HS2","LS2","LEG2")
