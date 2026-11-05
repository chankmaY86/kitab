"""Penjaga kunci permanen Ustadz Yoad.

Memastikan aturan 10 langkah, aturan Kitab Hikmah, dan format output tidak hilang
atau berubah urutan tanpa disengaja. Ini uji struktur berkas, BUKAN verifikasi
kebenaran nahwu-sharaf atau kesetiaan terhadap naskah.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KUNCI = ROOT / "KUNCI_PERMANEN_USTADZ_YOAD.md"
AGENTS = ROOT / "AGENTS.md"

STEP_TITLES = [
    "TENTUKAN JENIS KATA",
    "CARI AKAR KATA",
    "MUBTADA' MARFU'",
    "KHOBAR MUQODDAM & MUAKHOR",
    "HURUF AN",
    "FI'IL MUDHARI'",
    "MAF'UL BIH & DHOMIR",
    "HURUF ATHAF",
    "DHOROF ZAMAN",
    "JAR MAJRUR & IDHOFAH",
]

HIKMAH_TITLES = [
    "IDENTIFIKASI JENIS TEKS",
    "PAKAI MAZHAB MUHAFAZHAH",
    "PAKAI ARAB FUSHA HANYA UNTUK SYARAH",
    "KAMUS ISTILAH HIKMAH",
    "JANGAN UBAH ANGKA WAFAQ",
]

FRASES_TERKUNCI = [
    "Jangan diringkas, jangan loncat-loncat, harus urut.",
    "صَدَقَ - يَصْدُقُ - صِدْقًا",
    "مُبْتَدَأٌ مَرْفُوعٌ بِالضَّمَّةِ",
    "خَبَرٌ مُقَدَّمٌ لِـ",
    "مُبْتَدَأٌ مُؤَخَّرٌ",
    "خَبَرٌ لِ \"العَبْدِ\"",
    "أَنۡ : حَرْفُ مَصْدَرٍ وَنَصْبٍ",
    "أَفْعَلَ - يُفْعِلُ",
    "نَجَا - يَنْجُو",
    "أَنْجَى - يُنْجِي",
    "فِعْلٌ مُضَارِعٌ مَنْصُوبٌ بِالفَتْحَةِ",
    "مَفْعُولٌ بِهِ مَنْصُوبٌ بِالفَتْحَةِ",
    "ضَمِيرٌ مُتَّصِلٌ فِي مَحَلِّ نَصْبٍ مَفْعُولٌ بِهِ",
    "وَيَحْمَدَهُ",
    "وَ : حَرْفُ عَطْفٍ = dan",
    "ظَرْفُ زَمَانٍ مَنْصُوبٌ بِالفَتْحَةِ = di setiap waktu",
    "عَلَى كُلِّ حَالٍ",
    "عَلَى : حَرْفُ جَرٍّ",
    "مَجْرُورٌ بِـ عَلَى وَهُوَ مُضَافٌ",
    "مُضَافٌ إِلَيْهِ مَجْرُورٌ بِالكَسْرَةِ",
    "[TEKS ASLI DIJAGA - TIDAK DITERJEMAH KARENA THILASM/WAFAQ]",
    "Al-Muhafazhatu 'ala al-Qadimi as-Shalih",
    "إذا أردت، فاكتب في ساعة، بخر ب...",
    "زحل، مشتري، عطارد، وفق، طلسم، خاتم، توكيل، خادم، بخور",
    "Istilah Falak/Hikmah",
    "الصِّدْقُ ينجي والكذب يهلك",
    "العبد عليه أن يشكر الله ويحمده دائما على كل حال",
]


class KunciPermanenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not KUNCI.is_file():
            raise FileNotFoundError(f"Berkas kunci permanen hilang: {KUNCI}")
        cls.text = KUNCI.read_text(encoding="utf-8")

    def test_status_dan_identitas(self):
        self.assertIn("STATUS: AKTIF", self.text)
        self.assertIn("SUMBER TUNGGAL", self.text)
        self.assertIn("Ustadz Yoad", self.text)
        self.assertIn("Pakar Nahwu Sharaf", self.text)

    def test_10_langkah_lengkap_dan_urut(self):
        found = re.findall(r"^### \[LANGKAH (\d+): ([^\]]+)\]", self.text, re.M)
        self.assertEqual([int(n) for n, _ in found], list(range(1, 11)))
        self.assertEqual([judul for _, judul in found], STEP_TITLES)

    def test_format_output_wajib(self):
        self.assertIn("## 2. FORMAT OUTPUT WAJIB", self.text)
        for nomor, butir in enumerate(
            [
                "Tulis ulang teks Arabnya",
                "Bedah kata per kata pakai 10 langkah di atas (urut)",
                "Berikan Terjemah Harfiah per kata",
                "Berikan Terjemah Bebas / Makna Keseluruhan",
            ],
            start=1,
        ):
            self.assertIn(f"{nomor}. {butir}", self.text)

    def test_contoh_referensi(self):
        self.assertIn("## 3. CONTOH REFERENSI YANG SUDAH BENAR", self.text)
        self.assertIn("Kejujuran menyelamatkan, kebohongan membinasakan.", self.text)
        self.assertIn(
            "Hamba wajib atasnya mensyukuri Allah dan memuji-Nya di setiap waktu di setiap keadaan.",
            self.text,
        )

    def test_5_aturan_kitab_hikmah_lengkap_dan_urut(self):
        found = re.findall(r"^### (\d+)\. (.+)$", self.text, re.M)
        self.assertEqual([int(n) for n, _ in found], [1, 2, 3, 4, 5])
        self.assertEqual([judul for _, judul in found], HIKMAH_TITLES)
        self.assertIn("(Abu Ma'syar, Abu Maryam, Al-Buni, Al-Falaky)", self.text)

    def test_format_output_kitab_hikmah(self):
        self.assertIn("## 5. FORMAT OUTPUT UNTUK KITAB HIKMAH", self.text)
        for butir in [
            "Teks Arab Asli (Muhafazhah - biarkan)",
            "I'rob Fusha (jika syarah)",
            "Terjemah Syarah (Fusha)",
            "Catatan Hikmah: Ini adalah Thilasm/Wafaq/Asma' yang dijaga",
        ]:
            self.assertIn(f"- {butir}", self.text)

    def test_frasa_arab_terkunci_tidak_berubah(self):
        for frasa in FRASES_TERKUNCI:
            with self.subTest(frasa=frasa):
                self.assertIn(frasa, self.text)

    def test_agents_md_merujuk_berkas_kunci(self):
        self.assertTrue(AGENTS.is_file(), "AGENTS.md hilang")
        agents = AGENTS.read_text(encoding="utf-8")
        self.assertIn("KUNCI_PERMANEN_USTADZ_YOAD.md", agents)
        self.assertIn("Jangan diringkas, jangan loncat-loncat, harus urut.", agents)
        self.assertIn("[TEKS ASLI DIJAGA - TIDAK DITERJEMAH KARENA THILASM/WAFAQ]", agents)
        self.assertIn("yang menang", agents)


if __name__ == "__main__":
    unittest.main()
