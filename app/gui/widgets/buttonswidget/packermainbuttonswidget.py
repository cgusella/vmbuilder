from gui.widgets.buttonswidget.mainbuttonswidget import MainButtonsWidget
import constants
import os
import json
from builder.packer import Packer
from cli.provisionsreader import ProvisionConfigReader
from builder.error import (
    NoFileToUploadError,
    PackageNotFoundError,
    EmptyScriptError,
    UploadNameConflictError
)
from tkinter import filedialog
from tkinter import messagebox as mb


class PackerMainButtons(MainButtonsWidget):

    def __init__(self, master, provisions_configs, wanted_buttons: list):
        self.main = master.master
        self.main_buttons = super()
        self.main_buttons.__init__(master, provisions_configs, wanted_buttons)

    def _save_state_and_go_to_configs(self):
        from gui.views.packerview.packerconfigsview import PackerConfigsFrame
        new_packer_view = PackerConfigsFrame(
            master=self.main,
            provisions_configs=self.provisions_configs
        )
        # self.master.master is the mainview
        new_packer_view.grid(
            row=0,
            column=1,
            columnspan=self.master.master.columns-1,
            rowspan=self.master.master.rows,
            sticky=self.master.master.sticky_frame
        )

    def _save_state_and_go_to_provisions(self):
        self._save_configs_state()
        from gui.views.packerview.packerprovisionsview import PackerProvisionsView
        packer_configs_view = PackerProvisionsView(
            master=self.main,
            provisions_configs=self.provisions_configs
        )
        packer_configs_view.grid(
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
        self.provisions_configs["configurations"]["project_name"]["default"] = project_name
        self.provisions_configs["configurations"]["vbox_name"]["default"] = vbox_name
        self.provisions_configs["configurations"]["cpus"]["default"] = self.master.vbox_configs_frame.cpus_value.get()
        self.provisions_configs["configurations"]["memory"]["default"] = int(self.master.vbox_configs_frame.memory_slider.get())
        self.provisions_configs["configurations"]["disk_size"]["default"] = self.master.vbox_configs_frame.disk_slider_value.get()
        self.provisions_configs["configurations"]["disk_name"]["default"] = self.master.disk_name_entry.get()
        self.provisions_configs["configurations"]["iso_file"]["default"] = self.master.iso_frame.iso_file_entry.get()
        self.provisions_configs["configurations"]["iso_link"]["default"] = self.master.iso_frame.iso_link_entry.get()
        self.provisions_configs["configurations"]["iso_checksum"]["default"] = (
            f'{self.master.iso_frame.iso_checksum_algorithm.get()}:{self.master.iso_frame.iso_checksum_entry.get()}'
        )
        self.provisions_configs["configurations"]["preseed_file"]["default"] = self.master.preseed_files_option.get()

    def _save(self):
        if self.master.frame_name == 'configs':
            self._save_configs_state()
        project_name = self.provisions_configs["configurations"]["project_name"]["default"]
        for operation in ('install', 'uninstall', 'config'):
            self.provisions_configs["provisions"][f"packages_to_{operation}"] = list(
                self.provisions_configs["provisions"][f"packages_to_{operation}"]
            )
        dst = filedialog.asksaveasfile(
            initialdir=constants.PACKER_PROVS_CONFS_PATH,
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
            if project_name in os.listdir(constants.PACKER_MACHINES_PATH):
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
                vagrant_builder = Packer(self.provisions_configs)
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
