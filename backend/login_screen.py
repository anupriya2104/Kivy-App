from datetime import datetime

class LoginScreen:

    def __init__(self):

        self.username = ""   #var in snake case
        self.password = ""

        # Hardcoded credentials
        self.valid_username = "admin"
        self.valid_password = "password123"

        self.is_authenticated = False
        self.failed_attempts = 0

        self.last_login = None
        self.error_message = ""

    # ===========================================
    # SETTERS
    # ===========================================

    def SetUsername(self, username):

        self.username = username.strip()

    def SetPassword(self, password):

        self.password = password

    # ===========================================
    # GETTERS
    # ===========================================

    def GetUsername(self):

        return self.username

    def GetPassword(self):

        return self.password

    def GetErrorMessage(self):

        return self.error_message

    # ===========================================
    # AUTHENTICATE
    # ===========================================

    def Authenticate(self):

        if (
            self.username == self.valid_username
            and
            self.password == self.valid_password
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

    # ===========================================
    # RESET
    # ===========================================

    def Reset(self):

        self.username = ""
        self.password = ""