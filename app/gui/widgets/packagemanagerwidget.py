import constants
import customtkinter as ctk
import os
import shutil
from cli.newpackage import make_package_folder
from gui.views.utilsview import ScrollableCheckboxFrame
from gui.views.utilsview import (
    EditFileWindow,
    ScrollableButtonFrame
)
from PIL import Image
from tkinter import messagebox as mb


class PackageManagerWidget(ctk.CTkFrame):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        self.master = master
        ctk.CTkFrame.__init__(self, master)
        little_title = ctk.CTkFont(
            family='Sans',
            size=20,
            weight='bold'
        )
        self.label_font = ctk.CTkFont(
            family='Sans',
            size=16,
        )
        self.padx_std = (20, 20)
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

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        # add frame title
        packages_label = ctk.CTkLabel(
            master=self,
            text='Package Manager',
            font=little_title
        )
        packages_label.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=(20, 20),
            pady=(10, 2),
            sticky='wn'
        )

        # This frame has two different frame;
        # at left there is the package_manager_frame while
        # at right there is the selected packages frame
        self.fill_package_manager_frame()
        self.fill_selected_packages_frame()

    def fill_package_manager_frame(self):
        self.package_manager_frame = ctk.CTkFrame(self)
        self.package_manager_frame.columnconfigure(0, weight=1)
        self.package_manager_frame.columnconfigure(1, weight=1)
        self.package_manager_frame.columnconfigure(2, weight=1)
        self.package_manager_frame.rowconfigure(0, weight=1)
        self.package_manager_frame.rowconfigure(1, weight=5)
        self.package_manager_frame.rowconfigure(2, weight=1)
        self.package_manager_frame.rowconfigure(3, weight=1)
        self.package_manager_frame.grid(
            row=1,
            column=0,
            rowspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame,
        )
        add_to_install_button = ctk.CTkButton(
            master=self.package_manager_frame,
            text='Install',
            font=self.label_font,
            width=self.width_button_std,
            command=lambda: self._add_to_operation('install')
        )
        add_to_install_button.grid(
            row=0,
            column=0,
            padx=(10, 5),
            pady=self.pady_up,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )

        add_to_uninstall_button = ctk.CTkButton(
            self.package_manager_frame,
            text='Uninstall',
            font=self.label_font,
            width=self.width_button_std,
            command=lambda: self._add_to_operation('uninstall')
        )
        add_to_uninstall_button.grid(
            row=0,
            column=1,
            padx=self.pad_equal,
            pady=self.pady_up,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )

        add_to_config_button = ctk.CTkButton(
            master=self.package_manager_frame,
            text='Configure',
            font=self.label_font,
            width=self.width_button_std,
            command=lambda: self._add_to_operation('config')
        )
        add_to_config_button.grid(
            row=0,
            column=2,
            padx=self.pad_right,
            pady=self.pady_up,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )

        # add scrollable checkbox
        self.add_packages_scrollable()
        self.new_package_subframe()

        select_all_button = ctk.CTkButton(
            master=self.package_manager_frame,
            text='Select All',
            font=self.label_font,
            width=self.width_button_std,
            command=lambda: self._select_all()
        )
        select_all_button.grid(
            row=3,
            column=0,
            padx=self.pad_equal,
            pady=self.pady_down,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        deselect_all_button = ctk.CTkButton(
            master=self.package_manager_frame,
            text='Deselect All',
            font=self.label_font,
            width=self.width_button_std,
            command=self._deselect_all
        )
        deselect_all_button.grid(
            row=3,
            column=1,
            padx=self.pad_equal,
            pady=self.pady_down,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )

        self.delete_package_button = ctk.CTkButton(
            master=self.package_manager_frame,
            text='Delete',
            font=self.label_font,
            width=self.width_button_std,
            command=self._delete_packages,
            state='disabled'
        )
        self.delete_package_button.grid(
            row=3,
            column=2,
            padx=self.pad_right,
            pady=self.pady_down,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )

    def fill_selected_packages_frame(self):
        self.selected_packages_frame = ctk.CTkFrame(
            self,
            fg_color='transparent',
        )
        self.selected_packages_frame.columnconfigure(0, weight=1)
        self.selected_packages_frame.columnconfigure(1, weight=1)
        self.selected_packages_frame.columnconfigure(2, weight=1)
        self.selected_packages_frame.rowconfigure(0, weight=2)
        self.selected_packages_frame.rowconfigure(1, weight=0)
        self.selected_packages_frame.grid(
            row=1,
            column=1,
            rowspan=2,
            # padx=self.padx_std,
            # pady=self.pady_std,
            # ipadx=self.ipadx_std,
            # ipady=self.ipady_std,
            sticky=self.sticky_frame,
        )
        for operation in ('install', 'uninstall', 'config'):
            self._add_selected_packages_to(operation)

    def _add_selected_packages_to(self, operation: str):
        column = {
            'install': 0,
            'uninstall': 1,
            'config': 2
        }
        self.selected_packages_scrollable = ScrollableButtonFrame(
            master=self.selected_packages_frame,
            title=f'{operation.title()}',
            values=sorted(
                self.provisions_configs["provisions"][f"packages_to_{operation}"]
            ),
        )
        self.selected_packages_scrollable.grid(
            row=0,
            column=column[operation],
            padx=(3, 3),
            pady=self.pady_up,
            sticky=self.sticky_frame
        )
        # add clean button
        clean_button = ctk.CTkButton(
            master=self.selected_packages_frame,
            font=self.label_font,
            text='Clean',
            command=lambda operation=(operation,): self._clean_packages(*operation)
        )
        clean_button.grid(
            row=1,
            column=column[operation],
            pady=self.pady_std,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )

    def _check_package_selected(self, event):
        if self.packages_scrollable.get():
            self.delete_package_button.configure(state='normal')
        else:
            self.delete_package_button.configure(state='disabled')

    def _add_to_operation(self, opearation: str):
        for package in self.packages_scrollable.get():
            self.provisions_configs["provisions"][f"packages_to_{opearation}"].add(package)
        self._add_selected_packages_to(opearation)

    def new_package_subframe(self):
        # add new package sub frame
        new_package_subframe = ctk.CTkFrame(
            master=self.package_manager_frame,
            width=500,
            height=60,
            fg_color='transparent'
        )
        new_package_subframe.grid(
            row=2,
            column=0,
            columnspan=3,
            padx=self.padx_std,
            pady=self.pady_up,
            sticky=self.sticky_horizontal,
        )
        new_package_subframe.columnconfigure(0, weight=10)
        new_package_subframe.columnconfigure(1, weight=1)
        new_package_subframe.rowconfigure(0, weight=1)

        self.new_package_entry = ctk.CTkEntry(
            master=new_package_subframe,
            font=self.label_font,
            width=380,
            height=self.entry_height_std,
            placeholder_text='Insert New Package Name'
        )
        self.new_package_entry.grid(
            row=0,
            column=0,
            padx=(0, 0),
            pady=(0, 0),
            sticky=self.sticky_horizontal
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
            master=new_package_subframe,
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
        self.add_package_button.grid(
            row=0,
            column=1,
            sticky='w',
            padx=(0, 0),
            pady=(0, 0),
            ipadx=0,
            ipady=0
        )

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
                self.fill_package_manager_frame()
        else:
            mb.showerror('Error', 'You have selected no packages')

    def _add_package(self):
        package_name = self.new_package_entry.get()
        if package_name not in os.listdir(constants.PACKAGES_PATH):
            confirm = mb.askyesnocancel("Add package",
                                        f'You want to add "{package_name}" '
                                        'as package?')
            if confirm:
                make_package_folder(package_name)
                self.fill_package_manager_frame()
        else:
            mb.showerror('Error', 'Package already exists')

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

    def add_packages_scrollable(self, select_all=False):
        self.packages_scrollable = ScrollableCheckboxFrame(
            master=self.package_manager_frame,
            title='Packages',
            values=sorted([
                package for package in os.listdir(f'{constants.PACKAGES_PATH}')
                if package not in ('program-example', 'setup_scripts')
            ]),
            select_all=select_all
        )
        self.packages_scrollable.grid(
            row=1,
            column=0,
            columnspan=3,
            padx=self.padx_std,
            pady=self.pady_up,
            sticky='wens'
        )
        self.packages_scrollable.bind("<Motion>", self._check_package_selected)
        self.packages_scrollable.bind("<Leave>", self._check_package_selected)

    def _select_all(self):
        self.packages_scrollable.destroy()
        self.add_packages_scrollable(select_all=True)

    def _deselect_all(self):
        self.packages_scrollable.destroy()
        self.add_packages_scrollable()

    def _open_text_window(self, package, operation):
        EditFileWindow(self, package=package, operation=operation,
                       provisions_configs=self.provisions_configs)

    def _clean_packages(self, operation: str):
        self.provisions_configs["provisions"][f"packages_to_{operation}"] = set()
        self._add_selected_packages_to(operation)
