import constants
import os
import shutil
import customtkinter as ctk
from builder.vagrant import Vagrant
from cli.provisionsreader import ProvisionConfigReader
from cli.newpackage import make_package_folder
from tkinter import messagebox as mb
from tkinter import filedialog, StringVar
from builder.helper import is_empty_script
from builder.error import (
    NoFileToUploadError,
    PackageNotFoundError,
    EmptyScriptError,
    UploadNameConflictError
)
from gui.views.utilsview import ScrollableCheckboxFrame


class TextWindowView(ctk.CTkToplevel):
    def __init__(self, master, package, operation, provisions_configs):
        self.master = master
        self.package = package
        self.operation = operation
        self.provisions_configs = provisions_configs
        ctk.CTkToplevel.__init__(self, master)
        self.geometry(
            '400x400'
        )
        self.set_grid()
        file_label = ctk.CTkLabel(
            self,
            text=f'You are modifying "{operation}.sh"\nfrom package "{package}"'
        )
        file_label.grid(row=1, column=0, columnspan=3)
        self.open_text_box = ctk.CTkTextbox(self, width=600)
        with open(f'{constants.PACKAGES_PATH}/{package}/{operation}.sh') as file:
            text = file.read()
        self.open_text_box.insert('end', text)
        self.open_text_box.grid(row=2, column=0, columnspan=3)

        if self.operation == 'config':
            upload_button = ctk.CTkButton(
                self,
                text='Upload',
                command=self.upload_file
            )
            upload_button.grid(row=3, column=0)
            save_button = ctk.CTkButton(
                self,
                text='Save',
                command=self.save_file
            )
            save_button.grid(row=3, column=2)
        else:
            save_button = ctk.CTkButton(
                self,
                text='Save',
                command=self.save_file
            )
            save_button.grid(row=3, column=1)
        remove_button = ctk.CTkButton(
            self,
            text=f'Remove from {operation}',
            command=self.remove_from_opemainration
        )
        remove_button.grid(row=4, column=1)

    def set_grid(self):
        self.grid()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

    def save_file(self):
        with open(f'{constants.PACKAGES_PATH}/{self.package}/{self.operation}.sh', 'w') as file:
            file.write(self.open_text_box.get("1.0", "end"))
        self.master.add_vagrant_provisions_frame()
        self.destroy()

    def remove_from_operation(self):
        self.provisions_configs["provisions"][f'packages_to_{self.operation}'].remove(self.package)
        self.master.add_vagrant_provisions_frame()
        self.destroy()

    def upload_file(self):
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
        self.destroy()


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
        TextWindowView(self.master, operation=self.radio_var.get(),
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

        install_label = ctk.CTkLabel(
            selected_packages_frame,
            text='Install',
            font=self.font_std
        )
        install_label.grid(row=0, column=0, sticky='wn',
                           padx=self.padx_std, pady=self.pady_entry)
        uninstall_label = ctk.CTkLabel(
            selected_packages_frame,
            text='Uninstall',
            font=self.font_std
        )
        uninstall_label.grid(row=0, column=1, sticky='wn',
                             padx=self.padx_std, pady=self.pady_entry)
        config_label = ctk.CTkLabel(
            selected_packages_frame,
            text='Config',
            font=self.font_std
        )
        config_label.grid(row=0, column=2, sticky='wn',
                          padx=self.padx_std, pady=self.pady_entry)

        # add rows dinamically
        for operation in ('install', 'uninstall', 'config'):
            if operation == 'install':
                column_position = 0
            elif operation == 'uninstall':
                column_position = 1
            elif operation == 'config':
                column_position = 2
            if self.provisions_configs["provisions"][f'packages_to_{operation}']:
                for count, package in enumerate(self.provisions_configs["provisions"][f'packages_to_{operation}']):
                    row = 8 + count + 1
                    color = '#3996D5'
                    package_is_empty = is_empty_script(f'{constants.PACKAGES_PATH}/{package}/{operation}.sh')
                    if package_is_empty:
                        color = 'red'
                    package_button = ctk.CTkButton(
                        master=self,
                        text=f'{package}',
                        fg_color=color,
                        command=lambda args=(package, operation): self.open_text_window(*args)
                    )
                    package_button.grid(row=row, column=column_position)

    def add_packages_frame(self):
        packages_frame = ctk.CTkFrame(self)
        packages_frame.grid(row=1, column=1, rowspan=4, sticky='wens',
                            padx=self.padx_std, pady=self.pady_std,
                            ipadx=self.ipadx_std,
                            ipady=self.ipady_std)
        packages_frame.columnconfigure(0, weight=1)
        packages_frame.columnconfigure(1, weight=1)
        packages_frame.rowconfigure(0, weight=5)
        packages_frame.rowconfigure(1, weight=1)
        packages_frame.rowconfigure(2, weight=1)
        packages_frame.rowconfigure(3, weight=1)

        # add scrollable checkbox
        packages_scrollable = ScrollableCheckboxFrame(
            master=packages_frame,
            title='Packages',
            values=sorted([
                package for package in os.listdir(f'{constants.PACKAGES_PATH}')
                if package not in ('program-example', 'setup_scripts')
            ])
        )
        packages_scrollable.grid(row=0, column=0, columnspan=2, sticky='wens',
                                 padx=self.padx_std, pady=self.pady_std)

        # add new package
        new_package_label = ctk.CTkLabel(
            packages_frame,
            text='New package:',
            font=self.font_std
        )
        new_package_label.grid(row=1, column=0, sticky='w',
                               padx=self.padx_std, pady=self.pady_std,
                               ipadx=self.ipadx_std)
        self.new_package_entry = ctk.CTkEntry(
            packages_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std
        )
        self.new_package_entry.grid(row=2, column=0, columnspan=2, sticky='wne',
                               padx=self.padx_std, pady=self.pady_std)

        add_package_button = ctk.CTkButton(
            packages_frame,
            text='Add',
            font=self.font_std,
            width=self.width_button_std,
            command=self._add_package
        )
        add_package_button.grid(row=3, column=0,
                                padx=self.padx_std, pady=self.pady_std,
                                ipadx=self.ipadx_button,
                                ipady=self.ipady_button)
        delete_package_button = ctk.CTkButton(
            packages_frame,
            text='Delete',
            font=self.font_std,
            width=self.width_button_std
        )
        delete_package_button.grid(row=3, column=1,
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
            width=self.width_button_std
        )
        build_button.grid(row=0, column=1,
                          padx=self.padx_std, pady=self.pady_std,
                          ipadx=self.ipadx_button,
                          ipady=self.ipady_button)

    def _save_packages(self, operation: str):
        packages = list()
        for pack in self.packages_listbox.curselection():
            packages.append(
                self.packages_listbox.get(pack)
            )
        for package in packages:
            self.provisions_configs["provisions"][f"packages_to_{operation}"].add(package)
        self.master.add_vagrant_provisions_frame()

    def _delete_packages(self):
        packages_to_delete = ()
        for pack in self.packages_listbox.curselection():
            packages_to_delete += (self.packages_listbox.get(pack),)
        if packages_to_delete:
            warning_text = 'This operation is irreversible.\nYou choose to delete:\n'
            for package in packages_to_delete:
                warning_text += f'\t- {package}\n'
            warning_text += 'Confirm?'
            yes = mb.askyesno('Confirm Delete', warning_text)
            if yes:
                for package in packages_to_delete:
                    shutil.rmtree(f'{constants.PACKAGES_PATH}/{package}')
                self.master.add_vagrant_provisions_frame()
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

    def open_text_window(self, package, operation):
        TextWindowView(self.master, package=package, operation=operation,
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
