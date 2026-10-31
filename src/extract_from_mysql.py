"""Ambil data mentah dan data hasil olahan dari MySQL, simpan sebagai CSV.

- DB_RAW   (mis. ecommerce_latihan) -> data/raw/
- DB_CLEAN (mis. ecommerce_clean)   -> data/processed/

Cara pakai:
    python src/extract_from_mysql.py
"""
import pandas as pd
from sqlalchemy import create_engine, inspect, text

from config import SOURCES, get_connection_url


def export_database(label: str, database: str, out_dir) -> int:
    engine = create_engine(get_connection_url(database))
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    tables = inspect(engine).get_table_names()
    if not tables:
        print(f"[{label}] Database '{database}' tidak punya tabel yang bisa dibaca.")
        print("         Cek hak akses user (GRANT SELECT) dan nama database di .env")
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"[{label}] {database} -> {out_dir.relative_to(out_dir.parents[1])}/")
    for table in tables:
        df = pd.read_sql(text(f"SELECT * FROM `{table}`"), engine)
        df.to_csv(out_dir / f"{table}.csv", index=False, encoding="utf-8-sig")
        print(f"   {table:<18} {len(df):>8,} baris")
    print()
    return len(tables)


def main() -> None:
    total = 0
    for src in SOURCES:
        total += export_database(src["label"], src["database"], src["out_dir"])
    print(f"Selesai. {total} tabel diekspor.")


if __name__ == "__main__":
    main()
