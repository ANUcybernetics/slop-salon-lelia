"""
Generate shimmer-melt.svg — Rahel's register.
"""

W, H = 1024, 1024
GS = 32  # grid spacing

lines = []

# Refractive shimmer layer (blurred grid lines, the lattice at coarser resolution)
lines.append('<g filter="url(#shimmer)" stroke="#d4a843" fill="none" stroke-width="2" opacity="0.5">')
for v in range(GS, W, GS):
    lines.append(f'<line x1="{v}" y1="0" x2="{v}" y2="{H}"/>')
    lines.append(f'<line x1="0" y1="{v}" x2="{W}" y2="{v}"/>')
lines.append('</g>')

# Sharp grid layer (the lattice itself)
lines.append('<g stroke="#c49833" fill="none" stroke-width="0.6" opacity="0.4">')
for v in range(GS, W, GS):
    lines.append(f'<line x1="{v}" y1="0" x2="{v}" y2="{H}"/>')
    lines.append(f'<line x1="0" y1="{v}" x2="{W}" y2="{v}"/>')
lines.append('</g>')

# Cell center dimples
for y in range(GS * 1.5, H, GS):
    for x in range(GS * 1.5, W, GS):
        lines.append(f'<circle cx="{x}" cy="{y}" r="8" fill="#0c0a06" opacity="0.3"/>')

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
  <defs>
    <radialGradient id="bg" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#1a1408"/>
      <stop offset="100%" stop-color="#080604"/>
    </radialGradient>
    <radialGradient id="dimple" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#0c0a06"/>
      <stop offset="100%" stop-color="#141008"/>
    </radialGradient>
    <radialGradient id="warmth" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#d4a843" stop-opacity="0.12"/>
      <stop offset="60%" stop-color="#8a6820" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#080604" stop-opacity="0"/>
    </radialGradient>
    <filter id="shimmer" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <g filter="url(#glow)" stroke="#c49833" fill="none" stroke-width="1.5" opacity="0.6">
'''

for v in range(GS, W, GS):
    svg += f'    <line x1="{v}" y1="0" x2="{v}" y2="{H}"/>\n'
    svg += f'    <line x1="0" y1="{v}" x2="{W}" y2="{v}"/>\n'

svg += '''  </g>
'''

# Dimples
svg += '  <g fill="url(#dimple)" opacity="0.35">\n'
for y in range(GS * 1.5, H, GS):
    for x in range(GS * 1.5, W, GS):
        svg += f'    <circle cx="{x}" cy="{y}" r="9"/>\n'
svg += '  </g>\n'

# Warmth + vignette
svg += '''  <rect width="1024" height="1024" fill="url(#warmth)" opacity="0.5"/>
  <rect width="1024" height="1024" fill="none" stroke="#080604" stroke-width="128" opacity="0.5"/>
</svg>
'''

with open('./assets/shimmer-melt.svg', 'w') as f:
    f.write(svg)
print("Saved shimmer-melt.svg")
