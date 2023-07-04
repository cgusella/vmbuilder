import customtkinter as ctk
import gui.settings as settings
from gui.guistandard import GuiStandard
from tkinter import ttk


class VagrantBoxSetUpWidget(GuiStandard):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        ctk.CTkFrame.__init__(self, master)
        self.set_fonts()
        self.set_std_dimensions()
        self.initialize_elements()
        self.render_elements()

    def set_fonts(self):
        self.warning_font = ctk.CTkFont(**settings.WARNING_FONT)
        self.font_std = ctk.CTkFont(**settings.FONT_STD)

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_title = (10, 2)
        self.pady_entry = (2, 10)
        self.height = 40
        self.sticky_label = 'ws'
        self.sticky_horizontal = 'ew'

    def initialize_elements(self):
        self.hostname_label = ctk.CTkLabel(
            master=self,
            text="Hostname:",
            font=self.font_std
        )

        self.hostname_entry = ctk.CTkEntry(
            master=self,
            font=self.font_std,
            height=self.height,
            placeholder_text='Hostname for the new VM'
        )
        if self.provisions_configs["configurations"]['hostname']["default"]:
            self.hostname_entry.insert(
                0,
                self.provisions_configs["configurations"]['hostname']["default"]
            )
        self.vagrant_box_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text='Select or Insert Vagrant Box'
        )

        self.vagrant_box = ctk.StringVar(self)
        self.vagrant_box.set(self.provisions_configs["configurations"]["image"]["default"])
        self.vagrant_drop = ttk.Combobox(
            master=self,
            textvariable=self.vagrant_box,
            height=self.height,
            values=self.master.local_vagrant_boxes.split("\n"),
            font=self.font_std,
        )

        self.username_label = ctk.CTkLabel(
            master=self,
            text="Username:",
            font=self.font_std
        )

        self.username_entry = ctk.CTkEntry(
            master=self,
            font=self.font_std,
            height=self.height,
            placeholder_text="Existing user on the vagrant box"
        )
        if self.provisions_configs["credentials"]['username']:
            self.username_entry.insert(
                0,
                self.provisions_configs["credentials"]['username']
            )

        self.password_label = ctk.CTkLabel(
            master=self,
            text="Password:",
            font=self.font_std
        )
        self.password_entry = ctk.CTkEntry(
            master=self,
            font=self.font_std,
            height=self.height,
            placeholder_text="Password of the previous user"
        )
        if self.provisions_configs["credentials"]['password']:
            self.password_entry.insert(
                0,
                self.provisions_configs["credentials"]['password']
            )

        self.extra_user_label = ctk.CTkLabel(
            master=self,
            text="Extra user:",
            font=self.font_std
        )

        self.extra_user_entry = ctk.CTkEntry(
            master=self,
            font=self.font_std,
            height=self.height,
            placeholder_text="An extra user to be created"
        )
        if self.provisions_configs["credentials"]['extra_user']:
            self.extra_user_entry.insert(
                0,
                self.provisions_configs["credentials"]['extra_user']
            )

    def render_elements(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)
        self.hostname_label.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_title,
            sticky=self.sticky_label
        )
        self.hostname_entry.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_horizontal
        )
        self.vagrant_box_label.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_title,
            sticky=self.sticky_label
        )
        self.vagrant_drop.grid(
            row=3,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_horizontal
        )
        self.username_label.grid(
            row=4,
            column=0,
            padx=self.padx_std,
            pady=self.pady_title,
            sticky=self.sticky_label
        )
        self.username_entry.grid(
            row=5,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_horizontal
        )
        self.password_label.grid(
            row=6,
            column=0,
            padx=self.padx_std,
            pady=self.pady_title,
            sticky=self.sticky_label
        )
        self.password_entry.grid(
            row=7,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_horizontal
        )
        self.extra_user_label.grid(
            row=8,
            column=0,
            padx=self.padx_std,
            pady=self.pady_title,
            sticky=self.sticky_label
        )
        self.extra_user_entry.grid(
            row=9,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_horizontal
        )
