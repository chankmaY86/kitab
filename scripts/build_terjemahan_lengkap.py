#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rakit edisi TERJEMAHAN LENGKAP + TRANSLITERASI Asmak Thomthomiyah.

- Menyuntik 15 kotak wafaq APA ADANYA dari master ke Lampiran F (dikecualikan).
- Membangun DOCX edisi terjemahan memakai pembangun RTL yang sama.
- Menjalankan pembangun paket unduhan agar ZIP ikut terbarukan.

Catatan: ini edisi tersendiri atas perintah eksplisit pemilik kitab;
master TRANSKRIPSI_... tetap berstatus Muhafazhah dan tidak diubah.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.md"
TARGET = ROOT / "TERJEMAHAN_LENGKAP_ASMAK_THOMTHOMIYAH.md"
OUT_DOCX = ROOT / "TERJEMAHAN_LENGKAP_ASMAK_THOMTHOMIYAH.docx"
MARKER = "{{WAFAQ_APPENDIX}}"

COVER = {
    "title": "Terjemahan Lengkap + Transliterasi — الأسماء الطمطمية",
    "subject": "Terjemah Indonesia menyeluruh + alih aksara Latin, kecuali wafaq",
    "kicker": "TERJEMAHAN LENGKAP + TRANSLITERASI",
    "arab_title": "الأسماء الطمطمية",
    "arab_sub": "أسماء آصف ابن برخيا وكيفية العمل بيها",
    "source": "Sumber: transkrip 12 halaman · asmak thomthomiyah.pdf",
    "binding": "Edisi atas perintah eksplisit 5 Nov 2026 · master tetap Muhafazhah",
    "warning": ("WAFAQ DIKECUALIKAN: 15 kotak ٣×٣ beserta angka Arab-Indiknya tidak "
                "diterjemahkan dan tidak ditransliterasi. Vokal pada transliterasi adalah "
                "ijtihad bantu karena naskah gundul — bukan pensahihan bacaan atau ijazah."),
}


def extract_wafaq(md: str):
    return re.findall(r'<table dir="rtl"[^>]*>.*?</table>', md, flags=re.S)


def build():
    master = MASTER.read_text(encoding="utf-8")
    tables = extract_wafaq(master)
    if len(tables) != 15:
        raise ValueError(f"Harus ada 15 tabel wafaq, ditemukan {len(tables)}")

    appendix = []
    for i, t in enumerate(tables, 1):
        appendix.append(
            f"#### Wafaq {i}\n\n"
            f"> **[DIKECUALIKAN — WAFAQ]** Disalin apa adanya dari transkrip master. "
            f"Angka Arab-Indik dan label sel tengah tidak diterjemahkan, tidak "
            f"ditransliterasi, tidak diubah.\n\n{t}\n"
        )

    text = TARGET.read_text(encoding="utf-8")
    if MARKER not in text:
        # Idempoten: kalau sudah dirakit, jangan menyuntik dua kali.
        if "#### Wafaq 15" in text and "#### Wafaq 1\n" in text:
            pass
        else:
            raise ValueError("Penanda Lampiran F tidak ditemukan")
    else:
        text = text.replace(MARKER, "\n".join(appendix).rstrip())
        TARGET.write_text(text, encoding="utf-8")

    sys.path.insert(0, str(ROOT / "scripts"))
    import build_docx_asmak_thomthomiyah as builder
    docx = builder.build(md_path=TARGET, out=OUT_DOCX, cover=COVER)

    # Perbarui paket unduhan (ZIP + HTML offline master + catatan).
    subprocess.run([sys.executable, str(ROOT / "scripts" /
                                       "build_unduhan_asmak_thomthomiyah.py")],
                   cwd=ROOT, check=True)
    return TARGET, docx


if __name__ == "__main__":
    md, dx = build()
    print(f"MD  : {md.name} ({md.stat().st_size} bytes)")
    print(f"DOCX: {dx.name} ({dx.stat().st_size} bytes)")
