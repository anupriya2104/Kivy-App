from datetime import datetime

class CreateCaseScreen:

    def __init__(self):

        self.prefix = "06"

        self.business_value = "01"

        self.year_value = str(
            datetime.now().year
        )[-2:]

        self.serial_number = "0018"

    # =====================================================
    # PREFIX
    # =====================================================

    def SetPrefix(self, prefix):

        self.prefix = prefix

    def GetPrefix(self):

        return self.prefix

    # =====================================================
    # BUSINESS
    # =====================================================

    def SetBusiness(self, Business):

        self.business_value = Business

    def GetBusiness(self):

        return self.business_value

    # =====================================================
    # YEAR
    # =====================================================

    def SetYear(self, Year):

        self.year_value = Year

    def GetYear(self):

        return self.year_value

    # =====================================================
    # SERIAL
    # =====================================================

    def SetSerial(self, Serial):

        self.serial_number = Serial

    def GetSerial(self):

        return self.serial_number

    # =====================================================
    # CASE NUMBER
    # =====================================================

    def GetCaseNumber(self):

        return (
            f"{self.prefix}"
            f"{self.business_value}"
            f"{self.year_value}"
            f"{self.serial_number}"
        )

    # =====================================================
    # BUSINESS VALUES
    # =====================================================

    def GetBusinessValues(self):

        values = []

        for Number in range(1, 7):

            values.append(
                f"{Number:02}"
            )

        return values

    # =====================================================
    # YEAR VALUES
    # =====================================================

    def GetYearValues(self):

        current_year = datetime.now().year

        values = []

        for Year in range(
            current_year - 1,
            current_year + 2,
        ):

            values.append(
                str(Year)[-2:]
            )

        return values

    # =====================================================
    # RESET
    # =====================================================

    def Reset(self):

        self.business_value = "01"

        self.year_value = str(
            datetime.now().year
        )[-2:]

        self.serial_number = "0018"