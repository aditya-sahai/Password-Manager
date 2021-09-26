from UserManager import UserManager
from PasswordManager import PasswordManager
from InputMethods import InputMethods

import getpass

class Interface:
    def __init__(self):
        """
        Has input methods and uses PasswordManager and InputMethods classes.
        """
        self.Manager = UserManager()
        self.InputManager = InputMethods()
        self.user_signed_in = False

    def signin_signup(self):
        """
        Asks user if the user wants to sign in or signup and returns true if user logs in succefully.
        """
        print("\nEnter 'q' when asked for option number to quit.")
        print("\n1. Sign In")
        print("2. Sign Up")
        signup_or_signin = input("\nEnter Option Number\n>>> ").strip()

        if signup_or_signin == "1":
            user_input_data = self.InputManager.username_pwd_input()
            username = user_input_data["username"]
            password = user_input_data["password"]
            credentials_validity_user_info = self.Manager.check_user_credentials(username, password)

            if credentials_validity_user_info["username-match"] and credentials_validity_user_info["password-match"]:
                user = self.Manager.users[credentials_validity_user_info["user-index"]]
                print(f"\nSuccesfully logged in as {username}!")
                self.user_signed_in = True
                self.username = username
                self.password = password

            else:
                print("\nInvalid Username/Password.")


        elif signup_or_signin == "2":
            while True:
                username = input("\nUsername\n>>> ").strip().lower()

                if not self.Manager.check_user_credentials(username, None)["username-match"]:
                    break
                else:
                    print("\nUser with that username already exsits. Please enter a different username.")

            password = self.InputManager.confirm_pwd_input()
            self.Manager.sign_up(username, password)
            print(f"\nAccount With username, '{username}' created succesfully!")
            self.user_signed_in = True
            self.username = username
            self.password = password

        elif signup_or_signin == "q":
            self.user_signed_in = False

        else:
            print("\nSorry. Could not understand.")

    def password_options(self):
        """
        Asks the user what the user wants to do and calls the required methods.
        """
        print("\n1. View Saved Password")
        print("2. Write New Password")
        print("3. Edit Old Password")
        print("4. Delete Password")
        print("5. Change Account Password")
        print("6. Delete Account")
        option = input("\nEnter Option Number\n>>> ").strip()

        if option == "1":
            password_info = self.InputManager.app_password_input(True, False)
            self.PasswordProcessor.view_password(password_info["app"])

        elif option == "2":
            password_info = self.InputManager.app_password_input(True, True)
            self.PasswordProcessor.write_new_password(password_info["app"], password_info["password"])

        elif option == "3":
            password_info = self.InputManager.app_password_input(True, True)
            self.PasswordProcessor.update_saved_password(password_info["app"], password_info["password"])

        elif option == "4":
            password_info = self.InputManager.app_password_input(True, False)
            self.PasswordProcessor.delete_password(password_info["app"])

        elif option == "5":
            new_password = self.InputManager.confirm_pwd_input()
            self.Manager.change_password(self.username, self.password, new_password)
            print("\nPassword changed succesfully!")

        elif option == "6":
            confirmation = getpass.getpass(prompt="\nPress any key to confirm. Press q to cancel.").lower().strip()
            if confirmation != "q":
                self.Manager.delete_account(self.username, self.password)
                self.PasswordProcessor.delete_all_user_passwords()
                print("\nAccount deleted succesfully!")

            self.user_signed_in = False
            self.signin_signup()

            if self.user_signed_in:
                self.PasswordProcessor = PasswordManager(self.username)

        elif option == "q":
            self.user_signed_in = False

        else:
            print("\nSorry. Could not understand.")

    def main(self):
        """
        Has the main loop.
        """
        self.signin_signup()

        if self.user_signed_in:
            self.PasswordProcessor = PasswordManager(self.username)

            while self.user_signed_in:
                print("\nEnter 'q' when asked for option number to exit loop.")
                self.password_options()


if __name__ == "__main__":
    UI = Interface()
    UI.main()