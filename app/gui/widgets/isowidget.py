import constants
import customtkinter as ctk
import gui.settings as settings
import os
from gui.guistandard import GuiStandard
from tkinter import filedialog
from tkinter import ttk


class IsoWidget(GuiStandard):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        self.set_iso_folder_path_from_json()
        ctk.CTkFrame.__init__(self, master)
        self.set_fonts()
        self.set_std_dimensions()
        self.initialize_elements()
        self.render_elements()

    def set_fonts(self):
        self.font_std = ctk.CTkFont(**settings.FONT_STD)
        self.warning_font = ctk.CTkFont(**settings.WARNING_FONT)

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_title = (10, 2)
        self.pady_entry = (2, 10)
        self.entry_height_std = 50
        self.entry_width_std = 380
        self.sticky_label = 'w'
        self.sticky_entry = 'w'
        self.sticky_frame = 'wens'
        self.sticky_optionmenu = 'w'

    def initialize_elements(self):
        self.iso_link_label = ctk.CTkLabel(
            master=self,
            text='Insert Iso Link',
            font=self.font_std
        )
        self.iso_path_button = ctk.CTkButton(
            master=self,
            text='Set Iso Path',
            command=self._set_iso_folder_path
        )
        self.iso_folder_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text=f'Actual iso path: {self.iso_folder_path}'
        )
        self.iso_link_var = ctk.StringVar(self)
        self.iso_link_var.set(self.provisions_configs["configurations"]["iso_link"]["default"])
        self.iso_link_drop = ttk.Combobox(
            master=self,
            textvariable=self.iso_link_var,
            values=self._get_local_isofiles(),
            font=self.font_std,
        )
        self.iso_link_drop.bind("<<ComboboxSelected>>", self._check_if_disable_iso_file)
        self.iso_file_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text='Insert Iso File'
        )
        self.iso_file_entry = ctk.CTkEntry(
            master=self,
            font=self.font_std,
            placeholder_text='Iso File'
        )
        if self.provisions_configs["configurations"]["iso_file"]["default"]:
            self.iso_file_entry.insert(
                0,
                self.provisions_configs["configurations"]["iso_file"]["default"]
            )
        self.iso_checksum_subframe = ctk.CTkFrame(
            master=self,
            fg_color='transparent'
        )
        self._initialize_iso_checksum_elements()

    def _initialize_iso_checksum_elements(self):
        self.algorithm_label = ctk.CTkLabel(
            master=self.iso_checksum_subframe,
            text='Algorithm',
            font=self.font_std
        )
        self.iso_checksum_algorithm = ctk.CTkOptionMenu(
            master=self.iso_checksum_subframe,
            font=self.font_std,
            values=['SHA1', 'SHA224', 'SHA256', 'SHA384', 'SHA512', 'MD5']
        )
        self.iso_checksum_label = ctk.CTkLabel(
            master=self.iso_checksum_subframe,
            text='Insert Checksum',
            font=self.font_std
        )
        self.iso_checksum_entry = ctk.CTkEntry(
            master=self.iso_checksum_subframe,
            font=self.font_std,
            placeholder_text='Checksum'
        )
        if self.provisions_configs["configurations"]["iso_checksum"]["default"]:
            self.iso_checksum_algorithm.set(
                self.provisions_configs["configurations"]["iso_checksum"]["default"].split(':')[0]
            )
            self.iso_checksum_entry.insert(
                0,
                self.provisions_configs["configurations"]["iso_checksum"]["default"].split(':')[1]
            )

    def render_elements(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=3)
        self.iso_path_button.grid(
            row=0,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.iso_folder_label.grid(
            row=0,
            column=1,
            columnspan=3,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.iso_link_label.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.iso_link_drop.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_frame
        )
        self.iso_file_label.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.iso_file_entry.grid(
            row=4,
            column=0,
            sticky=self.sticky_frame,
            padx=self.padx_std,
            pady=self.pady_entry
        )
        self._render_iso_checksum_elements()
        self.iso_checksum_subframe.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky=self.sticky_frame
        )

    def _render_iso_checksum_elements(self):
        self.iso_checksum_subframe.columnconfigure(0, weight=0)
        self.iso_checksum_subframe.columnconfigure(1, weight=1)
        self.iso_checksum_subframe.rowconfigure(0, weight=0)
        self.iso_checksum_subframe.rowconfigure(1, weight=1)
        self.algorithm_label.grid(
            row=0,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.iso_checksum_algorithm.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_optionmenu
        )
        self.iso_checksum_label.grid(
            row=0,
            column=1,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.iso_checksum_entry.grid(
            row=1,
            column=1,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_frame
        )

    def get_iso_link(self):
        if self.iso_link_drop.get().startswith('http'):
            iso_link = self.iso_link_drop.get()
        else:
            iso_link = f'{self.iso_folder_path}/{self.iso_link_drop.get()}'
        return iso_link

    def _get_local_isofiles(self):
        iso_file_paths = list()
        try:
            folder_elements = os.listdir(self.iso_folder_path)
            iso_file_paths = [
                element for element in folder_elements
                if os.path.isfile(f'{self.iso_folder_path}/{element}') and not element.startswith('.')
            ]
        except FileNotFoundError:
            self.iso_folder_label.configure(
                text_color = 'red',
                text=f'Folder not found: {self.iso_folder_path}'
            )
        
        iso_file_paths.append(self.provisions_configs["configurations"]["iso_link"]["default"])
        return iso_file_paths

    def set_iso_folder_path_from_json(self):
        if self.provisions_configs["configurations"]["iso_directory"]["default"]:
            self.iso_folder_path = self.provisions_configs["configurations"]["iso_directory"]["default"]
        else:
            self.iso_folder_path = constants.ISO_PATH

    def _set_iso_folder_path(self):
        iso_folder_path = filedialog.askdirectory()
        if iso_folder_path:
            self.iso_folder_path = iso_folder_path
            self.iso_folder_label.configure(
                text=f'Actual iso path: {iso_folder_path}',
                text_color = ['black', 'white']
            )
            self.iso_link_drop.configure(
                values=self._get_local_isofiles()
            )
            self.provisions_configs["configurations"]["iso_directory"]["default"] = iso_folder_path

    def _check_if_disable_iso_file(self, event):
        iso_link = self.iso_link_drop.get()
        if iso_link.startswith('http'):
            self.iso_file_entry.configure(
                state='normal',
                text_color='black'
            )
        else:
            self.iso_file_entry.configure(
                state='disable',
                text_color='grey85'
            )
