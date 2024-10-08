import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Provided Base64-encoded public key string
public_key_str = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5KnodQEFGOoSH87ICB0LEbvfLhfavURtmw7gqmFvGp6gumwcnpp/F/cPr87w2JWHJ3tMpHaJKBjkU2MtALVUL9zewAJTXjJATu/E/MCNgxFH00Z4CUNSO6YdTL2P/tu7SbGVZ7xS6VGBgVq9rc/cQ2o6mFXSrnbMv1ynvfe77YIsT3wxB1ioJ2Y8e3JGJxs1shV7Y1lXrIauq+VzM7U29X/sgD8tVvWI4JFtKGt9Rnt0Z2knBejQzdEs4aNddfpSRQXjMChcg6TxylXRx6iCfU52jMXBesdkuUrpJBtFFshUiFHhEzkbjkUFqGyslmqW2YkKbGQgZoJIo6Sx054vcwIDAQAB"

# Decode the Base64 string
public_key_bytes = base64.b64decode(public_key_str)

# Print the decoded data
print(public_key_bytes)
