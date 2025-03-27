from cryptography.fernet import Fernet
from app import config
import base64

class EncryptionService:
    def __init__(self) -> None:
        key = base64.urlsafe_b64encode(config.Config.SECRET_KEY.encode()[:32].ljust(32, b'\0'))
        self.cipher_suite = Fernet(key)

    def encrypt(self, data: str) -> bytes:
        return self.cipher_suite.encrypt(data.encode())

    def decrypt(self, encrypted_data: bytes) -> str:
        return self.cipher_suite.decrypt(encrypted_data).decode() 