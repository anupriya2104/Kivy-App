from backend.create_case import CreateCaseScreen as CreateCaseScreenBackend

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget


YEAR_ITEM_HEIGHT = dp(60)


# =========================================================
# YEAR WHEEL WIDGET (Step 2/3)
# =========================================================

class YearWheel(MDScrollView):

    def __init__(self, YearOptions, InitialIndex, OnYearSelected, **kwargs):
        super().__init__(**kwargs)

        self.bar_width = 0
        self.do_scroll_x = False
        self.do_scroll_y = True

        self.year_options = YearOptions
        self.on_year_selected = OnYearSelected
        self.selected_index = InitialIndex
        self.snap_event = None

        self.layout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=[0, YEAR_ITEM_HEIGHT, 0, YEAR_ITEM_HEIGHT],
        )
        self.layout.bind(minimum_height=self.layout.setter("height"))

        self.labels = []

        for year_text in self.year_options:

            label = MDLabel(
                text=year_text,
                halign="center",
                size_hint_y=None,
                height=YEAR_ITEM_HEIGHT,
                font_style="H5",
                opacity=0.4,
            )

            self.layout.add_widget(label)
            self.labels.append(label)

        self.add_widget(self.layout)

        self.bind(scroll_y=self.OnScroll)

        Clock.schedule_once(self.InitScroll, 0)

    def InitScroll(self, dt):

        max_index = len(self.year_options) - 1

        self.scroll_y = 1.0 - (self.selected_index / max_index)
        self.OnScroll(self, self.scroll_y)

    def OnScroll(self, instance, value):

        max_index = len(self.year_options) - 1

        float_index = (1.0 - value) * max_index

        for index, label in enumerate(self.labels):

            distance = abs(index - float_index)

            if distance < 1:
                label.opacity = 1.0 - (0.6 * distance)
            else:
                label.opacity = 0.4

        nearest_index = int(round(float_index))
        nearest_index = max(0, min(nearest_index, max_index))

        self.selected_index = nearest_index
        self.on_year_selected(self.year_options[nearest_index])

        if self.snap_event:
            self.snap_event.cancel()

        self.snap_event = Clock.schedule_once(self.SnapToNearest, 0.15)

    def SnapToNearest(self, dt):

        max_index = len(self.year_options) - 1

        float_index = (1.0 - self.scroll_y) * max_index
        nearest_index = int(round(float_index))

        target_scroll_y = 1.0 - (nearest_index / max_index)

        if abs(self.scroll_y - target_scroll_y) > 0.001:

            Animation.cancel_all(self)
            animation = Animation(scroll_y=target_scroll_y, d=0.15, t="out_quad")
            animation.start(self)


# =========================================================
# MAIN SCREEN
# =========================================================

class CreateCaseScreenUI(MDScreen):

    TOTAL_STEPS = 3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = "create_case"

        # Backend Object
        self.ui_data = CreateCaseScreenBackend()

        self.current_step = 1

        self.CreateUIElements()

    # =====================================================
    # CREATE UI
    # =====================================================

    def CreateUIElements(self):

        panel_width = dp(500)

        root = MDBoxLayout(
            orientation="vertical",
            padding=dp(30),
            spacing=dp(20),
        )

        # -------------------------------------------------
        # HEADING
        # -------------------------------------------------

        heading = MDLabel(
            text="Create New Case",
            halign="center",
            font_style="H4",
            bold=True,
            size_hint_y=None,
            height=dp(60),
        )

        root.add_widget(heading)

        # -------------------------------------------------
        # PROGRESS BAR + STEP LABEL
        # -------------------------------------------------

        progress_wrap = MDBoxLayout(
            orientation="vertical",
            spacing=dp(6),
            size_hint=(None, None),
            width=panel_width,
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

        progress_wrap.add_widget(self.progress_bar)
        progress_wrap.add_widget(self.step_label)

        root.add_widget(progress_wrap)

        # -------------------------------------------------
        # STEP CONTENT AREA (swapped per step)
        # -------------------------------------------------

        self.step_container = MDBoxLayout(
            orientation="vertical",
            size_hint=(None, None),
            width=panel_width,
            height=dp(320),
            pos_hint={"center_x": 0.5},
        )

        root.add_widget(self.step_container)

        # Spacer pushes nav buttons to the bottom
        root.add_widget(Widget())

        # -------------------------------------------------
        # NAV ROW — Go Back (left) / Continue (right), always visible
        # -------------------------------------------------

        nav_row = MDBoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            width=panel_width,
            height=dp(55),
            pos_hint={"center_x": 0.5},
        )

        self.back_button = MDRaisedButton(
            text="Go Back",
            size_hint=(None, None),
            width=dp(150),
            height=dp(50),
        )
        self.back_button.bind(on_release=self.OnBackPressed)

        self.forward_button = MDRaisedButton(
            text="Continue",
            size_hint=(None, None),
            width=dp(150),
            height=dp(50),
            pos_hint={"right": 1},
        )
        self.forward_button.bind(on_release=self.OnForwardPressed)

        nav_row.add_widget(self.back_button)
        nav_row.add_widget(Widget())
        nav_row.add_widget(self.forward_button)

        root.add_widget(nav_row)

        self.add_widget(root)

        self.RenderStep()

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

        self.current_step = 1

        self.RenderStep()

    # =====================================================
    # STEP RENDERING
    # =====================================================

    def GetStepText(self):

        return f"Step {self.current_step}/{self.TOTAL_STEPS}"

    def RenderStep(self):

        self.step_container.clear_widgets()
        self.progress_bar.value = self.current_step
        self.step_label.text = self.GetStepText()

        if self.current_step == 1:
            self.RenderDepartmentStep()

        elif self.current_step == 2:
            self.RenderYearStep()

        elif self.current_step == 3:
            self.RenderSerialStep()

        if self.current_step == self.TOTAL_STEPS:
            self.forward_button.text = "Create Case"
        else:
            self.forward_button.text = "Continue"

    # -------------------------------------------------
    # STEP 1/3 — DEPARTMENT BUTTONS
    # -------------------------------------------------

    def RenderDepartmentStep(self):

        label = MDLabel(
            text="Select Department",
            halign="center",
            bold=True,
            size_hint_y=None,
            height=dp(40),
        )

        self.step_container.add_widget(label)

        buttons_wrap = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(260),
        )

        self.department_buttons = {}

        for code in self.ui_data.GetDepartmentOptions():

            button = MDRaisedButton(
                text=f"Department {code}",
                size_hint=(None, None),
                width=dp(460),
                height=dp(45),
                pos_hint={"center_x": 0.5},
                md_bg_color=self.GetDepartmentColor(code),
            )

            button.bind(
                on_release=lambda instance, value=code:
                self.OnDepartmentSelected(value)
            )

            self.department_buttons[code] = button
            buttons_wrap.add_widget(button)

        self.step_container.add_widget(buttons_wrap)

    def GetDepartmentColor(self, code):
        """Selected department renders darker/highlighted; others default blue."""

        if code == self.ui_data.GetDepartment():
            return (0.05, 0.30, 0.55, 1)

        return (0.20, 0.60, 0.95, 1)

    def OnDepartmentSelected(self, code):

        self.ui_data.SetDepartment(code)

        for department_code, button in self.department_buttons.items():
            button.md_bg_color = self.GetDepartmentColor(department_code)

    # -------------------------------------------------
    # STEP 2/3 — YEAR WHEEL
    # -------------------------------------------------

    def RenderYearStep(self):

        label = MDLabel(
            text="Select Year",
            halign="center",
            bold=True,
            size_hint_y=None,
            height=dp(40),
        )

        self.step_container.add_widget(label)

        year_options = self.ui_data.GetYearOptions()

        current_value = self.ui_data.GetYear()

        if current_value in year_options:
            initial_index = year_options.index(current_value)
        else:
            initial_index = 1  # middle = current year

        wheel_wrap = MDBoxLayout(
            size_hint_y=None,
            height=YEAR_ITEM_HEIGHT * 3,
            padding=[dp(100), 0, dp(100), 0],
        )

        self.year_wheel = YearWheel(
            YearOptions=year_options,
            InitialIndex=initial_index,
            OnYearSelected=self.OnYearSelected,
            size_hint_y=None,
            height=YEAR_ITEM_HEIGHT * 3,
        )

        wheel_wrap.add_widget(self.year_wheel)

        self.step_container.add_widget(wheel_wrap)

    def OnYearSelected(self, year_text):

        self.ui_data.SetYear(year_text)

    # -------------------------------------------------
    # STEP 3/3 — SERIAL NUMBER TEXTBOX
    # -------------------------------------------------

    def RenderSerialStep(self):

        label = MDLabel(
            text="Enter Case Serial Number",
            halign="center",
            bold=True,
            size_hint_y=None,
            height=dp(40),
        )

        self.step_container.add_widget(label)

        # hint = MDLabel(
        #     text="Numbers only — will be padded to 4 digits",
        #     halign="center",
        #     theme_text_color="Secondary",
        #     size_hint_y=None,
        #     height=dp(25),
        # )

        # self.step_container.add_widget(hint)

        field_wrap = MDBoxLayout(
            size_hint_y=None,
            height=dp(60),
            padding=[dp(80), 0, dp(80), 0],
        )

        self.serial_field = MDTextField(
            text=self.ui_data.GetSerialRaw(),
            mode="rectangle",
            input_filter="int",
            halign="center",
        )

        self.serial_field.bind(text=self.OnSerialChanged)

        field_wrap.add_widget(self.serial_field)

        self.step_container.add_widget(field_wrap)

        # preview = MDLabel(
        #     text=self.GetPreviewText(),
        #     halign="center",
        #     theme_text_color="Secondary",
        #     size_hint_y=None,
        #     height=dp(25),
        # )

        # self.preview_label = preview
        # self.step_container.add_widget(preview)

    def OnSerialChanged(self, instance, value):

        self.ui_data.SetSerialRaw(value)
        # self.preview_label.text = self.GetPreviewText()

    # =====================================================
    # NAVIGATION
    # =====================================================

    def OnBackPressed(self, *args):

        if self.current_step == 1:

            # Exit the whole flow back to the dashboard
            self.ui_data.Reset()
            self.current_step = 1
            self.manager.current = "home"
            return

        self.current_step -= 1
        self.RenderStep()

    def OnForwardPressed(self, *args):

        if self.current_step == 1:

            if not self.ui_data.IsDepartmentSelected():

                MDDialog(
                    title="Department Required",
                    text="Please select a department before continuing.",
                ).open()

                return

        if self.current_step == self.TOTAL_STEPS:

            if not self.ui_data.IsSerialValid():

                MDDialog(
                    title="Serial Number Required",
                    text="Please enter a serial number before creating the case.",
                ).open()

                return

            self.FinalizeCase()
            return

        self.current_step += 1
        self.RenderStep()

    # =====================================================
    # FINALIZE
    # =====================================================

    def FinalizeCase(self):

        case_number = self.ui_data.SaveCase()

        MDDialog(
            title="Case Created",
            text="Your new case has been created successfully.",
        ).open()

        # Reset flow for next use, but stay on this screen
        self.ui_data.Reset()
        self.current_step = 1
        self.RenderStep()

    # =====================================================
    # GO BACK
    # =====================================================

    def GoBack(self, *args):

        self.manager.current = "home"