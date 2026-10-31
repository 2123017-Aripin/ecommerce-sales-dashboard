import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")
pd.options.display.float_format = "{:,.1f}".format
pd.options.display.width = 200

def buat_engine(nama_db):
    url = URL.create(
        drivername="mysql+mysqlconnector",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=nama_db
    )
    return create_engine(url)

engine_raw = buat_engine(os.getenv("DB_NAME"))
engine_clean = buat_engine(os.getenv("DB_NAME_CLEAN"))

pelanggan = pd.read_sql("SELECT * FROM customers", engine_raw)
item_pesanan = pd.read_sql("SELECT * FROM order_items", engine_raw)
pesanan = pd.read_sql("SELECT * FROM orders", engine_raw)
pembayaran = pd.read_sql("SELECT * FROM payments", engine_raw)
produk = pd.read_sql("SELECT * FROM products", engine_raw)
shipments =pd.read_sql("SELECT * FROM shipments", engine_raw)

pelanggan['registered_at'] = pd.to_datetime(pelanggan['registered_at'])
pesanan['order_date'] = pd.to_datetime(pesanan['order_date'])
pembayaran['payment_date'] = pd.to_datetime(pembayaran['payment_date'])
shipments['shipped_at'] = pd.to_datetime(shipments['shipped_at'])
shipments['delivered_at'] = pd.to_datetime(shipments['delivered_at'])
produk['price'] = produk['price'].astype(float)
pembayaran['amount'] = pembayaran['amount'].astype(float)
pesanan[['shipping_cost', 'discount_amount']] = pesanan[['shipping_cost', 'discount_amount']].astype(float)
item_pesanan[['unit_price', 'discount_percent']] = item_pesanan[['unit_price', 'discount_percent']].astype(float)

for df in (pelanggan, item_pesanan, pesanan, pembayaran, produk, shipments):
    for k in df.select_dtypes(include='object').columns:
        df[k] = df[k].str.strip()

print("missing value per tabel:")
for nama, df in [("pelanggan", pelanggan),
    ("item_pesanan", item_pesanan),
    ("pesanan", pesanan),
    ("pembayaran", pembayaran),
    ("produk", produk),
    ("shipments", shipments)
]:
    print(f"{nama}: {int(df.isna().sum().sum()):,} missing value")

pembayaran_kosong = pembayaran.isnull().sum()
shipments_kosong = shipments.isnull().sum()
print(f'pembayaran kosong:\n{pembayaran_kosong}')
print(f'shipments kosong:\n{shipments_kosong}')

# payment_date kosong seharusnya status belum dibayar
print(f'pembayaran kosong (payment_date null):\n{pembayaran[pembayaran["payment_date"].isna()]["payment_status"].value_counts()}')

# delivered_at kosong seharusnya bukan status delivered
print(f'shipments kosong (shipped_at null):\n{shipments[shipments["shipped_at"].isna()]["tracking_status"].value_counts()}')
print(f'shipments kosong (delivered_at null):\n{shipments[shipments["delivered_at"].isna()]["tracking_status"].value_counts()}')

assert not item_pesanan.duplicated(subset="order_item_id").any(), "order_item_id duplikat"
assert (item_pesanan["quantity"] > 0).all(), "ada jumlah <= 0"
assert item_pesanan["discount_percent"].between(0, 100).all(), "diskon di luar 0-100"
assert set(item_pesanan["order_id"]) <= set(pesanan["order_id"]), "detail tanpa pesanan"
assert set(item_pesanan["product_id"]) <= set(produk["product_id"]), "detail tanpa produk"
assert pembayaran["order_id"].is_unique, "ada pesanan dengan >1 pembayaran"

fact = (
    item_pesanan
    .merge(pesanan[['order_id', 'customer_id', 'order_date', 'order_status', 'sales_channel', 'shipping_city', 'shipping_province']],
           on='order_id', how='left')
    .merge(pembayaran[['order_id', 'payment_method', 'payment_status']], on='order_id', how='left')
)
fact['gross_amount'] = fact['quantity'] * fact['unit_price']
fact['item_discount_amount'] = fact['gross_amount'] * fact['discount_percent'] / 100
fact['net_amount'] = fact['gross_amount'] - fact['item_discount_amount']

dim_pelanggan = pelanggan.copy()
dim_product = produk.copy()
dim_date = pd.DataFrame({'date': pd.date_range(start=pesanan['order_date'].min(), end=pesanan['order_date'].max())})

fact_pengiriman = shipments.copy()
fact_pengiriman['delivery_days'] = (
    fact_pengiriman['delivered_at'] - fact_pengiriman['shipped_at']
).dt.days

fact.to_sql("fact_penjualan", engine_clean, if_exists="replace", index=False)
dim_pelanggan.to_sql("dim_pelanggan", engine_clean, if_exists="replace", index=False)
dim_product.to_sql("dim_product", engine_clean, if_exists="replace", index=False)
dim_date.to_sql("dim_date", engine_clean, if_exists="replace", index=False)
fact_pengiriman.to_sql("fact_pengiriman", engine_clean, if_exists="replace", index=False)

print("\nSelesai. Tabel tersimpan di", os.getenv("DB_NAME_CLEAN"))
print(pd.read_sql("SELECT COUNT(*) AS baris FROM fact_penjualan", engine_clean))