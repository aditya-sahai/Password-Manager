from cryptography.fernet import Fernet
import json


class PasswordCryptography:
    ENCODING = "UTF-8"
    def __init__(self):
        self.PASSWORD_FILE_NAME = "passwords.json"

        with open(self.PASSWORD_FILE_NAME, "r") as password_file:
            self.password_data = json.load(password_file)

        self.KEY = self.password_data["key"].encode(PasswordCryptography.ENCODING)
        self.cryptor = Fernet(self.KEY)

    def write_password_data(self):
        """Writes the password data to the json file."""

        with open(self.PASSWORD_FILE_NAME, "w") as password_file:
            json.dump(self.password_data, password_file, indent=4)

    def check_duplicate_service(self, required_service):
        """Checks if the service already exists."""

        required_service = required_service.lower().strip().encode(PasswordCryptography.ENCODING)

        for password in self.password_data["passwords"]:
            service = password["service"].encode(PasswordCryptography.ENCODING)
            service = self.cryptor.decrypt(service)

            if required_service == service:
                return True

        return False

    def write_password(self, service, password):
        """Uses json and writes the service and password."""

        service = service.lower().strip().encode(PasswordCryptography.ENCODING)
        password = password.strip().encode(PasswordCryptography.ENCODING)

        encrypted_service = self.cryptor.encrypt(service).decode(PasswordCryptography.ENCODING)
        encrypted_password = self.cryptor.encrypt(password).decode(PasswordCryptography.ENCODING)

        self.password_data["passwords"].append({
            "service": encrypted_service,
            "password": encrypted_password,
        })

        self.write_password_data()

    def get_password(self, required_service):
        """Returns a string of the password of the given service."""

        required_service = required_service.lower().strip().encode(PasswordCryptography.ENCODING)

        for password in self.password_data["passwords"]:
            service = password["service"].encode(PasswordCryptography.ENCODING)
            service = self.cryptor.decrypt(service)

            if required_service == service:
                password_string = self.cryptor.decrypt(password["password"].encode(PasswordCryptography.ENCODING)).decode(PasswordCryptography.ENCODING)
                return password_string

        return None

    def update_password(self, required_service, new_password):
        """Updates the password."""

        required_service = required_service.lower().strip().encode(PasswordCryptography.ENCODING)

        for password_num, password in enumerate(self.password_data["passwords"]):
            service = password["service"].encode(PasswordCryptography.ENCODING)
            service = self.cryptor.decrypt(service)

            if service == required_service:
                new_password = self.cryptor.encrypt(new_password.encode(PasswordCryptography.ENCODING))
                self.password_data["passwords"][password_num]["password"] = new_password.decode(PasswordCryptography.ENCODING)
                self.write_password_data()
                break

    def remove_password(self, required_service):
        """Removes the password of the given service."""

        required_service = required_service.lower().strip().encode(PasswordCryptography.ENCODING)

        for password_num, password in enumerate(self.password_data["passwords"]):
            service = password["service"].encode(PasswordCryptography.ENCODING)
            service = self.cryptor.decrypt(service)

            if service == required_service:

                del self.password_data["passwords"][password_num]
                self.write_password_data()
                break


if __name__ == "__main__":
    Manager = PasswordCryptography()
