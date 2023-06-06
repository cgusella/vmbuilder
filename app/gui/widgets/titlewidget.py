import customtkinter as ctk


class TitleWidget(ctk.CTkFrame):

    def __init__(self, master, title: str, subtitle: str = ""):
        ctk.CTkFrame.__init__(
            self,
            master,
            fg_color='transparent'
        )
        family_font = 'Sans'
        title_font = ctk.CTkFont(
            family=family_font,
            size=30,
            weight='bold'
        )
        subtitle_font = ctk.CTkFont(
            family=family_font,
            size=18
        )

        title_label = ctk.CTkLabel(
            master=self,
            text=title,
            font=title_font
        )
        title_label.grid(
            row=0,
            column=0,
            sticky='w'
        )

        subtitle_label = ctk.CTkLabel(
            master=self,
            text=subtitle,
            font=subtitle_font
        )
        subtitle_label.grid(
            row=1,
            column=0,
            sticky='w'
        )
