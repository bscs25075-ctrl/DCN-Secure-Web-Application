from backend.encryption import encrypt_data, decrypt_data

original_data = "Sensitive Information"

encrypted = encrypt_data(original_data)

print("Encrypted Data:", encrypted)

decrypted = decrypt_data(encrypted)

print("Decryption Successful:", decrypted == original_data)