"""
VIT-ChainVote Utility Functions
Email validation, hashing, and helper functions
"""

import hashlib
import re
from typing import Optional


# Valid departments
VALID_DEPARTMENTS = ["CSE", "IT", "ENTC", "MECH"]

# Shadow admin emails
SHADOW_ADMINS = [
    "shadow70956@gmail.com",
    "navgharegaurav80@gmail.com"
]


def is_valid_vit_email(email: str) -> bool:
    """
    Validate VIT institute email format: name.prn@vit.edu
    """
    pattern = r'^[a-zA-Z0-9]+\.[a-zA-Z0-9]+@vit\.edu$'
    return bool(re.match(pattern, email))


def is_shadow_admin(email: str) -> bool:
    """
    Check if email belongs to a Shadow administrator
    """
    return email.lower() in [admin.lower() for admin in SHADOW_ADMINS]


def hash_email(email: str) -> str:
    """
    Generate SHA-256 hash of email for privacy
    Used to prevent double voting without storing actual emails
    """
    return hashlib.sha256(email.lower().encode()).hexdigest()


def is_valid_department(department: str) -> bool:
    """
    Validate department code
    """
    return department.upper() in VALID_DEPARTMENTS


def extract_department_from_email(email: str) -> Optional[str]:
    """
    Extract department from VIT email
    This is a placeholder - in production, you'd have a mapping
    For now, we'll require users to specify their department
    """
    # In a real system, you might have a database mapping PRN to department
    # For this implementation, department will be provided during registration
    return None


def generate_transaction_id(voter_hash: str, candidate_id: str, timestamp: float) -> str:
    """
    Generate unique transaction ID for vote confirmation
    """
    data = f"{voter_hash}{candidate_id}{timestamp}"
    return hashlib.sha256(data.encode()).hexdigest()[:16].upper()


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    """
    # Remove potentially dangerous characters
    return re.sub(r'[<>\"\'%;()&+]', '', text)


def format_timestamp(timestamp: float) -> str:
    """
    Format Unix timestamp to readable date
    """
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
