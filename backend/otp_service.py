"""
VIT-ChainVote OTP Service
Handles OTP generation and email delivery via SMTP_SSL (Fast & Legit)
"""

import smtplib
import random
import time
import os
from email.message import EmailMessage
from typing import Dict

class OTPService:
    """
    Manages OTP generation, storage, and email delivery using SSL for speed.
    """
    
    def __init__(self):
        self.otp_storage: Dict[str, Dict] = {}
        self.otp_expiry_seconds = 300  # 5 minutes
        
        # SMTP Configuration (Direct from User request)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465
        self.sender_email = os.getenv("EMAIL_USER", "otakuaniverseofficial@gmail.com")
        self.app_password = os.getenv("EMAIL_PASS", "adxpxirxgwnrcjlo")
    
    def generate_otp(self) -> str:
        """
        Generate a random 6-digit OTP
        """
        return str(random.randint(100000, 999999))
    
    def store_otp(self, email: str, otp: str) -> None:
        """
        Store OTP with timestamp for expiry tracking
        """
        self.otp_storage[email.lower()] = {
            "otp": otp,
            "timestamp": time.time()
        }
    
    def verify_otp(self, email: str, otp: str) -> bool:
        """
        Verify OTP and check expiry
        """
        email = email.lower()
        if email not in self.otp_storage:
            return False
        
        stored_data = self.otp_storage[email]
        if time.time() - stored_data["timestamp"] > self.otp_expiry_seconds:
            del self.otp_storage[email]
            return False
        
        if stored_data["otp"] == otp:
            del self.otp_storage[email]
            return True
        return False
    
    def send_otp_email(self, recipient_email: str, otp: str) -> bool:
        """
        Send OTP via SMTP_SSL (Port 465) - Maximum speed
        """
        msg = EmailMessage()
        msg["Subject"] = "Your OTP Code - VIT-ChainVote"
        msg["From"] = self.sender_email
        msg["To"] = recipient_email
        msg.set_content(f"Your VIT-ChainVote OTP is: {otp}\n\nThis code will expire in 5 minutes.")

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.app_password)
                server.send_message(msg)
            print(f"✅ OTP SENT SUCCESSFULLY to {recipient_email}")
            return True
        except Exception as e:
            print(f"❌ ERROR SENDING EMAIL: {e}")
            return False
            
    def generate_and_send_otp(self, email: str) -> bool:
        """
        Generate OTP, store it, and send via email
        """
        otp = self.generate_otp()
        self.store_otp(email, otp)
        return self.send_otp_email(email, otp)
