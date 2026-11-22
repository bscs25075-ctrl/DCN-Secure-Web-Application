from backend.auth import hash_password, verify_password, create_access_token

password = "TestPassword123"

# Test password hashing
hashed = hash_password(password)
print("Password Hashed Successfully!")

# Test password verification
result = verify_password(password, hashed)
print("Password Verification:", result)

# Test JWT token
token = create_access_token({"sub": "testuser"})
print("JWT Token Created Successfully!")
print("Token:", token)