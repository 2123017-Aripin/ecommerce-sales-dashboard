# Data Dictionary

Data bersifat sintetis (dummy), bukan data pelanggan asli.

## dim_date (1.394 baris)
| Kolom | Keterangan |
|---|---|
| date | Tanggal kalender (kunci relasi) |
| Year, Month Number, Month Name, Month Short, Quarter, Year Month | Kolom turunan untuk analisis waktu |

## dim_pelanggan (500 baris)
| Kolom | Keterangan |
|---|---|
| customer_id | ID pelanggan (primary key) |
| full_name, email, phone | Identitas pelanggan (sintetis) |
| city, province | Lokasi pelanggan |
| registered_at | Tanggal registrasi |
| customer_segment | Segmen pelanggan |

## dim_product (100 baris)
| Kolom | Keterangan |
|---|---|
| product_id | ID produk (primary key) |
| product_name, category, brand | Atribut produk |
| price, stock_qty | Harga dan stok |
| is_active | 1 = aktif |

## fact_penjualan (6.010 baris)
| Kolom | Keterangan |
|---|---|
| order_item_id | ID item order (primary key) |
| order_id | ID order (satu order bisa banyak item) |
| product_id, customer_id | Relasi ke dimensi |
| quantity, unit_price, discount_percent | Detail item |
| order_date | Tanggal order |
| order_status, sales_channel | Status order dan kanal penjualan |
| shipping_city, shipping_province | Tujuan pengiriman |
| payment_method, payment_status | Pembayaran |
| gross_amount, item_discount_amount, net_amount | Nilai transaksi |

## fact_pengiriman (2.000 baris)
| Kolom | Keterangan |
|---|---|
| shipment_id | ID pengiriman (primary key) |
| order_id | Relasi ke fact_penjualan |
| courier | Kurir |
| shipped_at, delivered_at | Tanggal kirim dan tiba |
| tracking_status | Status pengiriman |
| shipping_fee | Ongkos kirim |
| delivery_days | Lama pengiriman (hari) |

## Relasi (star schema)
- dim_date[date] 1 → * fact_penjualan[order_date]
- dim_pelanggan[customer_id] 1 → * fact_penjualan[customer_id]
- dim_product[product_id] 1 → * fact_penjualan[product_id]
- fact_penjualan[order_id] ↔ fact_pengiriman[order_id] (order_id di fact_penjualan tidak unik, perhatikan arah filter)
