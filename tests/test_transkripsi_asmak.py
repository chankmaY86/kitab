"""Uji struktur transkrip lengkap `asmak thomthomiyah.pdf`.

Ini uji keutuhan berkas (jumlah halaman, kotak wafaq, frasa penjaga),
BUKAN verifikasi bahasa Arab, harakat, atau klaim isi naskah.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANSKRIP = ROOT / "TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.md"
ASSETS = [
    ROOT / "assets" / "asmak_thomthomiyah_hal02_khatim_tulis_tangan.png",
    ROOT / "assets" / "asmak_thomthomiyah_hal10_asma_kabir.png",
]

# 15 kotak وافق ٣×٣: 14 khātam + خاتم الاسم الكبير.
# Angka Arab-Indik dipertahankan apa adanya (kunci permanen §4.5).
WAFAG = [
    [["١", "٣٢٥١", "٣"], ["٥", "اسم المريض", "٣٢٥٠"], ["٣٢٤٩", "٤", "٢"]],
    [["١", "٢٢٧٢", "٣"], ["٥", "اسم الحاجة", "٢٢٧١"], ["٢٢٧٠", "٤", "٢"]],
    [["١", "١٢٧٣", "٣"], ["٥", "اسم المسروق", "١٢٧٢"], ["١٢٧١", "٤", "٢"]],
    [["١", "٢٦٣٢", "٣"], ["٥", "اسم المجنون", "٢٦٣١"], ["٢٦٣٠", "٤", "٢"]],
    [["١", "١٣٠٤", "٣"], ["٥", "الاسم", "١٣٠٣"], ["١٣٠٢", "٤", "٢"]],
    [["١", "٩٠٩", "٣"], ["٥", "اسمك", "٩٠٨"], ["٩٠٧", "٤", "٢"]],
    [["١", "٨٣٠", "٣"], ["٥", "اسم المسروق", "٨٢٩"], ["٨٢٨", "٤", "٢"]],
    [["١", "١٦٣٠", "٣"], ["٥", "اسم العدو", "١٦٢٩"], ["١٦٢٨", "٤", "٢"]],
    [["١", "١٤٨٨", "٣"], ["٥", "اسم البلد", "١٤٨٧"], ["١٤٨٦", "٤", "٢"]],
    [["١", "٢٠٨٨", "٣"], ["٥", "اسم الشخص", "٢٠٨٧"], ["٢٠٨٦", "٤", "٢"]],
    [["١", "٢٦٨١", "٣"], ["٥", "الحاجة", "٢٦٨٠"], ["٢٦٧٩", "٤", "٢"]],
    [["١", "٢٠٨٦", "٣"], ["٥", "الحاجة", "٢٠٨٥"], ["٢٠٨٤", "٤", "٢"]],
    [["١", "٢٦٣٧", "٣"], ["٥", "", "٢٦٣٦"], ["٢٦٣٥", "٤", "٢"]],
    [["١", "٢٣١٠", "٣"], ["٥", "الحاجة", "٢٣٠٩"], ["٢٣٠٨", "٤", "٢"]],
    [["١١", "١١٧٩", "٣٣"], ["٥٥", "الاسم", "١١٦٨"], ["١١٥٧", "٤٤", "٢٢"]],
]

PENANDA = "[TEKS ASLI DIJAGA - TIDAK DITERJEMAH KARENA THILASM/WAFAQ]"


class TranskripAsmakTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not TRANSKRIP.is_file():
            raise FileNotFoundError(f"Berkas transkrip hilang: {TRANSKRIP}")
        cls.md = TRANSKRIP.read_text(encoding="utf-8")

    def test_12_halaman(self):
        self.assertEqual(len(re.findall(r"^### HAL \d+", self.md, re.M)), 12)

    def test_identifikasi_jenis_teks(self):
        self.assertIn("## 0. IDENTIFIKASI JENIS TEKS", self.md)
        self.assertIn("Al-Muhafazhatu 'ala al-Qadimi as-Shalih", self.md)

    def test_penanda_muhafazhah(self):
        self.assertGreaterEqual(self.md.count(PENANDA), 15)

    def test_15_kotak_wafaq_angka_asli(self):
        tables = re.findall(r"<table dir=\"rtl\".*?</table>", self.md, re.S)
        self.assertEqual(len(tables), 15)
        for i, (tb, exp) in enumerate(zip(tables, WAFAG), start=1):
            with self.subTest(wafaq=i):
                rows = re.findall(r"<tr>(.*?)</tr>", tb, re.S)
                got = [
                    [
                        c.replace("<br>", " ").replace("&nbsp;", "").strip()
                        for c in re.findall(r"<td>(.*?)</td>", r, re.S)
                    ]
                    for r in rows
                ]
                self.assertEqual(got, exp)

    def test_bagian_wajib_format_kitab_hikmah(self):
        for judul in [
            "## 1. TEKS ARAB ASLI",
            "## 2. I'ROB FUSHA",
            "## 3. TERJEMAH SYARAH",
            "## 4. CATATAN HIKMAH",
        ]:
            self.assertIn(judul, self.md)
        self.assertIn("Ini adalah Thilasm/Wafaq/Asma' yang dijaga", self.md)
        self.assertIn("Istilah Falak/Hikmah", self.md)

    def test_facsimile_assets_ada(self):
        for a in ASSETS:
            with self.subTest(asset=a.name):
                self.assertTrue(a.is_file())
                self.assertGreater(a.stat().st_size, 1000)
        for a in ASSETS:
            self.assertIn(f"assets/{a.name}", self.md)


if __name__ == "__main__":
    unittest.main()
