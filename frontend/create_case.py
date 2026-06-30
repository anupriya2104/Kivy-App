from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu

from kivy.metrics import dp

from backend.create_case import CreateCaseScreen


class CreateCaseScreenUI(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = "create_case"

        self.backend = CreateCaseScreen()

        self.BuildUI()

    def BuildUI(self):

        box_width = dp(100)
        box_height = dp(55)

        root = MDBoxLayout(
            orientation="vertical"
        )

        root.add_widget(MDLabel())

        # =====================================================
        # CENTER BLOCK
        # =====================================================

        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            adaptive_height=True,
            size_hint=(None, None),
            width=dp(600),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.5,
            },
        )

        # =====================================================
        # TITLE
        # =====================================================

        title = MDLabel(
            text="Create New Case",
            halign="center",
            font_style="H3",
            bold=True,
            size_hint_y=None,
            height=dp(60),
        )

        content.add_widget(title)

        # =====================================================
        # CASE NUMBER LABEL
        # =====================================================

        case_label = MDLabel(
            text="CASE NUMBER",
            halign="center",
            font_style="H6",
            bold=True,
            theme_text_color="Custom",
            text_color=(0.1, 0.45, 0.8, 1),
            size_hint_y=None,
            height=dp(35),
        )

        content.add_widget(case_label)

        # =====================================================
        # CASE NUMBER ROW
        # =====================================================

        case_row = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            adaptive_width=True,
            size_hint_y=None,
            height=box_height,
            pos_hint={"center_x": 0.5},
        )

        prefix_button = MDRaisedButton(
            text=self.backend.GetPrefix(),
            size_hint=(None, None),
            size=(box_width, box_height),
            md_bg_color=(0.20, 0.60, 0.95, 1),
        )



    # =====================================================
    # BUSINESS
    # =====================================================

    def SetBusiness(self, value):

        self.backend.SetBusiness(value)
        self.business_button.text = value
        self.business_menu.dismiss()
        self.UpdateCaseNumber()

    # =====================================================
    # YEAR
    # =====================================================

    def SetYear(self, value):

        self.backend.SetYear(value)
        self.year_button.text = value
        self.year_menu.dismiss()
        self.UpdateCaseNumber()

    # =====================================================
    # UPDATE CASE NUMBER
    # =====================================================

    def UpdateCaseNumber(self, *args):

        serial = self.serial_field.text
        self.backend.SetSerial(serial)
        self.case_number_label.text = self.backend.GetCaseNumber()

    # =====================================================
    # BACK
    # =====================================================

    def GoBack(self, *args):

        self.manager.current = "home"
