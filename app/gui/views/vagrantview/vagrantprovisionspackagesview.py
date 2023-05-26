import constants
import os
import shutil
import customtkinter as ctk
from builder.vagrant import Vagrant
from cli.provisionsreader import ProvisionConfigReader
from cli.newpackage import make_package_folder
from tkinter import messagebox as mb
from tkinter import StringVar
from builder.error import (
    NoFileToUploadError,
    PackageNotFoundError,
    EmptyScriptError,
    UploadNameConflictError
)
from gui.views.utilsview import (
    EditFileWindow,
    ScrollableButtonFrame,
    ScrollableCheckboxFrame,
    SetUpScriptEdit
)


class VagrantProvisionsPackagesFrame(ctk.CTkFrame):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        ctk.CTkFrame.__init__(self, master)
        self.family = 'Sans'
        self.title_std = ctk.CTkFont(family=self.master.family, size=30,
                                     weight='bold')
        self.font_std = ctk.CTkFont(family=self.master.family, size=20)
        self.set_std_dimensions()
        self.set_grid(rows=6, columns=2)
        self.add_titles()
        self.add_additional_scripts()
        self.add_selected_packages_frame()
        self.add_packages_frame()
        self.add_bottom_button_frame()

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)
        self.pady_title = (10, 2)
        self.pady_entry = (2, 10)
        self.pad_equal = (1, 1)
        self.ipadx_std = 10
        self.ipady_std = 10
        self.ipadx_button = 5
        self.ipady_button = 5
        self.entry_height_std = 50
        self.entry_width_std = 400
        self.width_button_std = 100

    def set_grid(self, rows: int, columns: int):
        self.grid()
        for i in range(columns):
            self.columnconfigure(i, weight=1)

        for i in range(rows):
            self.rowconfigure(i, weight=1)

    def add_titles(self):
        title_frame = ctk.CTkFrame(self, fg_color='transparent')
        title_frame.grid(row=0, column=0, columnspan=2,
                         sticky='wn', padx=self.padx_std, pady=self.pady_std)
        title_frame.columnconfigure(0, weight=1)
        title_frame.rowconfigure(0, weight=1)
        title_frame.rowconfigure(1, weight=1)
        self.vagrant_label = ctk.CTkLabel(
            title_frame,
            text="Vagrant",
            font=self.title_std
        )
        self.vagrant_label.grid(row=0, column=0, sticky='w')

        self.conf_label = ctk.CTkLabel(
            title_frame,
            text="Provisions",
            font=self.font_std
        )
        self.conf_label.grid(row=1, column=0, sticky='w')

    def add_additional_scripts(self):
        self.additional_scripts_frame = ctk.CTkFrame(self)
        self.additional_scripts_frame.grid(row=1, column=0, rowspan=2, sticky='wens',
                                           padx=self.padx_std, pady=self.pady_std,
                                           ipadx=self.ipadx_std,
                                           ipady=self.ipady_std)
        self.additional_scripts_frame.columnconfigure(0, weight=1)
        self.additional_scripts_frame.columnconfigure(1, weight=1)
        self.additional_scripts_frame.rowconfigure(0, weight=1)
        self.additional_scripts_frame.rowconfigure(1, weight=1)
        self.additional_scripts_frame.rowconfigure(2, weight=1)
        self.additional_scripts_frame.rowconfigure(3, weight=1)
        self.additional_scripts_frame.rowconfigure(4, weight=1)
        additional_scripts_label = ctk.CTkLabel(
            self.additional_scripts_frame,
            text='Additional Scripts',
            font=self.font_std
        )
        additional_scripts_label.grid(row=0, column=0, sticky='w',
                                      padx=self.padx_std, pady=self.pady_title)

        # add radiobuttons
        self.radio_var = StringVar(self, value=None)
        if self.provisions_configs["provisions"]['update_upgrade']:
            self.radio_var.set('update_upgrade')
            self._add_edit_button()
        if self.provisions_configs["provisions"]['update_upgrade_full']:
            self.radio_var.set('update_upgrade_full')
            self._add_edit_button()

        self.update_upgrade = ctk.CTkRadioButton(
            self.additional_scripts_frame,
            text="Update upgrade",
            variable=self.radio_var,
            value='update_upgrade',
            command=self._add_edit_button,
            font=self.font_std
        )
        self.update_upgrade.grid(row=1, column=0, sticky='w',
                                 padx=self.padx_std)

        self.update_upgrade_full = ctk.CTkRadioButton(
            self.additional_scripts_frame,
            text="Update upgrade full",
            variable=self.radio_var,
            value='update_upgrade_full',
            command=self._add_edit_button,
            font=self.font_std
        )
        self.update_upgrade_full.grid(row=2, column=0, sticky='w',
                                      padx=self.padx_std)
        self.update_upgrade_full = ctk.CTkRadioButton(
            self.additional_scripts_frame,
            text="None",
            variable=self.radio_var,
            value=None,
            font=self.font_std,
            command=self._remove_edit_button
        )
        self.update_upgrade_full.grid(row=3, column=0, sticky='w',
                                      padx=self.padx_std)

    def _add_edit_button(self):
        if self.radio_var.get() == 'update_upgrade':
            self._remove_edit_button()
            row = 1
            self.provisions_configs["provisions"]['update_upgrade_full'] = False
        elif self.radio_var.get() == 'update_upgrade_full':
            self._remove_edit_button()
            row = 2
            self.provisions_configs["provisions"]['update_upgrade'] = False
        self.provisions_configs["provisions"][f'{self.radio_var.get()}'] = True
        self.edit_upgrade_button = ctk.CTkButton(
            self.additional_scripts_frame,
            text='Edit',
            font=self.font_std,
            width=self.width_button_std,
            command=self._edit_update_script
        )
        self.edit_upgrade_button.grid(row=row, column=1)

    def _remove_edit_button(self):
        try:
            self.edit_upgrade_button.destroy()
        except (AttributeError, ValueError):
            pass

    def _edit_update_script(self):
        SetUpScriptEdit(self, operation=self.radio_var.get(),
                        provisions_configs=self.provisions_configs)

    def add_selected_packages_frame(self):
        selected_packages_frame = ctk.CTkFrame(self)
        selected_packages_frame.grid(row=3, column=0, rowspan=3, sticky='wnes',
                                     padx=self.padx_std, pady=self.pady_std,
                                     ipadx=self.ipadx_std,
                                     ipady=self.ipady_std)
        selected_packages_frame.columnconfigure(0, weight=1)
        selected_packages_frame.columnconfigure(1, weight=1)
        selected_packages_frame.columnconfigure(2, weight=1)
        selected_packages_frame.rowconfigure(0, weight=1)
        selected_packages_frame.rowconfigure(1, weight=10)
        selected_packages_frame.rowconfigure(2, weight=1)

        for count, operation in enumerate(('install', 'uninstall', 'config')):
            self.selected_packages_scrollable = ScrollableButtonFrame(
                master=selected_packages_frame,
                title=f'{operation.title()}',
                values=sorted(
                    self.provisions_configs["provisions"][f"packages_to_{operation}"]
                ),
            )
            self.selected_packages_scrollable.grid(
                row=1,
                column=count,
                sticky='wens',
                padx=self.padx_std, pady=self.pady_std
            )
            # add clean button
            clean_button = ctk.CTkButton(
                master=selected_packages_frame,
                font=self.font_std,
                text='Clean',
                command=lambda operation=(operation,): self._clean_packages(*operation)
            )
            clean_button.grid(row=2, column=count)

    def _clean_packages(self, operation: str):
        self.provisions_configs["provisions"][f"packages_to_{operation}"] = set()
        self.add_selected_packages_frame()

    def add_packages_frame(self, select_all=False):
        packages_frame = ctk.CTkFrame(self)
        packages_frame.grid(row=1, column=1, rowspan=4, sticky='wens',
                            padx=self.padx_std, pady=self.pady_std,
                            ipadx=self.ipadx_std,
                            ipady=self.ipady_std)
        packages_frame.columnconfigure(0, weight=1)
        packages_frame.columnconfigure(1, weight=1)
        packages_frame.columnconfigure(2, weight=1)
        packages_frame.rowconfigure(0, weight=1)
        packages_frame.rowconfigure(1, weight=10)
        packages_frame.rowconfigure(2, weight=1)
        packages_frame.rowconfigure(3, weight=1)
        packages_frame.rowconfigure(4, weight=1)

        # add install, uninstall, config
        add_to_install_button = ctk.CTkButton(
            packages_frame,
            text='Install',
            font=self.font_std,
            width=self.width_button_std,
            command=lambda: self._add_to_operation('install')
        )
        add_to_install_button.grid(row=0, column=0,
                                   padx=self.padx_std, pady=self.pady_std,
                                   ipadx=self.ipadx_button,
                                   ipady=self.ipady_button)
        add_to_uninstall_button = ctk.CTkButton(
            packages_frame,
            text='Uninstall',
            font=self.font_std,
            width=self.width_button_std,
            command=lambda: self._add_to_operation('uninstall')
        )
        add_to_uninstall_button.grid(row=0, column=1,
                                     padx=self.padx_std, pady=self.pady_std,
                                     ipadx=self.ipadx_button,
                                     ipady=self.ipady_button)
        add_to_config_button = ctk.CTkButton(
            packages_frame,
            text='Configure',
            font=self.font_std,
            width=self.width_button_std,
            command=lambda: self._add_to_operation('config')
        )
        add_to_config_button.grid(row=0, column=2,
                                  padx=self.padx_std, pady=self.pady_std,
                                  ipadx=self.ipadx_button,
                                  ipady=self.ipady_button)

        # add scrollable checkbox
        self.packages_scrollable = ScrollableCheckboxFrame(
            master=packages_frame,
            title='Packages',
            values=sorted([
                package for package in os.listdir(f'{constants.PACKAGES_PATH}')
                if package not in ('program-example', 'setup_scripts')
            ]),
            select_all=select_all
        )
        self.packages_scrollable.grid(row=1, column=0, columnspan=3,
                                      sticky='wens',
                                      padx=self.padx_std, pady=self.pady_std)

        # add new package
        new_package_label = ctk.CTkLabel(
            packages_frame,
            text='New package:',
            font=self.font_std
        )
        new_package_label.grid(row=2, column=0, sticky='w',
                               padx=self.padx_std, pady=self.pady_title,
                               ipadx=self.ipadx_std)
        self.new_package_entry = ctk.CTkEntry(
            packages_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std
        )
        self.new_package_entry.grid(row=3, column=0, columnspan=3, sticky='wne',
                                    padx=self.padx_std, pady=self.pady_entry)

        add_package_button = ctk.CTkButton(
            packages_frame,
            text='Add',
            font=self.font_std,
            width=self.width_button_std,
            command=self._add_package
        )
        add_package_button.grid(row=4, column=0,
                                padx=self.padx_std, pady=self.pady_std,
                                ipadx=self.ipadx_button,
                                ipady=self.ipady_button)

        if self.packages_scrollable.get():
            deselect_all_button = ctk.CTkButton(
                packages_frame,
                text='Deselect All',
                font=self.font_std,
                width=self.width_button_std,
                command=self.add_packages_frame
            )
            deselect_all_button.grid(row=4, column=1,
                                     padx=self.padx_std, pady=self.pady_std,
                                     ipadx=self.ipadx_button,
                                     ipady=self.ipady_button)
        else:
            select_all_button = ctk.CTkButton(
                packages_frame,
                text='Select All',
                font=self.font_std,
                width=self.width_button_std,
                command=lambda: self.add_packages_frame(select_all=True)
            )
            select_all_button.grid(row=4, column=1,
                                   padx=self.padx_std, pady=self.pady_std,
                                   ipadx=self.ipadx_button,
                                   ipady=self.ipady_button)
        delete_package_button = ctk.CTkButton(
            packages_frame,
            text='Delete',
            font=self.font_std,
            width=self.width_button_std,
            command=self._delete_packages
        )
        delete_package_button.grid(row=4, column=2,
                                   padx=self.padx_std, pady=self.pady_std,
                                   ipadx=self.ipadx_button,
                                   ipady=self.ipady_button)

    def add_bottom_button_frame(self):
        bottom_button_frame = ctk.CTkFrame(self)
        bottom_button_frame.grid(row=5, column=1, sticky='wens',
                                 padx=self.padx_std, pady=self.pady_std,
                                 ipadx=self.ipadx_std,
                                 ipady=self.ipady_std)
        bottom_button_frame.columnconfigure(0, weight=1)
        bottom_button_frame.columnconfigure(1, weight=1)
        bottom_button_frame.rowconfigure(0, weight=1)
        set_configs_button = ctk.CTkButton(
            bottom_button_frame,
            text='Set Configs',
            font=self.font_std,
            width=self.width_button_std,
            command=self.set_configs,
        )
        set_configs_button.grid(row=0, column=0,
                                padx=self.padx_std, pady=self.pady_std,
                                ipadx=self.ipadx_button,
                                ipady=self.ipady_button)
        build_button = ctk.CTkButton(
            bottom_button_frame,
            text='Build',
            font=self.font_std,
            width=self.width_button_std,
            command=self.build
        )
        build_button.grid(row=0, column=1,
                          padx=self.padx_std, pady=self.pady_std,
                          ipadx=self.ipadx_button,
                          ipady=self.ipady_button)

    def _delete_packages(self):
        if self.packages_scrollable.get():
            print(self.packages_scrollable.get())
            warning_text = 'This operation is irreversible.\nYou choose to delete:\n'
            for package in self.packages_scrollable.get():
                warning_text += f'\t- {package}\n'
            warning_text += 'Confirm?'
            yes = mb.askyesno('Confirm Delete', warning_text)
            if yes:
                for package in self.packages_scrollable.get():
                    print(f'{constants.PACKAGES_PATH}/{package}')
                    shutil.rmtree(f'{constants.PACKAGES_PATH}/{package}')
                self.add_packages_frame()
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
                self.add_packages_frame()
        else:
            mb.showerror('Error', 'Package already exists')

    def _open_text_window(self, package, operation):
        EditFileWindow(self, package=package, operation=operation,
                       provisions_configs=self.provisions_configs)

    def set_configs(self):
        from gui.views.vagrantview.vagrantconfigsview import VagrantConfigsFrame
        vagrant_configs_view = VagrantConfigsFrame(
            master=self.master,
            provisions_configs=self.provisions_configs
        )
        vagrant_configs_view.grid(row=0, column=1,
                                  columnspan=self.master.columns-1,
                                  rowspan=self.master.rows,
                                  sticky='wens')

    def build(self):
        try:
            provisions_configs_reader = ProvisionConfigReader(
                self.provisions_configs,
            )
            provisions_configs_reader.check_packages_existence_for()

            provisions_configs_reader.check_package_upload_files_existence()
            provisions_configs_reader.check_upload_file_name_duplicates()
            provisions_configs_reader.check_custom_script_existence()
            provisions_configs_reader.check_update_upgrade_type()
            provisions_configs_reader.check_if_clean_is_selected()
            vagrant_builder = Vagrant(self.provisions_configs)
            vagrant_builder.set_configs()
            vagrant_builder.set_provisions()
            vagrant_builder.set_credentials()
            vagrant_builder.create_project_folder()
            vagrant_builder.generate_main_file()
            info = mb.showinfo(
                title='Well done!',
                message=(
                    f'Your new "{self.provisions_configs["configurations"]["project_name"]}" machine '
                    'was succesfully created'
                )
            )
            if info == 'ok':
                exit()
        except (
            NoFileToUploadError,
            PackageNotFoundError,
            EmptyScriptError,
            UploadNameConflictError
        ) as error:
            mb.showerror('Error', error.msg)

    def _add_to_operation(self, opearation: str):
        for package in self.packages_scrollable.get():
            self.provisions_configs["provisions"][f"packages_to_{opearation}"].add(package)
        self.add_selected_packages_frame()
