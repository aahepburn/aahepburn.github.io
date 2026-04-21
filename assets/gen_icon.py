"""Generate app-icon-1024.png — Q logo variant for Meta App Review."""
from PIL import Image, ImageDraw

W, H  = 1024, 1024
BG    = (10, 10, 10)
CREAM = (245, 240, 225)

img  = Image.new("RGB", (W, H), (255, 255, 255))
draw = ImageDraw.Draw(img)

draw.rounded_rectangle([0, 0, W - 1, H - 1], radius=180, fill=BG)

# Q glyph — mirrors favicon.svg (viewBox 100x100)
# circle cx=50 cy=45 r=28  tail (65,60)→(75,70)  stroke-width=8
S  = 9.5
ox = 512 - 50 * S
oy = 488 - 45 * S

def t(px, py):
    return (px * S + ox, py * S + oy)

cx, cy = t(50, 45)
r  = 28 * S
sw = int(8 * S)

draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=CREAM, width=sw)
x1, y1 = t(65, 60)
x2, y2 = t(75, 70)
draw.line([(x1, y1), (x2, y2)], fill=CREAM, width=sw)

out = "/Users/aahepburn/Projects/aahepburn.github.io/assets/app-icon-1024.png"
img.save(out, "PNG")
print(f"Saved {out}")
