#!/usr/bin/env python3
"""Build the Quiet Signals Lab logo set with the wordmark outlined.

The wordmark is Helvetica Neue Bold with an accent full stop. This script sets the
text with HarfBuzz (so kerning is the font's own), converts every glyph to an SVG
path, and writes the finished logo files. The output needs no font to display.

Run it on a Mac, where Helvetica Neue is installed:

    pip3 install fonttools uharfbuzz cairosvg
    python3 tools/make_logos.py --out brand

Options:
    --font PATH     font file (.ttf, .otf or .ttc). Default: the macOS Helvetica Neue.
    --face NAME     full face name inside a .ttc. Default: "Helvetica Neue Bold".
    --out DIR       where to write the files. Default: brand
    --no-png        skip the PNG exports (they need cairosvg, which needs Cairo:
                    `brew install cairo` if the import fails).

Before publishing anything this produces, confirm your Helvetica Neue licence
covers use in a logo.
"""

import argparse
import os
import sys

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTCollection, TTFont

try:
    import uharfbuzz as hb
except ImportError:
    sys.exit("uharfbuzz is missing: pip3 install uharfbuzz")

# The palette. Same values as the Solander site and the lab site.
INK = "#101010"
PAPER = "#FFFFFF"
ACCENT = "#D2421F"

# Tracking, in em. Display sizes are set tighter than text sizes.
TRACK_DISPLAY = -0.035
TRACK_TEXT = -0.02

DEFAULT_FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
DEFAULT_FACE = "Helvetica Neue Bold"

# QSL in Morse code, in units where a dot is 1 x 1. Dash = 3, gaps = 1, letter gap = 3.
# Each entry is (x, width, colour key). The S is the accent.
MORSE_RULE = [
    (0, 3, "ink"), (4, 3, "ink"), (8, 1, "ink"), (10, 3, "ink"),        # Q  --.-
    (16, 1, "accent"), (18, 1, "accent"), (20, 1, "accent"),            # S  ...
    (24, 1, "ink"), (26, 3, "ink"), (30, 1, "ink"), (32, 1, "ink"),     # L  .-..
]
MORSE_RULE_UNITS = 33


def num(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Face:
    """A font face: outlines from fontTools, shaping from HarfBuzz."""

    def __init__(self, path, face_name):
        self.path = path
        if path.lower().endswith((".ttc", ".otc")):
            coll = TTCollection(path)
            names = []
            for i, f in enumerate(coll.fonts):
                full = (f["name"].getDebugName(4) or "").strip()
                names.append(full)
                if full.lower() == face_name.lower():
                    self.tt, self.index = f, i
                    break
            else:
                sys.exit(f"No face called {face_name!r} in {path}. Faces: {', '.join(names)}")
        else:
            self.tt, self.index = TTFont(path), 0
        self.glyphset = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.upem = self.tt["head"].unitsPerEm
        blob = hb.Blob.from_file_path(path)
        self.hbfont = hb.Font(hb.Face(blob, self.index))

    def shape(self, text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {"kern": True, "liga": False})
        return buf.glyph_infos, buf.glyph_positions


class Line:
    """One line of text, shaped, with glyphs relative to its own baseline origin."""

    def __init__(self, face, text, size, tracking):
        self.face, self.text, self.size = face, text, size
        scale = size / face.upem
        infos, poss = face.shape(text)
        self.glyphs = []  # (glyph name, x, y, char index)
        x = 0.0
        for i, (info, pos) in enumerate(zip(infos, poss)):
            name = face.order[info.codepoint]
            self.glyphs.append((name, x + pos.x_offset * scale, pos.y_offset * scale, info.cluster))
            x += pos.x_advance * scale
            if i < len(infos) - 1:
                x += tracking * size
        self.advance = x
        self.scale = scale

    def _transform(self, gx, gy, ox, oy):
        s = self.scale
        return (s, 0, 0, -s, ox + gx, oy - gy)

    def glyph_bounds(self, ox=0.0, oy=0.0):
        """Ink bounds of each glyph, in output coordinates (y down)."""
        out = []
        for name, gx, gy, _ in self.glyphs:
            bp = BoundsPen(self.face.glyphset)
            self.face.glyphset[name].draw(TransformPen(bp, self._transform(gx, gy, ox, oy)))
            if bp.bounds:
                out.append(bp.bounds)
        return out

    def bounds(self, ox=0.0, oy=0.0):
        bs = self.glyph_bounds(ox, oy)
        return (min(b[0] for b in bs), min(b[1] for b in bs),
                max(b[2] for b in bs), max(b[3] for b in bs))

    def paths(self, ox, oy, text_fill, stop_fill):
        """SVG path elements, the final full stop in its own colour."""
        by_fill = {}
        last = len(self.text) - 1
        for name, gx, gy, cluster in self.glyphs:
            is_stop = self.text[cluster] == "." and cluster == last
            fill = stop_fill if is_stop else text_fill
            pen = SVGPathPen(self.face.glyphset, ntos=num)
            self.face.glyphset[name].draw(TransformPen(pen, self._transform(gx, gy, ox, oy)))
            d = pen.getCommands()
            if d:
                by_fill.setdefault(fill, []).append(d)
        return "".join(f'<path fill="{f}" d="{" ".join(ds)}"/>' for f, ds in by_fill.items())


def svg_doc(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {num(w)} {num(h)}" '
            f'width="{num(w)}" height="{num(h)}" role="img" aria-label="{title}">'
            f"<title>{title}</title>{body}</svg>\n")


def morse_rule(x, y, unit, ink, accent):
    out = []
    for mx, mw, key in MORSE_RULE:
        fill = accent if key == "accent" else ink
        out.append(f'<rect x="{num(x + mx * unit)}" y="{num(y)}" width="{num(mw * unit)}" '
                   f'height="{num(unit)}" fill="{fill}"/>')
    return "".join(out)


def overlaps(a, b, gap):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] + gap <= b[1] or b[3] + gap <= a[1])


def wordmark(face, size, tracking, text_fill, stop_fill):
    line = Line(face, "Quiet Signals Lab.", size, tracking)
    x0, y0, x1, y1 = line.bounds()
    body = line.paths(-x0, -y0, text_fill, stop_fill)
    return svg_doc(x1 - x0, y1 - y0, body, "Quiet Signals Lab")


def stacked_lines(face, size, tracking):
    return [Line(face, t, size, tracking) for t in ("Quiet", "Signals", "Lab.")]


def check_stack(lines, baselines, x_for, size, label):
    """Warn when the descender of one line touches the line below."""
    gap = 0.03 * size
    for i in range(len(lines) - 1):
        upper = lines[i].glyph_bounds(x_for(lines[i]), baselines[i])
        lower = lines[i + 1].glyph_bounds(x_for(lines[i + 1]), baselines[i + 1])
        if any(overlaps(a, b, gap) for a in upper for b in lower):
            print(f"  warning: in {label}, '{lines[i].text}' comes within 0.03em of "
                  f"'{lines[i + 1].text}'. Raise --pitch.", file=sys.stderr)


def square_logo(face, S, pitch, bg, text_fill, stop_fill, with_morse=False):
    """Stacked wordmark anchored bottom-left. Margin 8.75% of the side, type 17.5%."""
    P = S * 28 / 320
    size = S * 56 / 320
    lines = stacked_lines(face, size, TRACK_DISPLAY)
    last_baseline = S - P
    baselines = [last_baseline - (len(lines) - 1 - i) * pitch * size for i in range(len(lines))]
    x_for = lambda ln: P - ln.bounds()[0]  # optical flush left: ink edge on the margin
    check_stack(lines, baselines, x_for, size, "square logo")
    body = f'<rect width="{num(S)}" height="{num(S)}" fill="{bg}"/>'
    if with_morse:
        unit = S * 5 / 320
        body += morse_rule(P, P, unit, text_fill, ACCENT)
    for ln, b in zip(lines, baselines):
        body += ln.paths(x_for(ln), b, text_fill, stop_fill)
    return svg_doc(S, S, body, "Quiet Signals Lab")


def avatar(face, S, pitch, bg, text_fill, stop_fill):
    """Stacked wordmark centred, so a circular crop keeps every letter."""
    size = S * 0.17
    lines = stacked_lines(face, size, TRACK_DISPLAY)
    baselines = [i * pitch * size for i in range(len(lines))]
    lefts = [-ln.bounds()[0] for ln in lines]
    boxes = [ln.bounds(l, b) for ln, l, b in zip(lines, lefts, baselines)]
    x0 = min(b[0] for b in boxes); y0 = min(b[1] for b in boxes)
    x1 = max(b[2] for b in boxes); y1 = max(b[3] for b in boxes)
    dx = (S - (x1 - x0)) / 2 - x0
    dy = (S - (y1 - y0)) / 2 - y0
    check_stack(lines, [b + dy for b in baselines], lambda ln: lefts[lines.index(ln)] + dx, size, "avatar")
    body = f'<rect width="{num(S)}" height="{num(S)}" fill="{bg}"/>'
    for ln, l, b in zip(lines, lefts, baselines):
        body += ln.paths(l + dx, b + dy, text_fill, stop_fill)
    return svg_doc(S, S, body, "Quiet Signals Lab")


def favicon(face, S, bg, text_fill, stop_fill):
    """'Q.' centred on a square. The Q fills about 62% of the height."""
    probe = Line(face, "Q.", 100, -0.04)
    bx0, by0, bx1, by1 = probe.bounds()
    size = 100 * min((S * 0.62) / (by1 - by0), (S * 0.80) / (bx1 - bx0))
    line = Line(face, "Q.", size, -0.04)
    x0, y0, x1, y1 = line.bounds()
    dx = (S - (x1 - x0)) / 2 - x0
    dy = (S - (y1 - y0)) / 2 - y0
    body = f'<rect width="{num(S)}" height="{num(S)}" fill="{bg}"/>' + line.paths(dx, dy, text_fill, stop_fill)
    return svg_doc(S, S, body, "Quiet Signals Lab")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--font", default=DEFAULT_FONT)
    ap.add_argument("--face", default=DEFAULT_FACE)
    ap.add_argument("--out", default="brand")
    ap.add_argument("--pitch", type=float, default=0.98, help="line spacing of the stacked logo, in em")
    ap.add_argument("--no-png", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(args.font):
        sys.exit(f"Font not found: {args.font}. Pass --font with the path to Helvetica Neue.")
    face = Face(args.font, args.face)
    os.makedirs(args.out, exist_ok=True)

    files = {
        "wordmark.svg": wordmark(face, 100, TRACK_DISPLAY, INK, ACCENT),
        "wordmark-dark.svg": wordmark(face, 100, TRACK_DISPLAY, PAPER, ACCENT),
        "wordmark-text.svg": wordmark(face, 18, TRACK_TEXT, INK, ACCENT),
        "wordmark-text-dark.svg": wordmark(face, 18, TRACK_TEXT, PAPER, ACCENT),
        "logo-square.svg": square_logo(face, 1000, args.pitch, PAPER, INK, ACCENT),
        "logo-square-dark.svg": square_logo(face, 1000, args.pitch, INK, PAPER, ACCENT),
        "logo-square-morse.svg": square_logo(face, 1000, args.pitch, PAPER, INK, ACCENT, with_morse=True),
        "logo-square-accent.svg": square_logo(face, 1000, args.pitch, ACCENT, INK, PAPER),
        "avatar.svg": avatar(face, 1000, args.pitch, INK, PAPER, ACCENT),
        "avatar-light.svg": avatar(face, 1000, args.pitch, PAPER, INK, ACCENT),
        "favicon.svg": favicon(face, 64, INK, PAPER, ACCENT),
    }
    for name, svg in files.items():
        with open(os.path.join(args.out, name), "w") as fh:
            fh.write(svg)
        print(f"wrote {os.path.join(args.out, name)}")

    if args.no_png:
        return
    try:
        import cairosvg
    except Exception as exc:  # cairosvg needs the Cairo library
        print(f"Skipped PNGs ({exc}). brew install cairo, then pip3 install cairosvg.", file=sys.stderr)
        return
    png = os.path.join(args.out, "png")
    os.makedirs(png, exist_ok=True)
    jobs = [
        ("favicon.svg", "favicon-16.png", 16), ("favicon.svg", "favicon-32.png", 32),
        ("favicon.svg", "favicon-48.png", 48), ("favicon.svg", "apple-touch-icon.png", 180),
        ("avatar.svg", "avatar-400.png", 400), ("avatar.svg", "avatar-800.png", 800),
        ("logo-square.svg", "logo-square-1024.png", 1024),
        ("logo-square-dark.svg", "logo-square-dark-1024.png", 1024),
    ]
    for src, dst, px in jobs:
        cairosvg.svg2png(bytestring=files[src].encode(), write_to=os.path.join(png, dst),
                         output_width=px, output_height=px)
        print(f"wrote {os.path.join(png, dst)}")
    cairosvg.svg2png(bytestring=files["wordmark.svg"].encode(),
                     write_to=os.path.join(png, "wordmark-1200.png"), output_width=1200)
    print(f"wrote {os.path.join(png, 'wordmark-1200.png')}")


if __name__ == "__main__":
    main()
