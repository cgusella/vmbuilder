import constants
import customtkinter as ctk
import os
from gui.guistandard import GuiStandard
from gui.widgets.vboxconfigswidget import VboxConfigsWidget
from gui.widgets.isowidget import IsoWidget
from gui.widgets.titlewidget import TitleWidget
from gui.widgets.projectnamewidget import PackerProjectNameWidget
from gui.views.packerview.packerprovisionsview import PackerProvisionsView
from gui.widgets.buttonswidget.packermainbuttonswidget import PackerMainButtons


class PackerConfigsFrame(GuiStandard):

    def __init__(self, master, provisions_configs: dict):
        self.frame_name = 'configs'
        self.master = master
        self.provisions_configs = provisions_configs
        ctk.CTkFrame.__init__(self, master)
        self.set_fonts()
        self.set_std_dimensions()
        self.initialize_elements()
        self.render_elements()

    def set_fonts(self):
        family = 'Sans'
        self.title_std = ctk.CTkFont(family=family, size=30, weight='bold')
        self.font_std = ctk.CTkFont(family=family, size=18)

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)
        self.pady_title = (10, 2)
        self.pady_entry = (2, 10)
        self.ipadx_std = 10
        self.ipady_std = 10
        self.width_button_std = 100
        self.entry_height_std = 40
        self.entry_width_std = 280
        self.sticky_label = 'w'
        self.sticky_entry = 'w'
        self.sticky_frame = 'wens'
        self.sticky_horizontal = 'we'

    def initialize_elements(self):
        self._initialize_subframes()
        self._initialize_disk_name_subframe_elements()
        self._initialize_preseed_subframe_elements()
        self._initialize_username_password_subframe_elements()

    def _initialize_subframes(self):
        self.title_widget = TitleWidget(
            master=self,
            title='Packer',
            subtitle='Configurations'
        )
        self.project_name_frame = PackerProjectNameWidget(
            master=self,
            provisions_configs=self.provisions_configs
        )
        self.disk_name_frame = ctk.CTkFrame(self)
        self.preseed_frame = ctk.CTkFrame(self)
        self.username_password_frame = ctk.CTkFrame(self)
        self.vbox_configs_frame = VboxConfigsWidget(
            master=self,
            provisions_configs=self.provisions_configs
        )
        self.set_main_buttons_frame = PackerMainButtons(
            master=self,
            provisions_configs=self.provisions_configs,
            wanted_buttons='provisions'
        )
        self.iso_frame = IsoWidget(
            self,
            self.provisions_configs
        )

    def _initialize_disk_name_subframe_elements(self):
        self.disk_name_label = ctk.CTkLabel(
            self.disk_name_frame,
            text='Insert Disk Name',
            font=self.font_std
        )

        self.disk_name_entry = ctk.CTkEntry(
            self.disk_name_frame,
            font=self.font_std,
            placeholder_text='Disk Name',
            height=self.entry_height_std
        )
        if self.provisions_configs["configurations"]["disk_name"]["default"]:
            self.disk_name_entry.insert(
                0,
                self.provisions_configs["configurations"]["disk_name"]["default"]
            )

    def _initialize_preseed_subframe_elements(self):
        self.select_preseed_label = ctk.CTkLabel(
            master=self.preseed_frame,
            text='Select Preseed File',
            font=self.font_std
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

    def _initialize_username_password_subframe_elements(self):
        self.username_label = ctk.CTkLabel(
            master=self.username_password_frame,
            text="Username:",
            font=self.font_std
        )

        self.username_entry = ctk.CTkEntry(
            master=self.username_password_frame,
            font=self.font_std,
            height=self.entry_height_std,
            placeholder_text="Username to be created"
        )
        if self.provisions_configs["credentials"]['username']:
            self.username_entry.insert(
                0,
                self.provisions_configs["credentials"]['username']
            )

        self.password_label = ctk.CTkLabel(
            master=self.username_password_frame,
            text="Password:",
            font=self.font_std
        )
        self.password_entry = ctk.CTkEntry(
            master=self.username_password_frame,
            font=self.font_std,
            height=self.entry_height_std,
            placeholder_text="Password of the previous user"
        )
        if self.provisions_configs["credentials"]['password']:
            self.password_entry.insert(
                0,
                self.provisions_configs["credentials"]['password']
            )

    def render_elements(self):
        self._render_disk_name_subframe_elements()
        self._render_preseed_subframe_elements()
        self._render_username_password_subframe_elements()
        self._render_subframes()

    def _render_disk_name_subframe_elements(self):
        self.disk_name_frame.columnconfigure(0, weight=1)
        self.disk_name_frame.rowconfigure(0, weight=1)
        self.disk_name_frame.rowconfigure(1, weight=1)
        self.disk_name_label.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_label
        )
        self.disk_name_entry.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_horizontal
        )

    def _render_preseed_subframe_elements(self):
        self.preseed_frame.rowconfigure(0, weight=1)
        self.preseed_frame.rowconfigure(1, weight=1)
        self.select_preseed_label.grid(
            row=0,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.preseed_files_option.grid(
            row=1,
            column=0,
            sticky='w',
            padx=self.padx_std,
            pady=self.pady_entry
        )

    def _render_username_password_subframe_elements(self):
        self.username_password_frame.columnconfigure(0, weight=1)
        self.username_password_frame.rowconfigure(0, weight=1)
        self.username_password_frame.rowconfigure(1, weight=1)
        self.username_password_frame.rowconfigure(2, weight=1)
        self.username_password_frame.rowconfigure(3, weight=1)
        self.username_label.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_label
        )
        self.username_entry.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_frame
        )
        self.password_label.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_label
        )
        self.password_entry.grid(
            row=3,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_frame
        )

    def _render_subframes(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
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
        self.username_password_frame.grid(
            row=3,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )
        self.preseed_frame.grid(
            row=4,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )
        self.iso_frame.grid(
            row=5,
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
            rowspan=4,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )
        self.set_main_buttons_frame.grid(
            row=0,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky='se'
        )

    def _save_and_pass_to_provisions(self):
        credentials = self.provisions_configs["credentials"]
        credentials["username"] = self.username_entry.get()
        credentials["password"] = self.password_entry.get()

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
            rowspan=3,
            columnspan=3,
            sticky=self.sticky_frame
        )
