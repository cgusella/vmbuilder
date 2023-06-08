import constants
import customtkinter as ctk
import os
from gui.widgets.vboxconfigswidget import VboxConfigsWidget
from gui.widgets.isowidget import IsoWidget
from gui.widgets.titlewidget import TitleWidget
from gui.widgets.projectnamewidget import PackerProjectNameWidget
from gui.views.packerview.packerprovisionsview import PackerProvisionsView


class PackerConfigsFrame(ctk.CTkFrame):

    def __init__(self, master, provisions_configs: dict):
        self.master = master
        self.provisions_configs = provisions_configs
        ctk.CTkFrame.__init__(self, master)
        self.title_std = ctk.CTkFont(family=self.master.family, size=30,
                                     weight='bold')
        self.font_std = ctk.CTkFont(family=self.master.family, size=18)
        self.set_grid()
        self.set_std_dimensions()
        self.add_title()
        self.add_project_name()
        self.add_disk_name()
        self.add_preseed_frame()
        self.add_iso_frame()
        self.add_vbox_configs()
        self.add_set_provisions_button()
        self.render()

    def set_grid(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)
        self.pady_title = (10, 2)
        self.pady_entry = (2, 10)
        self.ipadx_std = 10
        self.ipady_std = 10
        self.width_button_std = 100
        self.entry_height_std = 50
        self.entry_width_std = 280
        self.sticky_label = 'w'
        self.sticky_entry = 'w'
        self.sticky_frame = 'wens'

    def add_title(self):
        self.title_widget = TitleWidget(
            master=self,
            title='Packer',
            subtitle='Configurations'
        )

    def add_project_name(self):
        self.project_name_frame = PackerProjectNameWidget(
            master=self,
            provisions_configs=self.provisions_configs
        )

    def add_disk_name(self):
        self.disk_name_frame = ctk.CTkFrame(self)

        disk_name_label = ctk.CTkLabel(
            self.disk_name_frame,
            text='Insert Disk Name',
            font=self.font_std
        )
        disk_name_label.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_label
        )

        self.disk_name_entry = ctk.CTkEntry(
            self.disk_name_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std,
            placeholder_text='Disk Name'
        )
        if self.provisions_configs["configurations"]["disk_name"]["default"]:
            self.disk_name_entry.insert(
                0,
                self.provisions_configs["configurations"]["disk_name"]["default"]
            )
        self.disk_name_entry.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_entry
        )

    def add_preseed_frame(self):
        self.preseed_frame = ctk.CTkFrame(self)
        self.preseed_frame.rowconfigure(0, weight=1)
        self.preseed_frame.rowconfigure(1, weight=1)

        select_preseed_label = ctk.CTkLabel(
            master=self.preseed_frame,
            text='Select Preseed File',
            font=self.font_std
        )
        select_preseed_label.grid(
            row=0,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )

        self.preseed_files_option = ctk.CTkOptionMenu(
            master=self.preseed_frame,
            font=self.font_std,
            width=self.entry_width_std,
            values=os.listdir(constants.PACKER_PRESEEDS_PATH)
        )
        if self.provisions_configs["configurations"]["preseed_file"]["default"]:
            self.preseed_files_option.set(
                self.provisions_configs["configurations"]["preseed_file"]["default"]
            )
        self.preseed_files_option.grid(
            row=1,
            column=0,
            sticky='w',
            padx=self.padx_std,
            pady=self.pady_entry
        )

    def add_iso_frame(self):
        self.iso_frame = IsoWidget(
            self,
            self.provisions_configs
        )

    def add_vbox_configs(self):
        """Add entries for cpus, memory, disk size"""
        self.vbox_configs_frame = VboxConfigsWidget(
            master=self,
            provisions_configs=self.provisions_configs
        )

    def add_set_provisions_button(self):
        self.set_packer_provisions_button = ctk.CTkButton(
            self,
            text='Set Provisions',
            width=self.width_button_std,
            font=self.font_std,
            command=self._save_and_pass_to_provisions
        )

    def _save_and_pass_to_provisions(self):
        configs = self.provisions_configs["configurations"]
        configs["project_name"]["default"] = self.project_name_frame.project_name_entry.get()
        configs["vbox_name"]["default"] = self.vbox_configs_frame.vbox_name_entry.get()
        configs["cpus"]["default"] = self.vbox_configs_frame.cpus_slider.get()
        configs["memory"]["default"] = self.vbox_configs_frame.memory_slider.get()
        configs["disk_size"]["default"] = self.vbox_configs_frame.disk_slider.get()
        configs["disk_name"]["default"] = self.disk_name_entry.get()
        configs["iso_file"]["default"] = self.iso_frame.iso_file_entry.get()
        configs["iso_link"]["default"] = self.iso_frame.iso_link_entry.get()
        configs["checksum"]["default"] = (
            f'{self.iso_frame.checksum_algorithm.get()}:{self.iso_frame.checksum_entry.get()}'
        )
        configs["preseed_file"]["default"] = self.preseed_files_option.get()
        packer_provisions_view = PackerProvisionsView(
            self.master,
            self.provisions_configs
        )
        packer_provisions_view.grid(
            row=0,
            column=1,
            rowspan=self.master.rows,
            columnspan=self.master.columns-1,
            sticky=self.sticky_frame
        )

    def render(self):
        self.title_widget.grid(
            row=0,
            column=0,
            columnspan=2,
            rowspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_frame
        )
        self.project_name_frame.grid(
            row=1,
            column=0,
            sticky=self.sticky_frame,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std
        )
        self.disk_name_frame.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )
        self.preseed_frame.grid(
            row=3,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )
        self.iso_frame.grid(
            row=4,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )
        self.vbox_configs_frame.grid(
            row=1,
            column=1,
            rowspan=3,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )
        self.set_packer_provisions_button.grid(
            row=0,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky='se'
        )
