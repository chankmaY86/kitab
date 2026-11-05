"""Uji struktur transkrip lengkap `asmak thomthomiyah.pdf`.

Ini uji keutuhan berkas (jumlah halaman, kotak wafaq, frasa penjaga),
BUKAN verifikasi bahasa Arab, harakat, atau klaim isi naskah.
"""
import re
import unittest
from pathlib import Path

try:
    from docx import Document
    from docx.oxml.ns import qn
    HAS_DOCX = True
except ImportError:  # ketergantungan opsional: requirements-editorial.txt
    HAS_DOCX = False

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

    def test_lapis_latin_kunci_asma(self):
        self.assertIn("## 1A. LATINISASI KUNCI ASMA'", self.md)
        self.assertIn("ATAS PERMINTAAN EKSPLISIT", self.md)
        self.assertIn("tidak melatinisasi sembarangan", self.md)
        self.assertIn("Skema yang dipakai", self.md)
        self.assertIn("Angka وافق ٣×٣", self.md)  # angka wafaq tetap Arab
        # Kunci utama + 14 asma' + 2 azimah + 5 varian + 2 judul harus ada.
        for lafaz in [
            "طمطكطجيشمحمدأل", "طشر موشش", "مهرش الش", "طفطنطفش", "كويش ظرخ",
            "طمخ طميخ", "جفنض لمخ", "يرة بزيخ", "شوكج بجخ", "مذطص جبخ",
            "حشتم دمخ", "مظهر شمخ", "ديوم شلش", "ارخ شمرخ", "لمخ شدمخ",
            "تبخ بخ بخ هيسون", "دلدل طد ندكم",
        ]:
            with self.subTest(lafaz=lafaz):
                self.assertIn(lafaz, self.md)
        for latin in [
            "ṭ-m-ṭ-k-ṭ-j-y-sy-m-ḥ-m-d-ʾ-l", "ṭasyar mawsyasy",
            "al-Asmā", "al-Ism al-Kabīr", "Peta huruf tanpa vokal",
        ]:
            with self.subTest(latin=latin):
                self.assertIn(latin, self.md)

    @unittest.skipUnless(HAS_DOCX, "python-docx belum terpasang")
    def test_docx_tersedia_dan_utuh(self):
        docx = ROOT / "TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.docx"
        self.assertTrue(docx.is_file())
        self.assertGreater(docx.stat().st_size, 20000)
        d = Document(docx)
        self.assertEqual(d.core_properties.author, "Ustadz Yoad")
        self.assertEqual(len(d.inline_shapes), 2)
        rtl = [t for t in d.tables
               if t._tbl.tblPr.find(qn("w:bidiVisual")) is not None]
        self.assertEqual(len(rtl), 15, "15 kotak wafaq harus RTL")
        # Angka Arab-Indik di DOCX harus identik dengan master Markdown
        # (<br> pada sel tengah dirender sebagai baris baru, jadi dinormalkan).
        for i, (t, expected) in enumerate(zip(rtl, WAFAG), 1):
            got = [[" ".join(c.text.split()) for c in r.cells] for r in t.rows]
            with self.subTest(wafaq_ke=i):
                self.assertEqual(got, expected)
        text = "\n".join(p.text for p in d.paragraphs)
        for t in d.tables:
            for row in t.rows:
                text += "\n" + " | ".join(c.text for c in row.cells)
        self.assertNotIn("`", text)
        self.assertNotIn("*", text)  # markup Markdown tidak boleh tampil mentah
        for s in ["طمطكطجيشمحمدأل", "٣٢٥١", "ṭasyar mawsyasy",
                  "[TEKS ASLI DIJAGA - TIDAK DITERJEMAH KARENA THILASM/WAFAQ]"]:
            with self.subTest(s=s):
                self.assertIn(s, text)

    def test_builder_docx_ada(self):
        self.assertTrue((ROOT / "scripts" / "build_docx_asmak_thomthomiyah.py").is_file())
        self.assertTrue((ROOT / "scripts" / "build_unduhan_asmak_thomthomiyah.py").is_file())

    def test_paket_unduhan(self):
        import zipfile
        zpath = ROOT / "UNDUHAN_ASMAK_THOMTHOMIYAH.zip"
        self.assertTrue(zpath.is_file())
        self.assertGreater(zpath.stat().st_size, 50000)
        with zipfile.ZipFile(zpath) as z:
            self.assertIsNone(z.testzip())
            names = set(z.namelist())
        for n in [
            "CATATAN_UNDUHAN_ASMAK_THOMTHOMIYAH.md",
            "TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.docx",
            "TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.md",
            "TERJEMAH_SYARAH_FUSHA_ASMAK_THOMTHOMIYAH.md",
            "BACA_OFFLINE_ASMAK_THOMTHOMIYAH.html",
            "KUNCI_PERMANEN_USTADZ_YOAD.md",
            "assets/asmak_thomthomiyah_hal02_khatim_tulis_tangan.png",
            "assets/asmak_thomthomiyah_hal10_asma_kabir.png",
        ]:
            with self.subTest(anggota=n):
                self.assertIn(n, names)

    def test_terjemah_syarah_berdiri_sendiri(self):
        t = (ROOT / "TERJEMAH_SYARAH_FUSHA_ASMAK_THOMTHOMIYAH.md").read_text(
            encoding="utf-8")
        self.assertIn("SELESAI", t)
        self.assertIn("§4.3", t)
        self.assertIn("TIDAK diterjemahkan", t)
        self.assertEqual(len(re.findall(r"^\d+\. \*\*", t, re.M)), 18,
                         "18 poin terjemah syarah harus lengkap")
        self.assertNotIn("٣٢٥١", t)  # angka kotak وافق tidak masuk bagian terjemah
        self.assertIn("| ٧٧ |", t)  # tabel jadwal hari/waktu

    def test_html_offline_mandiri(self):
        h = (ROOT / "BACA_OFFLINE_ASMAK_THOMTHOMIYAH.html").read_text(
            encoding="utf-8")
        self.assertEqual(h.count("data:image/png;base64,"), 2)
        self.assertNotIn('src="assets/', h)
        self.assertEqual(len(re.findall(r'<table dir="rtl"', h)), 15)
        self.assertIn("dir=\"rtl\"", h)
        self.assertIn("طمطكطجيشمحمدأل", h)
        self.assertNotIn("**", h)


if __name__ == "__main__":
    unittest.main()
