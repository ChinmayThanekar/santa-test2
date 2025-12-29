import os
from datetime import datetime

DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "secret_santa_rooms.json")

def ensure_data_dir():
    """Create data directory if it doesn't exist"""
    os.makedirs(DATA_DIR, exist_ok=True)
