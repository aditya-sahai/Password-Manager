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

    def app_password_input(self, app_is_required, password_is_required):
        """
        Asks user for app and if password_requirement is true then also asks for password.
        """
        password = None
        app = None

        if app_is_required:
            app = input("\nApp\n>>> ").strip().lower()

        if password_is_required:
            password = input("\nPassword\n>>> ")

        return {
            "app": app,
            "password": password,
        }