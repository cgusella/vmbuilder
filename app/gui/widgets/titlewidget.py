import customtkinter as ctk
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
        family_font = 'Sans'
        self.title_font = ctk.CTkFont(
            family=family_font,
            size=30,
            weight='bold'
        )
        self.subtitle_font = ctk.CTkFont(
            family=family_font,
            size=18
        )

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
