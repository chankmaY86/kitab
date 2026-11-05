#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Siapkan PAKET UNDUHAN transkrip Asmak Thomthomiyah.

Menghasilkan (di root repo):
  TERJEMAH_SYARAH_FUSHA_ASMAK_THOMTHOMIYAH.md  -- bagian yang memang diterjemahkan
  BACA_OFFLINE_ASMAK_THOMTHOMIYAH.html         -- edisi baca mandiri, RTL, gambar tertanam
  CATATAN_UNDUHAN_ASMAK_THOMTHOMIYAH.md        -- penjelas isi & batas muhafazhah
  UNDUHAN_ASMAK_THOMTHOMIYAH.zip               -- semua berkas dalam satu unduhan

Batas kunci permanen §4: yang diterjemahkan HANYA syarah/kaifiyat/waktu/hari/
بخور/syarat. Asma', azimah, wafaq, thilasm, dan angka Arab-Indik tetap dijaga.
"""

import base64
import html as html_lib
import re
import zipfile
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.md"
DOCX = ROOT / "TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.docx"
KEY = ROOT / "KUNCI_PERMANEN_USTADZ_YOAD.md"
BUILDER = ROOT / "scripts" / "build_docx_asmak_thomthomiyah.py"
SERVER = ROOT / "scripts" / "serve_unduhan.py"
ASSETS = sorted((ROOT / "assets").glob("asmak_thomthomiyah_*.png"))

F_TERJEMAH = ROOT / "TERJEMAH_SYARAH_FUSHA_ASMAK_THOMTHOMIYAH.md"
F_HTML = ROOT / "BACA_OFFLINE_ASMAK_THOMTHOMIYAH.html"
F_CATATAN = ROOT / "CATATAN_UNDUHAN_ASMAK_THOMTHOMIYAH.md"
F_ZIP = ROOT / "UNDUHAN_ASMAK_THOMTHOMIYAH.zip"

ARABIC_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]")


def arabic_ratio(s: str) -> float:
    letters = [c for c in s if c.isalpha() or "\u0600" <= c <= "\u06ff"]
    if not letters:
        # Sel angka Arab-Indik murni tetap dianggap RTL
        return 1.0 if ARABIC_RE.search(s) else 0.0
    return sum(1 for c in letters if ARABIC_RE.search(c)) / len(letters)


def strip_tags(fragment: str) -> str:
    return html_lib.unescape(re.sub(r"<[^>]+>", " ", fragment))


# --------------------------------------------------------------------------
# 1. Berkas terjemah syarah berdiri sendiri
# --------------------------------------------------------------------------
def build_terjemah(md_text: str) -> str:
    start = md_text.index("## 3. TERJEMAH SYARAH (FUSHA)")
    end = md_text.index("## 4. CATATAN HIKMAH")
    body = md_text[start:end].rstrip()
    body = re.sub(r"\n---\s*$", "", body).rstrip()
    header = """# TERJEMAH SYARAH (FUSHA) — الأسماء الطمطمية

**Status:** SELESAI, sesuai batas `KUNCI_PERMANEN_USTADZ_YOAD.md` §4.3.
**Sumber:** `TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.md` §3 · 12 halaman · 5 November 2026.

> **Batas terjemah.** Yang diterjemahkan **hanya** tata cara (kaifiyat), waktu, hari,
> `بخور`, dan syarat, ditambah keterangan operasional jadwal. **Asma', azimah,
> الاسم الكبير, thilasm, dan seluruh angka وافق ٣×٣ TIDAK diterjemahkan** —
> berlaku `[TEKS ASLI DIJAGA - TIDAK DITERJEMAH KARENA THILASM/WAFAQ]`
> (kunci permanen §4.1–§4.2, §4.5). Istilah `خاتم`, `حرز`, `تسخير`, `بخور`, `وفق`
> adalah **Istilah Falak/Hikmah**, bukan terjemahan fusha bebas (§4.4).
> Klaim khasiat di bawah adalah **pernyataan naskah**, bukan jaminan hasil.
> Untuk bacaan amal/wirid/ijazah, rujuk lafaz Arab pada §1 dan guru yang berijazah.

---

"""
    return header + body + "\n"


# --------------------------------------------------------------------------
# 2. Edisi baca offline (HTML mandiri, RTL, gambar tertanam)
# --------------------------------------------------------------------------
CSS = """
:root{--ink:#1f2937;--navy:#1e3a8a;--emerald:#064e3b;--gold:#92400e;--line:#d7dee8}
*{box-sizing:border-box}
body{max-width:900px;margin:0 auto;padding:28px 22px 60px;background:#fff;color:var(--ink);
 font:16px/1.75 "Segoe UI",Calibri,Arial,sans-serif}
h1{font-size:1.9rem;color:var(--emerald);margin:.2em 0 .6em}
h2{font-size:1.35rem;color:var(--navy);border-bottom:2px solid var(--line);
 padding-bottom:.25em;margin-top:2em;break-after:avoid}
h3{font-size:1.12rem;color:var(--emerald);margin-top:1.6em;break-after:avoid}
p{margin:.55em 0}
blockquote{margin:1em 0;padding:.7em 1em;background:#f1f5f9;border-left:4px solid var(--navy);
 color:#475569;font-size:.93rem}
blockquote p{margin:.3em 0}
code,pre{font-family:Consolas,"Courier New",monospace}
code{background:#eef2f7;padding:.1em .35em;border-radius:3px;font-size:.9em}
pre{background:#f8fafc;border:1px solid var(--line);border-radius:6px;padding:12px 14px;
 overflow-x:auto;font-size:1.05rem;line-height:2}
pre code{background:none;padding:0}
[dir=rtl],[dir=rtl] pre,[dir=rtl] code,[dir=rtl] td{
 font-family:"Traditional Arabic","Noto Naskh Arabic","Amiri","Scheherazade New",
 "Arial",serif;font-size:1.25rem}
[dir=rtl]{text-align:right}
pre[dir=rtl]{text-align:right;direction:rtl}
table{border-collapse:collapse;width:100%;margin:1.1em 0;font-size:.9rem}
th,td{border:1px solid var(--line);padding:6px 9px;vertical-align:middle}
th{background:var(--emerald);color:#fff;text-align:left}
table[dir=rtl] th,table[dir=rtl] td{text-align:center}
img{max-width:100%;height:auto;display:block;margin:14px auto;border:1px solid var(--line)}
figcaption{text-align:center;font-size:.85rem;color:#64748b;margin-bottom:18px}
hr{border:0;border-top:1px solid var(--line);margin:2em 0}
.banner{background:#fff7ed;border:1px solid #fed7aa;color:#7c2d12;padding:14px 18px;
 border-radius:8px;margin:18px 0 26px;font-size:.93rem}
.toc{background:#f8fafc;border:1px solid var(--line);border-radius:8px;padding:14px 20px}
.toc a{color:var(--navy);text-decoration:none}
.toc a:hover{text-decoration:underline}
.meta{color:#64748b;font-size:.88rem}
@media print{
 body{max-width:none;padding:0;font-size:11pt}
 .toc{break-after:page}
 h2{break-after:avoid}
 pre,table,img{break-inside:avoid}
 a{color:inherit;text-decoration:none}
}
"""

BANNER = """<div class="banner"><strong>Catatan Ustadz Yoad.</strong>
Terjemah pada berkas ini <strong>selesai</strong> sebatas yang diizinkan kunci permanen §4.3:
tata cara, waktu, hari, <span dir="rtl">بخور</span>, dan syarat. Asma', azimah, thilasm,
wafaq, dan angka Arab-Indik <strong>sengaja dijaga</strong> dan tidak diterjemahkan
(<code>[TEKS ASLI DIJAGA - TIDAK DITERJEMAH KARENA THILASM/WAFAQ]</code>).
Lafaz Arab adalah rujukan mengikat; lapis Latin §1A hanya alat bantu indeks.</div>"""


def rtlize(html_text: str) -> str:
    """Beri dir=rtl pada blok yang mayoritas Arab (kecuali tabel HTML sudah RTL)."""
    def fix(match):
        tag, attrs, inner = match.group(1), match.group(2), match.group(3)
        if "dir=" in attrs:
            return match.group(0)
        if arabic_ratio(strip_tags(inner)) >= 0.55:
            return f"<{tag}{attrs} dir=\"rtl\" lang=\"ar\">{inner}</{tag}>"
        return match.group(0)

    for t in ["p", "h1", "h2", "h3", "li", "pre", "td", "th", "blockquote"]:
        html_text = re.sub(
            rf"<({t})([^>]*)>(.*?)</\1>", fix, html_text,
            flags=re.S | re.I,
        )
    return html_text


def build_html(md_text: str) -> str:
    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )
    # Gambar ditanam sebagai data URI agar berkas benar-benar mandiri.
    def embed(m):
        rel = m.group(2)
        p = ROOT / rel
        if not p.is_file():
            return m.group(0)
        b64 = base64.b64encode(p.read_bytes()).decode("ascii")
        return f'<img src="data:image/png;base64,{b64}" alt="{html_lib.escape(m.group(1))}">'
    body = re.sub(r'<img alt="([^"]*)" src="([^"]+)"\s*/?>', embed, body)
    body = rtlize(body)

    toc = []
    for i, m in enumerate(re.finditer(r"<h2[^>]*>(.*?)</h2>", body, re.S)):
        label = strip_tags(m.group(1)).strip()
        anchor = f"bag-{i}"
        body = body.replace(m.group(0), f'<h2 id="{anchor}">{m.group(1)}</h2>', 1)
        toc.append(f'<li><a href="#{anchor}">{html_lib.escape(label)}</a></li>')

    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Transkripsi Lengkap — الأسماء الطمطمية</title>
<style>{CSS}</style>
</head>
<body>
<h1>TRANSKRIPSI LENGKAP — <span dir="rtl" lang="ar">الأسماء الطمطمية</span></h1>
<p class="meta">Sumber: <code>asmak thomthomiyah.pdf</code> · 12 halaman · disusun 5 November 2026 ·
Ustadz Yoad · mengikat: <code>KUNCI_PERMANEN_USTADZ_YOAD.md</code></p>
{BANNER}
<nav class="toc"><strong>Daftar isi</strong><ol>{''.join(toc)}</ol></nav>
{body}
<hr>
<p class="meta">Edisi baca offline mandiri. Dapat dicetak / disimpan sebagai PDF dari browser
(File → Print → Save as PDF). Teks Arab ditata RTL; angka وافق tetap Arab-Indik.</p>
</body>
</html>
"""


CATATAN = """# CATATAN UNDUHAN — الأسماء الطمطمية

**Tanggal:** 5 November 2026 · **Cabang:** `arena/dc140e9f-kitab`
**Disusun:** Ustadz Yoad · **Aturan mengikat:** `KUNCI_PERMANEN_USTADZ_YOAD.md`

## Status pekerjaan

| Bagian | Status | Keterangan |
|---|---|---|
| Transkrip 12 halaman | **Selesai** | Teks Arab, basmalah/shalawat, muqaddimah, 14 asma', kaifiyat, penutup, jadwal |
| 15 kotak وافق ٣×٣ | **Selesai** | Angka Arab-Indik dijaga apa adanya, tabel RTL |
| 2 facsimile | **Selesai** | Thilasm tulis tangan hal. 2; `الاسم الكبير` hias hal. 10 |
| I'rob fusha (§2) | **Selesai** | Hanya untuk bagian syarah |
| **Terjemah syarah (§3)** | **SELESAI** | 18 poin + tabel jadwal hari/waktu; lihat `TERJEMAH_SYARAH_FUSHA_ASMAK_THOMTHOMIYAH.md` |
| Latinisasi kunci asma' (§1A) | **Selesai** | Lapis bantu atas permintaan eksplisit, skema dinyatakan |

## Yang TIDAK diterjemahkan (bukan pekerjaan yang tertunda)

Sesuai kunci permanen §4.1–§4.2 dan §4.5, berlaku
`[TEKS ASLI DIJAGA - TIDAK DITERJEMAH KARENA THILASM/WAFAQ]` untuk:
`طمطكطجيشمحمدأل`, ke-14 asma', azimah tambahan, seluruh isi kotak وافق,
thilasm gambar, dan doa penutup. Angka **tetap Arab-Indik** (`٣٢٥١`, `١١٧٩`, dll.).
Jadi "selesai diterjemahi" di sini berarti **seluruh bagian yang boleh diterjemahkan
sudah selesai**; sisanya memang wajib dijaga, bukan tertunda.

Klaim khasiat/perkara gaib adalah **isi naskah tradisi**, bukan bukti medis atau jaminan
hasil. Untuk amal, wirid, atau ijazah, rujuk **lafaz Arab** dan guru yang berijazah.
Kolom Latin §1A bukan pensahihan bacaan; vokalnya asumsi karena naskah gundul.

## Isi paket

| Berkas | Kegunaan |
|---|---|
| `TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.docx` | **Berkas utama**, siap dibuka di Word / Google Docs; Arab RTL, 15 tabel wafaq RTL, 2 gambar |
| `TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.md` | Master teks (sumber segala turunan) |
| `TERJEMAH_SYARAH_FUSHA_ASMAK_THOMTHOMIYAH.md` | Hanya bagian terjemah syarah, berdiri sendiri |
| `BACA_OFFLINE_ASMAK_THOMTHOMIYAH.html` | Edisi baca mandiri: gambar tertanam, RTL, bisa dicetak / disimpan PDF dari browser |
| `KUNCI_PERMANEN_USTADZ_YOAD.md` | Aturan mengikat (10 langkah + mazhab muhafazhah) |
| `assets/*.png` | 2 facsimile yang dipakai transkrip |
| `scripts/build_docx_asmak_thomthomiyah.py` | Pembangun DOCX (reproduksi) |
| `scripts/build_unduhan_asmak_thomthomiyah.py` | Pembangun paket unduhan ini |
| `scripts/serve_unduhan.py` | Halaman unduh langsung (live preview, port 8000) |

## Reproduksi

```
python3 -m venv .venv
.venv/bin/pip install -r requirements-editorial.txt
.venv/bin/python scripts/build_docx_asmak_thomthomiyah.py
.venv/bin/python scripts/build_unduhan_asmak_thomthomiyah.py
.venv/bin/python scripts/serve_unduhan.py      # halaman unduh: live preview port 8000
.venv/bin/python -m unittest discover -s tests -v
```
"""


def build():
    md_text = MD.read_text(encoding="utf-8")
    terjemah = build_terjemah(md_text)
    F_TERJEMAH.write_text(terjemah, encoding="utf-8")
    F_HTML.write_text(build_html(md_text), encoding="utf-8")
    F_CATATAN.write_text(CATATAN, encoding="utf-8")

    members = [
        F_CATATAN,
        DOCX,
        MD,
        F_TERJEMAH,
        F_HTML,
        KEY,
        BUILDER,
        SERVER,
        Path(__file__).resolve(),
    ] + ASSETS
    with zipfile.ZipFile(F_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in members:
            if not f.is_file():
                raise FileNotFoundError(f)
            arcname = str(f.relative_to(ROOT))
            z.write(f, arcname)
    return F_ZIP, members


if __name__ == "__main__":
    z, members = build()
    print(f"Tersimpan: {z.name} ({z.stat().st_size} bytes, {len(members)} berkas)")
    for f in [F_TERJEMAH, F_HTML, F_CATATAN]:
        print(f"  + {f.name} ({f.stat().st_size} bytes)")
