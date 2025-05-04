from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64

private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print("PRIVATE_KEY (PEM):")
print(private_key_pem.decode())

print("\nPUBLIC_KEY (PEM):")
print(public_key_pem.decode())

# Optional: Output in base64 for VAPID headers
print("\nBase64 PRIVATE_KEY:")
print(base64.urlsafe_b64encode(private_key_pem).decode())

print("\nBase64 PUBLIC_KEY:")
print(base64.urlsafe_b64encode(public_key_pem).decode())