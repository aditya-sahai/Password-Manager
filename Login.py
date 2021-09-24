import getpass
from hashlib import md5

from random import choice
import string

import json


class Login:
    def __init__(self):
        """
        Would have methods to accept credentials from user and check if they are valid or not.
        """
        self.USERS_FILE_NAME = "users.json"

        with open(self.USERS_FILE_NAME, "r") as users_f:
            self.users = json.load(users_f)

    def check_same_username(self, new_username):
        """
        Checks if a user with the entered username already exists.
        """
        username = md5(new_username.encode("UTF-8")).hexdigest()

        for user in self.users:
            if username == user["username"]:
                return True

        return False

    def get_new_user_info(self):
        """
        Asks user for username, password and confirms password.
        """
        while True:
            username = input("\nUsername: ").strip().lower()

            if not self.check_same_username(username):
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
        chars = string.ascii_letters + string.digits
        salt = ""

        for _ in range(16):
            salt += choice(chars)

        return salt

    def create_new_user(self):
        """
        Asks for username password ans asks user to confirm password.
        Adds salt and pepper to password and returns md5 hash.
        """
        user_info = self.get_new_user_info()
        username = user_info["username"]
        password = user_info["password"]

        salt = self.gen_salt()
        secure_password = f"{salt}{password}{choice(string.ascii_letters)}"

        hashed_password = md5(secure_password.encode("UTF-8")).hexdigest()
        hashed_username = md5(username.encode("UTF-8")).hexdigest()

        user_data = {
            "username": hashed_username,
            "password": hashed_password,
            "salt": salt
        }

        with open(self.USERS_FILE_NAME, "w") as users_f:
            self.users.append(user_data)
            json.dump(self.users, users_f, indent=4)


if __name__ == "__main__":
    LoginObject = Login()
    LoginObject.create_new_user()
