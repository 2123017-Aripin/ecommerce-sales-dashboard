"""Konfigurasi koneksi database dan path folder proyek."""
import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

load_dotenv(BASE_DIR / ".env")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Mendukung banyak database: DB_NAMES=db1,db2  (DB_NAME lama tetap bisa dipakai)
_names = os.getenv("DB_NAMES") or os.getenv("DB_NAME", "")
DB_NAMES = [n.strip() for n in _names.split(",") if n.strip()]

# Daftar tabel yang diambil. Skrip akan mencari tiap tabel di semua database di atas.
TABLES = [
    "dim_date",
    "dim_pelanggan",
    "dim_product",
    "fact_penjualan",
    "fact_pengiriman",
]


def get_connection_url(db_name: str) -> str:
    """Bangun URL koneksi SQLAlchemy (password di-encode agar karakter khusus aman)."""
    password = quote_plus(DB_PASSWORD)
    return f"mysql+pymysql://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{db_name}"
