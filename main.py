from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from frontend.login_screen import LoginScreenUI
from frontend.home_screen import HomeScreenUI
from frontend.create_case import CreateCaseScreenUI

class LoginApp(MDApp):

    def build(self):

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        screen_manager = ScreenManager()

        screen_manager.add_widget(LoginScreenUI())
        screen_manager.add_widget(HomeScreenUI())
        screen_manager.add_widget(CreateCaseScreenUI())

        return screen_manager

if __name__ == "__main__":
    LoginApp().run()