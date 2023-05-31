import constants
import customtkinter as ctk
import os
from existencecontroller.controller import launch_vboxmanage_lst_command


class PackerConfigsFrame(ctk.CTkFrame):

    def __init__(self, master, provisions_configs: dict):
        self.master = master
        self.provisions_configs = provisions_configs
        self.vbox_list = launch_vboxmanage_lst_command()
        ctk.CTkFrame.__init__(self, master)
        self.title_std = ctk.CTkFont(family=self.master.family, size=30,
                                     weight='bold')
        self.font_std = ctk.CTkFont(family=self.master.family, size=20)
        self.set_grid()
        self.set_std_dimensions()
        self.add_title()
        self.add_project_name()
        self.add_vboxname()

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
        self.ipadx_button = 5
        self.ipady_button = 5
        self.entry_height_std = 50
        self.entry_width_std = 380

    def add_title(self):
        title_frame = ctk.CTkFrame(self, fg_color='transparent')
        title_frame.grid(row=0, column=0, columnspan=2,
                         sticky='wn', padx=self.padx_std, pady=self.pady_std)
        title_frame.columnconfigure(0, weight=1)
        title_frame.rowconfigure(0, weight=1)
        title_frame.rowconfigure(1, weight=1)
        self.vagrant_label = ctk.CTkLabel(
            title_frame,
            text="Packer",
            font=self.title_std
        )
        self.vagrant_label.grid(row=0, column=0, sticky='w')

        self.conf_label = ctk.CTkLabel(
            title_frame,
            text="Configurations",
            font=self.font_std
        )
        self.conf_label.grid(row=1, column=0, sticky='w')

    def add_project_name(self):
        self.project_name_frame = ctk.CTkFrame(self)
        self.project_name_frame.grid(row=1, column=0, sticky='wne',
                                     padx=self.padx_std, pady=self.pady_std,
                                     ipadx=self.ipadx_std, ipady=self.ipady_std)
        # self.project_name_frame.grid_propagate(False)
        self.project_name_frame.columnconfigure(0, weight=1)
        self.project_name_frame.columnconfigure(1, weight=1)
        self.project_name_frame.rowconfigure(0, weight=1)
        self.project_name_frame.rowconfigure(1, weight=1)
        project_name_label = ctk.CTkLabel(
            self.project_name_frame,
            text="New Project Name:",
            font=self.font_std
        )
        project_name_label.grid(row=0, column=0, columnspan=2,
                                padx=self.padx_std, pady=self.pady_title,
                                sticky='w')
        self.entry_project_name = ctk.CTkEntry(
            self.project_name_frame,
            height=self.entry_height_std,
            width=self.entry_width_std,
            font=self.font_std,
            placeholder_text='Project name to be created'
        )
        if self.provisions_configs["configurations"]["project_name"] != "Project Name":
            self.entry_project_name.insert(
                0,
                self.provisions_configs["configurations"]["project_name"]
            )
        self.entry_project_name.grid(row=1, column=0, columnspan=2,
                                     padx=self.padx_std, pady=self.pady_entry,
                                     sticky='w')
        self.entry_project_name.bind("<Configure>", self._project_name_check)
        self.entry_project_name.bind("<KeyRelease>", self._project_name_check)

        self.warning_label_project = ctk.CTkLabel(
            self.project_name_frame,
            font=self.font_std
        )
        self.warning_label_project.grid(row=1, column=1, sticky='e',
                                        padx=self.padx_std, pady=0)
        if self.provisions_configs["configurations"]["project_name"] in os.listdir(f'{constants.PACKER_MACHINES_PATH}/'):
            self.warning_label_project.configure(
                text='A project with this name\nalready exists',
                text_color='red',
            )

    def _project_name_check(self, e):
        project_name_typed = self.entry_project_name.get()
        if project_name_typed not in os.listdir(f'{constants.PACKER_MACHINES_PATH}/'):
            self.entry_project_name.configure(border_color=["#979DA2", "#565B5E"])
            if self.warning_label_project.winfo_exists():
                self.warning_label_project.destroy()
        else:
            self.warning_label_project = ctk.CTkLabel(
                self.project_name_frame,
                text='A project with this name\nalready exists',
                text_color='red',
                font=self.font_std
            )
            self.warning_label_project.grid(row=1, column=1, sticky='e',
                                            padx=self.padx_std, pady=0)
            self.entry_project_name.configure(border_color='red')

    def add_vboxname(self):
        self.vbox_hostname_frame = ctk.CTkFrame(self)
        self.vbox_hostname_frame.grid(row=2, column=0, sticky='wne',
                                      padx=self.padx_std, pady=self.pady_std,
                                      ipadx=self.ipadx_std, ipady=self.ipady_std)
        self.vbox_hostname_frame.grid_propagate(False)
        self.vbox_hostname_frame.columnconfigure(0, weight=1)
        self.vbox_hostname_frame.columnconfigure(1, weight=1)
        self.vbox_hostname_frame.rowconfigure(0, weight=1)
        self.vbox_hostname_frame.rowconfigure(1, weight=1)
        vbox_name_label = ctk.CTkLabel(
            self.vbox_hostname_frame,
            text="Virtual box name:",
            font=self.font_std
        )
        vbox_name_label.grid(row=0, column=0, columnspan=2, sticky='w',
                             padx=self.padx_std, pady=self.pady_title)
        self.entry_vbox_name = ctk.CTkEntry(
            self.vbox_hostname_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std,
            placeholder_text='Virtualbox name to be created'
        )
        if self.provisions_configs["configurations"]['vbox_name'] != "Virtualbox Name":
            self.entry_vbox_name.insert(
                0,
                self.provisions_configs["configurations"]['vbox_name']
            )
        self.entry_vbox_name.grid(row=1, column=0, sticky='w',
                                  padx=self.padx_std, pady=self.pady_entry)
        self.entry_vbox_name.bind("<Configure>", self._vbox_name_check)
        self.entry_vbox_name.bind("<KeyRelease>", self._vbox_name_check)

        self.warning_label_vbox = ctk.CTkLabel(
            self.vbox_hostname_frame,
            font=self.font_std
        )
        self.warning_label_vbox.grid(row=1, column=1, sticky='e',
                                     padx=self.padx_std, pady=0)
        if self.provisions_configs["configurations"]['vbox_name'] in self.vbox_list:
            self.warning_label_vbox.configure(
                text='A box with this name\nalready exists',
                text_color='red',
            )

    def _vbox_name_check(self, e):
        vbox_name_typed = self.entry_vbox_name.get()
        if vbox_name_typed not in self.vbox_list:
            self.entry_vbox_name.configure(border_color=["#979DA2", "#565B5E"])
            if self.warning_label_vbox.winfo_exists():
                self.warning_label_vbox.destroy()
        if vbox_name_typed in self.vbox_list:
            self.warning_label_vbox = ctk.CTkLabel(
                self.vbox_hostname_frame,
                text='A box with this name\nalready exists',
                text_color='red',
                font=self.font_std
            )
            self.warning_label_vbox.grid(row=1, column=1, sticky='e',
                                         padx=self.padx_std, pady=0)
            self.entry_vbox_name.configure(border_color='red')
