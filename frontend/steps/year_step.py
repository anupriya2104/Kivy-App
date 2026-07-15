from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from kivy.metrics import dp

from frontend.year_wheel import YearWheel


class YearStep(MDBoxLayout):
    """
    Step 2 of Create Case.

    Allows the user to select the case year
    using the YearWheel widget.
    """

    def __init__(self, Backend, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"

        self.backend = Backend

        self.BuildUI()

    # ---------------------------------------------------------

    def BuildUI(self):

        title = MDLabel(
            text="Select Year",
            halign="center",
            bold=True,
            size_hint_y=None,
            height=dp(40),
        )

        self.add_widget(title)

        year_options = self.backend.GetYearOptions()

        current_year = self.backend.GetYear()

        if current_year in year_options:
            initial_index = year_options.index(current_year)
        else:
            initial_index = 1

        wheel_container = MDBoxLayout(
            size_hint_y=None,
            height=dp(180),
            padding=[dp(100), 0, dp(100), 0],
        )

        self.year_wheel = YearWheel(
            YearOptions=year_options,
            InitialIndex=initial_index,
            OnYearSelected=self.OnYearSelected,
            size_hint_y=None,
            height=dp(180),
        )

        wheel_container.add_widget(self.year_wheel)

        self.add_widget(wheel_container)

    # ---------------------------------------------------------

    def OnYearSelected(self, selected_year):

        self.backend.SetYear(selected_year)