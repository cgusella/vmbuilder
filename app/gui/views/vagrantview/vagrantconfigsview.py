import constants
import os
import customtkinter as ctk
from tkinter import messagebox as mb
from tkinter import StringVar


class VagrantConfigsFrame(ctk.CTkFrame):
    def __init__(self, master, provisions_configs):
        self.master = master
        ctk.CTkFrame.__init__(self, master)
        self.provisions_configs = provisions_configs
        self.title_std = ctk.CTkFont(family=self.master.family, size=30,
                                     weight='bold')
        self.font_std = ctk.CTkFont(family=self.master.family, size=20)
        self.set_grid()
        self.set_std_dimensions()
        self.add_select_vagrant_box()
        self.add_titles()
        self.add_project_name()
        self.add_vbox_hostname()
        self.add_connection_mode_frame()
        self.add_credentials_frame()
        self.add_set_provision_button()

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
        self.entry_width_std = 400

    def set_grid(self):
        self.grid()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # titles
        self.rowconfigure(0, weight=2)
        # project, vagrant box
        self.rowconfigure(1, weight=8)
        # vbox_host, connection mode
        self.rowconfigure(2, weight=8)
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
                                padx=self.padx_std, pady=self.pady_std,
                                ipadx=self.ipadx_std, ipady=self.ipady_std)
        project_name_frame.columnconfigure(0, weight=10)
        project_name_frame.columnconfigure(1, weight=1)
        project_name_frame.rowconfigure(0, weight=1)
        project_name_frame.rowconfigure(1, weight=1)
        project_name_label = ctk.CTkLabel(
            project_name_frame,
            text="New Project Name:",
            font=self.font_std
        )
        project_name_label.grid(row=0, column=0, columnspan=2,
                                padx=self.padx_std, pady=self.pady_title,
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
                                     padx=self.padx_std, pady=self.pady_entry,
                                     sticky='w')
        if self.provisions_configs["configurations"]["project_name"] in os.listdir(f'{constants.VAGRANT_MACHINES_PATH}/'):
            warning_label = ctk.CTkLabel(
                project_name_frame,
                text='A project with this name\nalready exists',
                text_color='red',
                font=self.font_std
            )
            warning_label.grid(row=1, column=1, sticky='e',
                               padx=self.padx_std, pady=self.pady_entry)

    def add_select_vagrant_box(self):
        """Select vagrant boxes.
        If there are no vagran boxes an entry is displayed,
        otherwise an optionmenu will appear"""
        vagrant_box_frame = ctk.CTkFrame(self)
        vagrant_box_frame.grid(row=1, column=1, sticky='wne',
                               padx=self.padx_std, pady=self.pady_std,
                               ipadx=self.ipadx_std, ipady=self.ipady_std)
        vagrant_box_frame.columnconfigure(0, weight=1)
        vagrant_box_frame.rowconfigure(0, weight=1)
        local_vagrant_boxes = self.master.local_vagrant_boxes
        if local_vagrant_boxes == 'No Box':
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
            self.vagrant_box.set(self.provisions_configs["configurations"]["image"])
            vagrant_drop = ctk.CTkOptionMenu(
                master=vagrant_box_frame,
                variable=self.vagrant_box,
                values=local_vagrant_boxes.split("\n"),
                font=self.font_std,
                width=self.entry_width_std,
                height=self.entry_height_std,
                dropdown_font=self.font_std
            )
            vagrant_drop.grid(row=0, column=0, sticky="ew",
                              padx=self.padx_std, pady=self.pady_std)

    def add_vbox_hostname(self):
        vbox_hostname_frame = ctk.CTkFrame(self)
        vbox_hostname_frame.grid(row=2, column=0, sticky='wne',
                                 padx=self.padx_std, pady=self.pady_std,
                                 ipadx=self.ipadx_std, ipady=self.ipady_std)
        vbox_hostname_frame.columnconfigure(0, weight=10)
        vbox_hostname_frame.columnconfigure(1, weight=5)
        vbox_hostname_frame.rowconfigure(0, weight=1)
        vbox_hostname_frame.rowconfigure(1, weight=1)
        vbox_hostname_frame.rowconfigure(2, weight=1)
        vbox_hostname_frame.rowconfigure(3, weight=1)
        vbox_name_label = ctk.CTkLabel(
            vbox_hostname_frame,
            text="Virtual box name:",
            font=self.font_std
        )
        vbox_name_label.grid(row=0, column=0, columnspan=2, sticky='w',
                             padx=self.padx_std, pady=self.pady_title)
        self.entry_vbox_name = ctk.CTkEntry(
            vbox_hostname_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std
        )
        self.entry_vbox_name.insert(
            0,
            self.provisions_configs["configurations"]['vbox_name']
        )
        self.entry_vbox_name.grid(row=1, column=0, sticky='w',
                                  padx=self.padx_std, pady=self.pady_entry)

        if self.provisions_configs["configurations"]['vbox_name'] in self.master.vbox_list:
            warning_label = ctk.CTkLabel(
                vbox_hostname_frame,
                text='A box with this name\nalready exists',
                text_color='red',
                font=self.font_std
            )
            warning_label.grid(row=1, column=1, sticky='e',
                               padx=self.padx_std, pady=self.pady_entry)

        hostname_label = ctk.CTkLabel(
            vbox_hostname_frame,
            text="Hostname:",
            font=self.font_std
        )
        hostname_label.grid(row=2, column=0, sticky='w',
                            padx=self.padx_std, pady=self.pady_title)
        self.entry_hostname = ctk.CTkEntry(
            vbox_hostname_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std
        )
        self.entry_hostname.insert(
            0,
            self.provisions_configs["configurations"]['hostname']
        )
        self.entry_hostname.grid(row=3, column=0, sticky='w',
                                 padx=self.padx_std, pady=self.pady_entry)

    def add_connection_mode_frame(self):
        connection_mode_frame = ctk.CTkFrame(self)
        connection_mode_frame.grid(row=2, column=1, sticky='wne',
                                   padx=self.padx_std, pady=self.pady_std,
                                   ipadx=self.ipadx_std, ipady=self.ipady_std)
        connection_mode_frame.columnconfigure(0, weight=1)
        connection_mode_frame.rowconfigure(0, weight=1)
        connection_mode_frame.rowconfigure(1, weight=1)

        ssh_label = ctk.CTkLabel(
            connection_mode_frame,
            text='Connection mode',
            font=self.font_std
        )
        ssh_label.grid(row=0, column=0, sticky='w',
                       padx=self.padx_std, pady=self.pady_std)
        self.connection_mode_var = StringVar()
        if self.provisions_configs["configurations"]["connection"] == 'key':
            self.connection_mode_var.set('key')
        elif self.provisions_configs["configurations"]["connection"] == 'password':
            self.connection_mode_var.set('password')
        ssh_key = ctk.CTkRadioButton(
            connection_mode_frame,
            text="ssh_key",
            variable=self.connection_mode_var,
            value='key',
            font=self.font_std
        )
        ssh_key.grid(row=1, column=0, padx=self.padx_std, pady=self.pady_std,
                     sticky='w')
        password = ctk.CTkRadioButton(
            connection_mode_frame,
            text="password",
            variable=self.connection_mode_var,
            value='password',
            command=self.set_connection_mode,
            font=self.font_std
        )
        password.grid(row=2, column=0, padx=self.padx_std, pady=self.pady_std,
                      sticky='w')

    def add_credentials_frame(self):
        credentials_frame = ctk.CTkFrame(self)
        credentials_frame.grid(row=3, column=0, sticky='wne',
                               padx=self.padx_std, pady=self.pady_std,
                               ipadx=self.ipadx_std, ipady=self.ipady_std)
        credentials_frame.columnconfigure(0, weight=1)
        credentials_frame.rowconfigure(0, weight=1)
        credentials_frame.rowconfigure(1, weight=1)
        credentials_frame.rowconfigure(2, weight=1)
        credentials_frame.rowconfigure(3, weight=1)
        credentials_frame.rowconfigure(4, weight=1)
        credentials_frame.rowconfigure(5, weight=1)
        username_label = ctk.CTkLabel(
            credentials_frame,
            text="Username:",
            font=self.font_std
        )
        username_label.grid(row=0, column=0, sticky='w',
                            padx=self.padx_std, pady=self.pady_title)
        self.entry_default_username = ctk.CTkEntry(
            credentials_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std
        )
        self.entry_default_username.insert(
            0,
            self.provisions_configs["credentials"]['username']
        )
        self.entry_default_username.grid(row=1, column=0, sticky='w',
                                         padx=self.padx_std,
                                         pady=self.pady_entry)

        password_label = ctk.CTkLabel(
            credentials_frame,
            text="Password:",
            font=self.font_std
        )
        password_label.grid(row=2, column=0, sticky='w',
                            padx=self.padx_std, pady=self.pady_title)
        self.entry_default_password = ctk.CTkEntry(
            credentials_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std
        )
        self.entry_default_password.insert(
            0,
            self.provisions_configs["credentials"]['password']
        )
        self.entry_default_password.grid(row=3, column=0, sticky='w',
                                         padx=self.padx_std,
                                         pady=self.pady_entry)

        extra_user_label = ctk.CTkLabel(
            credentials_frame,
            text="Extra user:",
            font=self.font_std
        )
        extra_user_label.grid(row=4, column=0, sticky='w',
                              padx=self.padx_std, pady=self.pady_title)
        self.entry_extra_user = ctk.CTkEntry(
            credentials_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std
        )
        self.entry_extra_user.insert(
            0,
            self.provisions_configs["credentials"]['extra_user']
        )
        self.entry_extra_user.grid(row=5, column=0, sticky='w',
                                   padx=self.padx_std, pady=self.pady_entry)

    def add_set_provision_button(self):
        set_provision_button_frame = ctk.CTkFrame(
            self,
            fg_color='transparent'
        )
        set_provision_button_frame.grid(row=3, column=1, sticky='wnse',
                                        padx=self.padx_std, pady=self.pady_std,
                                        ipadx=self.ipadx_std, ipady=self.ipady_std)
        set_provision_button_frame.columnconfigure(0, weight=1)
        set_provision_button_frame.rowconfigure(0, weight=1)
        set_provision_button = ctk.CTkButton(
            set_provision_button_frame,
            text='Set Provisions',
            command=self._go_to_provision_page,
            font=self.font_std
        )
        set_provision_button.grid(row=0, column=0, sticky='se',
                                  padx=self.padx_std, pady=self.pady_std,
                                  ipadx=self.ipadx_button,
                                  ipady=self.ipady_button)

    def _go_to_provision_page(self):
        project_name = self.entry_project_name.get()
        vbox_name = self.entry_vbox_name.get()
        # if project_name in os.listdir(constants.VAGRANT_MACHINES_PATH):
        #     mb.showwarning(
        #         title='Project name duplicate',
        #         message=(
        #             f'A project with the name "{project_name}" already exists.\n'
        #             'If you build this project you will override the old one.'
        #         )
        #     )
        if not project_name:
            mb.showerror('Error', 'You must choose a name for the project!')
        elif not vbox_name:
            mb.showerror('Error', 'You must choose a name for the virtual box machine!')
        # elif vbox_name in self.master.vbox_list:
        #     mb.showerror('Error', f'A box with the name "{vbox_name}" already exists!')
        elif not self.entry_default_username.get():
            mb.showerror('Error', 'You must specify the existing username of the vagrant box for vagrant to be able to connect to the machine!')
        elif not self.entry_default_password.get():
            mb.showerror('Error', 'You must specify the password of the specified user for vagrant to be able to connect to the machine!')
        elif self.vagrant_box.get() == 'Select Vagrant Box':
            mb.showerror('Error', 'You must choose a Vagrant box!')
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
