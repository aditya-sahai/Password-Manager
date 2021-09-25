import getpass
from UserManager import UserManager


class InputMethods:
    def username_pwd_input(self):
        """
        Asks for username and password.
        """
        username = input("\nUsername\n>>> ").strip().lower()
        password = getpass.getpass(prompt="\nPassword\n>>> ")

        return {
            "username": username,
            "password": password
        }

    def confirm_pwd_input(self):
        """
        Asks for password and confirmation password until they match.
        """
        while True:
            password = getpass.getpass(prompt="\nPassword\n>>> ")
            confirm_password = getpass.getpass(prompt="\nConfirm Password\n>>> ")

            if password == confirm_password:
                break

            else:
                print("\nPassword Do Not Match! Try Again!\n")

        return password