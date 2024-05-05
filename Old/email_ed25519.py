import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import credentials

# Generate Ed25519 key pair
private_key = ed25519.Ed25519PrivateKey.generate()
public_key = private_key.public_key()
# SMTP server configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# Create a message
message = MIMEMultipart()
message["From"] = credentials.SENDER_EMAIL
message["To"] = "shumh@bc.edu"
message["Subject"] = "Test Email"

# Add body to email
body = "This is a test signed email."
# Calculate hash of the body
digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
digest.update(body.encode())
hash_body = digest.finalize()

# Sign the hash with private key
signature = private_key.sign(
    hash_body
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
server.sendmail(credentials.SENDER_EMAIL, "yuaj@bc.edu", message.as_string())

# Send unsigned email
message_unsigned = MIMEMultipart()
message_unsigned["From"] = credentials.SENDER_EMAIL
message_unsigned["To"] = credentials.RECIPIENT_EMAIL
message_unsigned["Subject"] = "Unsigned Test Email"
message_unsigned.attach(MIMEText(body, "plain"))
server.sendmail(credentials.SENDER_EMAIL, "yuaj@bc.edu", message_unsigned.as_string())

# Quit the server
server.quit()

print("Email sent successfully.")
print("Public Key:", public_key_str)
print("Public Key cleaned:", public_key_str_cleaned)
