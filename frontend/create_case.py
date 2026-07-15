from backend.create_case import CreateCaseScreen as CreateCaseScreenBackend

from frontend.steps.department_step import DepartmentStep
from frontend.steps.year_step import YearStep
from frontend.steps.serial_step import SerialStep

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

from kivy.metrics import dp
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget


class CreateCaseScreenUI(MDScreen):
    """
    Create Case Screen

    Responsibilities
    ----------------
    • Build the overall screen.
    • Switch between steps.
    • Update progress bar.
    • Handle navigation.
    • Display dialogs.
    """

    TOTAL_STEPS = 3

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.name = "create_case"

        self.ui_data = CreateCaseScreenBackend()

        self.current_step = 1

        self.panel_width = dp(500)

        self.CreateUIElements()

    # =====================================================
    # BUILD COMPLETE SCREEN
    # =====================================================

    def CreateUIElements(self):

        self.root_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(30),
            spacing=dp(20),
        )

        self.BuildHeading()

        self.BuildProgressSection()

        self.BuildStepContainer()

        self.BuildNavigationBar()

        self.add_widget(self.root_layout)

        self.RenderStep()

    # =====================================================
    # HEADING
    # =====================================================

    def BuildHeading(self):

        heading = MDLabel(
            text="Create New Case",
            halign="center",
            font_style="H4",
            bold=True,
            size_hint_y=None,
            height=dp(60),
        )

        self.root_layout.add_widget(heading)

    # =====================================================
    # PROGRESS BAR
    # =====================================================

    def BuildProgressSection(self):

        progress_container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(6),
            size_hint=(None, None),
            width=self.panel_width,
            height=dp(80),
            pos_hint={"center_x": 0.5},
        )

        self.progress_bar = ProgressBar(
            max=self.TOTAL_STEPS,
            value=self.current_step,
            size_hint_y=None,
            height=dp(25),
        )

        self.step_label = MDLabel(
            text=self.GetStepText(),
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(20),
        )

        progress_container.add_widget(self.progress_bar)
        progress_container.add_widget(self.step_label)

        self.root_layout.add_widget(progress_container)

    # =====================================================
    # STEP CONTAINER
    # =====================================================

    def BuildStepContainer(self):

        self.step_container = MDBoxLayout(
            orientation="vertical",
            size_hint=(None, 1),
            width=self.panel_width,
            pos_hint={"center_x": 0.5},
        )

        self.root_layout.add_widget(self.step_container)

    # =====================================================
    # NAVIGATION BUTTONS
    # =====================================================

    def BuildNavigationBar(self):

        navigation_bar = MDBoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            width=self.panel_width,
            height=dp(55),
            pos_hint={"center_x": 0.5},
        )

        self.back_button = MDRaisedButton(
            text="Go Back",
            size_hint=(None, None),
            width=dp(150),
            height=dp(50),
        )

        self.back_button.bind(
            on_release=self.OnBackPressed
        )

        self.forward_button = MDRaisedButton(
            text="Continue",
            size_hint=(None, None),
            width=dp(150),
            height=dp(50),
        )

        self.forward_button.bind(
            on_release=self.OnForwardPressed
        )

        navigation_bar.add_widget(self.back_button)

        navigation_bar.add_widget(Widget())

        navigation_bar.add_widget(self.forward_button)

        self.root_layout.add_widget(navigation_bar)

    # =====================================================
    # DISPLAY
    # =====================================================

    def Display(self, Visible):
        """
        Show or hide the screen.
        """

        self.opacity = 1 if Visible else 0
        self.disabled = not Visible

    # =====================================================
    # RESET SCREEN
    # =====================================================

    def FillFromBackend(self):
        """
        Reset the screen whenever it is opened.
        """

        self.current_step = 1
        self.RenderStep()

    # =====================================================
    # STEP INFORMATION
    # =====================================================

    def GetStepText(self):

        return f"Step {self.current_step}/{self.TOTAL_STEPS}"

    # =====================================================
    # UPDATE PROGRESS BAR
    # =====================================================

    def UpdateProgress(self):
        """
        Updates:
        • Progress bar
        • Step label
        • Continue/Create button text
        """

        self.progress_bar.value = self.current_step

        self.step_label.text = self.GetStepText()

        if self.current_step == self.TOTAL_STEPS:

            self.forward_button.text = "Create Case"

        else:

            self.forward_button.text = "Continue"

    # =====================================================
    # STEP RENDERING
    # =====================================================

    def RenderStep(self):
        """
        Clears the current step and loads the
        appropriate step widget.
        """

        self.step_container.clear_widgets()

        self.UpdateProgress()

        if self.current_step == 1:

            department_step = DepartmentStep(
                Backend=self.ui_data
            )

            self.step_container.add_widget(
                department_step
            )

        elif self.current_step == 2:

            year_step = YearStep(
                Backend=self.ui_data
            )

            self.step_container.add_widget(
                year_step
            )

        elif self.current_step == 3:

            serial_step = SerialStep(
                Backend=self.ui_data
            )

            self.step_container.add_widget(
                serial_step
            )

    # =====================================================
    # NAVIGATION
    # =====================================================

    def OnBackPressed(self, *args):
        """
        Handles the Go Back button.
        """

        if self.current_step == 1:

            self.ui_data.Reset()

            self.current_step = 1

            self.manager.current = "home"

            return

        self.current_step -= 1

        self.RenderStep()

    # -----------------------------------------------------

    def OnForwardPressed(self, *args):
        """
        Handles Continue/Create Case button.
        """

        if self.current_step == 1:

            if not self.ui_data.IsDepartmentSelected():

                self.ShowErrorDialog(
                    title="Department Required",
                    message="Please select a department before continuing."
                )

                return

        if self.current_step == self.TOTAL_STEPS:

            if not self.ui_data.IsSerialValid():

                self.ShowErrorDialog(
                    title="Serial Number Required",
                    message="Please enter a serial number before creating the case."
                )

                return

            self.FinalizeCase()

            return

        self.current_step += 1

        self.RenderStep()

    # =====================================================
    # FINALIZE CASE
    # =====================================================

    def FinalizeCase(self):
        """
        Creates the case and displays the generated
        case number.
        """

        case_number = self.ui_data.SaveCase()

        self.ShowSuccessDialog(case_number)

        self.ui_data.Reset()

        self.current_step = 1

        self.RenderStep()

    # =====================================================
    # DIALOGS
    # =====================================================

    def ShowErrorDialog(
        self,
        title,
        message,
    ):
        """
        Displays an error dialog.
        """

        dialog = MDDialog(
            title=title,
            text=message,
        )

        dialog.open()

    # -----------------------------------------------------

    def ShowSuccessDialog(
        self,
        case_number,
    ):
        """
        Displays the generated case number after
        successful case creation.
        """

        dialog = MDDialog(
            title="Case Created",
            text=(
                "Your case has been created successfully.\n\n"
                f"Case Number:\n\n{case_number}"
            ),
        )

        dialog.open()

    # =====================================================
    # EXIT SCREEN
    # =====================================================

    def GoBack(self, *args):

        self.manager.current = "home"