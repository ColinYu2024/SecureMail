import hashlib
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import credentials

# Generate RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

public_key = private_key.public_key()

# SMTP server configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # Use 465 for SSL connection


# Create a message
message = MIMEMultipart()
message["From"] = credentials.SENDER_EMAIL
message["To"] = credentials.RECIPIENT_EMAIL
message["Subject"] = "Test Email"

# Add body to email
body = "This is a test email."
# Calculate hash of the body
digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
digest.update(body.encode())
hash_body = digest.finalize()

# Sign the hash with private key
signature = private_key.sign(
    hash_body,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Encode the signature using Base64
signature_b64 = base64.b64encode(signature)

# Attach the body and signature to the email
message.attach(MIMEText(body, "plain"))
message["X-Digital-Signature"] = signature_b64.decode()  # Convert signature to Base64 encoded string

# Add public key as a custom header
if public_key:
    public_key_str = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    # Clean public key
    public_key_str_cleaned = public_key_str.replace("\n", "").replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "")
    message["X-Public-Key-Debug"] = public_key_str_cleaned
else:
    print("Public key is None.")

# Connect to the SMTP server
server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()  # Secure the connection
server.login(credentials.SENDER_EMAIL, credentials.PASSWORD)  # Login

# Send the email
server.sendmail(credentials.SENDER_EMAIL, credentials.RECIPIENT_EMAIL, message.as_string())

# Quit the server
server.quit()

print("Email sent successfully.")
print("Public Key:", public_key_str)
print("Public Key cleaned:", public_key_str_cleaned)
