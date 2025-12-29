import json
import os
from datetime import datetime
from pathlib import Path

# Fix: Use absolute path and robust directory creation
BASE_DIR = Path(__file__).parent.parent  # Go up 2 levels to project root
DATA_DIR = BASE_DIR / "data"
DB_FILE = DATA_DIR / "secret_santa_rooms.json"

def ensure_data_dir():
    """Create data directory with full permissions"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    # Set write permissions
    os.chmod(DATA_DIR, 0o755)
    print(f"✅ Data dir ensured: {DATA_DIR.absolute()}")  # Debug

def load_database():
    """Load room database from JSON file"""
    ensure_data_dir()
    if DB_FILE.exists():
        try:
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
                print(f"✅ Loaded DB: {len(data)} rooms")  # Debug
                return data
        except Exception as e:
            print(f"⚠️ Error loading DB: {e}")
            return {}
    print("📭 No existing DB file")
    return {}

def save_database(database):
    """Save room database to JSON file with error handling"""
    ensure_data_dir()
    try:
        # Create backup first
        if DB_FILE.exists():
            backup = DB_FILE.with_suffix('.json.bak')
            DB_FILE.replace(backup)
        
        with open(DB_FILE, 'w') as f:
            json.dump(database, f, indent=2)
        os.chmod(DB_FILE, 0o644)
        print(f"💾 Saved DB: {len(database)} rooms")  # Debug
    except PermissionError as e:
        print(f"❌ Permission denied: {e}")
        print(f"   Path: {DB_FILE.absolute()}")
        print(f"   Permissions: {oct(os.stat(DB_FILE.parent).st_mode)[-3:]}")
        raise
    except Exception as e:
        print(f"❌ Save error: {e}")
        raise

def get_room_data(room_id):
    """Get or initialize room data"""
    db = load_database()
    if room_id not in db:
        db[room_id] = {
            'created': datetime.now().isoformat(),
            'participants_data': {},
            'event_name': f"Secret Santa Room {room_id}",
            'status': 'active'
        }
        print(f"🆕 Created room: {room_id}")  # Debug
        save_database(db)
    return db[room_id]

def update_room_data(room_id, data):
    """Update room data in database"""
    db = load_database()
    if room_id in db:
        db[room_id].update(data)
        save_database(db)
    return get_room_data(room_id)
