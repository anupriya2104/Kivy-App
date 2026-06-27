from datetime import datetime

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu

from kivy.metrics import dp


class CreateNewCaseScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = "create_case"

        self.business_value = "01"
        self.year_value = str(datetime.now().year)[-2:]

        self.build_ui()

    def build_ui(self):

        BOX_WIDTH = dp(100)
        BOX_HEIGHT = dp(55)

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
            height=BOX_HEIGHT,
            pos_hint={"center_x": 0.5},
        )

        prefix_btn = MDRaisedButton(
            text="06",
            size_hint=(None, None),
            size=(BOX_WIDTH, BOX_HEIGHT),
            md_bg_color=(0.20, 0.60, 0.95, 1),
        )

        # =====================================================
        # BUSINESS DROPDOWN
        # =====================================================

        self.business_btn = MDRaisedButton(
            text=self.business_value,
            size_hint=(None, None),
            size=(BOX_WIDTH, BOX_HEIGHT),
        )

        business_items = []

        for i in range(1, 8):

            value = f"{i:02}"

            business_items.append(
                {
                    "text": value,
                    "on_release": lambda x=value:
                    self.set_business(x)
                }
            )

        self.business_menu = MDDropdownMenu(
            caller=self.business_btn,
            items=business_items,
            width_mult=3,
        )

        self.business_btn.bind(
            on_release=lambda x:
            self.business_menu.open()
        )

        # =====================================================
        # YEAR DROPDOWN
        # =====================================================

        self.year_btn = MDRaisedButton(
            text=self.year_value,
            size_hint=(None, None),
            size=(BOX_WIDTH, BOX_HEIGHT),
        )

        year_items = []

        current_year = datetime.now().year

        for year in range(
            current_year -1,
            current_year +2,
        ):                          

            value = str(year)[-2:]

            year_items.append(
                {
                    "text": value,
                    "on_release": lambda x=value:
                    self.set_year(x)
                }
            )

        self.year_menu = MDDropdownMenu(
            caller=self.year_btn,
            items=year_items,
            width_mult=3,
        )

        self.year_btn.bind(
            on_release=lambda x:
            self.year_menu.open()
        )

        # =====================================================
        # SERIAL NUMBER
        # =====================================================

        self.serial_field = MDTextField(
            text="0018",
            mode="rectangle",
            size_hint=(None, None),
            size=(BOX_WIDTH, BOX_HEIGHT),
        )

        self.serial_field.bind(
            text=self.update_case_number
        )

        case_row.add_widget(prefix_btn)
        case_row.add_widget(self.business_btn)
        case_row.add_widget(self.year_btn)
        case_row.add_widget(self.serial_field)

        content.add_widget(case_row)

        # =====================================================
        # GENERATED NUMBER
        # =====================================================

        self.case_number_label = MDLabel(
            text="",
            halign="center",
            bold=True,
            font_style="H4",
            theme_text_color="Custom",
            text_color=(0.15, 0.15, 0.15, 1),
            size_hint_y=None,
            height=dp(60),
        )

        content.add_widget(self.case_number_label)

        self.update_case_number()

        # =====================================================
        # BUTTONS
        # =====================================================

        button_row = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(15),
            adaptive_width=True,
            size_hint_y=None,
            height=dp(55),
            pos_hint={"center_x": 0.5},
        )

        back_btn = MDRaisedButton(
            text="BACK",
            size_hint=(None, None),
            size=(dp(120), dp(45)),
        )

        back_btn.bind(
            on_release=self.go_back
        )

        create_btn = MDRaisedButton(
            text="CREATE CASE",
            size_hint=(None, None),
            size=(dp(180), dp(45)),
        )

        button_row.add_widget(back_btn)
        button_row.add_widget(create_btn)

        content.add_widget(button_row)

        root.add_widget(content)

        root.add_widget(MDLabel())

        self.add_widget(root)

    # =====================================================
    # BUSINESS
    # =====================================================

    def set_business(self, value):

        self.business_value = value
        self.business_btn.text = value

        self.business_menu.dismiss()

        self.update_case_number()

    # =====================================================
    # YEAR
    # =====================================================

    def set_year(self, value):

        self.year_value = value
        self.year_btn.text = value

        self.year_menu.dismiss()

        self.update_case_number()

    # =====================================================
    # UPDATE CASE NUMBER
    # =====================================================

    def update_case_number(self, *args):

        self.case_number_label.text = (
            f"06"
            f"{self.business_value}"
            f"{self.year_value}"
            f"{self.serial_field.text}"
        )

    # =====================================================
    # BACK
    # =====================================================

    def go_back(self, *args):

        self.manager.current = "home"