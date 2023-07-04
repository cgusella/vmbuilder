import constants
import customtkinter as ctk
import gui.settings as settings
import shutil
from gui.guistandard import GuiStandard
from tkinter import filedialog


class EditScriptButtonsWidget(GuiStandard):

    def __init__(self, master, package: str, operation: str, provisions_configs):
        self.master = master
        self.package = package
        self.operation = operation
        self.provisions_configs = provisions_configs
        ctk.CTkFrame.__init__(self, master)
        self.set_fonts()
        self.set_std_dimensions()
        self.initialize_elements()
        self.render_elements()

    def set_fonts(self):
        self.font_std = ctk.CTkFont(**settings.FONT_STD)

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)

    def initialize_elements(self):
        """Initilized wanted buttons"""
        self.save_button = ctk.CTkButton(
            self,
            font=self.font_std,
            text='Save',
            command=self._save
        )
        self.remove_button = ctk.CTkButton(
            self,
            font=self.font_std,
            text=f'Remove from {self.operation}',
            command=self._remove
        )
        if self.operation == 'config':
            self.upload_button = ctk.CTkButton(
                self,
                font=self.font_std,
                text='Upload',
                command=self._upload
            )

    def render_elements(self):
        """Render buttons on grid"""
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.save_button.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
        )
        self.remove_button.grid(
            row=0,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
        )
        if self.operation == 'config':
            self.upload_button.grid(
                row=0,
                column=2,
                padx=self.padx_std,
                pady=self.pady_std,
            )

    def _save(self):
        """Save scripted file"""
        with open(f'{constants.PACKAGES_PATH}/{self.package}/{self.operation}.sh', 'w') as file:
            file.write(self.master.open_text_box.get("1.0", "end"))
        self._reload_packages_scrollable()
        self.master.destroy()

    def _remove(self):
        """Remove package from operation"""
        self.provisions_configs["provisions"][f'packages_to_{self.operation}'].remove(self.package)
        self._reload_packages_scrollable()
        self.master.destroy()

    def _upload(self):
        filename = filedialog.askopenfilename(
            initialdir=f"{constants.VMBUILDER_PATH}",
            title="Select a File",
            filetypes=(
                ("Text files",
                 "*.txt*"),
                ("all files",
                 "*.*")
            )
        )
        shutil.copy(
            src=filename,
            dst=f'{constants.PACKAGES_PATH}/{self.package}/upload/'
        )
        self.master.destroy()

    def _reload_packages_scrollable(self):
        self.master.master.clean()
        self.master.master.set_values(
            sorted(
                self.provisions_configs["provisions"][f'packages_to_{self.operation}']
            )
        )
        self.master.master.add_button_values()
