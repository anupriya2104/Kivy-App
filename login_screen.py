from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDTextButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDCheckbox

from kivy.uix.image import Image
from kivy.metrics import dp


VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"


class LoginScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = "login"

        self.build_ui()

    def build_ui(self):

        root = MDBoxLayout(
            orientation="vertical",
            padding=[dp(40), dp(60), dp(40), dp(60)],
            spacing=dp(14),
        )

        # Top spacer
        root.add_widget(MDLabel(size_hint_y=0.3))

        # Logo
        logo = Image(
        source="resources/logo.png",
        size_hint=(None, None),
        size=(dp(100), dp(100)),
        pos_hint={"center_x": 0.5},
)

        # Title
        title = MDLabel(
            text="My Application",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height=dp(50),
        )

        # Subtitle
        subtitle = MDLabel(
            text="Welcome back",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(25),
        )

        # Username
        self.username = MDTextField(
            hint_text="Username",
            mode="rectangle",
            size_hint_x=1,
        )

        # Password
        self.password = MDTextField(
            hint_text="Password",
            password=True,
            mode="rectangle",
            size_hint_x=1,
        )

        # Show Password Row
        show_pw_row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(36),
            spacing=dp(6),
        )

        self.show_pw_checkbox = MDCheckbox(
            size_hint=(None, None),
            size=(dp(32), dp(32)),
        )

        self.show_pw_checkbox.bind(
            active=self.toggle_password
        )

        show_pw_label = MDLabel(
            text="Show password",
            size_hint_x=None,
            width=dp(120),
        )

        show_pw_label.bind(
            on_touch_down=self.label_tap_toggle
        )

        # LEFT aligned
        show_pw_row.add_widget(self.show_pw_checkbox)
        show_pw_row.add_widget(show_pw_label)
        show_pw_row.add_widget(MDLabel())

        # Login Button
        login_btn = MDRaisedButton(
            text="LOG IN",
            size_hint_x=1,
            height=dp(55),
        )

        login_btn.bind(
            on_release=self.login
        )

        # Forgot Password
        forgot_btn = MDTextButton(
            text="Forgot password?",
            pos_hint={"center_x": 0.5},
        )

        forgot_btn.bind(
            on_release=self.forgot_password
        )

        root.add_widget(logo)
        root.add_widget(title)
        root.add_widget(subtitle)

        root.add_widget(
            MDBoxLayout(
                size_hint_y=None,
                height=dp(10),
            )
        )

        root.add_widget(self.username)
        root.add_widget(self.password)
        root.add_widget(show_pw_row)

        root.add_widget(
            MDBoxLayout(
                size_hint_y=None,
                height=dp(10),
            )
        )

        root.add_widget(login_btn)
        root.add_widget(forgot_btn)

        # Bottom spacer
        root.add_widget(MDLabel(size_hint_y=0.4))

        self.add_widget(root)

    def toggle_password(self, instance, value):
        self.password.password = not value

    def label_tap_toggle(self, instance, touch):

        if instance.collide_point(*touch.pos):

            self.show_pw_checkbox.active = (
                not self.show_pw_checkbox.active
            )

            return True

        return False

    def login(self, *args):

        if (
            self.username.text == VALID_USERNAME
            and self.password.text == VALID_PASSWORD
        ):

            self.username.text = ""
            self.password.text = ""

            self.manager.current = "home"

        else:

            MDDialog(
                title="Error",
                text="Invalid username or password.",
            ).open()

    def forgot_password(self, *args):

        MDDialog(
            title="Forgot Password",
            text="Password reset will be implemented later.",
        ).open()

