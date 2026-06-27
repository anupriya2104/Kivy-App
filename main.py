from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from login_screen import LoginScreen
from home_screen import HomeScreen
from create_case import CreateNewCaseScreen


class LoginApp(MDApp):

    def build(self):

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        sm = ScreenManager()

        sm.add_widget(LoginScreen())
        sm.add_widget(HomeScreen())
        sm.add_widget(CreateNewCaseScreen())

        return sm


if __name__ == "__main__":
    LoginApp().run()