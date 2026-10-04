#!/usr/bin/env python3
import json, os, urllib.request, math, html
from datetime import date

USER = os.getenv("GITHUB_USER", "msaad-20007")
TOKEN = os.environ["GITHUB_TOKEN"]
Q = """
query($login:String!){
  user(login:$login){
    contributionsCollection{
      contributionCalendar{
        totalContributions
        weeks{
          firstDay
          contributionDays{date weekday contributionCount}
        }
      }
    }
  }
}
"""
body=json.dumps({"query":Q,"variables":{"login":USER}}).encode()
req=urllib.request.Request(
    "https://api.github.com/graphql", data=body,
    headers={"Authorization":f"Bearer {TOKEN}","Content-Type":"application/json","User-Agent":"saad-profile-activity"},
    method="POST")
with urllib.request.urlopen(req,timeout=30) as r:
    data=json.load(r)
if data.get("errors"): raise RuntimeError(json.dumps(data["errors"]))
cal=data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
weeks=cal["weeks"]; days=[d for w in weeks for d in w["contributionDays"]]
total=cal["totalContributions"]; peak=max([d["contributionCount"] for d in days] or [1])

W,H=1200,650
left,right,top,bottom=78,24,185,92
chart_w=W-left-right; chart_h=H-top-bottom
week_w=chart_w/max(1,len(weeks))
bar_w=max(2.0,(week_w-8)/7); max_bar_h=chart_h-34

bars=[]; month_labels=[]; last_month=None
for wi,week in enumerate(weeks):
    x0=left+wi*week_w+4
    fd=week.get("firstDay","")
    if fd and fd[:7]!=last_month:
        month_labels.append((x0,fd)); last_month=fd[:7]
    by_weekday={d.get("weekday"):d for d in week["contributionDays"]}
    for wd in range(1,8):
        d=by_weekday.get(wd)
        if not d: continue
        count=d["contributionCount"]
        bh=0 if peak==0 else max_bar_h*math.sqrt(count/peak)
        bx=x0+(wd-1)*(bar_w+0.9); by=top+chart_h-bh
        opacity=0.20+0.80*math.sqrt(count/peak) if count else 0.10
        bars.append(
            f'<rect x="{bx:.2f}" y="{by:.2f}" width="{bar_w:.2f}" height="{max(1.2,bh):.2f}" rx="1.6" fill="url(#bar)" opacity="{opacity:.3f}">'
            f'<title>{html.escape(d["date"])} · {count} contribution{"s" if count != 1 else ""}</title></rect>'
        )

months_svg=[]
for x,ds in month_labels:
    try: label=date.fromisoformat(ds).strftime("%b %Y").upper()
    except Exception: label=ds[:7]
    months_svg.append(f'<text x="{x:.1f}" y="{top-24}" fill="#8fa6c9" font-size="11" letter-spacing="1">{html.escape(label)}</text>')

weekday_svg=[]
for i,name in enumerate(["MON","TUE","WED","THU","FRI","SAT","SUN"]):
    weekday_svg.append(f'<text x="{left+i*74}" y="{H-26}" fill="#728bad" font-size="10" letter-spacing="1">{name}</text>')

svg=f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#071326"/><stop offset=".55" stop-color="#0b1730"/><stop offset="1" stop-color="#160b2e"/></linearGradient>
<linearGradient id="bar" x1="0" y1="1" x2="0" y2="0"><stop stop-color="#7b7cff"/><stop offset=".55" stop-color="#39f6ff"/><stop offset="1" stop-color="#d36bff"/></linearGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#6cefff" stroke-opacity=".055"/></pattern>
<filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="{W}" height="{H}" rx="28" fill="url(#bg)"/>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="28" fill="url(#grid)" stroke="#3cecff" stroke-opacity=".35"/>
<text x="58" y="56" fill="#6ef7ff" font-family="Arial,Helvetica,sans-serif" font-size="15" letter-spacing="4">04 / LIVE CONTRIBUTION DATA</text>
<text x="58" y="98" fill="#f1f7ff" font-family="Arial,Helvetica,sans-serif" font-size="30" font-weight="700">NEURAL ACTIVITY — 2D DAILY BARS</text>
<text x="58" y="126" fill="#728bad" font-family="Arial,Helvetica,sans-serif" font-size="14">{total} contributions · {len(days)} daily records · real GitHub contributionCalendar data</text>
<g font-family="Arial,Helvetica,sans-serif">
<rect x="{left-16}" y="{top-42}" width="{chart_w+20}" height="{chart_h+58}" rx="18" fill="#071426" stroke="#39f6ff" stroke-opacity=".35"/>
<line x1="{left}" y1="{top+chart_h}" x2="{W-right}" y2="{top+chart_h}" stroke="#5eefff" stroke-opacity=".25"/>
<line x1="{left}" y1="{top+chart_h-max_bar_h/2}" x2="{W-right}" y2="{top+chart_h-max_bar_h/2}" stroke="#5eefff" stroke-opacity=".06"/>
<line x1="{left}" y1="{top+chart_h-max_bar_h}" x2="{W-right}" y2="{top+chart_h-max_bar_h}" stroke="#5eefff" stroke-opacity=".06"/>
<text x="{left-8}" y="{top+chart_h+4}" text-anchor="end" fill="#607899" font-size="9">0</text>
<text x="{left-8}" y="{top+chart_h-max_bar_h/2+4}" text-anchor="end" fill="#607899" font-size="9">MID</text>
<text x="{left-8}" y="{top+chart_h-max_bar_h+4}" text-anchor="end" fill="#607899" font-size="9">PEAK</text>
{''.join(months_svg)}
<g filter="url(#glow)">{''.join(bars)}</g>
<text x="{left}" y="{H-45}" fill="#6ef7ff" font-size="10" letter-spacing="2">WEEKDAY ORDER</text>
{''.join(weekday_svg)}
</g>
<text x="58" y="{H-10}" fill="#7b8fae" font-family="Arial,Helvetica,sans-serif" font-size="11">Hover a bar for exact date + contribution count · height = daily contribution intensity · source: GitHub GraphQL</text>
</svg>"""
with open("assets/activity.svg", "w", encoding="utf-8") as f: f.write(svg)
print(f"Generated {total} contributions across {len(days)} daily records.")
