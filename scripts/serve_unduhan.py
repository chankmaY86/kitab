#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Halaman unduhan langsung untuk transkrip Asmak Thomthomiyah.

Dijalankan sebagai live preview Arena:
    .venv/bin/python scripts/serve_unduhan.py
Bind 0.0.0.0, hanya berkas yang masuk daftar putih yang disajikan.
Semua tautan relatif (tidak ada localhost di sisi browser).
"""

import html
import mimetypes
import os
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PORT = int(os.environ.get("PORT", "8000"))


def github_raw_base() -> str:
    """Dasar tautan unduh GitHub — tidak bergantung pada host preview sandbox."""
    try:
        remote = subprocess.check_output(
            ["git", "remote", "get-url", "origin"], cwd=ROOT,
            text=True).strip()
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"], cwd=ROOT,
            text=True).strip()
        slug = remote.split("github.com/")[-1].removesuffix(".git")
        return f"https://raw.githubusercontent.com/{slug}/{branch}"
    except Exception:
        return ("https://raw.githubusercontent.com/fatimah86-dot/kitab/"
                "arena/dc140e9f-kitab")


GH_RAW = github_raw_base()

# (nama berkas, judul, keterangan, utama?)
ENTRIES = [
    ("UNDUHAN_ASMAK_THOMTHOMIYAH.zip", "Paket lengkap (.zip)",
     "Semua berkas dalam satu unduhan — disarankan", True),
    ("TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.docx", "Transkrip lengkap (.docx)",
     "Berkas utama Word: 12 HAL, 15 wafaq RTL, 2 facsimile", False),
    ("TERJEMAHAN_LENGKAP_ASMAK_THOMTHOMIYAH.docx", "Terjemahan lengkap + transliterasi (.docx)",
     "Terjemah Indonesia menyeluruh + alih aksara Latin; wafaq dikecualikan", False),
    ("TERJEMAHAN_LENGKAP_ASMAK_THOMTHOMIYAH.md", "Terjemahan lengkap (.md)",
     "Sumber Markdown edisi terjemah; 12 HAL + Lampiran 15 wafaq", False),
    ("BACA_OFFLINE_ASMAK_THOMTHOMIYAH.html", "Edisi baca offline (.html)",
     "Mandiri, gambar tertanam, bisa dibaca/print di browser", False),
    ("TERJEMAH_SYARAH_FUSHA_ASMAK_THOMTHOMIYAH.md", "Terjemah Syarah (.md)",
     "18 poin + tabel jadwal; hanya bagian yang boleh diterjemahkan", False),
    ("TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.md", "Master Markdown (.md)",
     "Sumber segala turunan, termasuk §1A Latin bantu", False),
    ("CATATAN_UNDUHAN_ASMAK_THOMTHOMIYAH.md", "Catatan unduhan (.md)",
     "Status pekerjaan, batas muhafazhah, daftar isi paket", False),
    ("KUNCI_PERMANEN_USTADZ_YOAD.md", "Kunci permanen (.md)",
     "Aturan mengikat: 10 langkah + mazhab muhafazhah", False),
    ("assets/asmak_thomthomiyah_hal02_khatim_tulis_tangan.png", "Facsimile hal. 02 (.png)",
     "Thilasm tulis tangan — dijaga apa adanya", False),
    ("assets/asmak_thomthomiyah_hal10_asma_kabir.png", "Facsimile hal. 10 (.png)",
     "الاسم الكبير dengan glyph hias — dijaga apa adanya", False),
]

WHITELIST = {e[0] for e in ENTRIES}
MIME = {
    ".zip": "application/zip",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".md": "text/markdown; charset=utf-8",
    ".html": "text/html; charset=utf-8",
    ".png": "image/png",
}


def human(n: int) -> str:
    return f"{n / 1024:.0f} KB" if n < 1024 * 1024 else f"{n / 1024 / 1024:.1f} MB"


def render_index() -> str:
    rows = []
    for name, title, desc, primary in ENTRIES:
        p = ROOT / name
        size = human(p.stat().st_size) if p.is_file() else "—"
        link = f"/download/{name}"
        extra = ""
        if name.endswith(".html"):
            extra = (' <a class="mini" href="/preview" target="_blank" '
                     'rel="noopener">Lihat di tab baru ↗</a>')
        rows.append(f"""<tr class="{'utama' if primary else ''}">
<td><strong>{html.escape(title)}</strong><div class="d">{html.escape(desc)}</div>{extra}</td>
<td class="s">{size}</td>
<td><a class="btn {'btn-utama' if primary else ''}" href="{link}"
   download="{html.escape(Path(name).name)}">Unduh ↓</a></td></tr>""")

    big = ENTRIES[0][0]
    return f"""<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Unduhan — Asmak Thomthomiyah</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#f6f8fb;color:#1f2937;font:15px/1.65 "Segoe UI",Calibri,Arial,sans-serif}}
.wrap{{max-width:860px;margin:0 auto;padding:26px 20px 60px}}
h1{{font-size:1.6rem;color:#064e3b;margin:0 0 .2em}}
.arab{{direction:rtl;font-family:"Traditional Arabic","Noto Naskh Arabic",serif;font-size:1.5rem}}
.sub{{color:#64748b;font-size:.9rem;margin-bottom:18px}}
.card{{background:#fff;border:1px solid #dbe3ee;border-radius:12px;padding:20px 22px;
 box-shadow:0 2px 10px rgba(15,23,42,.05);margin-bottom:18px}}
.hero{{background:linear-gradient(135deg,#064e3b,#0f766e);color:#fff;border:0}}
.hero h2{{margin:.1em 0 .3em;font-size:1.25rem}}
.hero p{{opacity:.9;margin:0 0 14px;font-size:.93rem}}
.big{{display:inline-block;background:#fff;color:#064e3b;font-weight:700;text-decoration:none;
 padding:12px 22px;border-radius:8px;font-size:1rem}}
.big:hover{{background:#ecfdf5}}
table{{width:100%;border-collapse:collapse}}
td{{padding:11px 8px;border-top:1px solid #e8eef5;vertical-align:middle}}
tr.utama td{{background:#f0fdf4}}
td.s{{white-space:nowrap;color:#64748b;font-size:.86rem;text-align:right;width:90px}}
td:last-child{{width:110px;text-align:right}}
.d{{color:#64748b;font-size:.84rem;margin-top:2px}}
.btn{{display:inline-block;text-decoration:none;color:#1e3a8a;border:1px solid #c7d7f0;
 background:#f8fafc;padding:7px 14px;border-radius:7px;font-size:.88rem;white-space:nowrap}}
.btn:hover{{background:#e8f0fe}}
.btn-utama{{background:#1e3a8a;color:#fff;border-color:#1e3a8a}}
.mini{{font-size:.8rem;color:#1e3a8a}}
.note{{background:#fff7ed;border:1px solid #fed7aa;color:#7c2d12;border-radius:10px;
 padding:14px 18px;font-size:.9rem}}
code{{background:#eef2f7;padding:.1em .35em;border-radius:3px;font-size:.86em}}
.urls{{font-size:.82rem;color:#475569;word-break:break-all}}
a{{color:#1e3a8a}}
.tip{{font-size:.86rem;color:#475569;margin-top:10px}}
</style></head><body><div class="wrap">
<h1>Unduhan — Transkripsi Lengkap</h1>
<div class="arab" lang="ar">الأسماء الطمطمية</div>
<div class="sub">12 halaman · disusun 5 November 2026 · Ustadz Yoad ·
 aturan mengikat: <code>KUNCI_PERMANEN_USTADZ_YOAD.md</code></div>

<div class="card hero">
<h2>Paket lengkap, satu klik</h2>
<p>Berisi DOCX, master Markdown, terjemah syarah, edisi HTML offline, kunci permanen,
dua facsimile, dan skrip reproduksi.</p>
<a class="big" href="/download/{big}" download="{big}">⬇ Unduh {html.escape(big)}</a>
</div>

<div class="card" style="border-color:#86efac;background:#f0fdf4">
<strong>Tautan GitHub (paling andal — tidak lewat proxy preview)</strong>
<div class="tip">Kalau halaman ini error 502 atau tombol di atas tidak merespons, pakai
tautan langsung dari GitHub. Cabang sudah di-push ke
<code>arena/dc140e9f-kitab</code>.</div>
<div style="margin-top:10px">
<a class="btn btn-utama" href="{GH_RAW}/{big}">⬇ Unduh ZIP dari GitHub</a>
&nbsp;
<a class="btn" href="{GH_RAW}/TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.docx">⬇ DOCX dari GitHub</a>
&nbsp;
<a class="btn" href="{GH_RAW}/TERJEMAH_SYARAH_FUSHA_ASMAK_THOMTHOMIYAH.md">⬇ Terjemah dari GitHub</a>
&nbsp;
<a class="btn" href="{GH_RAW}/TERJEMAHAN_LENGKAP_ASMAK_THOMTHOMIYAH.docx">⬇ Terjemahan lengkap dari GitHub</a>
</div>
</div>

<div class="card">
<table>{''.join(rows)}</table>
</div>

<div class="card note">
<strong>Catatan Ustadz Yoad.</strong> Terjemah <strong>sudah selesai</strong> sebatas
kunci permanen §4.3: tata cara, waktu, hari, <span class="arab" lang="ar" style="font-size:1.05rem">بخور</span>,
dan syarat. Asma', azimah, thilasm, kotak وافق, dan angka Arab-Indik
<strong>sengaja dijaga</strong> dan tidak diterjemahkan
(<code>[TEKS ASLI DIJAGA - TIDAK DITERJEMAH KARENA THILASM/WAFAQ]</code>).
Klaim khasiat adalah pernyataan naskah, bukan jaminan hasil.
</div>

<div class="card">
<strong>Kalau tombol unduh tidak berjalan di panel preview</strong>
<div class="tip">1) Buka halaman ini di tab baru:
 <a href="/" target="_blank" rel="noopener">Buka di tab baru ↗</a>.
 2) Atau klik kanan tautan → <em>Save link as…</em>.
 3) Atau salin salah satu alamat berkas ke bilah alamat browser:</div>
<div class="urls" style="margin-top:8px">
<div><code>/download/UNDUHAN_ASMAK_THOMTHOMIYAH.zip</code></div>
<div><code>/download/TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.docx</code></div>
<div><code>/download/TERJEMAH_SYARAH_FUSHA_ASMAK_THOMTHOMIYAH.md</code></div>
<div><code>/preview</code> — edisi baca offline (dibuka, bukan diunduh)</div>
</div>
</div>
</div></body></html>"""


class Handler(BaseHTTPRequestHandler):
    server_version = "UnduhanAsmak/1.0"

    def log_message(self, fmt, *args):
        print("[unduhan] " + (fmt % args), flush=True)

    def _send(self, code, ctype, body: bytes, *, head=False,
              filename=None, inline=False):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if filename and not inline:
            self.send_header("Content-Disposition",
                             f'attachment; filename="{filename}"')
        # Sengaja TIDAK mengirim X-Frame-Options agar live preview bisa iframe.
        self.end_headers()
        if not head:
            self.wfile.write(body)

    def _serve(self, head=False):
        path = unquote(self.path.split("?", 1)[0])
        if path in ("/", "/index.html"):
            self._send(200, "text/html; charset=utf-8",
                       render_index().encode("utf-8"), head=head, inline=True)
            return
        if path == "/preview":
            p = ROOT / "BACA_OFFLINE_ASMAK_THOMTHOMIYAH.html"
            self._send(200, "text/html; charset=utf-8", p.read_bytes(),
                       head=head, inline=True)
            return
        if path.startswith("/download/"):
            name = path[len("/download/"):]
            if name not in WHITELIST:
                self._send(404, "text/plain; charset=utf-8",
                           b"Tidak ditemukan", head=head, inline=True)
                return
            p = ROOT / name
            if not p.is_file():
                self._send(404, "text/plain; charset=utf-8",
                           b"Berkas belum ada", head=head, inline=True)
                return
            ctype = MIME.get(p.suffix.lower(),
                             mimetypes.guess_type(p.name)[0] or "application/octet-stream")
            self._send(200, ctype, p.read_bytes(), head=head,
                       filename=p.name)
            return
        self._send(404, "text/plain; charset=utf-8",
                   b"Tidak ditemukan", head=head, inline=True)

    def do_GET(self):
        self._serve()

    def do_HEAD(self):
        self._serve(head=True)


def write_landing():
    """Tulis berkas HTML ber-tautan unduh ABSOLUT GitHub untuk present_file.

    Sengaja tidak memakai host preview sandbox: proxy live preview bisa 502.
    Berkas ini hasil-generate lokal, tidak masuk Git (lihat .gitignore).
    """
    items = [
        ("UNDUHAN_ASMAK_THOMTHOMIYAH.zip", "⬇ Paket lengkap (.zip) — disarankan"),
        ("TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.docx", "⬇ Transkrip lengkap (.docx)"),
        ("TERJEMAHAN_LENGKAP_ASMAK_THOMTHOMIYAH.docx", "⬇ TERJEMAHAN LENGKAP + transliterasi (.docx)"),
        ("TERJEMAHAN_LENGKAP_ASMAK_THOMTHOMIYAH.md", "⬇ Terjemahan lengkap (.md)"),
        ("TERJEMAH_SYARAH_FUSHA_ASMAK_THOMTHOMIYAH.md", "⬇ Terjemah Syarah (.md)"),
        ("BACA_OFFLINE_ASMAK_THOMTHOMIYAH.html", "⬇ Edisi baca offline (.html)"),
        ("CATATAN_UNDUHAN_ASMAK_THOMTHOMIYAH.md", "⬇ Catatan unduhan (.md)"),
        ("TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.md", "⬇ Master Markdown (.md)"),
    ]
    lis = "".join(
        f'<li><a href="{GH_RAW}/{html.escape(n)}" target="_blank" rel="noopener">'
        f'{html.escape(t)}</a><br><small>{GH_RAW}/{html.escape(n)}</small></li>'
        for n, t in items
    )
    doc = f"""<!DOCTYPE html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tautan unduh langsung — Asmak Thomthomiyah</title>
<style>body{{max-width:760px;margin:30px auto;padding:0 20px;
font:16px/1.7 "Segoe UI",Calibri,Arial,sans-serif;color:#1f2937}}
h1{{color:#064e3b;font-size:1.5rem}} li{{margin:14px 0;list-style:none;
background:#f8fafc;border:1px solid #dbe3ee;border-radius:9px;padding:12px 16px}}
a{{color:#1e3a8a;font-weight:600;text-decoration:none}} a:hover{{text-decoration:underline}}
small{{color:#64748b;word-break:break-all}} .note{{background:#fff7ed;border:1px solid #fed7aa;
border-radius:9px;padding:12px 16px;color:#7c2d12;font-size:.9rem}}
.ok{{background:#f0fdf4;border:1px solid #86efac;border-radius:9px;padding:12px 16px;
color:#14532d;font-size:.9rem}}</style></head><body>
<h1>Tautan unduh langsung (GitHub)</h1>
<div class="ok"><strong>Ini jalur utama.</strong> Tautan di bawah dihosting GitHub,
bukan lewat proxy live preview sandbox — jadi tidak terkena error 502.
Berkas sudah di-push ke cabang <code>arena/dc140e9f-kitab</code>.</div>
<p>Klik tautan untuk mengunduh. Untuk <code>.md</code>/<code>.html</code> yang tampil
di browser, klik kanan → <em>Save as…</em>; semuanya juga ada di dalam ZIP.</p>
<ul>{lis}</ul>
<div class="note"><strong>Catatan Ustadz Yoad.</strong> Terjemah selesai sebatas kunci
permanen §4.3 (kaifiyat, waktu, hari, بخور, syarat). Asma', azimah, wafaq, thilasm, dan
angka Arab-Indik tetap dijaga, tidak diterjemahkan.</div>
</body></html>"""
    out = ROOT / "UNDUHAN_LINK_LANGSUNG.html"
    out.write_text(doc, encoding="utf-8")
    return out


if __name__ == "__main__":
    landing = write_landing()
    if landing:
        print(f"Tautan absolut: {landing.name}", flush=True)
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Halaman unduhan siap di 0.0.0.0:{PORT}", flush=True)
    srv.serve_forever()
