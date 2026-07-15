from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import dp

YEAR_ITEM_HEIGHT = dp(60)


class YearWheel(MDScrollView):
    """
    Scroll wheel used to select the case year.

    The widget always snaps to the nearest year and
    informs the parent screen whenever the selection changes.
    """

    def __init__(
        self,
        YearOptions,
        InitialIndex,
        OnYearSelected,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.bar_width = 0
        self.do_scroll_x = False
        self.do_scroll_y = True

        self.year_options = YearOptions
        self.selected_index = InitialIndex
        self.on_year_selected = OnYearSelected

        self.snap_event = None

        self.layout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=[
                0,
                YEAR_ITEM_HEIGHT,
                0,
                YEAR_ITEM_HEIGHT
            ]
        )

        self.layout.bind(
            minimum_height=self.layout.setter("height")
        )

        self.labels = []

        self.CreateLabels()

        self.add_widget(self.layout)

        self.bind(scroll_y=self.OnScroll)

        Clock.schedule_once(self.InitializeScroll)

    # -----------------------------------------------------

    def CreateLabels(self):

        for year in self.year_options:

            label = MDLabel(
                text=year,
                halign="center",
                font_style="H5",
                opacity=0.4,
                size_hint_y=None,
                height=YEAR_ITEM_HEIGHT
            )

            self.labels.append(label)
            self.layout.add_widget(label)

    # -----------------------------------------------------

    def InitializeScroll(self, dt):

        maximum = len(self.year_options) - 1

        self.scroll_y = 1 - (self.selected_index / maximum)

        self.OnScroll(self, self.scroll_y)

    # -----------------------------------------------------

    def OnScroll(self, instance, value):

        maximum = len(self.year_options) - 1

        float_index = (1 - value) * maximum

        for index, label in enumerate(self.labels):

            distance = abs(index - float_index)

            if distance < 1:
                label.opacity = 1 - (distance * 0.6)
            else:
                label.opacity = 0.4

        nearest = round(float_index)

        nearest = max(0, min(nearest, maximum))

        self.selected_index = nearest

        self.on_year_selected(
            self.year_options[nearest]
        )

        if self.snap_event:
            self.snap_event.cancel()

        self.snap_event = Clock.schedule_once(
            self.SnapToNearest,
            0.15
        )

    # -----------------------------------------------------

    def SnapToNearest(self, dt):

        maximum = len(self.year_options) - 1

        float_index = (1 - self.scroll_y) * maximum

        nearest = round(float_index)

        target = 1 - (nearest / maximum)

        if abs(self.scroll_y - target) > 0.001:

            Animation.cancel_all(self)

            Animation(
                scroll_y=target,
                d=0.15,
                t="out_quad"
            ).start(self)