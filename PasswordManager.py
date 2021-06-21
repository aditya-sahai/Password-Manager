from cryptography.fernet import Fernet
import json
from hashlib import md5
import string
import random


class PasswordManager:
    def __init__(self):
        """
        Has methods to generate random passwords and read passwords from json file.
        """
        self.PASSWORD_FILE_NAME = "passwords.json"
        self.KEY_FILE_NAME = "passwords.key"
        self.KEY = self.get_key().encode()

        self.cryptor = Fernet(self.KEY)

        with open(self.PASSWORD_FILE_NAME, "r") as password_f:
            self.password_data = json.load(password_f)

    def get_key(self):
        """
        Checks if file has key else generates a new.
        """
        with open(self.KEY_FILE_NAME, "r") as key_f:
            key = key_f.read().strip()

        if key == "":
            key = Fernet.generate_key().decode()

            with open(self.KEY_FILE_NAME, "w") as key_f:
                key_f.write(key)

        return key

    def init_passwords(self):
        """
        Initializes the passwords.json file.
        """
        data = []

        with open(self.PASSWORD_FILE_NAME, "w") as f:
            json.dump(data, f, indent=4)

    def create_salt(self):
        """
        Returns a salt of 8 characters.
        """
        salt = ""
        for _ in range(8):
            salt += random.choice(string.ascii_letters + string.digits)

        return salt

    def get_hashed_password(self, password):
        """
        Adds salt and pepper to user password and hashes it.
        """
        salt = self.create_salt()
        pepper = random.choice(string.ascii_letters)
        hashed_password = md5(f"{salt}{password}{pepper}".encode()).hexdigest()

        return {
            "password": hashed_password,
            "salt": salt,
        }

    def create_new_user(self, username, password):
        """
        Creates a new user.
        """
        for user in self.password_data:
            if user["username"].lower() == username:
                return False

        password_info = self.get_hashed_password(password)
        self.password_data.append(
            {
                "username": username,
                "password": password_info["password"],
                "salt": password_info["salt"],
                "passwords": []
            }
        )

        with open(self.PASSWORD_FILE_NAME, "w") as f:
            json.dump(self.password_data, f, indent=4)

        return True


if __name__ == "__main__":
    Manager = PasswordManager()
    # Manager.create_new_user("aditya", "abcd123")