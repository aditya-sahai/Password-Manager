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
        with open(self.KEY_FILE_NAME, "r") as key_f:
            self.KEY = key_f.read().strip().encode()

        self.cryptor = Fernet(self.KEY)

        with open(self.PASSWORD_FILE_NAME, "r") as password_f:
            self.password_data = json.load(password_f)

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
                "username": username.strip(),
                "password": password_info["password"],
                "salt": password_info["salt"],
                "passwords": []
            }
        )

        with open(self.PASSWORD_FILE_NAME, "w") as f:
            json.dump(self.password_data, f, indent=4)

        return True

    def check_hashed_password(self, password, salt, hash):
        """
        Checks if the given password matches the hash
        """
        for pepper in string.ascii_letters:
            hashed_password = md5(f"{salt}{password}{pepper}".encode()).hexdigest()

            if hashed_password == hash:
                return True

        return False

    def check_user_info(self, username, password):
        """
        Returns true if username and password is correct.
        """
        for user in self.password_data:
            if user["username"].lower() == username.lower():
                password_is_correct = self.check_hashed_password(password, user["salt"], user["password"])

                if password_is_correct:
                    return True

        return False

    def write_new_password(self, username, app, password):
        """
        Writes a new password in the user's dict.
        """
        for user_num, user in enumerate(self.password_data):
            if user["username"].lower() == username.lower().strip():
                self.password_data[user_num]["passwords"].append(
                    {
                        "app": self.cryptor.encrypt(app.encode()).decode(),
                        "password": self.cryptor.encrypt(password.encode()).decode()
                    }
                )

        with open(self.PASSWORD_FILE_NAME, "w") as f:
            json.dump(self.password_data, f, indent=4)

    def get_password(self, username, app_name):
        """
        Returns password of app of user.
        """
        for user in self.password_data:
            if user["username"].lower() == username.lower().strip():
                for app in user["passwords"]:
                    app_name_f = self.cryptor.decrypt(app["app"].encode()).decode()

                    if app_name_f == app_name:
                        password = self.cryptor.decrypt(app["password"].encode()).decode()
                        return password

        return None


if __name__ == "__main__":
    Manager = PasswordManager()
