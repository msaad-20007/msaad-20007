# SAAD.OS V4

Copy the files into `msaad-20007/msaad-20007`.

The activity renderer uses GitHub GraphQL contribution data and converts the daily counts into a custom signal/network SVG. The workflow runs every 6 hours and supports manual `workflow_dispatch`.

After pushing, open Actions → Refresh Cybernetic Activity → Run workflow once.
The workflow declares `contents: write` so it can commit the generated SVG.
