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
from gui.views.provisionsview import ProvisionsFrame
from tkinter import filedialog
from tkinter import messagebox as mb


class VagrantProvisionsView(ProvisionsFrame):

    def __init__(self, master, provisions_configs):
        self.provisions_frame = super()
        self.provisions_frame.__init__(
            master=master,
            provisions_configs=provisions_configs,
            title='Vagrant'
        )

    def set_std_dimensions(self):
        self.provisions_frame.set_std_dimensions()

    def set_grid(self):
        self.provisions_frame.set_grid()

    def render(self):
        self.provisions_frame.render()

    def add_bottom_button_frame(self):
        self.provisions_frame.add_bottom_button_frame()

    def set_configs(self):
        from gui.views.vagrantview.vagrantconfigsview import VagrantConfigsView
        vagrant_configs_view = VagrantConfigsView(
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
        dst.write(json.dumps(self.provisions_configs, indent=2))
        dst.close()

    def build(self):
        try:
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
                        f'Your new "{self.provisions_configs["configurations"]["project_name"]["default"]}" machine '
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
