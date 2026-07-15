from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton

from kivy.metrics import dp


class DepartmentStep(MDBoxLayout):
    """
    Step 1 of Create Case.

    Displays all available departments and allows
    the user to select one.
    """

    def __init__(self, Backend, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"

        self.backend = Backend

        self.department_buttons = {}

        self.BuildUI()

    # ---------------------------------------------------------

    def BuildUI(self):

        title = MDLabel(
            text="Select Department",
            halign="center",
            bold=True,
            size_hint_y=None,
            height=dp(40),
        )

        self.add_widget(title)

        button_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(260),
        )

        for department_code in self.backend.GetDepartmentOptions():

            button = MDRaisedButton(
                text=f"Department {department_code}",
                size_hint=(None, None),
                width=dp(460),
                height=dp(45),
                pos_hint={"center_x": 0.5},
                md_bg_color=self.GetDepartmentColor(
                    department_code
                ),
            )

            button.bind(
                on_release=lambda instance,
                value=department_code:
                self.SelectDepartment(value)
            )

            self.department_buttons[
                department_code
            ] = button

            button_layout.add_widget(button)

        self.add_widget(button_layout)

    # ---------------------------------------------------------

    def GetDepartmentColor(self, department_code):

        if department_code == self.backend.GetDepartment():

            return (0.05, 0.30, 0.55, 1)

        return (0.20, 0.60, 0.95, 1)

    # ---------------------------------------------------------

    def SelectDepartment(self, department_code):

        self.backend.SetDepartment(department_code)

        self.RefreshButtons()

    # ---------------------------------------------------------

    def RefreshButtons(self):

        for code, button in self.department_buttons.items():

            button.md_bg_color = self.GetDepartmentColor(
                code
            )