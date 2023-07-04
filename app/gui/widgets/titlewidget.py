import customtkinter as ctk
import gui.settings as settings
from gui.guistandard import GuiStandard


class TitleWidget(GuiStandard):

    def __init__(self, master, title: str, subtitle: str = ""):
        self.title = title
        self.subtitle = subtitle
        ctk.CTkFrame.__init__(
            self,
            master,
            fg_color='transparent'
        )
        self.set_fonts()
        self.set_std_dimensions()
        self.initialize_elements()
        self.render_elements()

    def set_std_dimensions(self):
        pass

    def set_fonts(self):
        self.title_font = ctk.CTkFont(**settings.TITLE_VIEW_FONT)
        self.subtitle_font = ctk.CTkFont(**settings.SUBTITLE_VIEW_FONT)

    def initialize_elements(self):
        self.title_label = ctk.CTkLabel(
            master=self,
            text=self.title,
            font=self.title_font
        )
        self.subtitle_label = ctk.CTkLabel(
            master=self,
            text=self.subtitle,
            font=self.subtitle_font
        )

    def render_elements(self):
        self.title_label.grid(
            row=0,
            column=0,
            sticky='w'
        )
        self.subtitle_label.grid(
            row=1,
            column=0,
            sticky='w'
        )
