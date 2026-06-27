from datetime import datetime

class CreateCaseScreen:

    def __init__(self):

        self.prefix = "06"

        self.business_value = "01"

        self.year_value = str(
            datetime.now().year
        )[-2:]

        self.serial_number = "0018"

    def SetBusiness(self, value):

        self.business_value = value

    def SetYear(self, value):

        self.year_value = value

    def SetSerial(self, value):

        self.serial_number = value

    def GetCaseNumber(self):

        return (
            f"{self.prefix}"
            f"{self.business_value}"
            f"{self.year_value}"
            f"{self.serial_number}"
        )

    def GetBusinessValues(self):

        return [
            f"{i:02}"
            for i in range(1, 8)
        ]

    def GetYearValues(self):

        current_year = datetime.now().year

        return [
            str(year)[-2:]
            for year in range(
                current_year - 1,
                current_year + 2
            )
        ]