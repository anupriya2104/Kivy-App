from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField

from kivy.metrics import dp


class SerialStep(MDBoxLayout):
    """
    Step 3 of Create Case.

    Allows the user to enter the case serial number.
    """

    def __init__(self, Backend, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"

        self.backend = Backend

        self.BuildUI()

    # ---------------------------------------------------------
    # BUILD UI
    # ---------------------------------------------------------

    def BuildUI(self):

        title = MDLabel(
            text="Enter Case Serial Number",
            halign="center",
            bold=True,
            size_hint_y=None,
            height=dp(40),
        )

        self.add_widget(title)

        field_container = MDBoxLayout(
            size_hint_y=None,
            height=dp(60),
            padding=[dp(80), 0, dp(80), 0],
        )

        self.serial_field = MDTextField(
            mode="rectangle",
            input_filter="int",
            halign="center",
            text=self.backend.GetSerialRaw(),
        )

        self.serial_field.bind(
            text=self.OnSerialChanged
        )

        field_container.add_widget(
            self.serial_field
        )

        self.add_widget(field_container)

        # -----------------------------
        # Preview Label
        # (Optional - hidden for now)
        # -----------------------------

        self.preview_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(25),
            opacity=0,          # Keep hidden
        )

        self.add_widget(self.preview_label)

    # ---------------------------------------------------------
    # EVENTS
    # ---------------------------------------------------------

    def OnSerialChanged(self, instance, value):

        self.backend.SetSerialRaw(value)

        # Uncomment later if preview is required

        # self.preview_label.text = self.backend.GetPreviewCaseNumber()