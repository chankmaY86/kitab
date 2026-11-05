# CATATAN UNDUHAN — الأسماء الطمطمية

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

## Tautan unduh langsung (jalur utama)

Cabang `arena/dc140e9f-kitab` sudah di-push ke GitHub. Tautan ini **tidak lewat proxy
live preview sandbox**, jadi tidak terkena error 502:

| Berkas | Tautan |
|---|---|
| Paket lengkap .zip | `https://raw.githubusercontent.com/fatimah86-dot/kitab/arena/dc140e9f-kitab/UNDUHAN_ASMAK_THOMTHOMIYAH.zip` |
| Transkrip .docx | `https://raw.githubusercontent.com/fatimah86-dot/kitab/arena/dc140e9f-kitab/TRANSKRIPSI_ASMAK_THOMTHOMIYAH_LENGKAP.docx` |
| Terjemah Syarah .md | `https://raw.githubusercontent.com/fatimah86-dot/kitab/arena/dc140e9f-kitab/TERJEMAH_SYARAH_FUSHA_ASMAK_THOMTHOMIYAH.md` |
| Edisi baca offline .html | `https://raw.githubusercontent.com/fatimah86-dot/kitab/arena/dc140e9f-kitab/BACA_OFFLINE_ASMAK_THOMTHOMIYAH.html` |

Halaman GitHub: `https://github.com/fatimah86-dot/kitab/blob/arena/dc140e9f-kitab/UNDUHAN_ASMAK_THOMTHOMIYAH.zip`
(tombol *Download raw file*). Berkas `UNDUHAN_LINK_LANGSUNG.html` berisi kumpulan
tautan siap klik; ia hasil-generate lokal dan tidak masuk Git.

## Reproduksi

```
python3 -m venv .venv
.venv/bin/pip install -r requirements-editorial.txt
.venv/bin/python scripts/build_docx_asmak_thomthomiyah.py
.venv/bin/python scripts/build_unduhan_asmak_thomthomiyah.py
.venv/bin/python scripts/serve_unduhan.py      # halaman unduh: live preview port 8000
.venv/bin/python -m unittest discover -s tests -v
```
