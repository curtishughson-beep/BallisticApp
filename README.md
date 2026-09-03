# Moose Rifle Dope Card

An interactive holdover chart for sighting in a moose rifle — 7mm Remington Magnum
or .30-06 Springfield.
Single self-contained `index.html` — no build step, no dependencies, and no network
calls at all. Fonts are embedded, so it renders correctly with the phone in airplane
mode or 60 km down a cutline with no bars.

Pick your rifle, pick your load, pick your zero, and read the point of impact and
required hold at any range from the muzzle to 500 yards.

## What it does

- **Two cartridges**, selected at the top: 7mm Rem Mag (30 loads, 139–175 gr) and
  .30-06 Springfield (34 loads, 150–220 gr). The ammunition dropdown filters to the
  selected rifle and remembers the load you last used with each.
- **Zero range 50–400 yd**, on a slider with common presets and a "best all-round"
  button that picks the max-point-blank zero for an 18 in vital zone.
- **Point-of-impact chart, 0–500 yd**, with the hold needed printed under the axis
  at every 50 yards and a drag-anywhere readout.
- **Hold chart** every 25 yd: impact, hold, MOA, 1/4 MOA clicks, velocity, energy.
- **All-loads table** recomputed at whatever range the slider is on, sortable.

Conditions are deliberately fixed at ICAO standard sea-level air — the basis every
manufacturer uses for the numbers on the box, so the chart matches published data.

## Getting it on your phone for offline use

There are two ways, depending on how much you want it to feel like a real app.

### Installable app (recommended)

`app/` is a Progressive Web App — a real home-screen icon, full screen, no browser
chrome, and it keeps working with no signal because a service worker caches
everything on first load.

One-time setup, needs GitHub Pages switched on:

1. On GitHub, go to the repo → **Settings → Pages**.
2. Under **Build and deployment → Source** choose **Deploy from a branch**.
3. Pick this branch (or `main` after merging) and folder **`/ (root)`**, then **Save**.
4. Wait a minute for the first build, then open the site on the phone:

   **https://curtishughson-beep.github.io/BallisticApp/app/**

   The path is **case-sensitive** — `BallisticApp` with both capitals. Lowercase
   `ballisticapp` returns 404. Note it is the `/app/` folder, not the repo root:
   the root serves the same calculator but without the manifest and service worker,
   so it will not install or cache for offline use.
5. **iPhone:** Safari → Share → *Add to Home Screen*.
   **Android:** Chrome → ⋮ → *Install app* / *Add to Home screen*.

Open it once while you still have signal. After that it runs with the radio off.
On iOS, installing to the home screen is what makes the cache stick — a page merely
bookmarked in Safari can be evicted after about a week of disuse.

### Single file, no setup

`app/index.html` is completely self-contained. Save it to the phone (Files on iOS,
Downloads on Android) and open it in the browser. Everything works offline, you just
don't get the home-screen icon or full-screen chrome.

### Keeping the two in sync

`index.html` is the Artifact source and deliberately has no `<!doctype>`/`<head>`/
`<body>` — the Artifact host supplies those. The phone build needs a complete
document, so `build.py` wraps the same content and adds the manifest, icons, iOS meta
tags and service-worker registration:

```
python3 build.py     # regenerates app/index.html from index.html
```

Run it after any edit to `index.html`. Bump `CACHE` in `app/sw.js` when you want
installed phones to pick the new version up.

## The solver

Point-mass numerical integration with Heun's predictor–corrector at a 0.25 ms step,
using standard **G1 drag functions** (Cd interpolated against Mach) and a humid-air
density model. One bore-horizontal trajectory is integrated per load and any zero is
applied as a launch-angle offset, which keeps the zero and range sliders instant.

### Verification

| Check | Result |
|---|---|
| Retained velocity vs. published tables, cup-and-core loads, both cartridges | within 2–18 fps to 500 yd |
| Retained velocity, premium high-BC bullets (ELD-X, Terminal Ascent, Elite Hunter) | 50–140 fps optimistic; error scales with advertised BC, not with the solver |
| G1 vs. G7 drag model on bullets publishing both | agree within 3 fps at 500 yd |
| Muzzle energy, 162 gr @ 2940 fps | 3109 ft·lb vs. 3110 published |
| 10 mph full-value crosswind, 162 ELD-X | 4.6 in @ 300 yd, 13.4 in @ 500 yd vs. ~4.6 / ~13.9 published |
| Density ratio at ICAO standard | 1.0000 |
| Launch-angle offset vs. true re-integration at the zero angle, 5× finer step | exact to 0.000 in at 500 yd |
| Vertical drag damping | mean k ≈ 0.72 /s; drop legitimately ~13% under vacuum 0.5gt² |
| Offline operation | server killed and network cut: reloads, renders embedded fonts, and recomputes new loads with zero requests |

### Why the atmospherics were dropped

Measured, not assumed — 200 yd zero, path at 500 yd:

| Condition | 162 gr ELD-X | 150 gr Core-Lokt |
|---|---|---|
| ICAO standard | −36.4 in | −38.9 in |
| Stonewall, MB · 5 °C · 820 ft | −36.4 in | −38.8 in |
| …plus cold powder at 5 °C | −37.4 in | −39.8 in |
| Late season · −15 °C | −39.4 in | −42.6 in |

Air density is worth under 0.1 in at 500 yd at Manitoba elevations. Cold powder is
worth about 1 in near freezing. By comparison, ±50 fps of muzzle velocity is worth
±1.5 in, and scope height ±0.25 in is worth ±0.4 in.

## Limitations

Published velocities come from 24 in test barrels; real rifles routinely run 50–100
fps off them, which matters more than every weather effect combined. No wind, spin
drift, or shot angle is modelled. Confirm the hold on paper at the ranges you intend
to shoot.

## A note on advertised ballistic coefficients

Cup-and-core loads match their published tables here to within about 18 fps at 500 yd.
Premium high-BC bullets come out 50–140 fps *faster* than the maker's own table, and
the gap scales with the advertised BC rather than with anything in the solver — three
cup-and-core loads across both cartridges match tightly, which rules out a systematic
solver bias. Switching those bullets to their published G7 coefficients moves the
answer by under 3 fps, so the drag model is not the cause either. This is the familiar
tendency for advertised hunting-bullet BCs to run ahead of measured ones. In practice
it means a couple of inches less holdover than reality at 400–500 yd on those loads,
and nothing noticeable inside 300.
