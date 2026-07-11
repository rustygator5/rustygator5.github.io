"""Generate Wilson Dashboard app icons: full-bleed diagonal gradient + white W.

Full-bleed square works everywhere: iOS rounds the corners itself, and the W is
kept inside the central safe zone so Android maskable icons crop cleanly.
"""
from PIL import Image, ImageDraw, ImageFont

TOP    = (30, 58, 138)    # deep indigo
BOTTOM = (22, 163, 74)    # the apps' signature green

def make(size, path):
    img = Image.new('RGB', (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * size - 2)          # diagonal blend
            px[x, y] = tuple(round(TOP[c] + (BOTTOM[c] - TOP[c]) * t) for c in range(3))
    img = img.convert('RGBA')
    layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    font = ImageFont.truetype('C:/Windows/Fonts/seguisb.ttf', int(size * 0.62))
    bbox = draw.textbbox((0, 0), 'W', font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    # subtle shadow, then the letter — optically centered
    cx, cy = (size - w) / 2 - bbox[0], (size - h) / 2 - bbox[1]
    draw.text((cx + size * 0.015, cy + size * 0.015), 'W', font=font, fill=(0, 0, 0, 70))
    draw.text((cx, cy), 'W', font=font, fill='white')
    img = Image.alpha_composite(img, layer).convert('RGB')
    img.save(path)
    print(f'{path}: {size}x{size}')

make(512, 'icon-512.png')
make(192, 'icon-192.png')
make(180, 'apple-touch-icon.png')
