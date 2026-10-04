# Cybernetic Profile V5

V5 preserves the full-width cyberpunk visual scale. Project and social SVGs are visual-only and are wrapped in real README links, so navigation opens the destination instead of the SVG source.

The contribution section is a real-data 2D daily bar chart. GitHub Actions fetches the user's `contributionCalendar` through GraphQL and regenerates the SVG. Each week contains seven bars in Monday→Sunday order; taller bars mean more contributions that day. Month/year labels are shown, and each bar includes an SVG tooltip containing its exact date and contribution count.

The SVG is only the presentation layer; the underlying numbers are generated from GitHub contribution data on every workflow run, not a fake/static dataset. The native GitHub contribution profile link remains available for full native inspection.
