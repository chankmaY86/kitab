#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bangun TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.docx dari master Markdown.

Mengikuti konvensi repo (scripts/build_final_65.py):
- paragraf Arab RTL (w:bidi + w:rtl), font Traditional Arabic;
- tabel wafaq 3x3 RTL dengan w:bidiVisual sehingga kolom pertama di kanan;
- angka Arab-Indik dijaga apa adanya;
- gambar facsimile disematkan tanpa diubah.

Lapis Latin §1A adalah lapis BANTU; lafaz Arab tetap sumber mengikat.
"""

import re
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn, nsdecls

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.md"
OUT = ROOT / "TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.docx"

ARABIC_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]")
NOTE_RE = re.compile(r"\s*(\[[^\[\]]+\])\s*$")

C_NAVY = RGBColor(0x1E, 0x3A, 0x8A)
C_EMERALD = RGBColor(0x06, 0x4E, 0x3B)
C_GOLD = RGBColor(0x92, 0x40, 0x0E)
C_SLATE = RGBColor(0x1F, 0x29, 0x37)
C_MUTED = RGBColor(0x4B, 0x55, 0x63)


def has_arabic(s: str) -> bool:
    return bool(ARABIC_RE.search(s))


def set_bidi(p, rtl: bool):
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:bidi")):
        pPr.remove(old)
    el = OxmlElement("w:bidi")
    el.set(qn("w:val"), "1" if rtl else "0")
    pPr.append(el)


def set_shading(p, fill: str):
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    pPr.append(shd)


def set_cell_shading(cell, fill: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def style_run(run, text_is_arabic=False, size=10.5, bold=False, italic=False,
              color=None, mono=False):
    latin = "Consolas" if mono else "Calibri"
    run.bold = bold
    run.italic = italic
    run.font.name = latin
    run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), latin)
    rFonts.set(qn("w:hAnsi"), latin)
    rFonts.set(qn("w:cs"), "Traditional Arabic" if text_is_arabic else latin)
    szCs = rPr.find(qn("w:szCs"))
    if szCs is None:
        szCs = OxmlElement("w:szCs")
        rPr.append(szCs)
    szCs.set(qn("w:val"), str(int(size * 2)))
    if text_is_arabic and rPr.find(qn("w:rtl")) is None:
        rPr.append(OxmlElement("w:rtl"))
    if bold and rPr.find(qn("w:bCs")) is None:
        rPr.append(OxmlElement("w:bCs"))


INLINE_RE = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\[[^\]]+\])")


def emit_inline(p, text: str, base_arabic=False, size=10.5, color=C_SLATE,
                base_bold=False, base_italic=False):
    """Tulis teks dengan **bold**, *italic*, `code`, [penanda]; markup tidak tersisa."""
    text = text.replace("&nbsp;", "").replace("<br>", " ")
    for part in INLINE_RE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            s = part[2:-2]
            style_run(p.add_run(s), has_arabic(s) or base_arabic, size=size,
                      bold=True, italic=base_italic, color=color)
        elif part.startswith("*") and part.endswith("*"):
            s = part[1:-1]
            style_run(p.add_run(s), has_arabic(s) or base_arabic, size=size,
                      bold=base_bold, italic=True, color=color)
        elif part.startswith("`") and part.endswith("`"):
            s = part[1:-1]
            style_run(p.add_run(s), has_arabic(s), size=size - 0.5,
                      mono=True, color=C_NAVY if not has_arabic(s) else color)
        elif part.startswith("[") and part.endswith("]"):
            style_run(p.add_run(part), False, size=size - 1, italic=True,
                      color=C_MUTED)
        else:
            style_run(p.add_run(part), has_arabic(part) or base_arabic,
                      size=size, bold=base_bold, italic=base_italic, color=color)


def add_para(doc, text, rtl=False, size=10.5, color=C_SLATE, bold=False,
             italic=False, align=None, fill=None, space_after=4):
    p = doc.add_paragraph()
    set_bidi(p, rtl)
    if align is not None:
        p.alignment = align
    if fill:
        set_shading(p, fill)
    p.paragraph_format.space_after = Pt(space_after)
    emit_inline(p, text, base_arabic=rtl, size=size, color=color,
                base_bold=bold, base_italic=italic)
    return p


def add_heading(doc, text, level):
    sizes = {0: 22, 1: 15, 2: 12.5, 3: 11}
    colors = {0: C_EMERALD, 1: C_NAVY, 2: C_EMERALD, 3: C_GOLD}
    p = doc.add_paragraph()
    p.style = doc.styles["Heading 1" if level == 1 else "Heading 2" if level == 2 else "Heading 3"]
    set_bidi(p, False)
    p.paragraph_format.space_before = Pt(12 if level <= 1 else 8)
    p.paragraph_format.space_after = Pt(5)
    style_run(p.add_run(text), False, size=sizes[level], bold=True,
              color=colors[level])
    return p


def add_rtl_wafaq_table(doc, rows):
    table = doc.add_table(rows=len(rows), cols=3)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._tbl.tblPr
    for old in tblPr.findall(qn("w:bidiVisual")):
        tblPr.remove(old)
    tblPr.append(OxmlElement("w:bidiVisual"))
    for r_i, row in enumerate(rows):
        for c_i in range(3):
            cell = table.cell(r_i, c_i)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            val = (row[c_i] if c_i < len(row) else "").strip()
            val = val.replace("&nbsp;", "")
            parts = [x.strip() for x in val.split("<br>")]
            p = cell.paragraphs[0]
            p.clear()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_bidi(p, True)
            for j, part in enumerate(parts):
                if j:
                    p.add_run().add_break()
                style_run(p.add_run(part), True, size=13, color=C_SLATE)
    return table


def parse_md_table(lines):
    rows = []
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c or "") for c in cells):
            continue
        rows.append(cells)
    return rows


def add_md_table(doc, rows):
    if not rows:
        return None
    ncols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=ncols)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_i, row in enumerate(rows):
        for c_i in range(ncols):
            cell = table.cell(r_i, c_i)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if r_i == 0:
                set_cell_shading(cell, "064E3B")
            raw = row[c_i] if c_i < len(row) else ""
            p = cell.paragraphs[0]
            p.clear()
            p.paragraph_format.space_after = Pt(2)
            rtl_cell = has_arabic(raw.replace("`", "").replace("*", ""))
            set_bidi(p, rtl_cell)
            clean = raw.replace("`", "").replace("*", "").replace("&nbsp;", "")
            style_run(p.add_run(clean), rtl_cell,
                      size=9.5 if ncols >= 4 else 10,
                      bold=(r_i == 0),
                      color=RGBColor(0xFF, 0xFF, 0xFF) if r_i == 0 else C_SLATE)
    return table


def add_image(doc, path: Path, caption: str, width=4.6):
    p = doc.add_paragraph()
    set_bidi(p, False)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.add_run().add_picture(str(path), width=Inches(width))
    c = doc.add_paragraph()
    set_bidi(c, False)
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.space_after = Pt(8)
    style_run(c.add_run(caption), False, size=9, italic=True, color=C_MUTED)


def add_footer_page_number(doc):
    sec = doc.sections[0]
    p = sec.footer.paragraphs[0]
    set_bidi(p, False)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style_run(p.add_run("الأسماء الطمطمية · Ustadz Yoad · hlm. "),
              False, size=8.5, color=C_MUTED)
    r = p.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    r._r.addnext(fld)


DEFAULT_COVER = {
    "title": "Transkripsi Lengkap — الأسماء الطمطمية",
    "subject": "Transkrip 12 halaman + i'rob fusha + latinisasi bantu kunci asma'",
    "kicker": "TRANSKRIPSI LENGKAP",
    "arab_title": "الأسماء الطمطمية",
    "arab_sub": "أسماء آصف ابن برخيا وكيفية العمل بيها",
    "source": "Sumber: asmak thomthomiyah.pdf · 12 halaman · Google Drive",
    "binding": "Mengikat: KUNCI_PERMANEN_USTADZ_YOAD.md (Mazhab Muhafazhah)",
    "warning": ("PERHATIAN: azimah, asma', thilasm, dan angka wafaq dijaga apa adanya dan TIDAK "
                "diterjemahkan. Lapis Latin pada §1A hanyalah alat bantu indeks atas permintaan "
                "eksplisit; lafaz Arab tetap yang mengikat."),
}


def build(md_path=None, out=None, cover=None):
    """Bangun DOCX dari Markdown. Parameter opsional untuk edisi turunan."""
    src = Path(md_path) if md_path else MD_PATH
    dst = Path(out) if out else OUT
    c = {**DEFAULT_COVER, **(cover or {})}
    md = src.read_text(encoding="utf-8")
    lines = md.splitlines()

    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Inches(0.8)
    sec.bottom_margin = Inches(0.8)
    sec.left_margin = Inches(0.85)
    sec.right_margin = Inches(0.85)

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10.5)

    doc.core_properties.title = c["title"]
    doc.core_properties.author = "Ustadz Yoad"
    doc.core_properties.subject = c["subject"]
    doc.core_properties.keywords = "Kitab Gundul, Nahwu Sharaf, Muhafazhah, Asma', Wafaq"

    # ---- Sampul ----
    add_para(doc, c["kicker"], align=WD_ALIGN_PARAGRAPH.CENTER,
             size=20, color=C_EMERALD, bold=True, space_after=2)
    add_para(doc, c["arab_title"], rtl=True,
             align=WD_ALIGN_PARAGRAPH.CENTER, size=26,
             color=C_EMERALD, bold=True, space_after=2)
    add_para(doc, c["arab_sub"], rtl=True,
             align=WD_ALIGN_PARAGRAPH.CENTER, size=15,
             color=C_NAVY, space_after=14)
    add_para(doc, c["source"],
             align=WD_ALIGN_PARAGRAPH.CENTER, size=10, color=C_MUTED,
             space_after=2)
    add_para(doc, "Disusun 5 November 2026 · Ustadz Yoad · Pakar Nahwu Sharaf",
             align=WD_ALIGN_PARAGRAPH.CENTER, size=10, color=C_MUTED,
             space_after=2)
    add_para(doc, c["binding"],
             align=WD_ALIGN_PARAGRAPH.CENTER, size=10, color=C_MUTED,
             space_after=14)
    add_para(doc, c["warning"],
             align=WD_ALIGN_PARAGRAPH.CENTER, size=9.5, color=C_GOLD,
             italic=True, fill="FFF7ED", space_after=8)
    doc.add_page_break()

    i = 0
    in_code = False
    while i < len(lines):
        ln = lines[i].rstrip()

        if ln.startswith("```"):
            in_code = not in_code
            i += 1
            continue

        if in_code:
            if ln.strip():
                m = NOTE_RE.search(ln)
                note = m.group(1) if m else None
                body = NOTE_RE.sub("", ln).strip() if m else ln.strip()
                if body:
                    rtl = has_arabic(body)
                    add_para(doc, body, rtl=rtl, size=14 if rtl else 10,
                             color=C_SLATE,
                             align=WD_ALIGN_PARAGRAPH.RIGHT if rtl else None,
                             space_after=2)
                if note:
                    add_para(doc, note, size=8.5, color=C_MUTED, italic=True,
                             space_after=3)
            else:
                add_para(doc, "", size=6, space_after=0)
            i += 1
            continue

        if not ln.strip():
            i += 1
            continue

        if ln.strip() == "---":
            i += 1
            continue

        # Gambar
        mimg = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", ln.strip())
        if mimg:
            path = ROOT / mimg.group(2)
            if path.is_file():
                add_image(doc, path, mimg.group(1))
            i += 1
            continue

        # Tabel wafaq HTML RTL
        if ln.strip().startswith("<table"):
            block = []
            while i < len(lines) and "</table>" not in lines[i]:
                block.append(lines[i])
                i += 1
            if i < len(lines):
                block.append(lines[i]); i += 1
            html = "\n".join(block)
            cells = []
            for r in re.findall(r"<tr>(.*?)</tr>", html, re.S):
                cells.append(re.findall(r"<td>(.*?)</td>", r, re.S))
            add_rtl_wafaq_table(doc, [r for r in cells if r])
            add_para(doc, "", size=5, space_after=2)
            continue

        # Tabel Markdown
        if ln.lstrip().startswith("|"):
            block = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                block.append(lines[i]); i += 1
            add_md_table(doc, parse_md_table(block))
            add_para(doc, "", size=5, space_after=2)
            continue

        # Heading
        mh = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if mh:
            lvl = len(mh.group(1)) - 1
            add_heading(doc, mh.group(2).strip(), max(lvl, 0))
            i += 1
            continue

        # Blockquote
        if ln.lstrip().startswith(">"):
            txt = ln.lstrip()[1:].strip()
            if txt.startswith("- "):
                txt = "•  " + txt[2:]
            if txt:
                add_para(doc, txt, size=9.5, color=C_MUTED, italic=True,
                         fill="F1F5F9", space_after=3)
            i += 1
            continue

        # List
        mb = re.match(r"^\s*-\s+(.*)$", ln)
        if mb:
            p = add_para(doc, "", size=10, space_after=2)
            style_run(p.add_run("•  "), False, size=10, color=C_EMERALD)
            emit_inline(p, mb.group(1), size=10)
            i += 1
            continue
        mn = re.match(r"^\s*(\d+)\.\s+(.*)$", ln)
        if mn:
            p = add_para(doc, "", size=10, space_after=2)
            style_run(p.add_run(mn.group(1) + ".  "), False, size=10,
                      bold=True, color=C_EMERALD)
            emit_inline(p, mn.group(2), size=10)
            i += 1
            continue

        # Paragraf biasa
        add_para(doc, ln.strip(), size=10.5)
        i += 1

    add_footer_page_number(doc)
    doc.save(dst)
    return dst


if __name__ == "__main__":
    out = build()
    print(f"Tersimpan: {out} ({out.stat().st_size} bytes)")
