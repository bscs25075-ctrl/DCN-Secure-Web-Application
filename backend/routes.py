
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import SessionLocal
from backend.models import User
from backend.schemas import UserCreate, UserLogin, Token, SensitiveInfo
from backend.auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)
from backend.encryption import encrypt_data, decrypt_data

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# User Registration
@router.post("/register")
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        (User.email == user_data.email) |
        (User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email or username already registered"
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "username": new_user.username
    }


# User Login
@router.post("/login", response_model=Token)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if not user or not verify_password(
        user_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account is inactive"
        )

    access_token = create_access_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Protected User Profile
@router.get("/profile")
def get_profile(
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "Access granted!",
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }


# Admin Authorization
@router.get("/admin")
def admin_dashboard(
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access only"
        )

    return {
        "message": "Welcome to Admin Dashboard!",
        "username": user.username,
        "role": user.role
    }


# Save Sensitive Information (Encrypted)
@router.post("/secure-info")
def save_secure_info(
    data: SensitiveInfo,
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.encrypted_info = encrypt_data(data.information)
    db.commit()

    return {
        "message": "Information saved securely!"
    }


# Retrieve Sensitive Information (Decrypted)
@router.get("/secure-info")
def get_secure_info(
    user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not user.encrypted_info:
        raise HTTPException(
            status_code=404,
            detail="No secure information found"
        )

    return {
        "information": decrypt_data(user.encrypted_info)
    }
