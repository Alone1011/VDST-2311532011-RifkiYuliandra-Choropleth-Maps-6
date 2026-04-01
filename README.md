# Interactive Choropleth Map: Sumatera Barat (2015-2025)

![Choropleth Map Preview](https://img.shields.io/badge/Web_GIS-Vanilla_JS-blue.svg)
![Leaflet.js](https://img.shields.io/badge/Map_Engine-Leaflet.js-brightgreen.svg)
![Data Source](https://img.shields.io/badge/Data-BPS-orange.svg)

Aplikasi web pendeteksi sebaran peta interaktif (Web GIS) yang memvisualisasikan **13 Indikator Pembangunan Strategis** (seperti IPM, PDRB, Tingkat Pengangguran Terbuka, Angka Kemiskinan, hingga Gini Ratio) untuk wilayah administratif di seluruh cakupan Provinsi Sumatera Barat selama rentang waktu pengerjaan 1 dekade (2015 - 2025).

## 🌟 Fitur Utama

- **Pewarnaan Choropleth Adaptif**: Warna poligon beradaptasi secara otomatis berdasarkan sentimen indikator (Nuansa gradasi Merah Intens untuk indikator negatif, serta corak Biru Tua konstan untuk parameter bernuansa positif).
- **Legenda Otomatis Interval Cerdas**: Konstruksi batas kelas jenjang data (Class Interval) dan skala warna secara mandiri terkalibrasi *real-time* membidik nilai mutlak terendah ke tertinggi.
- **Pencarian String Dinamis (Fuzzy Feature)**: Pengambilan *missing link* key asimetris antar parameter `<option>` dengan GeoJSON Property dapat berjalan super kilat via validasi *Fuzzy Smart Lookup*.
- **Data Kosong Handled Gracefully**: Komputasi algoritma pencegahan macet (*NaN/Undefined*) untuk amankan data tahun prediksi BPS tanpa merusak fondasi Legenda, menggunakan visual warna abu-abu elegan (Status: Tidak Ada Data).
- **Control & Information Panel**: Pemantauan detail statistik tepat guna setiap kawasan hanya dengan menyorot area kursor tetikus (*Hover Response Highlight*).

## 🛠️ Stack Teknologi (Web & Pipeline)
- **Front-End Peta:** HTML5 Layouting, Moderen CSS Backdrop Filtering, Ekstensivitas Vanilla JavaScript, Leaflet.js BaseMap.
- **Data Preparation Engine:** Python 3 (Pandas & JSON Recursive Parsing).
- **Spasial Data Model:** *FeatureCollection* GeoJSON Restorasi (Handling data kordinat bersarang / *Triple Encoded Array Coordinates*).

## 🚀 Cara Menjalankan Secara Lokal (Local Deployment)

Sistem ini didesain tidak mengandalkan komunikasi *Backend Server* maupun *Database* berbayar, segala paket data ditanam menggunakan arsitektur statis JavaScript Array Objects (`sumbar-kabupaten-data.js`).

Demi melewati batas larangan ekstensi lintas origin (*CORS Block System*) pada pelacak Internet umum modern:
1. *Clone / Download* repositori kodingan ini.
2. Buka terminal (CMD / PowerShell / Bash) yang mengarah tepat ke dalam folder ekstrak.
3. Cetak landasan *Local Server* virtual bawaan SO Anda (Di Bawah ini merupakan skema menggunakan utilitas bawaan Python):
   ```bash
   python -m http.server 8000
   ```
4. Buka Browser jendelan berselancar Anda (Chrome/Firefox) kemudian kunjungi alamat: `http://localhost:8000`

## 👨‍💻 Hak Cipta & Kontributor Kegiatan
**Rifki Yuliandra (2311532011)**  
Tugas Mata Kuliah Visualisasi Data Spasio-Temporal (VDST)  
*Program Studi Informatika, Universitas Andalas*
