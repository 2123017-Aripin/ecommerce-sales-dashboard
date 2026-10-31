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

DB_RAW = os.getenv("DB_RAW", "ecommerce_latihan")
DB_CLEAN = os.getenv("DB_CLEAN", "ecommerce_clean")

# Setiap sumber: database mana -> disimpan ke folder mana.
# Semua tabel di database tersebut diambil otomatis (tidak perlu daftar tabel).
SOURCES = [
    {"label": "mentah", "database": DB_RAW, "out_dir": RAW_DIR},
    {"label": "hasil olahan", "database": DB_CLEAN, "out_dir": PROCESSED_DIR},
]


def get_connection_url(db_name: str) -> str:
    """Bangun URL koneksi SQLAlchemy (password di-encode agar karakter khusus aman)."""
    password = quote_plus(DB_PASSWORD)
    return f"mysql+pymysql://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{db_name}"
