"""Bersihkan data mentah dan simpan ke data/processed/.

Cara pakai:
    python src/clean_data.py

Yang dilakukan:
- Ubah kolom tanggal ke tipe tanggal murni (tanpa jam) agar relasi dim_date cocok.
- Buang baris duplikat.
- Hitung delivery_days jika kosong dan tanggal tersedia.
"""
import pandas as pd

from config import PROCESSED_DIR, RAW_DIR


def read_raw(name: str) -> pd.DataFrame:
    return pd.read_csv(RAW_DIR / f"{name}.csv")


def to_date(series: pd.Series) -> pd.Series:
    """Ubah ke tanggal saja (jam dibuang)."""
    return pd.to_datetime(series, errors="coerce").dt.normalize()


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # dim_date
    dim_date = read_raw("dim_date")
    dim_date["date"] = to_date(dim_date["date"])
    dim_date = dim_date.drop_duplicates(subset="date").sort_values("date")

    # dim_pelanggan
    dim_pelanggan = read_raw("dim_pelanggan").drop_duplicates(subset="customer_id")
    dim_pelanggan["registered_at"] = to_date(dim_pelanggan["registered_at"])

    # dim_product
    dim_product = read_raw("dim_product").drop_duplicates(subset="product_id")

    # fact_penjualan
    fact_penjualan = read_raw("fact_penjualan").drop_duplicates(subset="order_item_id")
    fact_penjualan["order_date"] = to_date(fact_penjualan["order_date"])

    # fact_pengiriman
    fact_pengiriman = read_raw("fact_pengiriman").drop_duplicates(subset="shipment_id")
    for col in ("shipped_at", "delivered_at"):
        fact_pengiriman[col] = to_date(fact_pengiriman[col])
    selisih = (fact_pengiriman["delivered_at"] - fact_pengiriman["shipped_at"]).dt.days
    fact_pengiriman["delivery_days"] = fact_pengiriman["delivery_days"].fillna(selisih)

    hasil = {
        "dim_date": dim_date,
        "dim_pelanggan": dim_pelanggan,
        "dim_product": dim_product,
        "fact_penjualan": fact_penjualan,
        "fact_pengiriman": fact_pengiriman,
    }
    for name, df in hasil.items():
        df.to_csv(PROCESSED_DIR / f"{name}.csv", index=False, encoding="utf-8-sig")
        print(f"{name:<18} {len(df):>8,} baris -> data/processed/{name}.csv")


if __name__ == "__main__":
    main()
