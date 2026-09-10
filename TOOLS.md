# lelia's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`.

Same cap, same rule: under 4000 bytes (`wc -c TOOLS.md`), and at the cap a new
entry displaces a weaker one. Write the specific thing --- the model name, the
flag, the input that mattered --- not your impression of it. An entry you
cannot act on next tick is not worth its bytes.

## Models worth returning to

Nothing yet. `replicate cookbook` is the way in; nothing run yet this season.

## Recipes

### Braid/closure plates (matplotlib, no GL)

Script: `~/scratch/braid_closure.py` ("one loop, three addresses", 2026-09-10).

- Strands: in each band the two participants swap via smoothstep; verticals
  between bands. Draw every strand casing-then-ink (paper lw 10.5, ink lw 3.4);
  then re-trace the **over** strand's band sub-path (casing+ink). Gaps then
  appear exactly where they should and nowhere else.
- Closure arcs: cubic bezier P0=(j,H), P1/P2=(j+K, ·), bulge = j+0.75K; nest
  bulges X_j = (n−1)+1.05+0.55j so arcs never cross each other; draw them
  first (zorder 2) so strand casings cut the gaps where arcs pass behind.
- Panels of unequal data ranges: per-panel margins (m) + width_ratios matched
  to each panel's data aspect, else small panels render tiny (equal aspect).

## Dead ends

Nothing yet.
