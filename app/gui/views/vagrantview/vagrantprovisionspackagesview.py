import constants
import os
import shutil
import customtkinter as ctk
import json
from builder.vagrant import Vagrant
from cli.provisionsreader import ProvisionConfigReader
from cli.newpackage import make_package_folder
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
from PIL import Image
from tkinter import filedialog
from tkinter import messagebox as mb
from tkinter import StringVar


class VagrantProvisionsPackagesFrame(ctk.CTkFrame):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        ctk.CTkFrame.__init__(self, master)
        self.family = 'Sans'
        self.title_std = ctk.CTkFont(family=self.master.family, size=30,
                                     weight='bold')
        self.little_title = ctk.CTkFont(family=self.master.family, size=20,
                                        weight='bold')
        self.font_std = ctk.CTkFont(family=self.master.family, size=20)
        self.set_std_dimensions()
        self.set_grid()
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
        self.pad_left = (10, 5)
        self.pad_right = (5, 10)
        self.pad_equal = (5, 5)
        self.ipadx_std = 10
        self.ipady_std = 10
        self.ipadx_button = 5
        self.ipady_button = 5
        self.entry_height_std = 50
        self.entry_width_std = 300
        self.width_button_std = 100
        self.padx_btn_right = (0, 5)
        self.padx_btn_left = (5, 0)

    def set_grid(self):
        self.grid()
        self.columnconfigure(0, weight=20)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

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
        self.additional_scripts_frame.rowconfigure(5, weight=1)
        self.additional_scripts_frame.grid_propagate(False)

        additional_scripts_label = ctk.CTkLabel(
            self.additional_scripts_frame,
            text='Additional Scripts',
            font=self.little_title
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
                                 padx=self.padx_std, pady=self.pady_std)

        self.update_upgrade_full = ctk.CTkRadioButton(
            self.additional_scripts_frame,
            text="Update upgrade full",
            variable=self.radio_var,
            value='update_upgrade_full',
            command=self._add_edit_button,
            font=self.font_std
        )
        self.update_upgrade_full.grid(row=2, column=0, sticky='w',
                                      padx=self.padx_std, pady=self.pady_std)
        self.update_upgrade_full = ctk.CTkRadioButton(
            self.additional_scripts_frame,
            text="None",
            variable=self.radio_var,
            value=None,
            font=self.font_std,
            command=self._remove_edit_button
        )
        self.update_upgrade_full.grid(row=3, column=0, sticky='w',
                                      padx=self.padx_std, pady=self.pady_std)

        # add checkbox for clean packages
        self.clean_var = StringVar()
        provisions = self.provisions_configs["provisions"]
        default_clean_var = 'clean_packages' if provisions["clean_packages"] else ''
        self.clean_var.set(default_clean_var)
        clean_button = ctk.CTkCheckBox(
            self.additional_scripts_frame,
            text="Clean packages",
            variable=self.clean_var,
            onvalue='clean_packages',
            offvalue='',
            height=1,
            width=15,
            font=self.font_std,
            command=self._check_checkbox_clean_status
        )
        clean_button.grid(row=4, column=0, sticky='w',
                          padx=self.padx_std, pady=self.pady_std)
        if self.clean_var.get():
            self._add_edit_clean_button()

        # add checkbox for reboot
        self.reboot = StringVar()
        provisions = self.provisions_configs["provisions"]
        default_reboot_var = 'reboot' if provisions["reboot"] else ''
        self.reboot.set(default_reboot_var)
        reboot_checkbox = ctk.CTkCheckBox(
            self.additional_scripts_frame,
            text="Reboot",
            variable=self.reboot,
            onvalue='reboot',
            offvalue='',
            height=1,
            width=15,
            font=self.font_std,
            command=self._check_checkbox_reboot_status
        )
        reboot_checkbox.grid(row=5, column=0, sticky='w',
                             padx=self.padx_std, pady=self.pady_std)
        if self.reboot.get():
            self._add_edit_reboot_button()

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
            command=lambda: self._edit_additional_script(self.radio_var)
        )
        self.edit_upgrade_button.grid(row=row, column=1)

    def _remove_edit_button(self):
        try:
            self.edit_upgrade_button.destroy()
        except (AttributeError, ValueError):
            pass

    def _check_checkbox_clean_status(self):
        if self.clean_var.get():
            self.provisions_configs["provisions"]["clean_packages"] = True
            self._add_edit_clean_button()
        else:
            self.provisions_configs["provisions"]["clean_packages"] = False
            self.edit_clean_button.destroy()

    def _check_checkbox_reboot_status(self):
        if self.reboot.get():
            self.provisions_configs["provisions"]["reboot"] = True
            self._add_edit_reboot_button()
        else:
            self.provisions_configs["provisions"]["reboot"] = False
            self.edit_reboot_button.destroy()

    def _add_edit_clean_button(self):
        self.edit_clean_button = ctk.CTkButton(
            self.additional_scripts_frame,
            text='Edit',
            font=self.font_std,
            width=self.width_button_std,
            command=lambda: self._edit_additional_script(self.clean_var)
        )
        self.edit_clean_button.grid(row=4, column=1)

    def _add_edit_reboot_button(self):
        self.edit_reboot_button = ctk.CTkButton(
            self.additional_scripts_frame,
            text='Edit',
            font=self.font_std,
            width=self.width_button_std,
            command=lambda: self._edit_additional_script(self.reboot)
        )
        self.edit_reboot_button.grid(row=5, column=1)

    def _edit_additional_script(self, variable):
        SetUpScriptEdit(self, variable=variable,
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

        selected_packages_label = ctk.CTkLabel(
            selected_packages_frame,
            text='Selected Packages',
            font=self.little_title
        )
        selected_packages_label.grid(row=0, column=0, columnspan=3, sticky='w',
                                     padx=self.padx_std, pady=self.pady_std)

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
            clean_button.grid(row=2, column=count,
                              pady=self.pady_std,
                              ipadx=self.ipadx_button,
                              ipady=self.ipady_button)

    def _clean_packages(self, operation: str):
        self.provisions_configs["provisions"][f"packages_to_{operation}"] = set()
        self.add_selected_packages_frame()

    def add_packages_frame(self, select_all=False):
        self.packages_frame = ctk.CTkFrame(self)
        self.packages_frame.grid(row=1, column=1, rowspan=4, sticky='wens',
                            padx=self.padx_std, pady=self.pady_std,
                            ipadx=self.ipadx_std,
                            ipady=self.ipady_std)
        self.packages_frame.columnconfigure(0, weight=1)
        self.packages_frame.columnconfigure(1, weight=1)
        self.packages_frame.columnconfigure(2, weight=1)
        self.packages_frame.rowconfigure(0, weight=1)
        self.packages_frame.rowconfigure(1, weight=1)
        self.packages_frame.rowconfigure(2, weight=10)
        self.packages_frame.rowconfigure(3, weight=1)
        self.packages_frame.rowconfigure(4, weight=1)
        self.packages_frame.rowconfigure(5, weight=1)

        # add frame title
        packages_label = ctk.CTkLabel(
            self.packages_frame,
            text='Packages Manager',
            font=self.little_title
        )
        packages_label.grid(row=0, column=0, columnspan=3, sticky='w',
                            padx=self.padx_std, pady=self.pady_title)
        # add install, uninstall, config
        add_to_install_button = ctk.CTkButton(
            self.packages_frame,
            text='Install',
            font=self.font_std,
            width=self.width_button_std,
            command=lambda: self._add_to_operation('install')
        )
        add_to_install_button.grid(row=1, column=0,
                                   padx=self.pad_left, pady=self.pady_std,
                                   ipadx=self.ipadx_button,
                                   ipady=self.ipady_button)
        add_to_uninstall_button = ctk.CTkButton(
            self.packages_frame,
            text='Uninstall',
            font=self.font_std,
            width=self.width_button_std,
            command=lambda: self._add_to_operation('uninstall')
        )
        add_to_uninstall_button.grid(row=1, column=1,
                                     padx=self.pad_equal, pady=self.pady_std,
                                     ipadx=self.ipadx_button,
                                     ipady=self.ipady_button)
        add_to_config_button = ctk.CTkButton(
            self.packages_frame,
            text='Configure',
            font=self.font_std,
            width=self.width_button_std,
            command=lambda: self._add_to_operation('config')
        )
        add_to_config_button.grid(row=1, column=2,
                                  padx=self.pad_right, pady=self.pady_std,
                                  ipadx=self.ipadx_button,
                                  ipady=self.ipady_button)

        # add scrollable checkbox
        self.packages_scrollable = ScrollableCheckboxFrame(
            master=self.packages_frame,
            title='Packages',
            values=sorted([
                package for package in os.listdir(f'{constants.PACKAGES_PATH}')
                if package not in ('program-example', 'setup_scripts')
            ]),
            select_all=select_all
        )
        self.packages_scrollable.grid(row=2, column=0, columnspan=3,
                                      sticky='wens',
                                      padx=self.padx_std, pady=self.pady_std)
        self.packages_scrollable.bind("<Motion>", self._check_package_selected)
        self.packages_scrollable.bind("<Leave>", self._check_package_selected)


        self.new_package_subframe()

        if self.packages_scrollable.get():
            deselect_all_button = ctk.CTkButton(
                self.packages_frame,
                text='Deselect All',
                font=self.font_std,
                width=self.width_button_std,
                command=self.add_packages_frame
            )
            deselect_all_button.grid(row=5, column=0,
                                     padx=self.pad_equal, pady=self.pady_std,
                                     ipadx=self.ipadx_button,
                                     ipady=self.ipady_button)
        else:
            select_all_button = ctk.CTkButton(
                self.packages_frame,
                text='Select All',
                font=self.font_std,
                width=self.width_button_std,
                command=lambda: self.add_packages_frame(select_all=True)
            )
            select_all_button.grid(row=5, column=0,
                                   padx=self.pad_equal, pady=self.pady_std,
                                   ipadx=self.ipadx_button,
                                   ipady=self.ipady_button)
        self.delete_package_button = ctk.CTkButton(
            self.packages_frame,
            text='Delete',
            font=self.font_std,
            width=self.width_button_std,
            command=self._delete_packages,
            state='disabled'
        )
        self.delete_package_button.grid(row=5, column=2,
                                   padx=self.pad_right, pady=self.pady_std,
                                   ipadx=self.ipadx_button,
                                   ipady=self.ipady_button)

    def _check_package_selected(self, e):
        print("hello")
        if self.packages_scrollable.get():
            self.delete_package_button.configure(state='normal')
        else:
            self.delete_package_button.configure(state='disabled')

    def add_bottom_button_frame(self):
        bottom_button_frame = ctk.CTkFrame(self)
        bottom_button_frame.grid(row=5, column=1, sticky='wens',
                                 padx=self.padx_std, pady=self.pady_std,
                                 ipadx=self.ipadx_std,
                                 ipady=self.ipady_std)
        bottom_button_frame.columnconfigure(0, weight=1)
        bottom_button_frame.columnconfigure(1, weight=1)
        bottom_button_frame.columnconfigure(2, weight=1)
        bottom_button_frame.rowconfigure(0, weight=1)
        set_configs_button = ctk.CTkButton(
            bottom_button_frame,
            text='Set Configs',
            font=self.font_std,
            width=self.width_button_std,
            command=self.set_configs,
        )
        set_configs_button.grid(row=0, column=0,
                                padx=self.pad_left, pady=self.pady_std,
                                ipadx=self.ipadx_button,
                                ipady=self.ipady_button)

        save_button = ctk.CTkButton(
            bottom_button_frame,
            text='Save',
            font=self.font_std,
            width=self.width_button_std,
            command=self._save,
        )
        save_button.grid(row=0, column=1,
                         padx=self.pad_equal, pady=self.pady_std,
                         ipadx=self.ipadx_button,
                         ipady=self.ipady_button)

        build_button = ctk.CTkButton(
            bottom_button_frame,
            text='Build',
            font=self.font_std,
            width=self.width_button_std,
            command=self.build
        )
        build_button.grid(row=0, column=2,
                          padx=self.pad_right, pady=self.pady_std,
                          ipadx=self.ipadx_button,
                          ipady=self.ipady_button)

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

    def _active_add_package(self, e):
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

    def _save(self):
        project_name = self.provisions_configs["configurations"]["project_name"]
        for operation in ('install', 'uninstall', 'config'):
            self.provisions_configs["provisions"][f"packages_to_{operation}"] = list(
                self.provisions_configs["provisions"][f"packages_to_{operation}"]
            )
        dst = filedialog.asksaveasfile(
            initialdir=constants.VAGRANT_PROVS_CONFS_PATH,
            initialfile=f'{project_name}.json',
            defaultextension='.json'
        )
        dst.write(json.dumps(self.provisions_configs, indent=2))
        dst.close()

    def build(self):
        try:
            project_name = self.provisions_configs["configurations"]["project_name"]
            if project_name in os.listdir(constants.VAGRANT_MACHINES_PATH):
                mb.showwarning(
                    title='Project name duplicate',
                    message=(
                        f'A project with the name "{project_name}" already exists.\n'
                        'If you build this project you will override the old one.'
                    )
                )
            vbox_name = self.provisions_configs["configurations"]["vbox_name"]
            if vbox_name in self.master.vbox_list:
                mb.showerror('Error', f'A box with the name "{vbox_name}" already exists!')
            else:
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
                mb.showinfo(
                    title='Well done!',
                    message=(
                        f'Your new "{self.provisions_configs["configurations"]["project_name"]}" machine '
                        'was succesfully created'
                    )
                )
                self.master.add_lateral_menu()
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

    def new_package_subframe(self):
        # add new package sub frame
        new_package_subframe = ctk.CTkFrame(
            self.packages_frame,
            width=500,
            height=60,
            fg_color='transparent'
        )
        new_package_subframe.grid(row=4, column=0, columnspan=3, sticky='w',
                                  padx=self.padx_std, pady=self.pady_entry)
        new_package_subframe.grid_propagate(False)
        new_package_subframe.columnconfigure(0, weight=10)
        new_package_subframe.columnconfigure(1, weight=1)
        new_package_subframe.rowconfigure(0, weight=1)
        self.new_package_entry = ctk.CTkEntry(
            new_package_subframe,
            font=self.font_std,
            width=450,
            height=self.entry_height_std,
            placeholder_text='Insert New Package Name'
        )
        self.new_package_entry.grid(row=0, column=0, sticky='e',
                                    padx=(0, 0), pady=(0, 0))
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
            new_package_subframe,
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
        self.add_package_button.grid(row=0, column=1, sticky='w',
                                padx=(0, 0), pady=(0, 0),
                                ipadx=0,
                                ipady=0)
