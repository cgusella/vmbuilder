import constants
import customtkinter as ctk
import os
import shutil
from cli.newpackage import make_package_folder
from gui.guistandard import GuiStandard
from gui.views.utilsview import ScrollableCheckboxFrame
from PIL import Image
from tkinter import messagebox as mb


class PackageManagerWidget(GuiStandard):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        ctk.CTkFrame.__init__(self, master)
        self.selected_package_frame = master.selected_packages_frame
        self.set_fonts()
        self.set_std_dimensions()
        self.initialize_elements()
        self.render_elements()

    def set_fonts(self):
        family = 'Sans'
        self.little_title = ctk.CTkFont(
            family=family,
            size=20,
            weight='bold'
        )
        self.label_font = ctk.CTkFont(
            family=family,
            size=16,
        )

    def set_std_dimensions(self):
        self.padx_std = (5, 5)
        self.pady_std = (10, 10)
        self.pady_up = (10, 0)
        self.pady_down = (0, 10)
        self.pad_right = (5, 10)
        self.pad_equal = (5, 5)
        self.pady_entry = (2, 10)
        self.entry_height_std = 50
        self.ipadx_std = 10
        self.ipady_std = 10
        self.ipadx_button = 5
        self.ipady_button = 5
        self.width_button_std = 100
        self.sticky_frame = 'wens'
        self.sticky_horizontal = 'ew'

    def initialize_elements(self):
        self.install_button = ctk.CTkButton(
            master=self,
            text='Install',
            font=self.label_font,
            width=self.width_button_std,
            command=self._add_selected_packages_to_install
        )
        self.uninstall_button = ctk.CTkButton(
            self,
            text='Uninstall',
            font=self.label_font,
            width=self.width_button_std,
            command=self._add_selected_packages_to_uninstall
        )
        self.config_button = ctk.CTkButton(
            master=self,
            text='Configure',
            font=self.label_font,
            width=self.width_button_std,
            command=self._add_selected_packages_to_config
        )
        self.packages_scrollable = ScrollableCheckboxFrame(
            master=self,
            title='Packages',
            values=sorted([
                package for package in os.listdir(f'{constants.PACKAGES_PATH}')
                if package not in ('program-example', 'setup_scripts')
            ]),
            command=self._active_deactive_operation_buttons
        )
        self.new_package_subframe = ctk.CTkFrame(
            master=self,
            width=500,
            height=60,
            fg_color='transparent'
        )
        self._initialize_new_package_subframe_elements()
        self.select_all_button = ctk.CTkButton(
            master=self,
            text='Select All',
            font=self.label_font,
            width=self.width_button_std,
            command=self._select_all
        )
        self.deselect_all_button = ctk.CTkButton(
            master=self,
            text='Deselect All',
            font=self.label_font,
            width=self.width_button_std,
            command=self._deselect_all
        )
        self.delete_package_button = ctk.CTkButton(
            master=self,
            text='Delete',
            font=self.label_font,
            width=self.width_button_std,
            command=self._delete_packages,
            state='disabled'
        )
        self._active_deactive_operation_buttons()

    def _initialize_new_package_subframe_elements(self):
        self.new_package_entry = ctk.CTkEntry(
            master=self.new_package_subframe,
            font=self.label_font,
            width=380,
            height=self.entry_height_std,
            placeholder_text='Insert New Package Name'
        )
        self.new_package_entry.bind('<KeyRelease>', self._active_add_package)
        self.plus_active = ctk.CTkImage(
            light_image=Image.open(f'{constants.VMBUILDER_PATH}/images/plus_light_cube.png'),
            dark_image=Image.open(f'{constants.VMBUILDER_PATH}/images/plus_dark_cube.png'),
            size=(45, 45)
        )
        self.plus_disabled = ctk.CTkImage(
            light_image=Image.open(f'{constants.VMBUILDER_PATH}/images/plus_disabled_cube.png'),
            size=(45, 45)
        )
        self.add_package_button = ctk.CTkButton(
            master=self.new_package_subframe,
            text='',
            image=self.plus_disabled,
            width=10,
            height=10,
            corner_radius=50,
            fg_color=['grey86', 'grey17'],
            hover_color=['grey76', 'grey7'],
            state='disabled',
            command=self._add_package
        )

    def _render_new_package_subframe_elements(self):
        self.new_package_subframe.columnconfigure(0, weight=10)
        self.new_package_subframe.columnconfigure(1, weight=1)
        self.new_package_subframe.rowconfigure(0, weight=1)
        self.new_package_entry.grid(
            row=0,
            column=0,
            padx=(0, 0),
            pady=(0, 0),
            sticky=self.sticky_horizontal
        )
        self.add_package_button.grid(
            row=0,
            column=1,
            sticky='w',
            padx=(0, 0),
            pady=(0, 0),
            ipadx=0,
            ipady=0
        )

    def render_elements(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.install_button.grid(
            row=0,
            column=0,
            padx=(10, 5),
            pady=self.pady_up,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        self.uninstall_button.grid(
            row=0,
            column=1,
            padx=self.pad_equal,
            pady=self.pady_up,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        self.config_button.grid(
            row=0,
            column=2,
            padx=self.pad_right,
            pady=self.pady_up,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        self.packages_scrollable.grid(
            row=1,
            column=0,
            columnspan=3,
            padx=self.padx_std,
            pady=self.pady_up,
            sticky='wens'
        )
        self.new_package_subframe.grid(
            row=2,
            column=0,
            columnspan=3,
            padx=self.padx_std,
            pady=self.pady_up,
            sticky=self.sticky_horizontal,
        )
        self._render_new_package_subframe_elements()
        self.select_all_button.grid(
            row=3,
            column=0,
            padx=self.pad_equal,
            pady=self.pady_down,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        self.deselect_all_button.grid(
            row=3,
            column=1,
            padx=self.pad_equal,
            pady=self.pady_down,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        self.delete_package_button.grid(
            row=3,
            column=2,
            padx=self.pad_right,
            pady=self.pady_down,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )

    def _active_deactive_operation_buttons(self):
        if self.packages_scrollable.get():
            self.delete_package_button.configure(state='normal')
            self.install_button.configure(state='normal')
            self.uninstall_button.configure(state='normal')
            self.config_button.configure(state='normal')
        else:
            self.delete_package_button.configure(state='disabled')
            self.install_button.configure(state='disabled')
            self.uninstall_button.configure(state='disabled')
            self.config_button.configure(state='disabled')

    def _select_all(self):
        self.packages_scrollable.select_all()
        self._active_deactive_operation_buttons()

    def _deselect_all(self):
        self.packages_scrollable.deselect_all()
        self._active_deactive_operation_buttons()

    def _add_selected_packages_to_install(self):
        for package in self.packages_scrollable.get():
            self.provisions_configs["provisions"]["packages_to_install"].add(package)
        self.selected_package_frame.install_scrollable.set_values(
            sorted(
                self.provisions_configs["provisions"]["packages_to_install"]
            )
        )
        self.selected_package_frame.install_scrollable.add_button_values()

    def _add_selected_packages_to_uninstall(self):
        for package in self.packages_scrollable.get():
            self.provisions_configs["provisions"]["packages_to_uninstall"].add(package)
        self.selected_package_frame.uninstall_scrollable.set_values(
            sorted(
                self.provisions_configs["provisions"]["packages_to_uninstall"]
            )
        )
        self.selected_package_frame.uninstall_scrollable.add_button_values()

    def _add_selected_packages_to_config(self):
        for package in self.packages_scrollable.get():
            self.provisions_configs["provisions"]["packages_to_config"].add(package)
        self.selected_package_frame.config_scrollable.set_values(
            sorted(
                self.provisions_configs["provisions"]["packages_to_config"]
            )
        )
        self.selected_package_frame.config_scrollable.add_button_values()

    def _delete_packages(self):
        if self.packages_scrollable.get():
            warning_text = 'This operation is irreversible.\nYou choose to delete:\n'
            for package in self.packages_scrollable.get():
                warning_text += f'\t- {package}\n'
            warning_text += 'Confirm?'
            yes = mb.askyesno('Confirm Delete', warning_text)
            if yes:
                for package in self.packages_scrollable.get():
                    shutil.rmtree(f'{constants.PACKAGES_PATH}/{package}')
                self.master.__init__(self, self.master, self.provisions_configs)
        else:
            mb.showerror('Error', 'You have selected no packages')

    def _active_add_package(self, event):
        new_package_typed = self.new_package_entry.get()
        if new_package_typed:
            self.add_package_button.configure(
                state="normal",
                image=self.plus_active
            )
        else:
            self.add_package_button.configure(
                state="disabled",
                image=self.plus_disabled
            )

    def _add_package(self):
        package_name = self.new_package_entry.get()
        if package_name not in os.listdir(constants.PACKAGES_PATH):
            confirm = mb.askyesnocancel("Add package",
                                        f'You want to add "{package_name}" '
                                        'as package?')
            if confirm:
                make_package_folder(package_name)
                self.packages_scrollable.clean()
                self.packages_scrollable.set_values(
                    sorted([
                        package for package in os.listdir(f'{constants.PACKAGES_PATH}')
                        if package not in ('program-example', 'setup_scripts')
                    ])
                )
                self.packages_scrollable.add_checkboxes()
        else:
            mb.showerror('Error', 'Package already exists')
