import constants
import os
import customtkinter as ctk
import json
from argumentparser.helper import get_local_vagrant_boxes
from builder.vagrant import Vagrant
from cli.provisionsreader import ProvisionConfigReader
from builder.error import (
    NoFileToUploadError,
    PackageNotFoundError,
    EmptyScriptError,
    UploadNameConflictError
)
from gui.widgets.additionalscriptwidget import AdditionalScriptWidget
from gui.widgets.packagemanagerwidget import PackageManagerWidget
from gui.widgets.titlewidget import TitleWidget
from existencecontroller.controller import launch_vboxmanage_lst_command
from tkinter import filedialog
from tkinter import messagebox as mb


class VagrantProvisionsPackagesFrame(ctk.CTkFrame):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        self.vbox_list = launch_vboxmanage_lst_command()
        self.local_vagrant_boxes = get_local_vagrant_boxes()
        ctk.CTkFrame.__init__(self, master)
        self.family = 'Sans'
        self.title_std = ctk.CTkFont(
            family=self.master.family,
            size=30,
            weight='bold'
        )
        self.little_title = ctk.CTkFont(
            family=self.master.family,
            size=20,
            weight='bold'
        )
        self.font_std = ctk.CTkFont(family=self.master.family, size=18)
        self.set_std_dimensions()
        self.set_grid()
        self.title_frame = TitleWidget(
            self,
            title='Vagrant',
            subtitle='Provisions'
        )
        self.package_manager_frame = PackageManagerWidget(
            self,
            self.provisions_configs
        )
        self.additional_scripts_frame = AdditionalScriptWidget(
            self,
            self.provisions_configs
        )
        self.add_bottom_button_frame()
        self.render()

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
        self.sticky_title = 'wn'
        self.sticky_label = 'ws'
        self.sticky_entry = 'wn'
        self.sticky_frame = 'wens'
        self.sticky_optionmenu = 'w'
        self.sticky_warningmsg = 'e'
        self.sticky_horizontal = 'ew'

    def set_grid(self):
        # self.grid()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

    def render(self):
        self.title_frame.grid(
            row=0,
            column=0,
            rowspan=2,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_frame,
        )
        self.package_manager_frame.grid(
            row=2,
            column=0,
            rowspan=3,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame,
        )
        self.additional_scripts_frame.grid(
            row=5,
            column=0,
            rowspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame,
        )
        self.bottom_button_frame.grid(
            row=5,
            column=1,
            rowspan=2,
            sticky=self.sticky_frame,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
        )

    def add_bottom_button_frame(self):
        self.bottom_button_frame = ctk.CTkFrame(
            self,
            fg_color='transparent',
        )
        # The order here is important.
        # Do not change the order between build, save, and set configs
        build_button = ctk.CTkButton(
            master=self.bottom_button_frame,
            text='Build',
            font=self.font_std,
            width=self.width_button_std,
            command=self.build
        )
        build_button.pack(
            side='right',
            anchor='se',
            padx=self.pad_right,
            pady=self.pady_std,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        save_button = ctk.CTkButton(
            master=self.bottom_button_frame,
            text='Save',
            font=self.font_std,
            width=self.width_button_std,
            command=self._save
        )
        save_button.pack(
            side='right',
            anchor='se',
            padx=self.pad_equal,
            pady=self.pady_std,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        set_configs_button = ctk.CTkButton(
            master=self.bottom_button_frame,
            text='Set Configs',
            font=self.font_std,
            width=self.width_button_std,
            command=self.set_configs
        )
        set_configs_button.pack(
            side='right',
            anchor='se',
            padx=self.pad_left,
            pady=self.pady_std,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )

    def set_configs(self):
        from gui.views.vagrantview.vagrantconfigsview import VagrantConfigsFrame
        vagrant_configs_view = VagrantConfigsFrame(
            master=self.master,
            provisions_configs=self.provisions_configs
        )
        vagrant_configs_view.grid(
            row=0,
            column=1,
            columnspan=self.master.columns-1,
            rowspan=self.master.rows,
            sticky=self.sticky_frame
        )

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
            if vbox_name in self.vbox_list:
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
