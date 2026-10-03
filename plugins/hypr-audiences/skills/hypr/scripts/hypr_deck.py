#!/usr/bin/env python3
"""Gera o deck "Audience Discovery" de um plano de audiências HYPR (.pptx),
seguindo a estrutura e identidade dos decks oficiais HYPR (FY26).

Uso: python3 hypr_deck.py plano.json saida.pptx
Requer: python-pptx

Texto com *asteriscos* vira destaque em azul HYPR.
"""
import json, sys, os, datetime, re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

# ---- Tokens (decks HYPR FY26) ----
DARK = RGBColor(0x14, 0x1B, 0x21)       # fundo escuro dos decks Audience Discovery
DARK2 = RGBColor(0x1B, 0x26, 0x2F)      # painéis escuros
LIGHT = RGBColor(0xFA, 0xFA, 0xFA)
CARD = RGBColor(0xF1, 0xF3, 0xF4)
CARD_BLUE = RGBColor(0xE9, 0xF3, 0xF7)
LINE = RGBColor(0xE2, 0xE6, 0xE9)
BLUE = RGBColor(0x4F, 0xA8, 0xCF)
BLUE_DEEP = RGBColor(0x33, 0x97, 0xB9)
INK = RGBColor(0x1B, 0x26, 0x2F)
BODY = RGBColor(0x55, 0x66, 0x70)
MUTED = RGBColor(0x8A, 0x9A, 0xA4)
MUTED_DARK = RGBColor(0x6E, 0x7E, 0x88)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SOFT = RGBColor(0xC9, 0xD2, 0xDB)

F_LIGHT, F_REG, F_MED, F_SEMI = "Montserrat Light", "Montserrat", "Montserrat Medium", "Montserrat SemiBold"
F_MONO = "IBM Plex Mono"

W, H = Inches(13.333), Inches(7.5)
MX = Inches(0.75)
YEAR = str(datetime.date.today().year)


def fmt_vol(v, short=False):
    v = float(v or 0)
    if v >= 1e6:
        s = f"{v/1e6:.1f}".replace(".", ",")
        if s.endswith(",0"): s = s[:-2]
        return (s, "M") if short else s + " mi"
    if v >= 1e3:
        return (f"{v/1e3:.0f}", "k") if short else f"{v/1e3:.0f} mil"
    return (f"{v:.0f}", "") if short else f"{v:.0f}"


def fmt_int(v):
    return f"{int(v or 0):,}".replace(",", ".")


def split_title(name):
    """Realça a última palavra relevante em azul: 'Visitantes de Postos Ipiranga' -> 'Visitantes de Postos *Ipiranga*'."""
    name = re.sub(r"\s*\(base \d\)$", "", name)
    words = name.split()
    if len(words) <= 1: return f"*{name}*"
    return " ".join(words[:-1]) + f" *{words[-1]}*"


class Deck:
    def __init__(self, plan):
        self.p = plan
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = W, H
        self.blank = self.prs.slide_layouts[6]
        self.n = 0
        self.all_auds = [dict(a, layer=l["name"]) for l in plan["layers"] for a in l["audiences"]]

    # ---------- primitivas ----------
    def _run(self, para, text, size, color, font, align=None, spacing=None):
        parts = text.split("*")
        for i, part in enumerate(parts):
            if not part: continue
            r = para.add_run(); r.text = part
            r.font.size = Pt(size); r.font.name = font
            r.font.color.rgb = BLUE if i % 2 else color
            if spacing is not None:
                r._r.get_or_add_rPr().set("spc", str(int(spacing * 100)))
        if align is not None: para.alignment = align

    def text(self, s, text, x, y, w, h, size, color, font=F_REG, align=None, lines=None, line_spacing=1.15, anchor=MSO_ANCHOR.TOP, spacing=None):
        tb = s.shapes.add_textbox(x, y, w, h)
        tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        for i, line in enumerate(lines if lines is not None else [text]):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.line_spacing = line_spacing
            self._run(para, line, size, color, font, align, spacing)
        return tb

    def mono(self, s, text, x, y, w, size=6.5, color=MUTED, align=None, h=Inches(0.22)):
        return self.text(s, text.upper(), x, y, w, h, size, color, F_MONO, align=align, spacing=0.6)

    def rect(self, s, x, y, w, h, fill, radius=None, line=None, lw=0.75):
        shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, x, y, w, h)
        if radius:
            shp.adjustments[0] = min(0.5, radius * 914400 / min(w, h)) if radius > 1 else radius
        if fill is None: shp.fill.background()
        else: shp.fill.solid(); shp.fill.fore_color.rgb = fill
        if line is not None: shp.line.color.rgb = line; shp.line.width = Pt(lw)
        else: shp.line.fill.background()
        shp.shadow.inherit = False
        return shp

    def hline(self, s, x, y, w, color=LINE, pt=0.75):
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x, y, x + w, y)
        ln.line.color.rgb = color; ln.line.width = Pt(pt)
        return ln

    def pill(self, s, text, x, y, fill=None, line=None, color=INK, size=6.5, font=F_MONO, dot=False, h=Inches(0.26), pad=Inches(0.16), w=None):
        label = ("●  " if dot else "") + text.upper() if font == F_MONO else (("●  " if dot else "") + text)
        est = Inches(0.062 if font == F_MONO else 0.075) * len(label) * (size / 7)
        w = w or est + pad * 2
        shp = self.rect(s, x, y, w, h, fill, radius=0.5, line=line)
        tf = shp.text_frame; tf.margin_left = tf.margin_right = pad; tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = False
        self._run(tf.paragraphs[0], label, size, color, font, PP_ALIGN.CENTER, 0.6 if font == F_MONO else None)
        return w

    def tag_box(self, s, text, x, y, w, h=Inches(0.42), dark=False):
        shp = self.rect(s, x, y, w, h, None, radius=0.08, line=DARK_LINE if dark else LINE)
        tf = shp.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = False
        tf.margin_top = tf.margin_bottom = 0
        self._run(tf.paragraphs[0], text.upper(), 7, WHITE if dark else INK, F_SEMI, PP_ALIGN.CENTER, 0.4)

    # ---------- chrome ----------
    def slide(self, dark, tag, footer_mid, footer_left=None):
        s = self.prs.slides.add_slide(self.blank); self.n += 1
        bg = s.background.fill; bg.solid(); bg.fore_color.rgb = DARK if dark else LIGHT
        fg = WHITE if dark else INK
        self.pill(s, tag, MX, Inches(0.42), None, line=(MUTED_DARK if dark else LINE), color=(SOFT if dark else BODY), size=6, dot=True, h=Inches(0.24))
        logo = os.path.join(ASSETS, "hypr_white.png" if dark else "hypr_dark.png")
        s.shapes.add_picture(logo, W - MX - Inches(1.05), Inches(0.44), width=Inches(1.05))
        fl = footer_left or "• HYPR Audiences"
        fc = MUTED_DARK if dark else MUTED
        self.mono(s, fl, MX, H - Inches(0.52), Inches(3), 5.5, fc)
        self.mono(s, footer_mid, Inches(4.5), H - Inches(0.52), Inches(4.33), 5.5, fc, align=PP_ALIGN.CENTER)
        self.mono(s, f"Nacional · {YEAR}", W - MX - Inches(3), H - Inches(0.52), Inches(3), 5.5, fc, align=PP_ALIGN.RIGHT)
        return s

    # ---------- slides ----------
    def cover(self):
        p = self.p
        s = self.slide(True, p.get("cover_tag", "Audience Discovery · " + YEAR), "Capa", "• FY26 Oficial")
        self.mono(s, f"01  {p['brand']}  ·  Audience Discovery", MX, Inches(3.25), Inches(8), 7, BLUE)
        title = p.get("cover_title") or f"Audiências para *{p['brand']}*."
        self.text(s, title, MX, Inches(3.55), Inches(11.5), Inches(1.9), 60, WHITE, F_LIGHT, line_spacing=1.0)
        sub = p.get("subtitle") or p.get("campaign", "")
        self.text(s, sub, MX, Inches(5.5), Inches(9), Inches(0.5), 15, SOFT, F_REG)
        meta = p.get("cover_meta") or " · ".join(x for x in [p.get("campaign_type", "Plano de audiências"), p.get("vertical", ""), p.get("region", "Nacional")] if x)
        self.mono(s, meta, MX, Inches(6.05), Inches(8), 6.5, MUTED_DARK)

    def summary(self, sections):
        s = self.slide(False, "00 Sumário", "Sumário")
        self.mono(s, f"Índice   {len(sections):02d} seções", MX, Inches(3.15), Inches(4), 6.5, MUTED)
        self.text(s, "O que preparamos\npara *vocês*.", MX, Inches(3.45), Inches(5.5), Inches(1.6), 38, INK, F_LIGHT, line_spacing=1.05)
        x, y, w = Inches(6.6), Inches(2.1), Inches(6)
        rh = Inches(0.62)
        self.hline(s, x, y, w)
        for i, name in enumerate(sections):
            yy = y + i * rh
            self.text(s, f"{i+1:02d}", x, yy + Inches(0.14), Inches(0.7), Inches(0.4), 18, BLUE, F_LIGHT)
            self.text(s, name, x + Inches(0.8), yy + Inches(0.19), w - Inches(0.8), Inches(0.4), 13, INK, F_REG)
            self.hline(s, x, yy + rh, w)

    def divider(self, num, title, sub):
        s = self.slide(True, "Audience Discovery · " + YEAR, f"Seção {num:02d}", "• FY26 Oficial")
        self.text(s, f"{num:02d}", MX, Inches(1.9), Inches(5), Inches(1.9), 110, BLUE, F_LIGHT, line_spacing=0.9)
        self.text(s, f"{title}*.*", MX, Inches(3.95), Inches(10), Inches(1.1), 56, WHITE, F_LIGHT)
        self.text(s, sub, MX, Inches(5.15), Inches(8), Inches(0.9), 16, SOFT, F_REG, line_spacing=1.3)

    def context(self):
        p = self.p
        s = self.slide(False, "01 Contexto", "O desafio")
        self.text(s, p.get("context_title") or f"{p['brand']} e seus concorrentes, tudo no mesmo *mapa*.", MX, Inches(1.35), Inches(10.5), Inches(1.4), 32, INK, F_LIGHT, line_spacing=1.05)
        cols = p.get("context_columns") or [
            ("Onde e quando ativar?", p.get("where", "")), ("Para quem?", p.get("who", "")), ("Como provar?", p.get("how", ""))]
        cw = (W - 2 * MX - Inches(0.8)) / 3
        y = Inches(4.55)
        for i, (head, body) in enumerate(cols):
            x = MX + i * (cw + Inches(0.4))
            self.hline(s, x, y, cw)
            self.text(s, f"{i+1:02d}", x, y + Inches(0.25), Inches(1), Inches(0.5), 26, BLUE, F_LIGHT)
            self.text(s, head, x, y + Inches(0.85), cw, Inches(0.35), 13, INK, F_REG)
            self.text(s, body, x, y + Inches(1.2), cw - Inches(0.3), Inches(0.9), 9.5, BODY, F_REG, line_spacing=1.35)
        # premissas (chips) discretas
        prem = p.get("premises") or []
        if prem:
            x = MX
            for t in prem[:4]:
                x += self.pill(s, t, x, Inches(3.3), CARD, None, BODY, 7, F_MED, h=Inches(0.3)) + Inches(0.12)

    def layers_overview(self):
        p = self.p
        layers = p["layers"]
        s = self.slide(False, "02 Audiências · Camadas", "Audience plan")
        total = len(self.all_auds); vol = sum(a.get("volume") or 0 for a in self.all_auds)
        tw = vol or 1
        aff = round(sum((a.get("affinity") or 0) * (a.get("volume") or 0) for a in self.all_auds) / tw)
        self.text(s, p.get("layers_title") or f"*{total} audiências* a partir do briefing.", MX, Inches(1.3), Inches(10.5), Inches(0.8), 32, INK, F_LIGHT)
        self.text(s, p.get("layers_sub") or "Cada camada recebe um papel e uma mensagem diferente. O Brand Affinity ordena quem entra primeiro.", MX, Inches(2.1), Inches(9.5), Inches(0.7), 13, BODY, F_REG, line_spacing=1.35)
        # número grande à direita
        num, suf = fmt_vol(vol, short=True)
        self.text(s, "", W - MX - Inches(3.2), Inches(1.3), Inches(3.2), Inches(0.8), 40, INK, F_LIGHT, align=PP_ALIGN.RIGHT, lines=[f"{num}"])
        tb = s.shapes[-1]; r = tb.text_frame.paragraphs[0].add_run(); r.text = suf; r.font.size = Pt(18); r.font.name = F_LIGHT; r.font.color.rgb = INK
        self.mono(s, f"volume bruto · {aff}% affinity média", W - MX - Inches(3.2), Inches(2.15), Inches(3.2), 6, MUTED, align=PP_ALIGN.RIGHT)
        n = len(layers); gap = Inches(0.25)
        cw = (W - 2 * MX - gap * (n - 1)) / n
        y, ch = Inches(3.1), Inches(3.55)
        for i, l in enumerate(layers):
            x = MX + i * (cw + gap)
            hi = (i == 0)
            self.rect(s, x, y, cw, ch, CARD_BLUE if hi else None, radius=0.08, line=None if hi else LINE)
            self.mono(s, f"{i+1:02d} · {l['name']}", x + Inches(0.3), y + Inches(0.3), cw, 6.5, BLUE if hi else MUTED)
            self.text(s, l.get("headline") or l["name"], x + Inches(0.3), y + Inches(0.6), cw - Inches(0.5), Inches(0.7), 15, INK, F_REG, line_spacing=1.15)
            self.text(s, l.get("description", ""), x + Inches(0.3), y + Inches(1.3), cw - Inches(0.55), Inches(1.2), 9.5, BODY, F_REG, line_spacing=1.35)
            lv = sum(a.get("volume") or 0 for a in l["audiences"]); num, suf = fmt_vol(lv, short=True)
            tb = self.text(s, num, x + Inches(0.3), y + ch - Inches(1.0), Inches(2.2), Inches(0.7), 34, INK, F_LIGHT)
            r = tb.text_frame.paragraphs[0].add_run(); r.text = suf; r.font.size = Pt(14); r.font.name = F_LIGHT; r.font.color.rgb = INK
            self.mono(s, f"{len(l['audiences'])} audiências\nestimadas", x + Inches(1.75) if lv < 1e7 else x + Inches(2.1), y + ch - Inches(0.88), Inches(1.5), 5.5, MUTED, h=Inches(0.4))

    def audience_card(self, a, idx, total):
        p = self.p
        s = self.slide(False, f"{p['brand']} · Audiência {idx:02d}/{total:02d}", "HYPR Special Audiences", "• Estimativas HYPR")
        # painel esquerdo
        px, py, pw, ph = MX, Inches(1.3), Inches(4.9), Inches(5.35)
        img = a.get("image")
        if img and os.path.exists(img):
            pic = s.shapes.add_picture(img, px, py, width=pw, height=ph)
            pic.crop_left = pic.crop_right = 0
        else:
            self.rect(s, px, py, pw, ph, DARK2, radius=0.08)
            self.pill(s, "HYPR Special Audiences", px + Inches(0.35), py + Inches(0.35), None, line=MUTED_DARK, color=SOFT, size=5.5, h=Inches(0.22))
            self.text(s, split_title(a["name"]), px + Inches(0.35), py + Inches(0.8), pw - Inches(0.7), Inches(1.6), 26, WHITE, F_LIGHT, line_spacing=1.05)
            self.mono(s, f"{a.get('main_category','')}  ·  {a.get('sub_category','')}", px + Inches(0.35), py + Inches(2.45), pw - Inches(0.7), 6, MUTED_DARK, h=Inches(0.4))
            # badge numérico
            self.rect(s, px + pw - Inches(1.05), py + ph - Inches(1.05), Inches(0.7), Inches(0.7), None, radius=0.08, line=MUTED_DARK)
            self.text(s, f"{idx:02d}", px + pw - Inches(1.05), py + ph - Inches(0.95), Inches(0.7), Inches(0.5), 16, WHITE, F_LIGHT, align=PP_ALIGN.CENTER)
            self.mono(s, a.get("layer", ""), px + Inches(0.35), py + ph - Inches(0.65), Inches(2.5), 6, BLUE)
        # coluna direita
        x = Inches(6.1); w = W - MX - x
        self.mono(s, a.get("layer", "Audiência").upper() + "      ", x, Inches(1.3), Inches(2), 6, MUTED)
        self.mono(s, a.get("sub_category", ""), x + Inches(1.6), Inches(1.3), Inches(4), 6, BLUE)
        tl = len(re.sub(r"\s*\(base \d\)$", "", a["name"]))
        self.text(s, split_title(a["name"]), x, Inches(1.55) if tl <= 34 else Inches(1.6), w, Inches(0.7), 30 if tl <= 26 else (24 if tl <= 34 else 20), INK, F_LIGHT)
        self.hline(s, x, Inches(2.3), w)
        # número grande
        num, suf = fmt_vol(a.get("volume"), short=True)
        tb = self.text(s, num, x, Inches(2.45), Inches(2.6), Inches(0.9), 48, INK, F_LIGHT)
        r = tb.text_frame.paragraphs[0].add_run(); r.text = suf; r.font.size = Pt(22); r.font.name = F_LIGHT; r.font.color.rgb = INK
        nx = x + Inches(0.75) * len(num) + Inches(0.55)
        self.mono(s, "Usuários\nestimados", nx, Inches(2.75), Inches(1.2), 5.5, MUTED, h=Inches(0.4))
        self.pill(s, p.get("region", "Nacional"), nx + Inches(1.15), Inches(2.72), CARD, None, INK, 7, F_MED, h=Inches(0.28))
        # três stats
        stats = [(fmt_int(a.get("addresses")), "Endereços\nmapeados"), (f"{a.get('affinity', 0)}%", "Brand\nAffinity"), (f"#{a.get('rank', idx)}", f"no ranking\nde {len(self.all_auds)}")]
        sw = Inches(2.1); sy = Inches(3.45)
        for i, (v, lab) in enumerate(stats):
            sx = x + i * sw
            if i: self.rect(s, sx - Inches(0.25), sy + Inches(0.05), Emu(9525), Inches(0.75), LINE)
            self.text(s, v, sx, sy, sw, Inches(0.5), 24, BLUE, F_LIGHT)
            self.mono(s, lab, sx, sy + Inches(0.5), sw, 5.5, MUTED, h=Inches(0.4))
        # tags
        tx, ty = x, Inches(4.45)
        for t in (a.get("tags") or [])[:3]:
            tx += self.pill(s, "+ " + t, tx, ty, CARD, None, BODY, 7, F_MED, h=Inches(0.28)) + Inches(0.1)
        # citação
        self.rect(s, x, Inches(4.95), Emu(19050), Inches(0.75), BLUE)
        quote = a.get("why") or a.get("description", "")
        self.text(s, quote, x + Inches(0.25), Inches(4.93), w - Inches(0.3), Inches(0.8), 12.5, INK, F_REG, line_spacing=1.3)
        self.mono(s, a.get("meta") or f"ID {a.get('id','')}", x + Inches(0.25), Inches(5.75), w, 6, MUTED)
        # redes mapeadas / categorias
        boxes = a.get("networks") or ([a["brand"]] if a.get("brand") else [])
        if not boxes: boxes = [a.get("sub_category", ""), a.get("main_category", "")]
        boxes = [b for b in boxes if b][:4]
        if boxes:
            self.mono(s, "Redes mapeadas" if a.get("networks") or a.get("brand") else "Categoria", x, Inches(6.05), w, 5.5, MUTED)
            bw = (w - Inches(0.15) * (len(boxes) - 1)) / len(boxes) if len(boxes) > 1 else Inches(2.8)
            bw = min(bw, Inches(3))
            for i, b in enumerate(boxes):
                self.tag_box(s, b, x + i * (bw + Inches(0.15)), Inches(6.27), bw, h=Inches(0.4))

    def ranking_table(self, auds, part=None):
        p = self.p
        s = self.slide(False, "02 Audiências · Ranking", "Audience ranking", "• Estimativas HYPR")
        self.text(s, (p.get("ranking_title") or "Ranking completo por *Brand Affinity*") + (f"  ·  {part}" if part else ""), MX, Inches(1.3), Inches(10), Inches(0.7), 28, INK, F_LIGHT)
        cx, cy, cw = MX, Inches(2.2), W - 2 * MX
        rh = Inches(0.37); ch = Inches(0.5) + rh * len(auds) + Inches(0.2)
        self.rect(s, cx, cy, cw, ch, WHITE, radius=0.06, line=LINE)
        cols = [(Inches(0.3), Inches(0.5), "#"), (Inches(0.8), Inches(3.9), "Audiência"), (Inches(4.8), Inches(1.6), "Camada"), (Inches(6.4), Inches(1.5), "Volume"), (Inches(7.9), Inches(1.4), "Endereços"), (Inches(9.3), Inches(2.3), "Brand Affinity")]
        for ox, ow, lab in cols:
            self.text(s, lab, cx + ox, cy + Inches(0.17), ow, Inches(0.3), 9, MUTED, F_MED)
        y = cy + Inches(0.5)
        for i, a in enumerate(auds):
            self.hline(s, cx + Inches(0.3), y, cw - Inches(0.6))
            yy = y + Inches(0.08)
            self.text(s, f"{a.get('rank', i+1):02d}", cx + Inches(0.3), yy, Inches(0.5), Inches(0.25), 9, BLUE, F_MED)
            self.text(s, re.sub(r"\s*\(base \d\)$", "", a["name"]), cx + Inches(0.8), yy, Inches(3.9), Inches(0.25), 9.5, INK, F_REG)
            self.text(s, a.get("layer", ""), cx + Inches(4.8), yy, Inches(1.6), Inches(0.25), 9, BODY, F_REG)
            self.text(s, fmt_vol(a.get("volume")), cx + Inches(6.4), yy, Inches(1.5), Inches(0.25), 9.5, INK, F_REG)
            self.text(s, fmt_int(a.get("addresses")), cx + Inches(7.9), yy, Inches(1.4), Inches(0.25), 9.5, INK, F_REG)
            aff = max(0, min(100, a.get("affinity") or 0)); bw = Inches(1.6)
            self.rect(s, cx + Inches(9.3), yy + Inches(0.07), bw, Inches(0.09), CARD, radius=0.5)
            self.rect(s, cx + Inches(9.3), yy + Inches(0.07), max(Emu(1), int(bw * aff / 100)), Inches(0.09), BLUE if aff >= 75 else MUTED, radius=0.5)
            self.text(s, f"{aff}%", cx + Inches(11.0), yy - Inches(0.01), Inches(0.6), Inches(0.25), 9.5, INK, F_MED)
            y += rh

    def platform(self):
        p = self.p
        sols = {x["solution"]: x for x in p.get("solutions", [])}
        s = self.slide(False, "03 Plataforma", "Core products")
        self.mono(s, "Uma jornada · quatro IQs", MX, Inches(1.3), Inches(5), 6.5, MUTED)
        self.text(s, p.get("platform_title") or "Como fecha o *ciclo*.", MX, Inches(1.55), Inches(10), Inches(0.8), 32, INK, F_LIGHT)
        self.text(s, p.get("platform_note") or "Os quatro pilares rodam sobre a mesma base e se informam: o lugar orienta onde ativar, o formato garante atenção, a transação mostra se virou venda e a pesquisa explica o que ficou.", MX, Inches(2.4), Inches(9.5), Inches(0.7), 12, BODY, F_REG, line_spacing=1.35)
        order = [("geoIQ", "Onde", "Places Graph"), ("adsIQ", "Com o quê", "Max Attention"), ("revIQ", "Quanto", "Groundflow"), ("askIQ", "Por quê", None)]
        gap = Inches(0.25); cw = (W - 2 * MX - gap * 3) / 4; y, ch = Inches(3.45), Inches(3.2)
        for i, (name, q, pw) in enumerate(order):
            x = MX + i * (cw + gap); sol = sols.get(name, {})
            ess = sol.get("priority") == "Essencial"
            self.rect(s, x, y, cw, ch, CARD_BLUE if ess else None, radius=0.08, line=None if ess else LINE)
            self.pill(s, f"{i+1}", x + Inches(0.3), y + Inches(0.3), INK, None, WHITE, 8, F_MED, h=Inches(0.3), w=Inches(0.3), pad=Inches(0.05))
            self.text(s, name, x + Inches(0.75), y + Inches(0.27), cw, Inches(0.4), 17, INK, F_REG)
            self.mono(s, q, x + Inches(0.3), y + Inches(0.78), cw, 6, BLUE)
            if pw: self.mono(s, f"powered by {pw}", x + Inches(0.3), y + Inches(0.98), cw, 5.5, MUTED)
            how = sol.get("how", "")
            self.text(s, how, x + Inches(0.3), y + Inches(1.35), cw - Inches(0.5), Inches(1.3), 9.5, BODY, F_REG, line_spacing=1.35)
            pr = sol.get("priority")
            if pr: self.pill(s, pr, x + Inches(0.3), y + ch - Inches(0.6), BLUE if ess else None, None if ess else LINE, WHITE if ess else BODY, 6, F_MONO, h=Inches(0.24))
        ds = sols.get("Demandshift")
        if ds and ds.get("priority") in ("Essencial", "Recomendado"):
            self.text(s, f"*Demandshift*  ·  {ds.get('how', '')}", MX, Inches(6.75), Inches(11.5), Inches(0.3), 9, BODY, F_REG)

    def measurement(self):
        p = self.p
        s = self.slide(False, "03 Plataforma · Mensuração", "Como provar")
        self.mono(s, "revIQ · powered by Groundflow", MX, Inches(1.3), Inches(5), 6.5, MUTED)
        self.text(s, p.get("measurement_title") or "A campanha virou *venda na loja*? E quanto.", MX, Inches(1.55), Inches(10), Inches(0.8), 32, INK, F_LIGHT)
        self.text(s, p.get("measurement") or "Comparamos o consumo nos pontos de venda das regiões expostas à campanha com regiões equivalentes não expostas, e medimos o incremento no SKU anunciado e na categoria.", MX, Inches(2.5), Inches(5.6), Inches(1.6), 13, BODY, F_REG, line_spacing=1.4)
        steps = p.get("measurement_steps") or [("Linha de base", "Vendas do SKU e da categoria antes do flight, região a região."), ("Exposto vs. controle", "Regiões impactadas comparadas a regiões equivalentes sem campanha."), ("Incremento", "A diferença entre os grupos é o efeito atribuível à mídia.")]
        cw = (W - 2 * MX - Inches(0.8)) / 3; y = Inches(4.55)
        for i, (head, body) in enumerate(steps):
            x = MX + i * (cw + Inches(0.4))
            self.hline(s, x, y, cw)
            self.text(s, f"{i+1:02d}", x, y + Inches(0.25), Inches(1), Inches(0.5), 26, BLUE, F_LIGHT)
            self.text(s, head, x, y + Inches(0.85), cw, Inches(0.35), 13, INK, F_REG)
            self.text(s, body, x, y + Inches(1.2), cw - Inches(0.3), Inches(0.9), 9.5, BODY, F_REG, line_spacing=1.35)

    def closing(self):
        p = self.p
        s = self.slide(True, "Próximos passos", "Próximos passos", "• FY26 Oficial")
        self.text(s, p.get("closing_title") or "Do bolso à *rua*.", MX, Inches(1.6), Inches(11), Inches(1.2), 56, WHITE, F_LIGHT)
        self.text(s, p.get("closing_subtitle") or "O que precisamos para ativar e medir este plano.", MX, Inches(2.8), Inches(9), Inches(0.5), 15, SOFT, F_REG)
        y = Inches(3.9)
        for i, st in enumerate((p.get("next_steps") or [])[:4]):
            self.hline(s, MX, y, Inches(8.5), MUTED_DARK)
            self.text(s, f"{i+1:02d}", MX, y + Inches(0.15), Inches(0.7), Inches(0.3), 12, BLUE, F_LIGHT)
            self.text(s, st, MX + Inches(0.75), y + Inches(0.17), Inches(7.7), Inches(0.35), 12.5, WHITE, F_REG)
            y += Inches(0.6)
        self.mono(s, "hyprgrid.ai", MX, Inches(6.5), Inches(3), 6.5, MUTED_DARK)

    def _clean(self):
        for sl in self.prs.slides:
            for shp in sl.shapes:
                st = shp._element.find(qn("p:style"))
                if st is not None: shp._element.remove(st)

    def build(self, out):
        p = self.p
        max_cards = int(p.get("max_audience_cards", 8))
        ranked = sorted(self.all_auds, key=lambda a: -(a.get("affinity") or 0))
        for i, a in enumerate(ranked): a.setdefault("rank", i + 1)
        cards = ranked[:max_cards]
        sections = ["Contexto & desafio", "Audiências propostas", "Plataforma HYPR · como fecha o ciclo", "Mensuração · exposto vs. controle", "Próximos passos"]
        self.cover(); self.summary(sections)
        self.divider(1, "Contexto", p.get("context_sub") or p.get("objective", "")); self.context()
        self.divider(2, "Audiências", p.get("audiences_sub") or f"{len(self.all_auds)} recortes para {p['brand']}, em {len(p['layers'])} camadas, ordenados por Brand Affinity.")
        self.layers_overview()
        for i, a in enumerate(cards): self.audience_card(a, i + 1, len(cards))
        per = 12
        chunks = [ranked[i:i + per] for i in range(0, len(ranked), per)]
        for ci, ch in enumerate(chunks): self.ranking_table(ch, f"{ci+1}/{len(chunks)}" if len(chunks) > 1 else None)
        self.divider(3, "Plataforma", p.get("platform_sub") or "Os quatro IQs em jogo e como cada um fecha o ciclo deste plano.")
        self.platform(); self.measurement(); self.closing()
        self._clean(); self.prs.save(out); return out


DARK_LINE = RGBColor(0x3A, 0x48, 0x53)

if __name__ == "__main__":
    if len(sys.argv) < 3: print(__doc__); sys.exit(1)
    plan = json.load(open(sys.argv[1], encoding="utf-8"))
    print(Deck(plan).build(sys.argv[2]))
