from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog

from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.metrics import dp


BUTTONS = [
    {"label": "      Create New Case     "},
    {"label": "Edit Existing Case Data"},
    {"label": " Show Assigned Tasks "},
    {"label": "         View Reports        "},
    {"label": "             Settings             "},
]


def MakeGradientTexture(width, height, top_color, bottom_color):

    texture = Texture.create(
        size=(width, height),
        colorfmt="rgb",
    )

    pixels = []

    for row in range(height):

        t = row / max(height - 1, 1)

        r = int(
            (top_color[0] * t +
             bottom_color[0] * (1 - t))
            * 255
        )

        g = int(
            (top_color[1] * t +
             bottom_color[1] * (1 - t))
            * 255
        )

        b = int(
            (top_color[2] * t +
             bottom_color[2] * (1 - t))
            * 255
        )

        pixels.extend([r, g, b] * width)

    texture.blit_buffer(
        bytes(pixels),
        colorfmt="rgb",
        bufferfmt="ubyte",
    )

    return texture


class HomeScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = "home"

        self.build_ui()

    # ==================================================
    # UI
    # ==================================================

    def BuildUI(self):

        with self.canvas.before:

            self._bg_rect = Rectangle(
                size=self.size,
                pos=self.pos,
            )

        self.bind(
            size=self._update_bg,
            pos=self._update_bg,
        )

        self._draw_gradient()

        root = MDBoxLayout(
            orientation="vertical",
        )

        root.add_widget(MDLabel())

        # ==============================
        # CENTER CONTENT
        # ==============================

        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            adaptive_height=True,
            size_hint=(None, None),
            width=dp(600),
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

        # ==============================
        # BUTTONS
        # ==============================

        BUTTON_WIDTH = dp(350)
        BUTTON_HEIGHT = dp(60)

        for item in BUTTONS:

            row = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=BUTTON_HEIGHT,
            )

            row.add_widget(MDLabel())

            btn = MDRaisedButton(
                text=item["label"],
                size_hint=(None, None),
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
            )

            btn.bind(
                on_release=lambda inst,
                l=item["label"]:
                self.on_button_click(l)
            )

            row.add_widget(btn)

            row.add_widget(MDLabel())

            content.add_widget(row)

        content.add_widget(
            MDBoxLayout(
                size_hint_y=None,
                height=dp(20),
            )
        )

        # ==============================
        # LOGOUT BUTTON
        # ==============================

        # logout_row = MDBoxLayout(
        #     orientation="horizontal",
        #     size_hint_y=None,
        #     height=dp(50),
        # )

        # logout_row.add_widget(MDLabel())

        # logout_btn = MDIconButton(
        #     icon="logout",
        # )

        # logout_btn.bind(
        #     on_release=self.go_back_to_login
        # )

        # logout_row.add_widget(logout_btn)

        # logout_row.add_widget(MDLabel())

        # content.add_widget(logout_row)

        # root.add_widget(content)

        # root.add_widget(MDLabel())

        # self.add_widget(root)

    # ==================================================
    # BACKGROUND
    # ==================================================

    def DrawGradient(self):

        w = max(int(self.width), 1)
        h = max(int(self.height), 1)

        texture = MakeGradientTexture(
            w,
            h,
            top_color=(0.99, 0.99, 1.00),
            bottom_color=(0.95, 0.96, 0.98),
        )

        self._bg_rect.texture = texture
        self._bg_rect.size = self.size
        self._bg_rect.pos = self.pos

    def UpdateBG(self, *args):
        self._draw_gradient()

    # ==================================================
    # EVENTS
    # ==================================================

    def OnButtonClick(self, label):

        if label.strip() == "Create New Case":

            self.manager.current = "create_case"

        else:

            MDDialog(
                title=label,
                text=f"{label} page will be implemented soon.",
            ).open()

    def GoBackToLogin(self, *args):

        self.manager.current = "login"