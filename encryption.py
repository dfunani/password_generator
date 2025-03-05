import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Cryptography:
    def __init__(self):
        self.password = os.getenv("FERNET_PASSWORD", "password").encode()
        self.salt = bytes(16)
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000
        )
        self.key = base64.urlsafe_b64encode(self.kdf.derive(self.password))
        self.cipher = Fernet(self.key)



    def encrypt(self, message):
        return self.cipher.encrypt(message)

    def decrypt(self, message):
        return self.cipher.decrypt(message)
