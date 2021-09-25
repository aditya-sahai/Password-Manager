from cryptography.fernet import Fernet
from hashlib import md5
import json

from InputMethods import InputMethods


class PasswordManager:
    def __init__(self, username):
        """
        Manages passwords stored by users.
        """
        self.PASSWORDS_FILE_NAME = "passwords.json"

        with open(self.PASSWORDS_FILE_NAME, "r") as passwords_f:
            self.passwords = json.load(passwords_f)

        self.user_index = self.find_user_in_file(username)

    def find_user_in_file(self, username):
        """
        Finds the user index.
        """
        hashed_username = md5(username.encode("UTF-8")).hexdigest()
        for index, password in enumerate(self.passwords):
            if password["username"] == hashed_username:
                return index

    def find_app(self, app):
        """
        Returns index of dict with matching app name.
        """
        for index, password in enumerate(self.passwords[self.user_index]["passwords"]):
            decryptor = Fernet(password["key"].encode("UTF-8"))
            if decryptor.decrypt(password["app"].encode("UTF-8")).decode("UTF-8") == app:
                return index

        return None

    def write_new_password(self, app, password):
        """
        Writes app and password in the passwords file.
        """
        key = Fernet.generate_key()
        encryptor = Fernet(key)

        encrypted_app = encryptor.encrypt(app.encode("UTF-8")).decode("UTF-8")
        encrypted_password = encryptor.encrypt(password.encode("UTF-8")).decode("UTF-8")

        new_password_data = {
            "key": key.decode("UTF-8"),
            "app": encrypted_app,
            "password": encrypted_password,
        }


        if self.find_app(app) != None:
            print(f"\nYou have already saved a password with the app name '{app}'.")
            print("\nWould You like to edit the previously saved password?\n1.Yes\n2.No")
            option = input("\nEnter Option Number\n>>> ").strip()

            if option == "1":
                InputManager = InputMethods()
                password_info = InputManager.app_password_input(False, True)
                self.update_saved_password(app, password_info["password"])
                return

            elif option == "2":
                exit()

        else:
            self.passwords[self.user_index]["passwords"].append(new_password_data)
            with open(self.PASSWORDS_FILE_NAME, "w") as passwords_f:
                json.dump(self.passwords, passwords_f, indent=4)

            print(f"\nSuccesfully saved password for app '{app}'.")


    def update_saved_password(self, app, new_password):
        """
        Returns decrypted password.
        """
        password_index = self.find_app(app)

        if password_index != None:
            encryptor = Fernet(self.passwords[self.user_index]["passwords"][password_index]["key"].encode("UTF-8"))
            self.passwords[self.user_index]["passwords"][password_index]["password"] = encryptor.encrypt(new_password.encode("UTF-8")).decode("UTF-8")
            print(f"\nPassword for app '{app}' editted succefully.")

        else:
            print(f"\nYou dont have any password saved for the app named '{app}'.")
            print(f"\nWould You like to write a new password for '{app}'?\n1.Yes\n2.No")
            option = input("\nEnter Option Number\n>>> ").strip()

            if option == "1":
                InputManager = InputMethods()
                password_info = InputManager.app_password_input(False, True)
                self.write_new_password(app, password_info["password"])
                return

            elif option == "2":
                exit()

        with open(self.PASSWORDS_FILE_NAME, "w") as passwords_f:
            json.dump(self.passwords, passwords_f, indent=4)
