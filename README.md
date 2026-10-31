# E-Commerce Sales Dashboard

Dashboard analisis penjualan, produk, pelanggan, dan pengiriman menggunakan **MySQL, Python, dan Power BI**.

## Tujuan
Memantau performa revenue, perilaku pelanggan, performa produk, dan efektivitas pengiriman.

## Dataset
| Tabel | Isi | Baris |
|---|---|---|
| dim_date | Kalender | 1.394 |
| dim_pelanggan | Data pelanggan | 500 |
| dim_product | Data produk | 100 |
| fact_penjualan | Transaksi | 6.010 |
| fact_pengiriman | Pengiriman | 2.000 |

Data bersifat sintetis (dummy), bukan data pelanggan asli.

## Alur kerja
1. **Ekstraksi**: ambil data dari MySQL dengan Python (`src/extract_from_mysql.py`)
2. **Pembersihan**: standarisasi tanggal dan duplikat (`src/clean_data.py`)
3. **Pemodelan**: star schema di Power BI
4. **Analisis**: DAX measure (lihat `docs/measures.md`)
5. **Visualisasi**: dashboard 4 halaman

## Halaman dashboard
1. Executive Overview
2. Product Analysis
3. Customer Analysis
4. Shipping & Fulfillment

## Preview
![Executive Overview](images/page1_overview.png)

## Insight utama
- (tulis 3-5 temuan dari data Anda)

## Cara menjalankan
```bash
# 1. Install dependensi
pip install -r requirements.txt

# 2. Atur koneksi database
cp .env.example .env      # lalu isi data MySQL Anda

# 3. Ambil data dari MySQL
python src/extract_from_mysql.py

# 4. Bersihkan data
python src/clean_data.py
```
Lalu buka `powerbi/ecommerce_dashboard.pbix`, arahkan sumber data ke folder `data/processed/`.

## Struktur folder
```
├── data/raw/          # hasil ekstraksi dari MySQL
├── data/processed/    # data bersih untuk Power BI
├── src/               # kode Python
├── notebooks/         # eksplorasi data (opsional)
├── powerbi/           # file .pbix dan export PDF
├── images/            # screenshot dashboard
└── docs/              # data dictionary dan DAX measures
```

## Tools
MySQL, Python (pandas, SQLAlchemy), Power BI Desktop, DAX
