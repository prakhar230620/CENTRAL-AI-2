from cryptography.fernet import Fernet
import base64
import logging
import os

class Encryption:
    def __init__(self, key=None):
        self.logger = logging.getLogger(__name__)
        if key:
            self.key = base64.urlsafe_b64encode(key.encode())
        else:
            self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode()
        encrypted_data = self.cipher_suite.encrypt(data)
        self.logger.info("Data encrypted successfully")
        return encrypted_data

    def decrypt(self, encrypted_data):
        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
        self.logger.info("Data decrypted successfully")
        return decrypted_data

    def encrypt_file(self, file_path):
        with open(file_path, 'rb') as file:
            file_data = file.read()
        encrypted_data = self.encrypt(file_data)
        encrypted_file_path = file_path + '.encrypted'
        with open(encrypted_file_path, 'wb') as file:
            file.write(encrypted_data)
        self.logger.info(f"File {file_path} encrypted and saved as {encrypted_file_path}")

    def decrypt_file(self, encrypted_file_path):
        with open(encrypted_file_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = self.decrypt(encrypted_data)
        decrypted_file_path = encrypted_file_path[:-10]  # Remove '.encrypted'
        with open(decrypted_file_path, 'wb') as file:
            file.write(decrypted_data)
        self.logger.info(f"File {encrypted_file_path} decrypted and saved as {decrypted_file_path}")

    @staticmethod
    def generate_key():
        return Fernet.generate_key()