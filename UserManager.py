import getpass
from hashlib import md5
from cryptography.fernet import Fernet

from random import choice
import json


class UserManager:
    CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    def __init__(self):
        """
        Would have methods to accept credentials from user and check if they are valid or not.
        """
        self.USERS_FILE_NAME = "users.json"

        with open(self.USERS_FILE_NAME, "r") as users_f:
            self.users = json.load(users_f)

    def check_user_credentials(self, username, password):
        """
        Checks if a user with the entered username already exists.
        """
        username = md5(username.encode("UTF-8")).hexdigest()
        username_match = False
        password_match = False
        user_index = None

        for i, user in enumerate(self.users):
            if user["username"] == username:
                username_match = True
                user_index = i

                for char in UserManager.CHARS:
                    secure_password = f"{user['salt']}{password}{char}"
                    hashed_password = md5(secure_password.encode("UTF-8")).hexdigest()

                    if user["password"] == hashed_password:
                        password_match = True
                        break

        return {
            "username-match": username_match,
            "password-match": password_match,
            "user-index": user_index,
        }

    def gen_salt(self):
        """
        Generates 16 char long salt.
        """
        salt = ""

        for _ in range(16):
            salt += choice(UserManager.CHARS)

        return salt

    def sign_up(self, username, password):
        """
        Asks for username password ans asks user to confirm password.
        Adds salt and pepper to password and returns md5 hash.
        """
        salt = self.gen_salt()
        secure_password = f"{salt}{password}{choice(UserManager.CHARS)}"

        hashed_password = md5(secure_password.encode("UTF-8")).hexdigest()
        hashed_username = md5(username.encode("UTF-8")).hexdigest()

        user_data = {
            "username": hashed_username,
            "password": hashed_password,
            "salt": salt,
            "key": Fernet.generate_key().decode(),
            "passwords": [],
        }

        with open(self.USERS_FILE_NAME, "w") as users_f:
            self.users.append(user_data)
            json.dump(self.users, users_f, indent=4)

    def delete_account(self, username, password):
        """
        Checks if password entered by user for confirmation matches and then deletes account.
        """
        credentials_validity_user_info = self.check_user_credentials(username, password)

        if credentials_validity_user_info["username-match"] and credentials_validity_user_info["password-match"]:
            del self.users[credentials_validity_user_info["user-index"]]

        with open(self.USERS_FILE_NAME, "w") as users_f:
            json.dump(self.users, users_f, indent=4)

    def change_password(self, username, old_password, new_password):
        """
        Changes the password of a user.
        """
        index = self.check_user_credentials(username, old_password)["user-index"]
        salt = self.gen_salt()
        secure_password = f"{salt}{new_password}{choice(UserManager.CHARS)}"
        hashed_password = md5(secure_password.encode("UTF-8")).hexdigest()
        self.users[index]["password"] = hashed_password
        self.users[index]["salt"] = salt

        with open(self.USERS_FILE_NAME, "w") as users_f:
            json.dump(self.users, users_f, indent=4)


if __name__ == "__main__":
    Manager = UserManager()