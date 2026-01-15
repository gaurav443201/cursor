"""
VIT-ChainVote OTP Service
Handles OTP generation and email delivery via SMTP (Port 587 with STARTTLS)
"""

import smtplib
import random
import time
import os
from email.message import EmailMessage
from typing import Dict, Tuple

import logging
logger = logging.getLogger(__name__)

class OTPService:
    """
    Manages OTP generation, storage, and email delivery using TLS for compatibility.
    """
    
    def __init__(self):
        self.otp_storage: Dict[str, Dict] = {}
        self.otp_expiry_seconds = 300  # 5 minutes
        
        # SMTP Configuration (Standard TLS Port 587 for Cloud Compatibility)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("EMAIL_USER", "otakuaniverseofficial@gmail.com")
        self.app_password = os.getenv("EMAIL_PASS", "adxpxirxgwnrcjlo")
    
    def generate_otp(self) -> str:
        return str(random.randint(100000, 999999))
    
    def store_otp(self, email: str, otp: str) -> None:
        self.otp_storage[email.lower()] = {
            "otp": otp,
            "timestamp": time.time()
        }
    
    def verify_otp(self, email: str, otp: str) -> bool:
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
    
    def send_otp_email(self, recipient_email: str, otp: str) -> Tuple[bool, str]:
        """
        Internal method to send email via SMTP Port 587
        """
        msg = EmailMessage()
        msg["Subject"] = "Your OTP Code - VIT-ChainVote"
        msg["From"] = self.sender_email
        msg["To"] = recipient_email
        msg.set_content(f"Your VIT-ChainVote OTP is: {otp}\n\nThis code will expire in 5 minutes.")

        try:
            # Using port 587 with STARTTLS for maximum reliability on Render
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10.0) as server:
                server.starttls()
                server.login(self.sender_email, self.app_password)
                server.send_message(msg)
            logger.info(f"✅ OTP SENT successfully to {recipient_email}")
            return True, "OTP sent successfully"
        except smtplib.SMTPAuthenticationError:
            err = "SMTP Auth Failed: Check EMAIL_USER and EMAIL_PASS on Render"
            logger.error(f"❌ {err}")
            return False, err
        except Exception as e:
            err = f"SMTP Error (Port 587): {str(e)}"
            logger.error(f"❌ {err}")
            return False, err
            
    def generate_and_send_otp(self, email: str) -> Tuple[bool, str]:
        """
        Main entry point for OTP generation and delivery
        """
        otp = self.generate_otp()
        self.store_otp(email, otp)
        return self.send_otp_email(email, otp)
