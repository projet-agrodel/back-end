from cryptography.fernet import Fernet
from app import config
import base64

class EncryptionService:

    def encrypt(self, data: str) -> bytes:
        return self.cipher_suite.encrypt(data.encode())

    def decrypt(self, encrypted_data: bytes) -> str:
        return self.cipher_suite.decrypt(encrypted_data).decode() 