# Asrār Rūḥāniyyah — Pembaca 5 Lapis

Aplikasi web (PWA-ready, React + Vite) untuk membaca master editorial
`REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.md` dari repo ini.

Setiap halaman disajikan dalam lima lapis: **Arab · Latin · Terjemahan · Syarah · Khususiyah**,
tanpa menulis ulang teks — parser hanya memecah struktur master.

## Menjalankan

```sh
cd kitab-app
npm install
npm run dev      # http://localhost:5173
```

Perintah lain:

| Perintah | Fungsi |
|---|---|
| `npm run data` | Bangun ulang `src/data/kitab.json` dari master Markdown |
| `npm run build` | Bangun data + bundel produksi ke `dist/` |
| `npm run preview` | Sajikan hasil build |
| `npm run check` | Uji data, pencarian, dan render seluruh blok (tanpa browser) |

Master dibaca dari `../REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.md`. Untuk memakai berkas lain:

```sh
KITAB_MASTER=/jalur/ke/master.md npm run data
```

## Fitur

- **Daftar halaman** dengan saring per bagian (Pembuka, Faedah, Doa & Riyadhah, Pelajaran), penanda wafaq, dan pencarian judul.
- **Pembaca lima lapis**: tiap lapis bisa ditampilkan/disembunyikan; preferensi disimpan di perangkat.
- **Tabel wafaq** dirender sebagai kotak huruf/angka RTL (terdeteksi otomatis huruf vs angka), bukan tabel markdown datar.
- **Pencarian penuh** di 65 halaman × 5 lapis, di sisi klien, dengan sorotan dan cuplikan per lapis.
- **Penanda halaman** dan **lanjut baca** tersimpan di `localStorage`.
- **Tema** terang / sepia / malam, pengatur ukuran huruf Arab dan Latin, pilihan font Arab (Amiri atau sistem).
- **Salin halaman**, **cetak** (gaya cetak khusus), daftar isi berbentuk laci, pintasan `←` `→` dan `/`.
- Nada dan struktur mengikuti naskah: klaim khasiat ditandai sebagai isi tradisi, bukan bukti medis.

## Struktur

```
kitab-app/
├── scripts/
│   ├── build-data.mjs   # master .md  →  src/data/kitab.json
│   ├── titles.txt       # judul Latin & bagian per halaman
│   └── check.mjs        # uji data + pencarian + render
├── src/
│   ├── components/      # Home, Reader, Blocks, SearchView, SettingsView, Drawer, Icons
│   ├── lib/             # text.js (parser inline), search.js (indeks), store.js (localStorage)
│   ├── data/kitab.json  # hasil parser (dibangun, ikut repo agar app langsung jalan)
│   ├── App.jsx          # router hash + topbar + tema
│   └── index.css
└── public/art/sampul.jpg
```

## Catatan editorial yang dipertahankan

- Teks ditampilkan apa adanya, termasuk penanda `[konfirmasi editorial: ٤]` dan
  `[Rajah Huruf — tidak diterjemahkan]` (yang terakhir ditampilkan sebagai label kecil, bukan teks mentah).
- Halaman master 01–65 dipetakan ke folio cetak pada naskah; delapan folio yang tidak tersedia pada
  pindaian (14, 36–37, 40, 48, 56, 62, 72) dicatat di halaman Tentang aplikasi.
- Aplikasi ini alat baca, bukan pengesahan harakat, nahwu-sharaf, maupun khasiat.
