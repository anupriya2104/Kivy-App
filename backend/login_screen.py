from datetime import datetime

class LoginScreen:

    def __init__(self):

        self.username = ""
        self.password = ""

        self.remember_me = False
        self.is_authenticated = False
        self.failed_attempts = 0

        self.last_login = None
        self.error_message = ""

    def SetUsername(self, username):
        self.username = username.strip()

    def SetPassword(self, password):
        self.password = password

    def Authenticate(self, valid_username, valid_password):

        if (
            self.username == valid_username
            and self.password == valid_password
        ):

            self.is_authenticated = True
            self.failed_attempts = 0
            self.last_login = datetime.now()
            self.error_message = ""

            return True

        self.is_authenticated = False
        self.failed_attempts += 1
        self.error_message = "Invalid username or password."

        return False