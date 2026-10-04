#!/usr/bin/env python3
import json, os, urllib.request, math, html
from datetime import date

USER = os.getenv("GITHUB_USER", "msaad-20007")
TOKEN = os.environ["GITHUB_TOKEN"]

QUERY = (
    "query($login:String!){"
    "user(login:$login){"
    "contributionsCollection{"
    "contributionCalendar{"
    "totalContributions "
    "weeks{firstDay contributionDays{date weekday contributionCount}}"
    "}}}}"
)

body = json.dumps({"query": QUERY, "variables": {"login": USER}}).encode()
req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=body,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "msaad-20007-cybernetic-profile",
    },
    method="POST",
)
with urllib.request.urlopen(req, timeout=30) as response:
    payload = json.load(response)

if payload.get("errors"):
    raise RuntimeError(json.dumps(payload["errors"]))

calendar = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
weeks = calendar["weeks"]
days = [d for w in weeks for d in w["contributionDays"]]
total = calendar["totalContributions"]
peak = max((d["contributionCount"] for d in days), default=0)

W, H = 1200, 610
left, right, top, bottom = 76, 28, 142, 76
chart_w, chart_h = W-left-right, H-top-bottom
week_w = chart_w / max(1, len(weeks))
bar_gap = 1.2
bar_w = max(1.7, min(4.2, (week_w-10)/7))
max_bar_h = chart_h - 42

bars, month_labels = [], []
last_month = None
for wi, week in enumerate(weeks):
    x0 = left + wi*week_w + 5
    fd = week.get("firstDay", "")
    month_key = fd[:7]
    if fd and month_key != last_month:
        try:
            label = date.fromisoformat(fd).strftime("%b %Y").upper()
        except ValueError:
            label = month_key.upper()
        month_labels.append((x0, label))
        last_month = month_key

    by_weekday = {d.get("weekday"): d for d in week["contributionDays"]}
    for weekday in range(1, 8):
        d = by_weekday.get(weekday)
        if not d:
            continue
        count = d["contributionCount"]
        intensity = 0 if peak == 0 else math.sqrt(count/peak)
        bh = 2 if count == 0 else 10 + max_bar_h*intensity
        bx = x0 + (weekday-1)*(bar_w+bar_gap)
        by = top + chart_h - bh
        title = f'{d["date"]} · {count} contribution{"s" if count != 1 else ""}'
        bars.append(
            f'<rect x="{bx:.2f}" y="{by:.2f}" width="{bar_w:.2f}" '
            f'height="{bh:.2f}" rx="1.8" fill="url(#bar)" '
            f'opacity="{0.18+0.82*intensity:.3f}">'
            f'<title>{html.escape(title)}</title></rect>'
        )

months_svg = [
    f'<text x="{x:.1f}" y="{top-22}" fill="#9bb0d2" font-size="11" '
    f'font-weight="700" letter-spacing="1">{html.escape(label)}</text>'
    for x, label in month_labels
]
weekday_svg = [
    f'<text x="{left+i*67}" y="{H-25}" fill="#7f95b8" font-size="10" '
    f'letter-spacing="1.5">{name}</text>'
    for i, name in enumerate(["MON","TUE","WED","THU","FRI","SAT","SUN"])
]
stats = (
    f'<text x="{W-390}" y="48" fill="#6ef7ff" font-size="12" '
    f'letter-spacing="1.5">TOTAL {total:,}</text>'
    f'<text x="{W-250}" y="48" fill="#9b86ff" font-size="12" '
    f'letter-spacing="1.5">PEAK {peak}</text>'
    f'<text x="{W-115}" y="48" fill="#d36bff" font-size="12" '
    f'letter-spacing="1.5">LIVE</text>'
)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#071326"/><stop offset=".55" stop-color="#0b1730"/><stop offset="1" stop-color="#160b2e"/></linearGradient>
<linearGradient id="bar" x1="0" y1="1" x2="0" y2="0"><stop stop-color="#39f6ff"/><stop offset=".55" stop-color="#7b7cff"/><stop offset="1" stop-color="#d36bff"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#6cefff" stroke-opacity=".045"/></pattern>
<filter id="glow"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="{W}" height="{H}" rx="28" fill="url(#bg)"/>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="28" fill="url(#grid)" stroke="#3cecff" stroke-opacity=".35"/>
<g font-family="Arial,Helvetica,sans-serif">
<text x="58" y="46" fill="#6ef7ff" font-size="14" letter-spacing="3.5">04 / LIVE CONTRIBUTION DATA</text>
{stats}
<text x="58" y="83" fill="#f1f7ff" font-size="28" font-weight="700">DAILY CONTRIBUTION BARS</text>
<text x="58" y="108" fill="#728bad" font-size="13">Real GitHub contribution calendar · 7 daily bars per week · hover a bar for exact date and count</text>
<rect x="{left-10}" y="{top-8}" width="{chart_w+20}" height="{chart_h+16}" rx="16" fill="#071426" stroke="#39f6ff" stroke-opacity=".22"/>
{''.join(months_svg)}
<path d="M{left} {top+chart_h}H{left+chart_w}" stroke="#39f6ff" stroke-opacity=".25"/>
<path d="M{left} {top+chart_h*.25}H{left+chart_w} M{left} {top+chart_h*.5}H{left+chart_w} M{left} {top+chart_h*.75}H{left+chart_w}" stroke="#6cefff" stroke-opacity=".06"/>
<g filter="url(#glow)">{''.join(bars)}</g>
<text x="58" y="{H-25}" fill="#667eaa" font-size="10" letter-spacing="1.5">WEEKDAY KEY</text>
{''.join(weekday_svg)}
<text x="58" y="{H-48}" fill="#6ef7ff" font-size="10" letter-spacing="1.5">DATA PIPELINE</text>
<text x="155" y="{H-48}" fill="#7187aa" font-size="10">GitHub GraphQL → contributionCalendar → SVG renderer → README</text>
</g>
</svg>"""

with open("assets/activity.svg", "w", encoding="utf-8", newline="\n") as f:
    f.write(svg)
