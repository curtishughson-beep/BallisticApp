# 7mm Rem Mag Dope Card

An interactive holdover chart for sighting in a 7mm Remington Magnum for moose.
Single self-contained `index.html` — no build step, no dependencies.

Pick your load from the dropdown, pick your zero, and read the point of impact and
required hold at any range from the muzzle to 500 yards.

## What it does

- **30 popular factory loads**, 139–175 gr, in one dropdown grouped by brand.
- **Zero range 50–400 yd**, on a slider with common presets and a "best all-round"
  button that picks the max-point-blank zero for an 18 in vital zone.
- **Point-of-impact chart, 0–500 yd**, with the hold needed printed under the axis
  at every 50 yards and a drag-anywhere readout.
- **Hold chart** every 25 yd: impact, hold, MOA, 1/4 MOA clicks, velocity, energy.
- **All-loads table** recomputed at whatever range the slider is on, sortable.

Conditions are deliberately fixed at ICAO standard sea-level air — the basis every
manufacturer uses for the numbers on the box, so the chart matches published data.

## The solver

Point-mass numerical integration with Heun's predictor–corrector at a 0.25 ms step,
using standard **G1 drag functions** (Cd interpolated against Mach) and a humid-air
density model. One bore-horizontal trajectory is integrated per load and any zero is
applied as a launch-angle offset, which keeps the zero and range sliders instant.

### Verification

| Check | Result |
|---|---|
| Retained velocity vs. published tables (Barnes 140 TTSX, Remington 150 Core-Lokt, Federal 160 Partition) | within 2–18 fps to 500 yd |
| Muzzle energy, 162 gr @ 2940 fps | 3109 ft·lb vs. 3110 published |
| 10 mph full-value crosswind, 162 ELD-X | 4.6 in @ 300 yd, 13.4 in @ 500 yd vs. ~4.6 / ~13.9 published |
| Density ratio at ICAO standard | 1.0000 |
| Launch-angle offset vs. true re-integration at the zero angle, 5× finer step | exact to 0.000 in at 500 yd |
| Vertical drag damping | mean k ≈ 0.72 /s; drop legitimately ~13% under vacuum 0.5gt² |

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
