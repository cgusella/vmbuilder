import constants
import os
import customtkinter as ctk
from argumentparser.helper import get_local_vagrant_boxes
from existencecontroller.controller import launch_vboxmanage_lst_command
from gui.views.errors.errorview import ErrorMessage
from tkinter import StringVar


class VagrantConfigsFrame(ctk.CTkFrame):
    def __init__(self, master, provisions_configs):
        ctk.CTkFrame.__init__(self, master)
        self.provisions_configs = provisions_configs
        self.padx_std = (10, 10)
        self.pady_std = (10, 10)
        self.entry_height_std = 50
        self.entry_width_std = 400
        self.title_std = ctk.CTkFont(family=self.master.family, size=30,
                                     weight='bold')
        self.font_std = ctk.CTkFont(family=self.master.family, size=25)
        self.set_grid()

        self.add_titles()
        self.add_project_name()
        self.add_select_vagrant_box()

        # start form to get new machine configurations
        # self.startcolumn = 1
        # self.add_project_frame()
        # self.add_vbox_hostname()
        # self.add_credentials_frame()
        # self.add_select_vagrant_box()
        # self.add_connection_mode_frame()

    def set_grid(self):
        self.grid()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # titles
        self.rowconfigure(0, weight=2)
        # project, vagrant box
        self.rowconfigure(1, weight=2)
        # vbox_host, connection mode
        self.rowconfigure(2, weight=2)
        # username_password, set provision button
        self.rowconfigure(3, weight=1)

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
            text="Configurations",
            font=self.font_std
        )
        self.conf_label.grid(row=1, column=0, sticky='w')

    def add_project_name(self):
        project_name_frame = ctk.CTkFrame(self)
        project_name_frame.grid(row=1, column=0, sticky='wne',
                                padx=self.padx_std, pady=self.pady_std)
        project_name_frame.columnconfigure(0, weight=1)
        project_name_frame.columnconfigure(1, weight=1)
        project_name_frame.rowconfigure(0, weight=1)
        project_name_frame.rowconfigure(1, weight=1)
        project_name_label = ctk.CTkLabel(
            project_name_frame,
            text="New Project Name:",
            font=self.font_std
        )
        project_name_label.grid(row=0, column=0, columnspan=2,
                                padx=self.padx_std, pady=self.pady_std,
                                sticky='w')
        self.entry_project_name = ctk.CTkEntry(
            project_name_frame,
            height=self.entry_height_std,
            width=self.entry_width_std,
            font=self.font_std
        )
        self.entry_project_name.insert(
            0,
            self.provisions_configs["configurations"]["project_name"]
        )
        self.entry_project_name.grid(row=1, column=0, columnspan=2,
                                     padx=self.padx_std, pady=self.pady_std,
                                     sticky='w')

    def add_select_vagrant_box(self):
        """Select vagrant boxes.
        If there are no vagran boxes an entry is displayed,
        otherwise an optionmenu will appear"""
        vagrant_box_frame = ctk.CTkFrame(self)
        vagrant_box_frame.grid(row=1, column=1, sticky='wne',
                               padx=self.padx_std, pady=self.pady_std)
        vagrant_box_frame.columnconfigure(0, weight=1)
        vagrant_box_frame.rowconfigure(0, weight=1)
        if get_local_vagrant_boxes() == 'No Box':
            # add column since we have two objects in this frame
            vagrant_box_frame.columnconfigure(1, weight=1)
            vagrant_box_name_label = ctk.CTkLabel(
                vagrant_box_frame,
                text=(
                    'You do not have local Vagrant boxes.\n'
                    'Insert cloud Vagrant box name:'
                ),
                font=self.font_std,
                justify='left'
            )
            vagrant_box_name_label.grid(row=0, column=0, padx=self.padx_std,
                                        pady=self.pady_std, sticky='w')
            self.vagrant_box = ctk.CTkEntry(
                vagrant_box_frame,
                font=self.font_std,
                width=self.entry_width_std,
                height=self.entry_height_std
            )
            self.vagrant_box.insert(
                0,
                self.provisions_configs["configurations"]["image"]
            )
            self.vagrant_box.grid(row=1, column=0, sticky='ws',
                                  padx=self.padx_std, pady=self.pady_std)
        else:
            self.vagrant_box = ctk.StringVar(self)
            self.vagrant_box.set('Select Vagrant Box')
            vagrant_drop = ctk.CTkOptionMenu(
                master=vagrant_box_frame,
                variable=self.vagrant_box,
                values=get_local_vagrant_boxes().split("\n"),
                font=self.font_std,
                width=self.entry_width_std,
                height=self.entry_height_std,
                dropdown_font=self.font_std
            )
            vagrant_drop.grid(row=0, column=0, sticky="ew",
                              padx=self.padx_std, pady=self.pady_std)

    def add_vbox_hostname(self):
        vbox_hostname_frame = ctk.CTkFrame(self)
        vbox_hostname_frame.grid(row=5, column=self.startcolumn, columnspan=2)
        vbox_hostname_frame.columnconfigure(0, weight=1)
        vbox_hostname_frame.columnconfigure(1, weight=1)
        vbox_hostname_frame.rowconfigure(0, weight=1)
        vbox_hostname_frame.rowconfigure(1, weight=1)
        vbox_name_label = ctk.CTkLabel(vbox_hostname_frame, text="Virtual box name:")
        vbox_name_label.grid(row=0, column=0)
        self.entry_vbox_name = ctk.CTkEntry(vbox_hostname_frame)
        self.entry_vbox_name.insert(
            0,
            self.provisions_configs["configurations"]['vbox_name']
        )
        self.entry_vbox_name.grid(row=1, column=0,
                                  padx=(10, 10), pady=(10, 10))

        hostname_label = ctk.CTkLabel(vbox_hostname_frame, text="Hostname:")
        hostname_label.grid(row=0, column=1)
        self.entry_hostname = ctk.CTkEntry(vbox_hostname_frame)
        self.entry_hostname.insert(
            0,
            self.provisions_configs["configurations"]['hostname']
        )
        self.entry_hostname.grid(row=1, column=1,
                                 padx=(10, 10), pady=(10, 10))

    def add_credentials_frame(self):
        credentials_frame = ctk.CTkFrame(self)
        credentials_frame.grid(row=7, column=self.startcolumn, columnspan=2)
        credentials_frame.columnconfigure(0, weight=1)
        credentials_frame.columnconfigure(1, weight=1)
        credentials_frame.rowconfigure(0, weight=1)
        credentials_frame.rowconfigure(1, weight=1)
        credentials_frame.rowconfigure(2, weight=1)
        credentials_frame.rowconfigure(3, weight=1)
        username_label = ctk.CTkLabel(credentials_frame, text="Username:")
        username_label.grid(row=0, column=0)
        self.entry_default_username = ctk.CTkEntry(credentials_frame)
        self.entry_default_username.insert(
            0,
            self.provisions_configs["credentials"]['username']
        )
        self.entry_default_username.grid(row=1, column=0,
                                         padx=(10, 10), pady=(10, 10))

        machine_name_label = ctk.CTkLabel(credentials_frame, text="Password:")
        machine_name_label.grid(row=0, column=1)
        self.entry_default_password = ctk.CTkEntry(credentials_frame)
        self.entry_default_password.insert(
            0,
            self.provisions_configs["credentials"]['password']
        )
        self.entry_default_password.grid(row=1, column=1,
                                         padx=(10, 10), pady=(10, 10))

        machine_name_label = ctk.CTkLabel(credentials_frame, text="Extra user:")
        machine_name_label.grid(row=2, column=0, columnspan=2)
        self.entry_extra_user = ctk.CTkEntry(credentials_frame)
        self.entry_extra_user.insert(
            0,
            self.provisions_configs["credentials"]['extra_user']
        )
        self.entry_extra_user.grid(row=3, column=0, columnspan=2,
                                   padx=(10, 10), pady=(10, 10))

    def add_select_vagrant_box_old(self):
        # Select vagrant boxes.
        # If there are no vagran boxes an entry is displayed,
        # otherwise an optionmenu will appear
        if get_local_vagrant_boxes() == 'No Box':
            no_box_frame = ctk.CTkFrame(
                self,
            )
            no_box_frame.grid(row=12, column=self.startcolumn, columnspan=2)
            no_box_frame.columnconfigure(0, weight=1)
            no_box_frame.rowconfigure(0, weight=1)
            no_box_frame.rowconfigure(1, weight=1)
            vagrant_box_name_label = ctk.CTkLabel(
                no_box_frame,
                text=(
                    'You do not have local Vagrant box.\n'
                    'Insert cloud Vagrant box name:'
                )
            )
            vagrant_box_name_label.grid(row=0, column=0)
            self.vagrant_box = ctk.CTkEntry(no_box_frame)
            self.vagrant_box.insert(
                0,
                self.provisions_configs["configurations"]["image"]
            )
            self.vagrant_box.grid(row=1, column=0,
                                  padx=(10, 10), pady=(10, 10))
        else:
            self.vagrant_box = ctk.StringVar(self)
            self.vagrant_box.set('Select Vagrant Box')
            vagrant_drop = ctk.CTkOptionMenu(
                master=self,
                variable=self.vagrant_box,
                values=get_local_vagrant_boxes().split("\n"),
            )
            vagrant_drop.grid(row=11, column=self.startcolumn, sticky="ew", columnspan=2)

    def add_connection_mode_frame(self):
        connection_mode_frame = ctk.CTkFrame(self)
        connection_mode_frame.grid(row=13, column=self.startcolumn, columnspan=2, rowspan=2,
                                   padx=(10, 10), pady=(10, 10))
        connection_mode_frame.columnconfigure(0, weight=1)
        connection_mode_frame.columnconfigure(1, weight=1)
        connection_mode_frame.rowconfigure(0, weight=1)
        connection_mode_frame.rowconfigure(1, weight=1)

        ssh_label = ctk.CTkLabel(connection_mode_frame, text='Connection mode')
        ssh_label.grid(row=0, column=0, columnspan=2)
        self.connection_mode_var = StringVar()
        if self.provisions_configs["configurations"]["connection"] == 'key':
            self.connection_mode_var.set('key')
        elif self.provisions_configs["configurations"]["connection"] == 'password':
            self.connection_mode_var.set('password')
        ssh_key = ctk.CTkRadioButton(
            connection_mode_frame,
            text="ssh_key",
            variable=self.connection_mode_var,
            value='key'
        )
        ssh_key.grid(row=1, column=0, padx=(10, 10), pady=(10, 10))
        password = ctk.CTkRadioButton(
            connection_mode_frame,
            text="password",
            variable=self.connection_mode_var,
            value='password',
            command=self.set_connection_mode
        )
        password.grid(row=1, column=1, padx=(10, 10), pady=(10, 10))

        save_button = ctk.CTkButton(
            self,
            text='Set Provisions',
            command=self.go_to_provision_page
        )
        save_button.grid(row=15, column=self.startcolumn, columnspan=2)

    def go_to_provision_page(self):
        project_name = self.entry_project_name.get()
        if project_name in os.listdir(constants.VAGRANT_MACHINES_PATH):
            ErrorMessage(self, 'A machine with this name already exists')
        elif not project_name:
            ErrorMessage(self, 'You must choose a name for the virtual machine')
        elif not self.entry_vbox_name.get():
            ErrorMessage(self, 'You must choose a name for the virtual box machine')
        elif self.entry_vbox_name.get() in launch_vboxmanage_lst_command():
            ErrorMessage(self, 'A box with the same name already exists')
        elif not self.entry_hostname.get():
            ErrorMessage(self, 'You must choose a hostname')
        elif not self.entry_default_username.get():
            ErrorMessage(self, 'You must choose a main username')
        elif not self.entry_default_password.get():
            ErrorMessage(self, 'You must choose a password')
        elif self.vagrant_box.get() == 'Select Vagrant Box':
            ErrorMessage(self, 'You must select a Vagrant box')
        else:
            self.provisions_configs["configurations"]["project_name"] = project_name
            self.provisions_configs["configurations"]["vbox_name"] = self.entry_vbox_name.get()
            self.provisions_configs["configurations"]["hostname"] = self.entry_hostname.get()
            self.provisions_configs["credentials"]["username"] = self.entry_default_username.get()
            self.provisions_configs["credentials"]["password"] = self.entry_default_password.get()
            self.provisions_configs["credentials"]["extra_user"] = self.entry_extra_user.get()
            self.provisions_configs["configurations"]["image"] = self.vagrant_box.get()
            self.destroy()
            self.master.add_vagrant_provisions_frame()

    def get_vagrant_configs(self):
        return self.provisions_configs

    def set_connection_mode(self):
        self.provisions_configs["configurations"]["connection"] = self.connection_mode_var.get()
