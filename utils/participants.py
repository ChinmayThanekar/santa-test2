import random
import hashlib
from config.participants import PARTICIPANTS

def generate_pin(name):
    """Generate unique 4-digit PIN for participant"""
    seed = f"{name}{random.randint(1000, 9999)}"
    return str(int(hashlib.md5(seed.encode()).hexdigest(), 16) % 10000).zfill(4)

def is_valid_participant(name, participants=PARTICIPANTS):
    """Check if name is valid participant"""
    return name.strip().lower() in [p.lower() for p in participants]

def get_other_participants(name, participants=PARTICIPANTS):
    """Get all participants except the given name"""
    return [n for n in participants if n.lower() != name.lower()]
