from __future__ import annotations

import math
import os
import random
import textwrap
import urllib.request
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
USERNAME = os.getenv("PROFILE_USER", "Larpsec1337")
TOKEN = os.getenv("GITHUB_TOKEN", "")

W, H = 960, 540
FRAMES = 56
FPS_MS = 70

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
]
BOLD_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf",
]


def choose_font(paths: list[str], size: int):
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def font(size: int, bold: bool = False):
    return choose_font(BOLD_PATHS if bold else FONT_PATHS, size)


def fetch_profile() -> dict:
    req = urllib.request.Request(
        f"https://api.github.com/users/{USERNAME}",
        headers={
            "User-Agent": "Larpsec1337-profile-chaos-generator",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
            "Accept": "application/vnd.github+json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return {"login": USERNAME, "public_repos": "?", "followers": "?", "following": "?"}


def stripe(draw: ImageDraw.ImageDraw, y: int, h: int, offset: int, colors=((255, 238, 0), (0, 0, 0))):
    block = 36
    for x in range(-block * 2, W + block * 2, block):
        i = (x // block) & 1
        draw.polygon(
            [(x + offset, y), (x + block + offset, y), (x + block // 2 + offset, y + h), (x - block // 2 + offset, y + h)],
            fill=colors[i],
        )


def window(draw, box, title, lines, accent, jitter=0):
    x0, y0, x1, y1 = box
    x0 += jitter
    x1 += jitter
    draw.rectangle((x0, y0, x1, y1), fill=(4, 4, 8), outline=accent, width=2)
    draw.rectangle((x0, y0, x1, y0 + 25), fill=accent)
    draw.text((x0 + 7, y0 + 5), title, font=font(12, True), fill=(0, 0, 0))
    draw.text((x1 - 20, y0 + 4), "×", font=font(14, True), fill=(0, 0, 0))
    y = y0 + 33
    for line in lines:
        draw.text((x0 + 9, y), line, font=font(12), fill=(220, 230, 235))
        y += 17
        if y > y1 - 18:
            break


def terminal_lines(frame: int, stats: dict) -> list[str]:
    pool = [
        f"user={USERNAME}",
        f"repos={stats.get('public_repos','?')} followers={stats.get('followers','?')}",
        "mount /dev/reality /mnt/README",
        "warning: semantic checksum mismatch",
        "grep -R 'meaning' /proc/self  -> 0 results",
        "fork bomb prevented by README parser",
        "packet source: 127.0.0.1 // destination: ???",
        "[OK] paranoia daemon started (cosmetic)",
        "[ERR] normal presentation layer unavailable",
        "[OK] recursive profile mirror mounted",
        "[??] cursor is observing you",
        "sudo rm -rf /boring/profile",
        "echo 'EVERYTHING IS CONNECTED' > /tmp/noise",
        "segfault at 0xDEADC0DE: aesthetics overflow",
        "NOTICE: this is an intentionally fictional interface",
    ]
    start = frame % len(pool)
    return [pool[(start + i) % len(pool)] for i in range(8)]


def draw_network(draw: ImageDraw.ImageDraw, frame: int):
    nodes = [(670, 320), (760, 275), (855, 335), (720, 405), (845, 445), (615, 435)]
    labels = ["README", "404", "YOU", "ROOT", "???", "ORIGIN"]
    for i, a in enumerate(nodes):
        for j, b in enumerate(nodes):
            if j <= i or (i + j + frame) % 3:
                continue
            draw.line((a, b), fill=(140, 0, 255), width=1)
    for i, ((x, y), label) in enumerate(zip(nodes, labels)):
        r = 7 + ((frame + i * 3) % 4)
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(0, 255, 220), outline=(255, 255, 255))
        draw.text((x + 10, y - 8), label, font=font(10, True), fill=(255, 80, 180))


def glitch(img: Image.Image, frame: int) -> Image.Image:
    rng = random.Random(9000 + frame)
    out = img.copy()
    for _ in range(10):
        y = rng.randrange(0, H - 8)
        h = rng.randrange(2, 16)
        dx = rng.randrange(-30, 31)
        band = out.crop((0, y, W, min(H, y + h)))
        out.paste(band, (dx, y))
    if frame % 9 == 0:
        r, g, b = out.split()
        r = Image.new("L", out.size, 0).transform(out.size, Image.AFFINE, (1, 0, 4, 0, 1, 0)) if False else r
    return out


def make_frame(frame: int, stats: dict) -> Image.Image:
    rng = random.Random(1337 * 1000 + frame)
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)

    for _ in range(700):
        x = rng.randrange(W)
        y = rng.randrange(H)
        c = rng.choice([(0, 30, 35), (18, 0, 28), (35, 0, 15), (0, 15, 5), (22, 22, 22)])
        d.point((x, y), fill=c)
    for y in range(0, H, 4):
        d.line((0, y, W, y), fill=(12, 12, 16))

    stripe(d, 0, 28, (frame * 8) % 72)
    d.text((14, 34), f"// {USERNAME.upper()} // INCIDENT README // FRAME {frame:04d}", font=font(20, True), fill=(255, 70, 170))
    d.text((14, 62), "THIS PROFILE HAS EXCEEDED THE MAXIMUM SAFE DENSITY OF INFORMATION", font=font(13, True), fill=(0, 255, 220))

    warnings = ["DO NOT REFRESH", "THE README IS LOOKING BACK", "404 REALITY NOT FOUND", "TOO MANY LAYERS", "NORMALITY WAS DEPRECATED"]
    msg = warnings[(frame // 7) % len(warnings)]
    if frame % 4 != 0:
        d.text((W//2, 105), msg, anchor="mm", font=font(35, True), fill=(255, 235, 0), stroke_width=2, stroke_fill=(120, 0, 140))

    window(d, (18, 145, 535, 300), "root@github:/proc/profile", terminal_lines(frame, stats), (0, 255, 190), jitter=((frame % 11) == 0) * 3)

    x0, y0, x1, y1 = 550, 145, 942, 300
    d.rectangle((x0, y0, x1, y1), fill=(235, 225, 195), outline=(145, 30, 70), width=3)
    d.rectangle((x0, y0, x1, y0+30), fill=(255, 90, 150))
    d.text((x0+8, y0+6), "LARPSEC1337 (UNVERIFIED ENTITY)", font=font(13, True), fill=(20, 0, 8))
    info = [
        ("TYPE", "profile / containment breach"),
        ("STATUS", "rendering" if frame % 2 else "REDACTED"),
        ("THREAT", f"{((frame * 37) % 100):02d}% aesthetic hazard"),
        ("ORIGIN", "github.com/Larpsec1337"),
        ("CANON", "disputed by 14 editors"),
        ("NOTES", "[citation needed] [citation needed]"),
    ]
    yy = y0 + 38
    for k, v in info:
        d.text((x0+8, yy), k, font=font(11, True), fill=(100, 0, 45))
        d.text((x0+98, yy), v, font=font(11), fill=(30, 20, 25))
        yy += 19

    d.rectangle((18, 316, 585, 517), fill=(15, 8, 5), outline=(180, 80, 30), width=2)
    d.text((30, 325), "EVIDENCE BOARD // ALL ARROWS EVENTUALLY POINT BACK TO README.md", font=font(12, True), fill=(255, 180, 40))
    cards = [
        (40, 360, "COMMIT\n7f3a??"),
        (180, 390, "BADGE\nSERVICE"),
        (320, 355, "STATIC\nNOISE"),
        (455, 405, "PROFILE\nMIRROR"),
        (265, 455, "YOU ARE\nHERE"),
    ]
    centers = []
    for i, (x, y, txt) in enumerate(cards):
        w, h = 94, 48
        centers.append((x+w//2, y+h//2))
        fill = (245, 235, 180) if i != 4 else (255, 120, 170)
        d.rectangle((x, y, x+w, y+h), fill=fill, outline=(0,0,0))
        d.text((x+7, y+7), txt, font=font(10, True), fill=(20, 10, 10))
    for i in range(len(centers)):
        a = centers[i]
        b = centers[(i * 2 + 2 + frame // 8) % len(centers)]
        d.line((a, b), fill=(255, 40, 40), width=2)

    d.rectangle((603, 316, 942, 517), fill=(3, 3, 9), outline=(110, 0, 220), width=2)
    d.text((614, 326), "CAUSALITY GRAPH (DO NOT INTERPRET)", font=font(12, True), fill=(180, 90, 255))
    draw_network(d, frame)

    pts = []
    for x in range(615, 930, 4):
        t = (x - 615) / 28 + frame * 0.28
        y = 385 + int(math.sin(t) * 20 + math.sin(t * 2.17) * 8)
        pts.append((x, y))
    d.line(pts, fill=(0, 255, 120), width=2)

    ticker = "  //  ".join([
        "NO JAVASCRIPT WAS HARMED",
        "GITHUB SANITIZER WON",
        "GIF-BASED HALLUCINATION ENGINE ONLINE",
        "README.md IS A CONTAINMENT VESSEL",
        "LARPSEC1337",
        "THERE IS NO FINAL LAYER",
    ])
    tw = d.textbbox((0,0), ticker, font=font(12, True))[2]
    xx = -((frame * 14) % max(1, tw))
    d.rectangle((0, 519, W, 539), fill=(255, 0, 120))
    d.text((xx, 521), ticker + "  //  " + ticker, font=font(12, True), fill=(0,0,0))

    for i in range(4):
        if (frame + i) % 7 == 0:
            x = rng.randrange(80, 800)
            y = rng.randrange(85, 500)
            d.rectangle((x, y, x+rng.randrange(60, 180), y+rng.randrange(8, 16)), fill=(255, 255, 255))
            d.rectangle((x+4, y+3, x+rng.randrange(45, 150), y+8), fill=(0,0,0))

    if frame % 8 in (0, 1):
        crop = img.crop((220, 180, 340, 245)).resize((240, 130), Image.Resampling.NEAREST)
        img.paste(crop, (365, 88))
        d = ImageDraw.Draw(img)
        d.rectangle((365, 88, 605, 218), outline=(255, 0, 0), width=2)
        d.text((370, 92), "ENHANCE x2000", font=font(10, True), fill=(255,255,0))

    img = glitch(img, frame)
    return img


def save_gif(frames: list[Image.Image], path: Path, duration=FPS_MS):
    paletted = []
    for f in frames:
        paletted.append(f.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))
    paletted[0].save(
        path,
        save_all=True,
        append_images=paletted[1:],
        duration=duration,
        loop=0,
        disposal=2,
        optimize=False,
    )


def make_ticker(stats: dict):
    w, h = 960, 120
    frames = []
    text = (
        f"LARPSEC1337 // PUBLIC_REPOS={stats.get('public_repos','?')} // "
        "NORMAL PROFILE MODULE REMOVED // SIGNAL ACQUIRED // "
        "THE README CONTAINS A SMALLER README CONTAINING A SMALLER README // "
    )
    fnt = font(18, True)
    for i in range(42):
        im = Image.new("RGB", (w, h), (0, 0, 0))
        d = ImageDraw.Draw(im)
        for y in range(0, h, 4):
            d.line((0, y, w, y), fill=(20, 0, 25))
        d.rectangle((0, 0, w, 22), fill=(255, 235, 0))
        d.text((10, 2), "EMERGENCY BROADCAST SYSTEM // PROFILE CORRUPTION EVENT", font=font(13, True), fill=(0,0,0))
        bbox = d.textbbox((0,0), text, font=fnt)
        tw = bbox[2] - bbox[0]
        x = w - ((i * 31) % (tw + w))
        d.text((x, 43), text + text, font=fnt, fill=(0,255,210))
        d.text((10, 82), "█████████████▒▒▒▒▒▒▒▒▒▒▒  DO NOT ATTEMPT TO MAKE SENSE OF THE GRAPHICS  ▒▒▒▒▒▒▒▒▒██████████", font=font(12, True), fill=(255,0,130))
        frames.append(im.convert("P", palette=Image.Palette.ADAPTIVE, colors=64))
    frames[0].save(ASSETS / "ticker.gif", save_all=True, append_images=frames[1:], duration=65, loop=0, disposal=2, optimize=False)


def main():
    stats = fetch_profile()
    frames = [make_frame(i, stats) for i in range(FRAMES)]
    save_gif(frames, ASSETS / "chaos.gif")
    make_ticker(stats)
    print(f"generated {ASSETS / 'chaos.gif'}")
    print(f"generated {ASSETS / 'ticker.gif'}")


if __name__ == "__main__":
    main()
