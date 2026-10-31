"""Template pengolahan data mentah -> data hasil olahan.

Letakkan kode Python pembersihan/transformasi milik Anda di sini (atau ganti file ini
dengan kode Anda). Alur yang disarankan:

    data/raw/*.csv  (dari ecommerce_latihan)
        -> transformasi pandas
        -> data/processed/*.csv  (dan/atau ditulis ke database ecommerce_clean)

Cara pakai:
    python src/clean_data.py
"""
import pandas as pd

from config import PROCESSED_DIR, RAW_DIR


def read_raw(name: str) -> pd.DataFrame:
    return pd.read_csv(RAW_DIR / f"{name}.csv")


def to_date(series: pd.Series) -> pd.Series:
    """Ubah ke tanggal saja (jam dibuang) supaya relasi dim_date di Power BI cocok."""
    return pd.to_datetime(series, errors="coerce").dt.normalize()


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # TODO: tempel kode transformasi Anda di sini. Contoh pola:
    #
    # orders = read_raw("orders")
    # orders["order_date"] = to_date(orders["order_date"])
    # orders = orders.drop_duplicates(subset="order_id")
    # ...
    # fact_penjualan = ...   # hasil join orders + order_items + payments
    # fact_penjualan.to_csv(PROCESSED_DIR / "fact_penjualan.csv", index=False, encoding="utf-8-sig")

    print("Belum ada transformasi. Isi kode Anda di src/clean_data.py")


if __name__ == "__main__":
    main()
