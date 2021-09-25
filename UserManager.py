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

    def get_new_user_info(self):
        """
        Asks user for username, password and confirms password.
        """
        while True:
            username = input("\nUsername: ").strip().lower()

            if not self.check_user_credentials(username, None)["username-match"]:
                break
            else:
                print("User With That Username Already Exists! Please enter a different username.")

        print()

        while True:
            password = getpass.getpass(prompt="Password: ")
            confirm_password = getpass.getpass(prompt="Confirm Password: ")

            if password == confirm_password:
                break

            else:
                print("\nPassword Do Not Match! Try Again!\n")

        return {
            "username": username,
            "password": password
        }

    def gen_salt(self):
        """
        Generates 16 char long salt.
        """
        salt = ""

        for _ in range(16):
            salt += choice(UserManager.CHARS)

        return salt

    def sign_up(self):
        """
        Asks for username password ans asks user to confirm password.
        Adds salt and pepper to password and returns md5 hash.
        """
        user_info = self.get_new_user_info()
        username = user_info["username"]
        password = user_info["password"]

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

    def sign_in(self):
        """
        Asks for username and password and checks if credentials are valid.
        """
        username = input("\nUsername: ").strip().lower()
        print()
        password = getpass.getpass(prompt="Password: ")

        credentials_validity = self.check_user_credentials(username, password)
        return credentials_validity["username-match"] and credentials_validity["password-match"]

    def delete_account(self, username, password):
        """
        Checks if password entered by user for confirmation matches and then deletes account.
        """
        credentials_validity_user_info = self.check_user_credentials(username, password)

        if credentials_validity_user_info["username-match"] and credentials_validity_user_info["password-match"]:
            del self.users[credentials_validity_user_info["user-index"]]

        with open(self.USERS_FILE_NAME, "w") as users_f:
            json.dump(self.users, users_f, indent=4)


if __name__ == "__main__":
    Manager = UserManager()
    print(Manager.delete_account("aditya", "hyper@$$"))
