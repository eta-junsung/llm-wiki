import csv, statistics as st
rows=[]
with open(r"C:\Users\echog\eta\projects\g\8kw-ev-wpt-tx\verify_dt250\digital.csv") as f:
    r=csv.reader(f); next(r)
    for line in r:
        t=float(line[0]); ch=[int(x) for x in line[1:5]]
        rows.append((t,ch))
t0=rows[0][0]; t1=rows[-1][0]; span=t1-t0
lo=t0+0.10*span; hi=t0+0.90*span
names=["HS1","LS1","HS2","LS2"]
rises={n:[] for n in names}; falls={n:[] for n in names}
prev=rows[0][1]
for i in range(1,len(rows)):
    t,ch=rows[i]
    for c in range(4):
        if ch[c]!=prev[c]:
            if lo<=t<=hi:
                (rises if ch[c]==1 else falls)[names[c]].append(t)
    prev=ch
def ns(x): return x*1e9
def hightime(n):
    res=[]; fs=sorted(falls[n])
    for tr in sorted(rises[n]):
        nx=[f for f in fs if f>tr]
        if nx: res.append(ns(nx[0]-tr))
    return res
H={n:hightime(n) for n in names}
def gaps(fa,ri):
    res=[]; rs=sorted(rises[ri])
    for tf in sorted(falls[fa]):
        nx=[r for r in rs if r>tf]
        if nx: res.append(ns(nx[0]-tf))
    return res
A1=gaps("HS2","LS2"); A2=gaps("LS2","HS2")
# A: sum & asymmetry per cycle (pair A1[i],A2[i])
m=min(len(A1),len(A2))
sums=[A1[i]+A2[i] for i in range(m)]
asym=[A1[i]-A2[i] for i in range(m)]
print("A3sum med/min/max",round(st.median(sums),2),round(min(sums),2),round(max(sums),2))
print("A_asym(A1-A2) med/min/max",round(st.median(asym),2),round(min(asym),2),round(max(asym),2))
# B2 high-time leg match
def diff(a,b):
    m=min(len(H[a]),len(H[b]))
    d=[H[a][i]-H[b][i] for i in range(m)]
    return round(st.median(d),2),round(min(d),2),round(max(d),2)
print("B2_HS1vsHS2",diff("HS1","HS2"))
print("B2_LS1vsLS2",diff("LS1","LS2"))
# B4 pulse-width spread (max-min) per channel
for n in names:
    sp=round(max(H[n])-min(H[n]),2)
    print("B4_spread_"+n,sp)
