class HomeScreen:

    def __init__(self):

        self.buttons = [
            "      Create New Case    ",
            "Edit Existing Case Data",
            " Show Assigned Tasks ",
            "         View Reports        ",
            "             Settings             ",
        ]

        self.selected_button = ""

    # =====================================================
    # GET BUTTONS
    # =====================================================

    def GetButtons(self):

        return self.buttons

    # =====================================================
    # SET SELECTED BUTTON
    # =====================================================

    def SetSelectedButton(self, ButtonName):

        self.selected_button = ButtonName

    # =====================================================
    # GET SELECTED BUTTON
    # =====================================================

    def GetSelectedButton(self):

        return self.selected_button