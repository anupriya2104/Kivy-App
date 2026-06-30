from backend.login_screen import LoginScreen as LoginScreenBackend

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDTextButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDCheckbox

from kivy.uix.image import Image
from kivy.metrics import dp


class LoginScreenUI(MDScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.name = "login"

        # Backend Object
        self.ui_data = LoginScreenBackend()

        self.CreateUIElements()

    # =====================================================
    # CREATE UI
    # =====================================================

    def CreateUIElements(self):

        root = MDBoxLayout(
            orientation="vertical",
            padding=[dp(40), dp(60), dp(40), dp(60)],
            spacing=dp(14),
        )

        root.add_widget(
            MDLabel(
                size_hint_y=0.3
            )
        )

        logo = Image(
            source="resources/logo.png",
            size_hint=(None, None),
            size=(dp(100), dp(100)),
            pos_hint={
                "center_x": 0.5
            },
        )

        title = MDLabel(
            text="My Application",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height=dp(50),
        )

        subtitle = MDLabel(
            text="Welcome back",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(25),
        )

        self.username = MDTextField(
            hint_text="username",
            mode="rectangle",
            size_hint_x=1,
        )

        self.password = MDTextField(
            hint_text="password",
            password=True,
            mode="rectangle",
            size_hint_x=1,
        )

        show_password_row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(36),
            spacing=dp(6),
        )

        self.ShowPasswordCheckBox = MDCheckbox(
            size_hint=(None, None),
            size=(dp(32), dp(32)),
        )

        self.ShowPasswordCheckBox.bind(
            active=self.TogglePassword
        )

        show_password_label = MDLabel(
            text="Show password",
            size_hint_x=None,
            width=dp(120),
        )

        show_password_label.bind(
            on_touch_down=self.LabelTapToggle
        )

        show_password_row.add_widget(
            self.ShowPasswordCheckBox
        )

        show_password_row.add_widget(
            show_password_label
        )

        show_password_row.add_widget(
            MDLabel()
        )

        login_button = MDRaisedButton(
            text="LOG IN",
            size_hint_x=1,
            height=dp(55),
        )

        login_button.bind(
            on_release=self.Login
        )

        forgot_password_button = MDTextButton(
            text="Forgot password?",
            pos_hint={
                "center_x": 0.5
            },
        )

        forgot_password_button.bind(
            on_release=self.ForgotPassword
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
        root.add_widget(show_password_row)

        root.add_widget(
            MDBoxLayout(
                size_hint_y=None,
                height=dp(10),
            )
        )

        root.add_widget(login_button)
        root.add_widget(forgot_password_button)

        root.add_widget(
            MDLabel(
                size_hint_y=0.4
            )
        )

        self.add_widget(root)

    # =====================================================
    # DISPLAY
    # =====================================================

    def Display(self, Visible):

        self.opacity = 1 if Visible else 0

        self.disabled = not Visible

    # =====================================================
    # FILL FROM BACKEND
    # =====================================================

    def FillFromBackend(self):

        self.username.text = self.ui_data.username

        self.password.text = self.ui_data.password

        # =====================================================
    # TOGGLE PASSWORD
    # =====================================================

    def TogglePassword(self, instance, value):

        self.password.password = not value

    # =====================================================
    # LABEL TAP
    # =====================================================

    def LabelTapToggle(self, instance, touch):

        if instance.collide_point(*touch.pos):

            self.ShowPasswordCheckBox.active = (
                not self.ShowPasswordCheckBox.active
            )

            return True

        return False

    # =====================================================
    # LOGIN
    # =====================================================

    def Login(self, *args):

        # Copy values from UI to Backend
        self.ui_data.SetUsername(
            self.username.text
        )

        self.ui_data.SetPassword(
            self.password.text
        )

        # Authenticate using Backend
        if self.ui_data.Authenticate():
            self.ui_data.Reset()

            self.FillFromBackend()

            self.manager.current = "home"

        else:

            MDDialog(
                title="Error",
                text=self.ui_data.error_message,
            ).open()

    # =====================================================
    # FORGOT PASSWORD
    # =====================================================

    def ForgotPassword(self, *args):

        MDDialog(
            title="Forgot password",
            text="password reset will be implemented later.",
        ).open()