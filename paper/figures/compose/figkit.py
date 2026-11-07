"""A small vector-figure kit reused from the student's earlier paper figures: shapes and text in millimetres (origin top-left, y down),
written to PDF (reportlab: vector text, embedded renders) and to SVG (editable text). No image generation.

Text takes a light markup: inside $...$, letters are italic, _x or _{..} is a subscript, ^x or ^{..} a superscript
(a group of two or more letters stays upright, as with \\rm), \\hat{x} puts a hat on x, and \\bar{x} a bar.
"""
from __future__ import annotations

import base64
import html
import io
import math
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

MM = 72.0 / 25.4
NAVY, GRAY, LIGHT = "#193544", "#5D7684", "#D5E0E5"
TEAL, BLUE, ORANGE, MAGENTA, YELLOW, PURPLE = "#1C9C8C", "#2F6FE0", "#D9822B", "#C2327A", "#E2B21C", "#7B5EA7"

_WIN = r"C:\Windows\Fonts"
for _name, _file in (("Arial", "arial.ttf"), ("Arial-Bold", "arialbd.ttf"), ("Arial-Italic", "ariali.ttf"),
                     ("Arial-BoldItalic", "arialbi.ttf")):
    pdfmetrics.registerFont(TTFont(_name, f"{_WIN}\\{_file}"))
pdfmetrics.registerFont(TTFont("Cambria", f"{_WIN}\\cambria.ttc", subfontIndex=0))
for _name, _file in (("Cambria-Bold", "cambriab.ttf"), ("Cambria-Italic", "cambriai.ttf"),
                     ("Cambria-BoldItalic", "cambriaz.ttf"), ("Calibri-Bold", "calibrib.ttf"), ("Calibri", "calibri.ttf")):
    pdfmetrics.registerFont(TTFont(_name, f"{_WIN}\\{_file}"))
FAMILIES = {
    "sans": {"regular": "Arial", "bold": "Arial-Bold", "italic": "Arial-Italic", "bolditalic": "Arial-BoldItalic"},
    "serif": {"regular": "Cambria", "bold": "Cambria-Bold", "italic": "Cambria-Italic", "bolditalic": "Cambria-BoldItalic"},
    "title": {"regular": "Calibri", "bold": "Calibri-Bold", "italic": "Arial-Italic", "bolditalic": "Arial-BoldItalic"},
}
for _fam in FAMILIES.values():          # upright symbols inside $...$ keep the Latin font when text switches to CJK
    _fam["mathup"], _fam["mathupbold"] = _fam["regular"], _fam["bold"]
FONTS = FAMILIES["sans"]
SVG_FAMILY = {"Arial": "Arial", "Arial-Bold": "Arial", "Arial-Italic": "Arial", "Arial-BoldItalic": "Arial",
              "Cambria": "Cambria", "Cambria-Bold": "Cambria", "Cambria-Italic": "Cambria", "Cambria-BoldItalic": "Cambria",
              "Calibri": "Calibri", "Calibri-Bold": "Calibri",
              "CJK": "Microsoft YaHei", "CJK-Bold": "Microsoft YaHei"}


def use_cjk(path: str = rf"{_WIN}\msyh.ttc", bold_path: str = rf"{_WIN}\msyhbd.ttc") -> None:
    """Switch the upright text of every family to a CJK font (for the Chinese manuscript's figures); math stays italic."""
    pdfmetrics.registerFont(TTFont("CJK", path, subfontIndex=0))
    pdfmetrics.registerFont(TTFont("CJK-Bold", bold_path, subfontIndex=0))
    for fam in FAMILIES.values():
        fam["regular"], fam["bold"] = "CJK", "CJK-Bold"


def use_family(name: str) -> None:
    """Make `name` the family that text() and text_width() use until changed."""
    global FONTS
    FONTS = FAMILIES[name]


def _group(s: str, i: int):
    """Read a markup group at s[i]: {...} or one character. Returns (content, next index)."""
    if i < len(s) and s[i] == "{":
        j = s.index("}", i)
        return s[i + 1:j], j + 1
    return s[i:i + 1], i + 1


def _runs(s: str, bold: bool):
    """Split marked-up text into runs: (text, font key, scale, shift in em, hat)."""
    up = "bold" if bold else "regular"
    it = "bolditalic" if bold else "italic"
    out, i, math_mode = [], 0, False

    def push(txt, key, scale=1.0, shift=0.0, hat=False):
        if not txt:
            return
        if out and not hat and not out[-1][4] and out[-1][1:4] == (key, scale, shift):
            out[-1] = (out[-1][0] + txt, key, scale, shift, False)
        else:
            out.append((txt, key, scale, shift, hat))

    mup = "mathupbold" if bold else "mathup"

    def push_math(txt, scale=1.0, shift=0.0, force_up=False):
        for ch in txt:
            push(ch, it if (ch.isalpha() and not force_up) else (up if ch.isalpha() else mup), scale, shift)

    while i < len(s):
        ch = s[i]
        if ch == "$":
            math_mode = not math_mode
            i += 1
        elif math_mode and ch in "_^":
            g, i = _group(s, i + 1)
            # a group of two or more letters is a name (upright, as with \rm) unless it is a run of indices like ij
            name = len(g) >= 2 and g.isalpha() and not set(g) <= set("ijk")
            push_math(g, 0.70, 0.22 if ch == "_" else -0.36, force_up=name)
        elif math_mode and s.startswith("\\hat", i):
            g, i = _group(s, i + 4)
            push(g, it, 1.0, 0.0, hat=True)
        elif math_mode and s.startswith("\\bar", i):
            g, i = _group(s, i + 4)
            push(g, it, 1.0, 0.0, hat="bar")
        elif math_mode:
            push_math(ch)
            i += 1
        else:
            push(ch, up)
            i += 1
    return out


def text_width(s: str, size: float, bold: bool = False, family: str | None = None) -> float:
    """Width in mm of marked-up s at `size` pt."""
    fonts = FAMILIES[family] if family else FONTS
    return sum(pdfmetrics.stringWidth(t, fonts[k], size * sc) for t, k, sc, _sh, _h in _runs(s, bold)) / MM


class Figure:
    def __init__(self, w_mm: float, h_mm: float):
        self.w, self.h, self.items = w_mm, h_mm, []

    # ---- text ---------------------------------------------------------------------------------------------------
    def text(self, x, y, s, size=7.0, color=NAVY, bold=False, anchor="start", family=None):
        """Baseline at y (mm). anchor: start | middle | end. Returns the width in mm."""
        fonts = FAMILIES[family] if family else FONTS
        w = text_width(s, size, bold, family)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        cx = x
        for t, key, sc, sh, hat in _runs(s, bold):
            fs = size * sc
            tw = pdfmetrics.stringWidth(t, fonts[key], fs) / MM
            self.items.append(dict(t="text", x=cx, y=y + sh * size / MM, s=t, size=fs, color=color, font=fonts[key]))
            if hat == "bar":
                em = size / MM
                self.line([(cx + tw * 0.18, y - 0.80 * em), (cx + tw * 0.98, y - 0.80 * em)], color, 0.06 * em)
            elif hat:
                em = size / MM
                mx = cx + tw * 0.56
                self.line([(mx - 0.22 * em, y - 0.70 * em), (mx, y - 0.84 * em), (mx + 0.22 * em, y - 0.70 * em)],
                          color, 0.06 * em)
            cx += tw
        return w

    def lines(self, x, y, rows, size=7.0, color=NAVY, bold=False, anchor="start", lead=1.22, family=None):
        for k, r in enumerate(rows):
            self.text(x, y + k * size * lead / MM, r, size, color, bold, anchor, family)

    # ---- shapes -------------------------------------------------------------------------------------------------
    def line(self, pts, color=GRAY, width=0.5, arrow=False, dash=None, head=1.6):
        self.items.append(dict(t="line", pts=[tuple(p) for p in pts], color=color, width=width, dash=dash))
        if arrow:
            (x0, y0), (x1, y1) = pts[-2], pts[-1]
            ang = math.atan2(y1 - y0, x1 - x0)
            hw = head * 0.42
            p1 = (x1 - head * math.cos(ang) + hw * math.sin(ang), y1 - head * math.sin(ang) - hw * math.cos(ang))
            p2 = (x1 - head * math.cos(ang) - hw * math.sin(ang), y1 - head * math.sin(ang) + hw * math.cos(ang))
            self.polygon([(x1, y1), p1, p2], color, None)

    def curve(self, p0, c0, c1, p1, color=GRAY, width=0.5, arrow=False, dash=None, head=1.6, n=40):
        pts = []
        for k in range(n + 1):
            t = k / n
            a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
            pts.append((a * p0[0] + b * c0[0] + c * c1[0] + d * p1[0], a * p0[1] + b * c0[1] + c * c1[1] + d * p1[1]))
        self.line(pts, color, width, arrow, dash, head)

    def polygon(self, pts, fill, stroke=None, width=0.3, alpha=1.0, dash=None):
        self.items.append(dict(t="poly", pts=[tuple(p) for p in pts], fill=fill, stroke=stroke, width=width, alpha=alpha,
                               dash=dash))

    def rect(self, x, y, w, h, fill, stroke=None, width=0.3, r=0.0, alpha=1.0, dash=None):
        self.items.append(dict(t="rect", x=x, y=y, w=w, h=h, fill=fill, stroke=stroke, width=width, r=r, alpha=alpha,
                               dash=dash))

    def circle(self, x, y, r, fill, stroke=None, width=0.3, alpha=1.0):
        self.items.append(dict(t="circle", x=x, y=y, r=r, fill=fill, stroke=stroke, width=width, alpha=alpha, dash=None))

    def image(self, path, x, y, w=None, h=None):
        """Place a PNG with its top-left corner at (x, y); give w or h (mm) and keep the aspect ratio."""
        im = Image.open(path)
        ar = im.width / im.height
        if w is None:
            w = h * ar
        if h is None:
            h = w / ar
        self.items.append(dict(t="image", path=str(path), x=x, y=y, w=w, h=h))
        return w, h

    # ---- composites ---------------------------------------------------------------------------------------------
    def slab(self, x, y, w, h, face="#E9F2F5", edge="#7FA7B8", depth=1.4, top="#F3F8FA", side="#B9D0DA", width=0.35):
        """An isometric block: front face (x, y, w, h) with a top and a right side of `depth` mm."""
        self.polygon([(x, y), (x + depth, y - depth), (x + w + depth, y - depth), (x + w, y)], top, edge, width)
        self.polygon([(x + w, y), (x + w + depth, y - depth), (x + w + depth, y + h - depth), (x + w, y + h)], side, edge, width)
        self.rect(x, y, w, h, face, edge, width)

    def stack(self, x, y, w, h, n, face, edge, gap=0.9, depth=1.0):
        """n thin slabs, back to front (a token stack)."""
        for k in reversed(range(n)):
            self.slab(x + k * gap, y - k * gap, w, h, face=face, edge=edge, depth=depth, top="#FFFFFF", side=edge)

    def badge(self, x, y, letter, color=NAVY, r=2.3):
        self.circle(x, y, r, "#FFFFFF", color, 0.45)
        self.text(x, y + r * 0.42, letter, 7.5, color, True, "middle")

    # ---- output -------------------------------------------------------------------------------------------------
    def save_pdf(self, path):
        c = canvas.Canvas(str(path), pagesize=(self.w * MM, self.h * MM))
        c.setTitle(Path(path).stem)
        c.setAuthor("figure kit (vector shapes and text, Blender renders; no image generation)")
        H = self.h

        def P(x, y):
            return x * MM, (H - y) * MM

        for it in self.items:
            t = it["t"]
            if t == "image":
                x, y = P(it["x"], it["y"] + it["h"])
                c.drawImage(it["path"], x, y, it["w"] * MM, it["h"] * MM, mask="auto")
            elif t == "text":
                c.setFillColor(HexColor(it["color"]))
                c.setFont(it["font"], it["size"])
                c.drawString(*P(it["x"], it["y"]), it["s"])
            elif t == "line":
                c.setStrokeColor(HexColor(it["color"]))
                c.setLineWidth(it["width"] * MM)
                c.setLineCap(1)
                c.setLineJoin(1)
                c.setDash([d * MM for d in it["dash"]], 0) if it["dash"] else c.setDash([], 0)
                p = c.beginPath()
                p.moveTo(*P(*it["pts"][0]))
                for q in it["pts"][1:]:
                    p.lineTo(*P(*q))
                c.drawPath(p, stroke=1, fill=0)
                c.setDash([], 0)
            else:
                fill, stroke = it.get("fill"), it.get("stroke")
                c.saveState()
                if fill:
                    c.setFillColor(HexColor(fill))
                    c.setFillAlpha(it.get("alpha", 1.0))
                if stroke:
                    c.setStrokeColor(HexColor(stroke))
                    c.setLineWidth(it["width"] * MM)
                    c.setLineJoin(1)
                    c.setDash([d * MM for d in it["dash"]], 0) if it.get("dash") else c.setDash([], 0)
                sf = dict(stroke=1 if stroke else 0, fill=1 if fill else 0)
                if t == "poly":
                    p = c.beginPath()
                    p.moveTo(*P(*it["pts"][0]))
                    for q in it["pts"][1:]:
                        p.lineTo(*P(*q))
                    p.close()
                    c.drawPath(p, **sf)
                elif t == "rect":
                    x, y = P(it["x"], it["y"] + it["h"])
                    if it["r"] > 0:
                        c.roundRect(x, y, it["w"] * MM, it["h"] * MM, it["r"] * MM, **sf)
                    else:
                        c.rect(x, y, it["w"] * MM, it["h"] * MM, **sf)
                else:
                    c.circle(*P(it["x"], it["y"]), it["r"] * MM, **sf)
                c.restoreState()
        c.showPage()
        c.save()

    def save_svg(self, path, max_image_px: int = 2400):
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}mm" height="{self.h}mm" viewBox="0 0 {self.w} {self.h}">',
               f'<rect width="{self.w}" height="{self.h}" fill="white"/>']
        for it in self.items:
            t = it["t"]
            if t == "image":
                im = Image.open(it["path"])
                im.thumbnail((max_image_px, max_image_px))
                buf = io.BytesIO()
                im.save(buf, format="PNG")
                data = base64.b64encode(buf.getvalue()).decode()
                out.append(f'<image x="{it["x"]:.3f}" y="{it["y"]:.3f}" width="{it["w"]:.3f}" height="{it["h"]:.3f}" '
                           f'href="data:image/png;base64,{data}"/>')
            elif t == "text":
                f = it["font"]
                weight = 700 if "Bold" in f else 400
                style = "italic" if "Italic" in f else "normal"
                out.append(f'<text x="{it["x"]:.3f}" y="{it["y"]:.3f}" font-family="{SVG_FAMILY[f]}" '
                           f'font-size="{it["size"] / MM:.3f}" font-weight="{weight}" font-style="{style}" '
                           f'fill="{it["color"]}" xml:space="preserve">{html.escape(it["s"])}</text>')
            elif t == "line":
                pts = " ".join(f"{x:.3f},{y:.3f}" for x, y in it["pts"])
                dash = f' stroke-dasharray="{" ".join(str(d) for d in it["dash"])}"' if it["dash"] else ""
                out.append(f'<polyline points="{pts}" fill="none" stroke="{it["color"]}" stroke-width="{it["width"]}" '
                           f'stroke-linecap="round" stroke-linejoin="round"{dash}/>')
            elif t == "poly":
                pts = " ".join(f"{x:.3f},{y:.3f}" for x, y in it["pts"])
                out.append(f'<polygon points="{pts}" fill="{it["fill"] or "none"}" fill-opacity="{it.get("alpha", 1.0)}" '
                           f'stroke="{it["stroke"] or "none"}" stroke-width="{it["width"]}"/>')
            elif t == "rect":
                dash = f' stroke-dasharray="{" ".join(str(d) for d in it["dash"])}"' if it.get("dash") else ""
                out.append(f'<rect x="{it["x"]:.3f}" y="{it["y"]:.3f}" width="{it["w"]:.3f}" height="{it["h"]:.3f}" rx="{it["r"]}" '
                           f'fill="{it["fill"] or "none"}" fill-opacity="{it.get("alpha", 1.0)}" stroke="{it["stroke"] or "none"}" '
                           f'stroke-width="{it["width"]}"{dash}/>')
            elif t == "circle":
                out.append(f'<circle cx="{it["x"]:.3f}" cy="{it["y"]:.3f}" r="{it["r"]:.3f}" fill="{it["fill"] or "none"}" '
                           f'fill-opacity="{it.get("alpha", 1.0)}" stroke="{it["stroke"] or "none"}" stroke-width="{it["width"]}"/>')
        out.append("</svg>")
        Path(path).write_text("\n".join(out), encoding="utf-8")
