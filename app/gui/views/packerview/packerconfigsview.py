import constants
import customtkinter as ctk
import os
from gui.widgets.vboxconfigswidget import VboxConfigsWidget
from gui.widgets.isowidget import IsoWidget
from gui.widgets.titlewidget import TitleWidget


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
        self.add_iso_frame()
        self.add_vbox_configs()

    def set_grid(self):
        self.grid()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

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
        self.entry_height_std = 50
        self.entry_width_std = 380
        self.sticky_label = 'w'
        self.sticky_entry = 'w'
        self.sticky_frame = 'wens'

    def add_title(self):
        self.title_widget = TitleWidget(
            master=self,
            title='Packer',
            subtitle='Configurations'
        )

        self.title_widget.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_frame
        )

    def add_project_name(self):
        self.project_name_frame = ctk.CTkFrame(self)
        self.project_name_frame.columnconfigure(0, weight=1)
        self.project_name_frame.columnconfigure(1, weight=1)
        self.project_name_frame.rowconfigure(0, weight=1)
        self.project_name_frame.rowconfigure(1, weight=1)

        self.project_name_frame.grid(
            row=1,
            column=0,
            sticky=self.sticky_frame,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std
        )

        project_name_label = ctk.CTkLabel(
            master=self.project_name_frame,
            text="New Project Name:",
            font=self.font_std
        )
        project_name_label.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_title,
            sticky=self.sticky_label
        )

        self.entry_project_name = ctk.CTkEntry(
            master=self.project_name_frame,
            height=self.entry_height_std,
            width=self.entry_width_std,
            font=self.font_std,
            placeholder_text='Project name to be created'
        )
        if self.provisions_configs["configurations"]["project_name"]["default"]:
            self.entry_project_name.insert(
                0,
                self.provisions_configs["configurations"]["project_name"]["default"]
            )
        self.entry_project_name.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_entry
        )
        self.entry_project_name.bind("<Configure>", self._project_name_check)
        self.entry_project_name.bind("<KeyRelease>", self._project_name_check)

        self.warning_label_project = ctk.CTkLabel(
            master=self.project_name_frame,
            font=self.font_std
        )
        self.warning_label_project.grid(
            row=1,
            column=1,
            padx=self.padx_std,
            pady=0,
            sticky=self.sticky_label
        )
        if self.provisions_configs["configurations"]["project_name"] in os.listdir(f'{constants.PACKER_MACHINES_PATH}/'):
            self.warning_label_project.configure(
                text='A project with this name\nalready exists',
                text_color='red'
            )

    def _project_name_check(self, event):
        project_name_typed = self.entry_project_name.get()
        if project_name_typed not in os.listdir(f'{constants.PACKER_MACHINES_PATH}/'):
            self.entry_project_name.configure(border_color=["#979DA2", "#565B5E"])
            if self.warning_label_project.winfo_exists():
                self.warning_label_project.destroy()
        else:
            self.warning_label_project = ctk.CTkLabel(
                master=self.project_name_frame,
                text='A project with this name\nalready exists',
                text_color='red',
                font=self.font_std
            )
            self.warning_label_project.grid(
                row=1,
                column=1,
                padx=self.padx_std,
                pady=0,
                sticky=self.sticky_label
            )
            self.entry_project_name.configure(border_color='red')

    def add_disk_name(self):
        self.disk_name_frame = ctk.CTkFrame(self)
        self.disk_name_frame.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )

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
        self.disk_name_entry.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_entry
        )

    def add_iso_frame(self):
        iso_frame = IsoWidget(
            self,
            self.provisions_configs
        )
        iso_frame.grid(
            row=4,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )

    def add_vbox_configs(self):
        """Add entries for cpus, memory, disk size"""
        vbox_configs = VboxConfigsWidget(
            master=self,
            provisions_configs=self.provisions_configs
        )
        vbox_configs.grid(
            row=1,
            column=1,
            rowspan=3,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )

    def add_set_provisions(self):
        pass
