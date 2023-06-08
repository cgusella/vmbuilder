import abc
import customtkinter as ctk
import constants
import os
import json
from builder.vagrant import Vagrant
from cli.provisionsreader import ProvisionConfigReader
from builder.error import (
    NoFileToUploadError,
    PackageNotFoundError,
    EmptyScriptError,
    UploadNameConflictError
)
from tkinter import filedialog
from tkinter import messagebox as mb


class MainButtonsWidget(abc.ABC, ctk.CTkFrame):

    def __init__(self, master, provisions_configs, wanted_buttons: list):
        self.provisions_configs = provisions_configs
        self.master = master
        ctk.CTkFrame.__init__(self, master, fg_color='transparent')
        self.font_std = ctk.CTkFont(family='Sans', size=18)
        self.set_std_dimensions()
        # The order here is important.
        # Do not change the order between build, save, and set configs
        build_button = ctk.CTkButton(
            master=self,
            text='Build',
            font=self.font_std,
            width=self.width_button_std,
            command=self._build
        )
        build_button.pack(
            side='right',
            anchor='ne',
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        save_button = ctk.CTkButton(
            master=self,
            text='Save',
            font=self.font_std,
            width=self.width_button_std,
            command=self._save
        )
        save_button.pack(
            side='right',
            anchor='ne',
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        if 'configs' in wanted_buttons:
            set_configs_button = ctk.CTkButton(
                master=self,
                text='Set Configs',
                font=self.font_std,
                width=self.width_button_std,
                command=self._save_state_and_go_to_configs
            )
            set_configs_button.pack(
                side='right',
                anchor='ne',
                padx=self.padx_std,
                pady=self.pady_std,
                ipadx=self.ipadx_button,
                ipady=self.ipady_button
            )
        if 'provisions' in wanted_buttons:
            set_provision_button = ctk.CTkButton(
                master=self,
                text='Set Provisions',
                command=self._save_state_and_go_to_provisions,
                font=self.font_std
            )
            set_provision_button.pack(
                side='right',
                anchor='ne',
                padx=self.padx_std,
                pady=self.pady_std,
                ipadx=self.ipadx_button,
                ipady=self.ipady_button
            )
        if 'networks' in wanted_buttons:
            set_network_button = ctk.CTkButton(
                master=self,
                text='Set Network',
                font=self.font_std,
                width=self.width_button_std,
                command=self._save_state_and_go_to_networks
            )
            set_network_button.pack(
                side='right',
                anchor='ne',
                padx=self.padx_std,
                pady=self.pady_std,
                ipadx=self.ipadx_button,
                ipady=self.ipady_button
            )

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)
        self.width_button_std = 40
        self.ipadx_button = 5
        self.ipady_button = 5
        self.sticky_frame = 'wens'

    @abc.abstractmethod
    def _save(self):
        pass

    @abc.abstractmethod
    def _build(self):
        pass

    @abc.abstractmethod
    def _save_state_and_go_to_configs(self):
        pass

    @abc.abstractmethod
    def _save_state_and_go_to_provisions(self):
        pass

    @abc.abstractmethod
    def _save_state_and_go_to_networks(self):
        pass


class VagrantMainButtons(MainButtonsWidget):

    def __init__(self, master, provisions_configs, wanted_buttons: list):
        self.main = master.master
        self.main_buttons = super()
        self.main_buttons.__init__(master, provisions_configs, wanted_buttons)

    def _save_state_and_go_to_configs(self):
        if self.master.frame_name == 'networks':
            pass
        elif self.master.frame_name == 'provisions':
            pass
        from gui.views.vagrantview.vagrantconfigsview import VagrantConfigsView
        new_vagrant_view = VagrantConfigsView(
            master=self.main,
            provisions_configs=self.provisions_configs
        )
        # self.master.master is the mainview
        new_vagrant_view.grid(
            row=0,
            column=1,
            columnspan=self.master.master.columns-1,
            rowspan=self.master.master.rows,
            sticky=self.master.master.sticky_frame
        )

    def _save_state_and_go_to_provisions(self):
        if self.master.frame_name == 'configs':
            self._save_configs_state()
        elif self.master.frame_name == 'networks':
            pass
        from gui.views.vagrantview.vagrantprovisionspackagesview import VagrantProvisionsView
        vagrant_configs_view = VagrantProvisionsView(
            master=self.main,
            provisions_configs=self.provisions_configs
        )
        vagrant_configs_view.grid(
            row=0,
            column=1,
            columnspan=self.main.columns-1,
            rowspan=self.main.rows,
            sticky=self.main.sticky_frame
        )

    def _save_state_and_go_to_networks(self):
        if self.master.frame_name == 'configs':
            self._save_configs_state()
        elif self.master.frame_name == 'provisions':
            pass
        from gui.views.vagrantview.vagrantnetworkview import VagrantNetworkView
        new_vagrant_view = VagrantNetworkView(
            master=self.main,
            provisions_configs=self.provisions_configs
        )
        new_vagrant_view.grid(
            row=0,
            column=1,
            columnspan=self.main.columns-1,
            rowspan=self.main.rows,
            sticky=self.main.sticky_frame
        )

    def _save_configs_state(self):
        project_name = self.master.project_name_frame.project_name_entry.get()
        vbox_name = self.master.vbox_configs_frame.vbox_name_entry.get()
        if not project_name:
            mb.showerror('Error', 'You must choose a name for the project!')
        elif not vbox_name:
            mb.showerror(
                'Error',
                'You must choose a name for the virtual box machine!')
        elif not self.master.vagrant_box_setup_frame.username_entry.get():
            mb.showerror(
                'Error',
                (
                    'You must specify the existing username of the vagrant '
                    'box for vagrant to be able to connect to the machine!'
                )
            )
        elif not self.master.vagrant_box_setup_frame.password_entry.get():
            mb.showerror(
                'Error',
                ('You must specify the password of the specified user for '
                    'vagrant to be able to connect to the machine!')
            )
        elif not self.master.vagrant_box_setup_frame.vagrant_box.get():
            mb.showerror('Error', 'You must choose a Vagrant box!')
        else:
            self.provisions_configs["configurations"]["project_name"]["default"] = project_name
            self.provisions_configs["configurations"]["vbox_name"]["default"] = vbox_name
            self.provisions_configs["configurations"]["hostname"]["default"] = self.master.vagrant_box_setup_frame.hostname_entry.get()
            self.provisions_configs["credentials"]["username"] = self.master.vagrant_box_setup_frame.username_entry.get()
            self.provisions_configs["credentials"]["password"] = self.master.vagrant_box_setup_frame.password_entry.get()
            self.provisions_configs["credentials"]["extra_user"] = self.master.vagrant_box_setup_frame.extra_user_entry.get()
            self.provisions_configs["configurations"]["image"]["default"] = self.master.vagrant_box_setup_frame.vagrant_box.get()
            self.provisions_configs["configurations"]["cpus"]["default"] = self.master.vbox_configs_frame.cpus_value.get()
            self.provisions_configs["configurations"]["memory"]["default"] = int(self.master.vbox_configs_frame.memory_slider.get())
            self.provisions_configs["configurations"]["disk_size"]["default"] = self.master.vbox_configs_frame.disk_slider_value.get()

    def _save(self):
        if self.master.frame_name == 'configs':
            self._save_configs_state()
        project_name = self.provisions_configs["configurations"]["project_name"]["default"]
        for operation in ('install', 'uninstall', 'config'):
            self.provisions_configs["provisions"][f"packages_to_{operation}"] = list(
                self.provisions_configs["provisions"][f"packages_to_{operation}"]
            )
        dst = filedialog.asksaveasfile(
            initialdir=constants.VAGRANT_PROVS_CONFS_PATH,
            initialfile=f'{project_name}.json',
            defaultextension='.json'
        )
        if dst:
            dst.write(json.dumps(self.provisions_configs, indent=2))
            dst.close()

    def _build(self):
        try:
            if self.master.frame_name == 'configs':
                self._save_configs_state()
            project_name = self.provisions_configs["configurations"]["project_name"]["default"]
            if project_name in os.listdir(constants.VAGRANT_MACHINES_PATH):
                mb.showwarning(
                    title='Project name duplicate',
                    message=(
                        f'A project with the name "{project_name}" already exists.\n'
                        'If you build this project you will override the old one.'
                    )
                )
            vbox_name = self.provisions_configs["configurations"]["vbox_name"]["default"]
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
                        f'Your new "{self.provisions_configs["configurations"]["project_name"]["default"]}" machine '
                        'was succesfully created'
                    )
                )
                self.main.add_lateral_menu()
        except (
            NoFileToUploadError,
            PackageNotFoundError,
            EmptyScriptError,
            UploadNameConflictError
        ) as error:
            mb.showerror('Error', error.msg)
