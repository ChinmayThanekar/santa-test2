import json
import os
from datetime import datetime
from config.settings import DB_FILE

def load_database():
    """Load room database from JSON file"""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_database(database):
    """Save room database to JSON file"""
    with open(DB_FILE, 'w') as f:
        json.dump(database, f, indent=2)

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
        save_database(db)
    return db[room_id]

def update_room_data(room_id, data):
    """Update room data in database"""
    db = load_database()
    if room_id in db:
        db[room_id].update(data)
        save_database(db)
    return get_room_data(room_id)
