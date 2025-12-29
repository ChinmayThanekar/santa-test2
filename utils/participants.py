import random
import hashlib
from config.participants import PARTICIPANTS

def normalize_name(name):
    """Normalize name to lowercase for case-insensitive comparison"""
    return name.strip().lower()

def generate_pin(name):
    """Generate unique 4-digit PIN for participant"""
    seed = f"{name}{random.randint(1000, 9999)}"
    return str(int(hashlib.md5(seed.encode()).hexdigest(), 16) % 10000).zfill(4)

def is_valid_participant(name, participants=PARTICIPANTS):
    """Check if name is valid participant (case-insensitive)"""
    normalized = normalize_name(name)
    return normalized in [p.lower() for p in participants]

def get_other_participants(name, participants=PARTICIPANTS):
    """Get all participants except the given name (case-insensitive)"""
    normalized = normalize_name(name)
    return [n for n in participants if n.lower() != normalized]

def find_existing_participant(name, participants_data):
    """Find existing participant data by normalized name"""
    normalized = normalize_name(name)
    for stored_name, data in participants_data.items():
        if normalize_name(stored_name) == normalized:
            return stored_name, data
    return None, None
