from backend.home_screen import HomeScreen as HomeScreenBackend

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.metrics import dp


def MakeGradientTexture(Width, Height, TopColor, BottomColor):

    texture_object = Texture.create(
        size=(Width, Height),
        colorfmt="rgb",
    )

    pixels = []

    for row in range(Height):

        T = row / max(Height - 1, 1)

        R = int(
            (
                TopColor[0] * T
                + BottomColor[0] * (1 - T)
            ) * 255
        )

        G = int(
            (
                TopColor[1] * T
                + BottomColor[1] * (1 - T)
            ) * 255
        )

        B = int(
            (
                TopColor[2] * T
                + BottomColor[2] * (1 - T)
            ) * 255
        )

        pixels.extend([R, G, B] * Width)

    texture_object.blit_buffer(
        bytes(pixels),
        colorfmt="rgb",
        bufferfmt="ubyte",
    )

    return texture_object


class HomeScreenUI(MDScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.name = "home"

        # Backend Object
        self.ui_data = HomeScreenBackend()

        self.CreateUIElements()

    # =====================================================
    # CREATE UI
    # =====================================================

    def CreateUIElements(self):

        with self.canvas.before:

            self.BackgroundRectangle = Rectangle(
                size=self.size,
                pos=self.pos,
            )

        self.bind(
            size=self.UpdateBackground,
            pos=self.UpdateBackground,
        )

        self.DrawGradient()

        root = MDBoxLayout(
            orientation="vertical",
        )

        root.add_widget(
            MDLabel()
        )

        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            adaptive_height=True,
            size_hint=(None, None),
            width=dp(400),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.5,
            },
        )

        title = MDLabel(
            text="Dashboard",
            halign="center",
            bold=True,
            font_style="H3",
            size_hint_y=None,
            height=dp(70),
        )

        subtitle = MDLabel(
            text="Welcome Back",
            halign="center",
            bold=True,
            font_style="H5",
            size_hint_y=None,
            height=dp(40),
        )

        description = MDLabel(
            text="Manage your case data and assigned tasks.",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(30),
        )

        content.add_widget(title)
        content.add_widget(subtitle)
        content.add_widget(description)

        content.add_widget(
            MDBoxLayout(
                size_hint_y=None,
                height=dp(15),
            )
        )

        button_width = dp(350)
        button_height = dp(60)

        for label in self.ui_data.GetButtons():

            button = MDRaisedButton(
                text=label,
                size_hint=(None, None),
                size=(dp(360), dp(60)),
                pos_hint={"center_x": 0.5},
            )

            button.bind(
                on_release=lambda instance, value=label:
                self.OnButtonClick(value)
            )

            content.add_widget(button)

        root.add_widget(content)

        root.add_widget(
            MDLabel()
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

        pass

        # =====================================================
    # DRAW GRADIENT
    # =====================================================

    def DrawGradient(self):

        Width = max(int(self.width), 1)
        Height = max(int(self.height), 1)

        texture_object = MakeGradientTexture(
            Width,
            Height,
            TopColor=(0.99, 0.99, 1.00),
            BottomColor=(0.95, 0.96, 0.98),
        )

        self.BackgroundRectangle.texture = texture_object
        self.BackgroundRectangle.size = self.size
        self.BackgroundRectangle.pos = self.pos

    # =====================================================
    # UPDATE BACKGROUND
    # =====================================================

    def UpdateBackground(self, *args):

        self.DrawGradient()

    # =====================================================
    # BUTTON CLICK
    # =====================================================

    def OnButtonClick(self, label):

        self.ui_data.SetSelectedButton(label)

        if self.ui_data.GetSelectedButton() == "Create New Case":

            self.manager.current = "create_case"

        else:

            MDDialog(
                title=self.ui_data.GetSelectedButton(),
                text=f"{self.ui_data.GetSelectedButton()} page will be implemented soon.",
            ).open()
            
    # =====================================================
    # GO BACK TO LOGIN
    # =====================================================

    def GoBackToLogin(self, *args):

        self.manager.current = "login"