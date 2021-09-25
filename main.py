from UserManager import UserManager
from PasswordManager import PasswordManager
from InputMethods import InputMethods


Manager = UserManager()
InputManager = InputMethods()

print("\nEnter 'q' when asked for option number to quit.")
print("\n1. Sign In")
print("2. Sign Up")
signup_or_signin = input("\nEnter Option Number\n>>> ").strip()
user_signed_in = False

if signup_or_signin == "1":
    user_input_data = InputManager.username_pwd_input()
    username = user_input_data["username"]
    password = user_input_data["password"]
    credentials_validity_user_info = Manager.check_user_credentials(username, password)

    if credentials_validity_user_info["username-match"] and credentials_validity_user_info["password-match"]:
        user = Manager.users[credentials_validity_user_info["user-index"]]
        print(f"\nSuccesfully logged in as {username}!")
        user_signed_in = True

    else:
        print("\nInvalid Username/Password.")

elif signup_or_signin == "2":
    while True:
        username = input("\nUsername\n>>> ").strip().lower()

        if not Manager.check_user_credentials(username, None)["username-match"]:
            break
        else:
            print("\nUser with that username already exsits. Please enter a different username.")

    password = InputManager.confirm_pwd_input()
    Manager.sign_up(username, password)
    print(f"\nAccount With username, '{username}' created succesfully!")
    user_signed_in = True

elif signup_or_signin == "q":
    exit()

else:
    print("\nSorry. Could not understand.")

if user_signed_in:
    PasswordProcessor = PasswordManager(username)

    print("\n1. View Saved Password")
    print("2. Write New Password")
    print("3. Edit Old Password")
    print("4. Delete Password")
    print("5. Change Account Password")
    print("6. Delete Account")
    option = input("\nEnter Option Number\n>>> ").strip()

    if option == "1":
        pass

    elif option == "2":
        password_info = InputManager.app_password_input(True, True)
        PasswordProcessor.write_new_password(password_info["app"], password_info["password"])

    elif option == "3":
        password_info = InputManager.app_password_input(True, True)
        PasswordProcessor.update_saved_password(password_info["app"], password_info["password"])

    elif option == "4":
        pass

    elif option == "5":
        # Change Password Option
        new_password = InputManager.confirm_pwd_input()
        Manager.change_password(username, password, new_password)
        print("\nPassword changed succesfully!")

    elif option == "6":
        # Delete Account Option
        confirmation = getpass.getpass(prompt="\nPress any key to confirm. Press q to cancel").lower().strip()
        if confirmation != "q":
            Manager.delete_account(username, password)
        print("\nAccount deleted succesfully!")

    elif option == "q":
        exit()

    else:
        print("\nSorry. Could not understand.")