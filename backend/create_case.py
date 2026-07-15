from datetime import datetime


class CreateCaseScreen:
    """
    Backend for Create Case Screen.

    Responsibilities
    ----------------
    • Store case information.
    • Validate user input.
    • Generate the final case number.
    • Reset the form.
    """

    PREFIX = "06"
    DEPARTMENT_COUNT = 5

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self):

        print("CreateCaseScreen Backend Initialized")

        self.Reset()

    # =====================================================
    # RESET
    # =====================================================

    def Reset(self):
        """
        Reset all case information.
        """

        self.department_code = None

        self.year_value = self.GetCurrentYear()

        self.serial_raw = ""

    # =====================================================
    # CURRENT YEAR
    # =====================================================

    def GetCurrentYear(self):
        """
        Returns current year in two-digit format.
        Example:
            2026 -> "26"
        """

        return str(datetime.now().year)[-2:]

    # =====================================================
    # DEPARTMENT
    # =====================================================

    def GetDepartmentOptions(self):
        """
        Returns available department codes.

        Example:
            ['01','02','03','04','05']
        """

        return [

            f"{number:02}"

            for number in range(
                1,
                self.DEPARTMENT_COUNT + 1
            )

        ]

    # -----------------------------------------------------

    def SetDepartment(
        self,
        department_code,
    ):

        self.department_code = department_code

    # -----------------------------------------------------

    def GetDepartment(self):

        return self.department_code

    # -----------------------------------------------------

    def IsDepartmentSelected(self):

        return self.department_code is not None

    # =====================================================
    # YEAR
    # =====================================================

    def GetYearOptions(self):
        """
        Returns

        Previous Year
        Current Year
        Next Year
        """

        current_year = datetime.now().year

        return [

            str(year)[-2:]

            for year in range(
                current_year - 1,
                current_year + 2,
            )

        ]

    # -----------------------------------------------------

    def SetYear(
        self,
        year_value,
    ):

        self.year_value = year_value

    # -----------------------------------------------------

    def GetYear(self):

        return self.year_value

    # =====================================================
    # SERIAL NUMBER
    # =====================================================

    def SetSerialRaw(
        self,
        serial_number,
    ):
        """
        Store only numeric characters.
        Maximum length = 4 digits.
        """

        digits = "".join(

            character

            for character in serial_number

            if character.isdigit()

        )

        self.serial_raw = digits[:4]

    # -----------------------------------------------------

    def GetSerialRaw(self):

        return self.serial_raw

    # -----------------------------------------------------

    def GetSerialPadded(self):
        """
        Returns serial number
        padded to four digits.
        """

        if not self.serial_raw:

            return "0000"

        return self.serial_raw.zfill(4)

    # -----------------------------------------------------

    def IsSerialValid(self):

        return len(self.serial_raw) > 0

    # =====================================================
    # CASE NUMBER
    # =====================================================

    def GetCaseNumber(self):
        """
        Generates the complete
        10-digit case number.

        Format

        Prefix
        Department
        Year
        Serial

        Example

        0601260023
        """

        return (
            self.PREFIX
            + self.department_code
            + self.year_value
            + self.GetSerialPadded()
        )

    # -----------------------------------------------------

    def GetCasePreview(self):
        """
        Returns preview of the
        case number while typing.
        """

        department = self.department_code

        if department is None:

            department = "--"

        return (
            self.PREFIX
            + department
            + self.year_value
            + self.GetSerialPadded()
        )

    # =====================================================
    # SAVE CASE
    # =====================================================

    def SaveCase(self):
        """
        Save the case.

        Database/File persistence can
        be added here later.

        Returns
        -------
        Generated Case Number
        """

        case_number = self.GetCaseNumber()

        # Future:
        # Insert into database.
        # Write to file.
        # Call API.

        return case_number