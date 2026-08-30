from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session
import re

from db.database import get_db
from db.models import User

router = APIRouter()

class RegisterRequest(BaseModel):
    full_name: str
    phone: str
    pan_number: str

class LoginRequest(BaseModel):
    phone: str

class VerifyOTPRequest(BaseModel):
    phone: str
    otp: str

# In-memory store for mocked OTPs (in production, use Redis)
mock_otp_store = {}

def verify_pan_format(pan: str) -> bool:
    """Mock PAN verification: Checks standard 10-char format (5 letters, 4 digits, 1 letter)."""
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    return bool(re.match(pattern, pan.upper()))

@router.post("/register")
def register_user(req: RegisterRequest, db: Session = Depends(get_db)):
    if not verify_pan_format(req.pan_number):
        raise HTTPException(status_code=400, detail="Invalid PAN Card format. Must be like ABCDE1234F.")
    
    # Check if user exists
    existing = db.query(User).filter((User.phone == req.phone) | (User.pan_number == req.pan_number.upper())).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this phone or PAN already exists.")
    
    # Create user
    new_user = User(
        full_name=req.full_name,
        phone=req.phone,
        pan_number=req.pan_number.upper(),
        is_verified=True # Simulating successful PAN verification API call
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Account created successfully. You can now login.", "user_id": new_user.id}

@router.post("/login")
def login_user(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == req.phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="Phone number not registered. Please sign up.")
    
    # Generate Mock OTP
    otp = "123456"  # Mock OTP for local testing
    mock_otp_store[req.phone] = otp
    print(f"[AUTH] MOCK SMS: OTP for {req.phone} is {otp}")
    
    return {"message": "OTP sent to registered mobile number."}

@router.post("/verify-otp")
def verify_otp(req: VerifyOTPRequest, db: Session = Depends(get_db)):
    stored_otp = mock_otp_store.get(req.phone)
    if not stored_otp or stored_otp != req.otp:
        raise HTTPException(status_code=401, detail="Invalid or expired OTP.")
    
    user = db.query(User).filter(User.phone == req.phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
        
    # Clear OTP
    del mock_otp_store[req.phone]
    
    # In production, return a real JWT token here
    return {
        "message": "Login successful",
        "token": f"mock_jwt_token_{user.id}",
        "user": {
            "name": user.full_name,
            "phone": user.phone
        }
    }
