#!/usr/bin/env python3
"""Gera o deck resumo de um plano de audiências HYPR (.pptx) no design system HYPR.

Uso: python3 hypr_deck.py plano.json saida.pptx
Requer: python-pptx (pip install python-pptx)

Texto com *asteriscos* vira destaque em azul HYPR. Ver deck_schema.md para o formato do JSON.
"""
import json, sys, os, datetime
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

# ---- Design tokens (extraídos dos decks HYPR) ----
DARK = RGBColor(0x1B, 0x26, 0x2F)
LIGHT = RGBColor(0xFA, 0xFA, 0xFA)
BLUE = RGBColor(0x33, 0x97, 0xB9)
CARD = RGBColor(0xEC, 0xEF, 0xF0)
BAR = RGBColor(0xC9, 0xD2, 0xDB)
BODY = RGBColor(0x53, 0x68, 0x72)
MUTED = RGBColor(0x78, 0x90, 0x9C)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK_CARD = RGBColor(0x26, 0x33, 0x3D)
DARK_LINE = RGBColor(0x3A, 0x48, 0x53)
F_LIGHT, F_REG, F_MED, F_SEMI = "Montserrat Light", "Montserrat", "Montserrat Medium", "Montserrat SemiBold"

W, H = Inches(13.333), Inches(7.5)
MX = Inches(0.6)


def fmt_vol(v):
    v = float(v or 0)
    if v >= 1e6: return f"{v/1e6:.1f}".replace(".", ",").replace(",0", "") + " mi"
    if v >= 1e3: return f"{v/1e3:.0f} mil"
    return f"{v:.0f}"


class Deck:
    def __init__(self, plan):
        self.p = plan
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = W, H
        self.blank = self.prs.slide_layouts[6]
        self.n = 0

    # ---------- primitivas ----------
    def slide(self, dark, tag):
        s = self.prs.slides.add_slide(self.blank)
        self.n += 1
        bg = s.background.fill; bg.solid(); bg.fore_color.rgb = DARK if dark else LIGHT
        fg = WHITE if dark else DARK
        # tag pill
        pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, MX, Inches(0.42), Inches(0.12) + Inches(0.085) * len(tag) + Inches(0.3), Inches(0.24))
        pill.adjustments[0] = 0.5
        pill.fill.background(); pill.line.color.rgb = fg; pill.line.width = Pt(0.75); pill.shadow.inherit = False
        tf = pill.text_frame; tf.margin_top = tf.margin_bottom = 0; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        self._run(tf.paragraphs[0], tag.upper(), 7, fg, F_MED, align=PP_ALIGN.CENTER, spacing=1)
        # wordmark
        logo = os.path.join(ASSETS, "hypr_white.png" if dark else "hypr_dark.png")
        s.shapes.add_picture(logo, W - MX - Inches(1.15), Inches(0.42), width=Inches(1.15))
        # footer
        sq = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, MX, H - Inches(0.55), Inches(0.13), Inches(0.13))
        sq.fill.solid(); sq.fill.fore_color.rgb = fg; sq.line.fill.background(); sq.shadow.inherit = False
        self.text(s, "HYPR Audiences", Inches(2.1), H - Inches(0.6), Inches(3), Inches(0.25), 7, fg, F_MED)
        self.text(s, self.p.get("brand", ""), Inches(5.9), H - Inches(0.6), Inches(3), Inches(0.25), 7, fg, F_MED)
        self.text(s, str(self.n).zfill(2), W - MX - Inches(1), H - Inches(0.6), Inches(1), Inches(0.25), 7, fg, F_MED, align=PP_ALIGN.RIGHT)
        return s

    def _run(self, para, text, size, color, font, align=None, spacing=None):
        # *destaque* em azul
        parts = text.split("*")
        for i, part in enumerate(parts):
            if not part: continue
            r = para.add_run(); r.text = part
            r.font.size = Pt(size); r.font.name = font
            r.font.color.rgb = BLUE if i % 2 else color
            if spacing:
                rPr = r._r.get_or_add_rPr(); rPr.set("spc", str(int(spacing * 100)))
        if align is not None: para.alignment = align

    def text(self, s, text, x, y, w, h, size, color, font=F_REG, align=None, lines=None, line_spacing=1.15, anchor=MSO_ANCHOR.TOP, spacing=None):
        tb = s.shapes.add_textbox(x, y, w, h)
        tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        items = lines if lines is not None else [text]
        for i, line in enumerate(items):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.line_spacing = line_spacing
            self._run(para, line, size, color, font, align, spacing)
        return tb

    def rect(self, s, x, y, w, h, color, radius=None, line=None):
        shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, x, y, w, h)
        if radius: shp.adjustments[0] = radius
        if color is None: shp.fill.background()
        else: shp.fill.solid(); shp.fill.fore_color.rgb = color
        if line: shp.line.color.rgb = line; shp.line.width = Pt(0.75)
        else: shp.line.fill.background()
        shp.shadow.inherit = False
        return shp

    def title(self, s, eyebrow, title, dark=False, y=Inches(1.05), size=34, width=Inches(10.5)):
        fg = WHITE if dark else DARK
        if eyebrow:
            self.text(s, eyebrow.upper(), MX, y, Inches(6), Inches(0.25), 7.5, MUTED, F_SEMI, spacing=1)
            y += Inches(0.3)
        self.text(s, title, MX, y, width, Inches(1.2), size, fg, F_LIGHT, line_spacing=1.05)

    # ---------- slides ----------
    def cover(self):
        p = self.p
        s = self.slide(True, "Plano de audiências")
        self.text(s, f"{p['brand']}.", MX, Inches(1.45), Inches(11), Inches(1.2), 66, WHITE, F_LIGHT)
        self.text(s, p.get("campaign_title") or f"*{p.get('campaign','')}*", MX, Inches(2.55), Inches(11.5), Inches(1), 40, WHITE, F_LIGHT)
        sub = p.get("subtitle") or "Audiências ranqueadas por Brand Affinity e a plataforma HYPR para ativar e medir o plano inteiro."
        self.text(s, sub, MX + Inches(0.05), Inches(3.75), Inches(7.5), Inches(0.9), 14, WHITE, F_REG, line_spacing=1.3)
        self.text(s, p.get("date") or datetime.date.today().strftime("%d/%m/%Y"), MX + Inches(0.05), Inches(4.9), Inches(4), Inches(0.3), 9, MUTED, F_MED, spacing=1)

    def briefing(self):
        p = self.p
        s = self.slide(False, "Briefing")
        self.title(s, None, p.get("briefing_title") or f"O que a {p['brand']} *precisa*.")
        y = Inches(2.35)
        obj = p.get("objective", "")
        self.text(s, obj, MX, y, Inches(5.6), Inches(1.2), 15, BODY, F_REG, line_spacing=1.35)
        prem = p.get("premises") or []
        if prem:
            self.text(s, "PREMISSAS", MX, y + Inches(1.5), Inches(4), Inches(0.25), 7.5, MUTED, F_SEMI, spacing=1)
            self.text(s, "", MX, y + Inches(1.85), Inches(5.6), Inches(2), 11.5, BODY, F_REG, lines=[f"·  {x}" for x in prem], line_spacing=1.45)
        items = list((p.get("briefing") or {}).items())[:6]
        cx, cw, ch = Inches(7.0), Inches(2.75), Inches(1.15)
        for i, (k, v) in enumerate(items):
            x = cx + (i % 2) * (cw + Inches(0.15)); yy = y + (i // 2) * (ch + Inches(0.15))
            self.rect(s, x, yy, cw, ch, CARD, radius=0.06)
            self.text(s, k.upper(), x + Inches(0.2), yy + Inches(0.18), cw - Inches(0.4), Inches(0.25), 7, MUTED, F_SEMI, spacing=1)
            self.text(s, str(v), x + Inches(0.2), yy + Inches(0.45), cw - Inches(0.4), Inches(0.65), 12, DARK, F_REG, line_spacing=1.2)

    def summary(self):
        p = self.p; sm = p.get("summary", {})
        auds = [a for l in p["layers"] for a in l["audiences"]]
        count = sm.get("count") or len(auds)
        vol = sm.get("volume_total") or sum(a.get("volume") or 0 for a in auds)
        tw = sum(a.get("volume") or 0 for a in auds) or 1
        aff = sm.get("affinity_avg") or round(sum((a.get("affinity") or 0) * (a.get("volume") or 0) for a in auds) / tw)
        s = self.slide(False, "Resumo")
        self.title(s, None, p.get("summary_title") or f"Um plano com *{count} audiências* em {len(p['layers'])} camadas.")
        stats = [(str(count), "AUDIÊNCIAS", "selecionadas no catálogo HYPR"),
                 (fmt_vol(vol), "VOLUME BRUTO", "soma das audiências; há sobreposição entre elas"),
                 (f"{aff}%", "BRAND AFFINITY MÉDIA", "ponderada pelo volume de cada audiência")]
        cw = Inches(3.9); y = Inches(2.7)
        for i, (num, lab, note) in enumerate(stats):
            x = MX + i * (cw + Inches(0.2))
            self.rect(s, x, y, cw, Inches(2.6), CARD, radius=0.04)
            self.text(s, lab, x + Inches(0.3), y + Inches(0.3), cw, Inches(0.25), 7.5, MUTED, F_SEMI, spacing=1)
            self.text(s, num, x + Inches(0.3), y + Inches(0.75), cw - Inches(0.5), Inches(1.1), 54, BLUE if i == 2 else DARK, F_LIGHT)
            self.text(s, note, x + Inches(0.3), y + Inches(1.95), cw - Inches(0.6), Inches(0.5), 9.5, BODY, F_REG)
        # mini-barras por camada
        lx = MX; ly = Inches(5.65)
        for l in p["layers"]:
            n = len(l["audiences"]); v = sum(a.get("volume") or 0 for a in l["audiences"])
            self.text(s, f"{l['name'].upper()}  ·  {n} aud.  ·  {fmt_vol(v)}", lx, ly, Inches(3.1), Inches(0.25), 7.5, BODY, F_MED, spacing=0.5)
            lx += Inches(3.05)

    def layer_slides(self):
        p = self.p
        rows = []
        for l in p["layers"]:
            rows.append(("h", l))
            rows += [("a", a) for a in l["audiences"]]
        per = 11
        chunks, cur = [], []
        for r in rows:
            if len(cur) >= per and r[0] == "h" or len(cur) >= per + 1:
                chunks.append(cur); cur = []
            cur.append(r)
        if cur: chunks.append(cur)
        for ci, chunk in enumerate(chunks):
            s = self.slide(False, "Audiências")
            self.title(s, f"Ranking por Brand Affinity{'  ·  ' + str(ci+1) + '/' + str(len(chunks)) if len(chunks) > 1 else ''}",
                       p.get("layers_title") or "As audiências *certas*, em ordem de afinidade.", size=28)
            y = Inches(2.15)
            cols = [(MX, Inches(3.6), "AUDIÊNCIA"), (Inches(4.3), Inches(3.3), "BRAND AFFINITY"), (Inches(7.75), Inches(1.2), "VOLUME"), (Inches(9.05), Inches(3.7), "POR QUE ENTRA")]
            for x, w, lab in cols:
                self.text(s, lab, x, y, w, Inches(0.2), 6.5, MUTED, F_SEMI, spacing=1)
            y += Inches(0.3)
            rh = Inches(0.36)
            for kind, obj in chunk:
                if kind == "h":
                    y += Inches(0.06)
                    self.text(s, f"*{obj['name']}*" + (f"  ·  {obj.get('description','')}" if obj.get("description") else ""), MX, y, Inches(12), Inches(0.25), 9, DARK, F_SEMI)
                    y += Inches(0.3)
                    continue
                a = obj
                ln = s.shapes.add_connector(1, MX, y + rh, W - MX, y + rh); ln.line.color.rgb = CARD; ln.line.width = Pt(0.75)
                self.text(s, a["name"], MX, y + Inches(0.02), Inches(3.6), Inches(0.2), 9.5, DARK, F_REG)
                self.text(s, a.get("id", ""), MX, y + Inches(0.19), Inches(3.6), Inches(0.15), 6, MUTED, F_REG)
                aff = max(0, min(100, a.get("affinity") or 0)); bw = Inches(2.5)
                self.rect(s, Inches(4.3), y + Inches(0.12), bw, Inches(0.1), CARD, radius=0.5)
                self.rect(s, Inches(4.3), y + Inches(0.12), max(Emu(1), int(bw * aff / 100)), Inches(0.1), BLUE if aff >= 75 else (MUTED if aff >= 50 else BAR), radius=0.5)
                self.text(s, f"{aff}%", Inches(6.95), y + Inches(0.06), Inches(0.7), Inches(0.2), 10, DARK, F_MED)
                self.text(s, fmt_vol(a.get("volume")), Inches(7.75), y + Inches(0.06), Inches(1.2), Inches(0.2), 10, DARK, F_LIGHT)
                why = a.get("why", "")
                if len(why) > 125: why = why[:122].rsplit(" ", 1)[0] + "..."
                self.text(s, why, Inches(9.05), y + Inches(0.03), Inches(3.7), Inches(0.32), 7.5, BODY, F_REG, line_spacing=1.1)
                y += rh + Inches(0.04)

    def platform(self):
        p = self.p
        sols = {x["solution"]: x for x in p.get("solutions", [])}
        s = self.slide(True, "Plataforma HYPR")
        self.title(s, None, p.get("platform_title") or "Quatro IQs. *Uma resposta só*.", dark=True)
        self.text(s, p.get("platform_note") or "Os pilares operam juntos, sobre a mesma base, em circuito fechado: o lugar orienta onde ativar, o formato garante atenção, a transação mostra se virou venda e a pesquisa explica o porquê.",
                  MX, Inches(1.95), Inches(9.5), Inches(0.7), 12.5, RGBColor(0xC9, 0xD2, 0xDB), F_REG, line_spacing=1.35)
        order = [("geoIQ", "ONDE", "Places Graph"), ("adsIQ", "COM O QUÊ", "Max Attention"), ("revIQ", "QUANTO", "Groundflow"), ("askIQ", "POR QUÊ", None)]
        cw, ch, y = Inches(2.88), Inches(3.05), Inches(3.05)
        for i, (name, q, pw) in enumerate(order):
            x = MX + i * (cw + Inches(0.2))
            sol = sols.get(name, {})
            self.rect(s, x, y, cw, ch, DARK_CARD, radius=0.04)
            self.text(s, q, x + Inches(0.25), y + Inches(0.25), cw, Inches(0.2), 7, BLUE, F_SEMI, spacing=1)
            self.text(s, name, x + Inches(0.25), y + Inches(0.5), cw, Inches(0.6), 30, WHITE, F_LIGHT)
            if pw: self.text(s, f"powered by {pw}", x + Inches(0.25), y + Inches(1.1), cw, Inches(0.2), 7.5, MUTED, F_MED)
            how = sol.get("how", "")
            if len(how) > 150: how = how[:147].rsplit(" ", 1)[0] + "..."
            self.text(s, how, x + Inches(0.25), y + Inches(1.45), cw - Inches(0.45), Inches(1.2), 9.5, RGBColor(0xC9, 0xD2, 0xDB), F_REG, line_spacing=1.3)
            pr = sol.get("priority")
            if pr:
                pill = self.rect(s, x + Inches(0.25), y + ch - Inches(0.45), Inches(1.45), Inches(0.24), BLUE if pr == "Essencial" else None, radius=0.5, line=None if pr == "Essencial" else MUTED)
                tf = pill.text_frame; tf.margin_top = tf.margin_bottom = 0; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
                self._run(tf.paragraphs[0], pr.upper(), 6.5, WHITE, F_SEMI, PP_ALIGN.CENTER, 1)
            if i < 3:
                self.text(s, "→", x + cw - Inches(0.02), y + Inches(0.55), Inches(0.25), Inches(0.4), 14, BLUE, F_LIGHT, align=PP_ALIGN.CENTER)
        ds = sols.get("Demandshift")
        if ds and ds.get("priority") in ("Essencial", "Recomendado"):
            self.text(s, f"*Demandshift*  ·  {ds.get('how','')}", MX, Inches(6.3), Inches(12), Inches(0.35), 9.5, RGBColor(0xC9, 0xD2, 0xDB), F_REG)

    def measurement(self):
        p = self.p
        s = self.slide(False, "Mensuração")
        self.title(s, "revIQ  ·  powered by Groundflow", p.get("measurement_title") or "Não é alcance. É *diferença mensurada*.")
        self.text(s, p.get("measurement") or "Comparamos o consumo nos pontos de venda das regiões expostas à campanha com regiões equivalentes não expostas, medindo o incremento no SKU anunciado e na categoria.",
                  MX, Inches(2.4), Inches(6.2), Inches(1.4), 14, BODY, F_REG, line_spacing=1.4)
        steps = p.get("measurement_steps") or [("01", "Linha de base", "Vendas do SKU e da categoria antes do flight, por região."),
                                               ("02", "Exposto vs. controle", "Regiões impactadas comparadas a regiões equivalentes sem campanha."),
                                               ("03", "Incremento", "A diferença entre os grupos é o efeito atribuível à mídia.")]
        y = Inches(2.4)
        for num, head, body in steps:
            self.rect(s, Inches(7.4), y, Inches(5.33), Inches(1.15), CARD, radius=0.05)
            self.text(s, num, Inches(7.65), y + Inches(0.25), Inches(0.8), Inches(0.6), 26, BLUE, F_LIGHT)
            self.text(s, head, Inches(8.5), y + Inches(0.22), Inches(4), Inches(0.3), 12, DARK, F_MED)
            self.text(s, body, Inches(8.5), y + Inches(0.52), Inches(4), Inches(0.55), 9.5, BODY, F_REG, line_spacing=1.25)
            y += Inches(1.3)

    def closing(self):
        p = self.p
        s = self.slide(True, "Próximos passos")
        self.text(s, p.get("closing_title") or "Do bolso à rua.", MX, Inches(1.35), Inches(11), Inches(1), 54, WHITE, F_LIGHT)
        self.text(s, p.get("closing_subtitle") or "*Do plano à venda na loja.*", MX, Inches(2.35), Inches(11), Inches(1), 40, WHITE, F_LIGHT)
        y = Inches(3.7)
        for i, st in enumerate((p.get("next_steps") or [])[:4]):
            self.text(s, str(i + 1).zfill(2), MX, y, Inches(0.6), Inches(0.3), 11, BLUE, F_MED)
            self.text(s, st, MX + Inches(0.6), y, Inches(9), Inches(0.35), 13, WHITE, F_REG)
            y += Inches(0.5)
        self.text(s, "hyprgrid.ai", MX, Inches(6.3), Inches(3), Inches(0.3), 10, MUTED, F_MED, spacing=1)

    def _clean(self):
        # remove estilos do tema (sombras, contornos) de todas as formas
        from pptx.oxml.ns import qn
        for sl in self.prs.slides:
            for shp in sl.shapes:
                st = shp._element.find(qn("p:style"))
                if st is not None: shp._element.remove(st)

    def build(self, out):
        self.cover(); self.briefing(); self.summary(); self.layer_slides(); self.platform(); self.measurement(); self.closing()
        self._clean()
        self.prs.save(out)
        return out


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    plan = json.load(open(sys.argv[1], encoding="utf-8"))
    print(Deck(plan).build(sys.argv[2]))
