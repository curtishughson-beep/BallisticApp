# 7mm Rem Mag Dope Card

An interactive ballistics solver for sighting in a 7mm Remington Magnum for moose.
Single self-contained `index.html` — no build step, no dependencies. Open it, or
serve it anywhere static.

## What it does

- **30 popular factory loads**, 139–175 gr, with manufacturer-published muzzle
  velocity and ballistic coefficient (G1, plus G7 where the maker publishes one).
- **Range slider, 25–500 yd**, driving live drop, MOA dial-up and exact 1/4 MOA
  click counts, wind drift, impact velocity, retained energy, and flight time.
- **Sight-in card** — what your 100 yd group should measure for any zero, max
  point blank range for an 18 in vital zone, and an ethical range ceiling.
- **Dead-hold impact target** showing where a centre hold actually lands against
  the vitals at the selected range.
- **Range-correction tool** — enter where the group landed, get clicks to move it.
- **All-loads comparison table** recomputed at whatever range the slider is on.
- Conditions: temperature, elevation, humidity, wind speed and clock direction,
  barrel length, scope height, and an optional chronographed velocity override.
  Manitoba presets included.

## The solver

Point-mass numerical integration in three dimensions with Heun's
predictor–corrector at a 0.25 ms step:

- Standard **G1 and G7 drag functions** (Cd interpolated against Mach).
- **Humid-air density ratio** from temperature, elevation, and relative humidity
  (standard lapse for station pressure, Magnus for vapour pressure).
- **Crosswind integrated directly** into the relative-airspeed vector rather than
  approximated with a lag-time formula.
- Powder-temperature and barrel-length velocity corrections.

One bore-horizontal trajectory is integrated per load and any zero is applied as a
launch-angle offset, which keeps the zero and range controls instant.

### Verification

Checked against manufacturer-published data and analytically:

| Check | Result |
|---|---|
| Retained velocity vs. published tables (Barnes 140 TTSX, Remington 150 Core-Lokt, Federal 160 Partition) | within 2–18 fps to 500 yd |
| Muzzle energy, 162 gr @ 2940 fps | 3109 ft·lb vs. 3110 published |
| 10 mph full-value crosswind, 162 ELD-X | 4.6 in @ 300 yd, 13.4 in @ 500 yd vs. ~4.6 / ~13.9 published |
| Density ratio at ICAO standard | 1.0000 |
| Launch-angle offset vs. true re-integration at the zero angle, 5× finer step | exact to 0.000 in at 500 yd |
| Vertical drag damping | mean k ≈ 0.72 /s, drop legitimately ~13% under vacuum 0.5gt² |

## Limitations

Published velocities come from 24 in test barrels and real rifles routinely run
50–100 fps off the box — use the chronograph field. The solver does not model spin
drift, aerodynamic jump, Coriolis, or uphill/downhill shot angle; past roughly
400 yd those begin to matter. Confirm the dope on paper at the ranges you intend
to shoot.
