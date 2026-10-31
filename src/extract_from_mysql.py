"""Ambil tabel dari satu atau lebih database MySQL dan simpan sebagai CSV di data/raw/.

Cara pakai:
    python src/extract_from_mysql.py
"""
import pandas as pd
from sqlalchemy import create_engine, inspect, text

from config import DB_NAMES, RAW_DIR, TABLES, get_connection_url


def main() -> None:
    if not DB_NAMES:
        raise ValueError("DB_NAMES belum diisi. Salin .env.example menjadi .env dan lengkapi.")

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Koneksi ke tiap database + catat tabel apa saja yang ada di dalamnya
    engines = {}
    lokasi = {}  # nama_tabel -> daftar database yang memilikinya
    for db in DB_NAMES:
        engine = create_engine(get_connection_url(db))
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engines[db] = engine
        print(f"Koneksi berhasil: {db}")
        for t in inspect(engine).get_table_names():
            lokasi.setdefault(t, []).append(db)
    print()

    # 2. Ekspor tiap tabel dari database tempatnya berada
    tidak_ada = []
    for table in TABLES:
        dbs = lokasi.get(table)
        if not dbs:
            tidak_ada.append(table)
            continue
        if len(dbs) > 1:
            print(f"PERINGATAN: tabel '{table}' ada di {dbs}, memakai '{dbs[0]}'.")
        db = dbs[0]
        df = pd.read_sql(text(f"SELECT * FROM `{table}`"), engines[db])
        out_path = RAW_DIR / f"{table}.csv"
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        print(f"{table:<18} dari {db:<20} {len(df):>8,} baris -> {out_path.name}")

    if tidak_ada:
        print(f"\nTabel tidak ditemukan di database mana pun: {tidak_ada}")
        print("Cek nama tabel di src/config.py (TABLES) atau hak akses user.")
    else:
        print("\nSelesai. File tersimpan di data/raw/")


if __name__ == "__main__":
    main()
