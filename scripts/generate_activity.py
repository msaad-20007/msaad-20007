#!/usr/bin/env python3
# Monthly cybernetic activity chart.
# This profile intentionally uses a visual/demo monthly series so the chart shape
# stays consistent with the README design.
from pathlib import Path

values = [3,6,4,8,5,7,2,9,6,4,7,5,8,3,6,10,5,7,4,8,6,3,9,5,7,4,6,8,5,9]
W,H=1040,520
left,right,top,bottom=78,28,54,86
plot_w=W-left-right
plot_h=H-top-bottom
maxv=10
bar_w=21
gap=(plot_w-30*bar_w)/29

svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#07111f"/><stop offset=".55" stop-color="#0a1428"/><stop offset="1" stop-color="#171334"/></linearGradient>
<linearGradient id="barCyan" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#07547d"/><stop offset=".45" stop-color="#00d9ff"/><stop offset="1" stop-color="#1b6cff"/></linearGradient>
<linearGradient id="barPurple" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4d126e"/><stop offset=".45" stop-color="#c72cf5"/><stop offset="1" stop-color="#6e39ff"/></linearGradient>
<linearGradient id="barGreen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#075e5a"/><stop offset=".45" stop-color="#21e5b2"/><stop offset="1" stop-color="#18a98e"/></linearGradient>
<linearGradient id="barOrange" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#743006"/><stop offset=".45" stop-color="#ff9b13"/><stop offset="1" stop-color="#c64a08"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#273a5c" stroke-opacity=".22"/></pattern>
</defs>
<rect width="100%" height="100%" rx="18" fill="url(#bg)"/>
<rect x="20" y="18" width="{W-40}" height="{H-36}" rx="14" fill="url(#grid)" stroke="#16375a"/>
<text x="50" y="50" fill="#00e5ff" font-family="Arial,sans-serif" font-size="12" letter-spacing="3">MONTHLY ACTIVITY // 30 DAYS</text>
<text x="{W-50}" y="50" text-anchor="end" fill="#8b9bc0" font-family="Arial,sans-serif" font-size="10" letter-spacing="2">DEMO DATA</text>
'''
for v in range(0,11,2):
    y=top+plot_h-(v/maxv)*plot_h
    svg+=f'<line x1="{left}" y1="{y:.1f}" x2="{W-right}" y2="{y:.1f}" stroke="#355071" stroke-opacity=".42"/>'
    svg+=f'<text x="{left-15}" y="{y+4:.1f}" text-anchor="end" fill="#91a4c7" font-family="Arial,sans-serif" font-size="11">{v}</text>'
svg+=f'<text x="24" y="{top+plot_h/2}" transform="rotate(-90 24 {top+plot_h/2})" text-anchor="middle" fill="#b8c7e5" font-family="Arial,sans-serif" font-size="11" letter-spacing="2">HOURS</text>'
colors=["barCyan","barPurple","barGreen","barOrange"]
for i,val in enumerate(values):
    x=left+i*(bar_w+gap); bh=(val/maxv)*plot_h; y=top+plot_h-bh; depth=9
    svg+=f'<polygon points="{x+bar_w},{y+5} {x+bar_w+depth},{y-2} {x+bar_w+depth},{top+plot_h-2} {x+bar_w},{top+plot_h}" fill="#081a31" stroke="#183a59" stroke-width=".7"/>'
    svg+=f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w}" height="{bh:.1f}" rx="2" fill="url(#{colors[i%4]})" stroke="#5beaff" stroke-opacity=".35"/>'
    svg+=f'<polygon points="{x},{y} {x+bar_w},{y} {x+bar_w+depth},{y-7} {x+depth},{y-7}" fill="#78efff" fill-opacity=".55" stroke="#a8f7ff" stroke-opacity=".6"/>'
    svg+=f'<text x="{x+bar_w/2}" y="{y-13}" text-anchor="middle" fill="#d8f9ff" font-family="Arial,sans-serif" font-size="10" font-weight="bold">{val}h</text>'
    svg+=f'<text x="{x+bar_w/2+2}" y="{top+plot_h+24}" transform="rotate(-45 {x+bar_w/2+2} {top+plot_h+24})" text-anchor="end" fill="#7f91b5" font-family="Arial,sans-serif" font-size="9">2026-{i+1:02d}</text>'
    svg+=f'<line x1="{x+bar_w/2}" y1="{top+plot_h+2}" x2="{x+bar_w/2}" y2="{top+plot_h+8}" stroke="#54708e"/>'
svg+=f'<text x="{W/2}" y="{H-16}" text-anchor="middle" fill="#00e5ff" font-family="Arial,sans-serif" font-size="10" letter-spacing="2">DATE / DAY</text></svg>'
Path(__file__).resolve().parents[1].joinpath("assets/activity.svg").write_text(svg,encoding="utf-8")
