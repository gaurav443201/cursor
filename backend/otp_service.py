"""
VIT-ChainVote OTP Service
Handles OTP generation and email delivery via SMTP
"""

import smtplib
import random
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Optional
import os


class OTPService:
    """
    Manages OTP generation, storage, and email delivery
    """
    
    def __init__(self):
        self.otp_storage: Dict[str, Dict] = {}
        self.otp_expiry_seconds = 300  # 5 minutes
        
        # SMTP Configuration
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_user = os.getenv("EMAIL_USER", "otakuaniverseofficial@gmail.com")
        self.email_pass = os.getenv("EMAIL_PASS", "adxpxirxgwnrcjlo")
    
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
        stored_otp = stored_data["otp"]
        timestamp = stored_data["timestamp"]
        
        # Check expiry
        if time.time() - timestamp > self.otp_expiry_seconds:
            del self.otp_storage[email]
            return False
        
        # Verify OTP
        if stored_otp == otp:
            del self.otp_storage[email]  # Remove after successful verification
            return True
        
        return False
    
    def send_otp_email(self, recipient_email: str, otp: str) -> bool:
        """
        Send OTP via SMTP email
        """
        try:
            # Create email message
            message = MIMEMultipart("alternative")
            message["Subject"] = "🔐 VIT-ChainVote Authentication Code"
            message["From"] = self.email_user
            message["To"] = recipient_email
            
            # Email body with VIT branding
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 15px;
                        padding: 40px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 30px;
                    }}
                    .logo {{
                        font-size: 32px;
                        font-weight: bold;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                    }}
                    .otp-box {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        font-size: 36px;
                        font-weight: bold;
                        letter-spacing: 8px;
                        padding: 20px;
                        text-align: center;
                        border-radius: 10px;
                        margin: 30px 0;
                    }}
                    .info {{
                        color: #666;
                        font-size: 14px;
                        text-align: center;
                        margin-top: 20px;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #eee;
                        color: #999;
                        font-size: 12px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div class="logo">🗳️ VIT-ChainVote</div>
                        <p style="color: #666; margin-top: 10px;">Secure Blockchain Voting System</p>
                    </div>
                    
                    <h2 style="color: #333; text-align: center;">Your Authentication Code</h2>
                    
                    <div class="otp-box">{otp}</div>
                    
                    <div class="info">
                        <p>⏱️ This code will expire in <strong>5 minutes</strong></p>
                        <p>🔒 Never share this code with anyone</p>
                        <p>If you didn't request this code, please ignore this email</p>
                    </div>
                    
                    <div class="footer">
                        <p>VIT-ChainVote | Powered by Blockchain Technology</p>
                        <p>Secured by Proof-of-Work Consensus</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            html_part = MIMEText(html_body, "html")
            message.attach(html_part)
            
            # Send email via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_pass)
                server.send_message(message)
            
            return True
            
        except Exception as e:
            print(f"Error sending OTP email: {e}")
            return False
    
    def generate_and_send_otp(self, email: str) -> bool:
        """
        Generate OTP, store it, and send via email
        """
        otp = self.generate_otp()
        self.store_otp(email, otp)
        return self.send_otp_email(email, otp)
    
    def cleanup_expired_otps(self) -> None:
        """
        Remove expired OTPs from storage
        """
        current_time = time.time()
        expired_emails = [
            email for email, data in self.otp_storage.items()
            if current_time - data["timestamp"] > self.otp_expiry_seconds
        ]
        
        for email in expired_emails:
            del self.otp_storage[email]
