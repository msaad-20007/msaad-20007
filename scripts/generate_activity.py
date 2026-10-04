#!/usr/bin/env python3
import json, os, urllib.request, math, html
USER=os.getenv("GITHUB_USER","msaad-20007")
TOKEN=os.environ["GITHUB_TOKEN"]
Q='query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}'
body=json.dumps({"query":Q,"variables":{"login":USER}}).encode()
req=urllib.request.Request("https://api.github.com/graphql",data=body,headers={"Authorization":f"Bearer {TOKEN}","Content-Type":"application/json","User-Agent":"saad-profile-activity"},method="POST")
with urllib.request.urlopen(req,timeout=30) as r: data=json.load(r)
if data.get("errors"): raise RuntimeError(json.dumps(data["errors"]))
cal=data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
days=[d for w in cal["weeks"] for d in w["contributionDays"]]
peak=max([d["contributionCount"] for d in days] or [1]); total=cal["totalContributions"]
left,bottom,usable,height=22,216,1038,174
pts=[]
for i,d in enumerate(days):
    x=left+i/max(1,len(days)-1)*usable
    y=bottom-(math.sqrt(d["contributionCount"]/peak) if peak else 0)*(height-12)
    pts.append((x,y,d["contributionCount"],d["date"]))
path=" ".join(("M" if i==0 else "L")+f"{x:.1f},{y:.1f}" for i,(x,y,_,_) in enumerate(pts))
links="".join(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#a97bff" stroke-opacity=".16"/>' for a,b in zip(pts,pts[1:]) if a[2] and b[2])
nodes="".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.4+5.2*math.sqrt(c/peak):.2f}" fill="#67f5ff" opacity="{.38+.62*math.sqrt(c/peak):.3f}"><title>{html.escape(d)}: {c} contributions</title></circle>' for x,y,c,d in pts if c)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="490" viewBox="0 0 1200 490">
<defs><linearGradient id="b"><stop stop-color="#071326"/><stop offset=".55" stop-color="#0b1730"/><stop offset="1" stop-color="#160b2e"/></linearGradient><filter id="g"><feGaussianBlur stdDeviation="4" result="x"/><feMerge><feMergeNode in="x"/><feMergeNode in="SourceGraphic"/></feMerge></filter><pattern id="p" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#6cefff" stroke-opacity=".055"/></pattern></defs>
<rect width="1200" height="490" rx="28" fill="url(#b)"/><rect x="1" y="1" width="1198" height="488" rx="28" fill="url(#p)" stroke="#3cecff" stroke-opacity=".35"/>
<text x="58" y="64" fill="#6ef7ff" font-family="Arial" font-size="15" letter-spacing="4">04 / LIVE CONTRIBUTION SIGNAL</text><text x="58" y="105" fill="#f1f7ff" font-family="Arial" font-size="30" font-weight="700">NEURAL ACTIVITY MAP</text><text x="58" y="133" fill="#728bad" font-family="Arial" font-size="14">{total} contributions in the last year · real GitHub data</text>
<g transform="translate(58 170)"><rect width="1084" height="260" rx="18" fill="#071426" stroke="#39f6ff" stroke-opacity=".35"/><path d="M22 216H1060 M22 178H1060 M22 140H1060 M22 102H1060 M22 64H1060" stroke="#5eefff" stroke-opacity=".06"/><g>{links}</g><path d="{path}" fill="none" stroke="#39f6ff" stroke-opacity=".62" stroke-width="2" filter="url(#g)"/><path d="{path}" fill="none" stroke="#b66cff" stroke-opacity=".25" stroke-width="8" filter="url(#g)"/><g>{nodes}</g><rect x="20" y="42" width="2" height="180" fill="#d36bff" opacity=".55"><animate attributeName="x" values="20;1058;20" dur="6s" repeatCount="indefinite"/></rect><text x="32" y="28" fill="#7d96bb" font-size="10" letter-spacing="2">CONTRIBUTION SIGNAL / DAILY INTENSITY / ACTIVE-DAY NETWORK</text></g>
<text x="58" y="460" fill="#6ef7ff" font-family="Arial" font-size="12" letter-spacing="2">SOURCE</text><text x="120" y="460" fill="#7b8fae" font-family="Arial" font-size="12">GitHub GraphQL contributionCalendar → custom SVG renderer → README</text></svg>'''
open("assets/activity.svg","w",encoding="utf-8").write(svg)
print(f"Generated {total} contributions.")
