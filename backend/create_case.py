from datetime import datetime

class CreateCaseScreen:

    PREFIX = "06"

    DEPARTMENT_COUNT = 5

    def __init__(self):
        
        print("CreateCaseScreen backend initialized")
        self.department_code = None
        self.year_value = str(datetime.now().year)[-2:]
        self.serial_raw = ""
    

    # =====================================================
    # DEPARTMENT (STEP 1/3)
    # =====================================================

    def GetDepartmentOptions(self):
        """Returns the list of 2-digit department codes, e.g. ['01', ..., '05']."""

        options = []

        for number in range(1, self.DEPARTMENT_COUNT + 1):
            options.append(f"{number:02}")

        return options

    def SetDepartment(self, department_code):

        self.department_code = department_code

    def GetDepartment(self):

        return self.department_code

    def IsDepartmentSelected(self):

        return self.department_code is not None

    # =====================================================
    # YEAR (STEP 2/3)
    # =====================================================

    def GetYearOptions(self):
        """Returns [prev_year, current_year, next_year] as 2-digit strings."""

        current_year = datetime.now().year

        options = []

        for year in range(current_year - 1, current_year + 2):
            options.append(str(year)[-2:])

        return options

    def SetYear(self, year_value):

        self.year_value = year_value

    def GetYear(self):

        return self.year_value

    # =====================================================
    # SERIAL NUMBER (STEP 3/3)
    # =====================================================

    def SetSerialRaw(self, raw_text):
        """Stores raw digit input typed by the user (not yet padded)."""

        digits_only = "".join(
            character for character in raw_text if character.isdigit()
        )

        # Cap at 4 digits since the final field is 4 digits wide
        self.serial_raw = digits_only[:4]

    def GetSerialRaw(self):

        return self.serial_raw

    def GetSerialPadded(self):
        """Returns the serial number zero-padded to 4 digits."""

        if self.serial_raw == "":
            return "0000"

        return self.serial_raw.zfill(4)

    def IsSerialValid(self):

        return len(self.serial_raw) > 0

    # =====================================================
    # FINAL CASE NUMBER
    # =====================================================

    def GetCaseNumber(self):
        """Builds the full hidden 10-digit case number."""

        return (
            f"{self.PREFIX}"
            f"{self.department_code}"
            f"{self.year_value}"
            f"{self.GetSerialPadded()}"
        )

    def SaveCase(self):
        """
        Finalizes the case. Returns the generated case number.
        Persistence (DB / file) can be plugged in here later.
        """

        case_number = self.GetCaseNumber()

        # Placeholder for real persistence — currently just returns the code
        return case_number

    # =====================================================
    # RESET
    # =====================================================

    def Reset(self):

        self.department_code = None
        self.year_value = str(datetime.now().year)[-2:]
        self.serial_raw = ""