from PasswordCryptography import *


class Interface(PasswordCryptography):
    def __init__(self):
        super().__init__()
        self.ADMINPASSWORD = b"gAAAAABe9gx0ty_p1Mk_Lnvgt1c3aToBJkaYI1LOj0diqCkTtlMMXhk3IHvd7sNo4GA455T2eOFw2fR-0u17CaXgKvCVpCzmXA=="

    def check_admin_password(self, user_password):
        """Checks if the password entered by user is correct."""

        user_password = user_password.strip()
        decrypted_admin_password = self.cryptor.decrypt(self.ADMINPASSWORD).decode(PasswordCryptography.ENCODING)

        if user_password == decrypted_admin_password:
            return True

        return False

    def main(self):

        user_password = input("\nEnter the admin password\n>>>")

        if user_password.strip() == "q":
            exit()

        user_verified = self.check_admin_password(user_password)

        if user_verified:
            print("\nEnter the requirement number.")
            user_need = input("What do you wish to do\n\n1) Write New Password\n2) Update Password\n3) Remove Password\n4) Get Password\n\n>>>").strip()

            if user_need == "q":
                exit()

            if not user_need.isdigit():
                print("\nCould Not Understand.")
                print("Please Try Again.")
                self.main()
                exit()

            service = input("\nEnter the website/app of the password\n>>>")
            if service.lower().strip() == "q":
                exit()

            if user_need == "1":
                duplicate_status = self.check_duplicate_service(service)

                if not duplicate_status:

                    password = input("\nEnter the new password\n>>>")
                    if password.strip() == "q":
                        exit()
                    self.write_password(service, password)
                    print("\nWritten New Password")

                else:
                    print("\nFound same service.")
                    user_update_status = input("\nWould you like to update the password\n\n1) Yes\n2) No\n\n>>>").strip()

                    if user_update_status == "1":
                        password = input("\nEnter the new password\n>>>")
                        if password.strip() == "q":
                            exit()
                        self.update_password(service, password)
                        print("\nUpdated Password")

                    elif user_update_status == "2":
                        exit()

                    else:
                        print("\nCould Not Understand.")
                        print("Please Try Again.")
                        self.main()

            elif user_need == "2":
                duplicate_status = self.check_duplicate_service(service)

                if duplicate_status:
                    password = input("\nEnter the new password\n>>>")
                    if password.strip() == "q":
                        exit()
                    self.update_password(service, password)
                    print("\nUpdated Password")

                else:
                    print(f"\nCould not find website/app '{service}'.")
                    user_write_new_status = input(f"\nWould you like to create a new password for the website/app '{service}'\n\n1) Yes\n2) No\n\n>>>").strip()

                    if user_write_new_status.lower() == "q":
                        exit()

                    elif user_write_new_status == "1":
                        password = input("\nEnter the new password\n>>>")
                        if password.strip() == "q":
                            exit()
                        self.write_password(service, password)

                    else:
                        exit()

            elif user_need == "3":
                duplicate_status = self.check_duplicate_service(service)

                if duplicate_status:
                    self.remove_password(service)
                    print("\nRemoved Password")

                else:
                    print(f"\nCould not find website/app '{service}'.")

            elif user_need == "4":
                duplicate_status = self.check_duplicate_service(service)

                if duplicate_status:
                    password = self.get_password(service)
                    print(f"\nPassword: {password}")
                else:
                    print(f"\nCould not find website/app '{service}'.")

            else:
                print("\nCould Not Understand.")
                print("Please Try Again.")
                self.main()

        else:
            print("\nIncorrect Password")


if __name__ == "__main__":
    Chatbot = Interface()
    print("Type 'q' to quit at any time.")
    Chatbot.main()
