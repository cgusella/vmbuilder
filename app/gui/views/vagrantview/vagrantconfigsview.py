import constants
import os
import customtkinter as ctk
from argumentparser.helper import get_local_vagrant_boxes
from existencecontroller.controller import launch_vboxmanage_lst_command
from tkinter import messagebox as mb
from tkinter import StringVar


class VagrantConfigsFrame(ctk.CTkFrame):
    def __init__(self, master, provisions_configs):
        self.master = master
        self.provisions_configs = provisions_configs
        self.vbox_list = launch_vboxmanage_lst_command()
        self.local_vagrant_boxes = get_local_vagrant_boxes()

        ctk.CTkFrame.__init__(self, master)
        self.title_std = ctk.CTkFont(
            family=self.master.family,
            size=30,
            weight='bold'
        )
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
        self.entry_width_std = 380
        self.sticky_title = 'wn'
        self.sticky_label = 'ws'
        self.sticky_entry = 'wn'
        self.sticky_frame = 'wens'
        self.sticky_optionmenu = 'w'
        self.sticky_warningmsg = 'e'
        self.sticky_horizontal = 'ew'

    def set_grid(self):
        self.grid()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # titles
        self.rowconfigure(0, weight=1)
        # project name
        self.rowconfigure(1, weight=1)
        # vbox_host, connection mode
        self.rowconfigure(2, weight=1)
        # select vagrant box
        self.rowconfigure(3, weight=1)
        # username_password, set provision button
        self.rowconfigure(4, weight=1)

    def set_general_row_col_conf(self, frame:ctk.CTkFrame, rows: int, columns: int):
        # self.grid()
        for i in range(columns):
            frame.columnconfigure(i, weight=1)

        for i in range(rows):
            frame.rowconfigure(i, weight=1)

    def add_titles(self):
        title_frame = ctk.CTkFrame(self, fg_color='transparent')

        self.set_general_row_col_conf(
            frame=title_frame,
            rows=2,
            columns=1
        )

        title_frame.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            # sticky='wn'
            sticky=self.sticky_frame
        )

        self.vagrant_label = ctk.CTkLabel(
            master=title_frame,
            text="Vagrant",
            font=self.title_std
        )
        self.vagrant_label.grid(
            row=0,
            column=0,
            sticky=self.sticky_label
        )

        self.conf_label = ctk.CTkLabel(
            title_frame,
            text="Configurations",
            font=self.font_std
        )
        self.conf_label.grid(
            row=1,
            column=0,
            sticky=self.sticky_label
        )

    def add_project_name(self):
        self.project_name_frame = ctk.CTkFrame(self)

        self.set_general_row_col_conf(
            frame=self.project_name_frame,
            rows=2,
            columns=2
        )

        self.project_name_frame.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_horizontal
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
        if self.provisions_configs["configurations"]["project_name"] != "Project Name":
            self.entry_project_name.insert(
                0,
                self.provisions_configs["configurations"]["project_name"]
            )
        self.entry_project_name.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_entry
        )
        self.entry_project_name.bind("<KeyRelease>", self._project_name_check)
        self.entry_project_name.bind("<Configure>", self._project_name_check)

        self.warning_label_project = ctk.CTkLabel(
            master=self.project_name_frame,
            text='',
            font=self.font_std
        )
        self.warning_label_project.grid(
            row=1,
            column=1,
            padx=self.padx_std,
            pady=0,
            sticky=self.sticky_warningmsg
        )
        if self.provisions_configs["configurations"]["project_name"] in os.listdir(f'{constants.VAGRANT_MACHINES_PATH}/'):
            self.warning_label_project.configure(
                text='A project with this name\nalready exists',
                text_color='red',
            )

    def _project_name_check(self, event):
        project_name_typed = self.entry_project_name.get()
        if project_name_typed not in os.listdir(f'{constants.VAGRANT_MACHINES_PATH}/'):
            self.warning_label_project.configure(text='')
            self.entry_project_name.configure(border_color=["#979DA2", "#565B5E"])
        else:
            self.warning_label_project.configure(
                text='A project with this name\nalready exists',
                text_color='red',
            )
            self.entry_project_name.configure(border_color='red')

    def add_select_vagrant_box(self):
        """Select vagrant boxes.
        If there are no vagran boxes an entry is displayed,
        otherwise an optionmenu will appear"""
        vagrant_box_frame = ctk.CTkFrame(self)
        vagrant_box_frame.columnconfigure(0, weight=1)
        vagrant_box_frame.rowconfigure(0, weight=1)
        vagrant_box_frame.rowconfigure(1, weight=1)

        vagrant_box_frame.grid(
            row=3,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_horizontal
        )

        vagrant_box_label = ctk.CTkLabel(
            master=vagrant_box_frame,
            font=self.font_std,
            text='Select or Insert Vagrant Box'
        )
        vagrant_box_label.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_title,
            sticky=self.sticky_label
        )

        self.vagrant_box = ctk.StringVar(self)
        self.vagrant_box.set(self.provisions_configs["configurations"]["image"])
        vagrant_drop = ctk.CTkComboBox(
            master=vagrant_box_frame,
            variable=self.vagrant_box,
            values=self.local_vagrant_boxes.split("\n"),
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std,
            dropdown_font=self.font_std,
        )
        vagrant_drop.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_horizontal
        )

    def add_vbox_hostname(self):
        self.vbox_hostname_frame = ctk.CTkFrame(self)

        self.set_general_row_col_conf(
            frame=self.vbox_hostname_frame,
            rows=4,
            columns=2
        )

        self.vbox_hostname_frame.grid_propagate(False)
        self.vbox_hostname_frame.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_horizontal,
        )
        vbox_name_label = ctk.CTkLabel(
            master=self.vbox_hostname_frame,
            text="Virtual box name:",
            font=self.font_std
        )
        vbox_name_label.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_title,
            sticky=self.sticky_label
        )
        self.entry_vbox_name = ctk.CTkEntry(
            master=self.vbox_hostname_frame,
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
        self.entry_vbox_name.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_entry
        )
        self.entry_vbox_name.bind("<KeyRelease>", self._vbox_name_check)
        self.entry_vbox_name.bind("<Configure>", self._vbox_name_check)

        self.warning_label_vbox = ctk.CTkLabel(
            master=self.vbox_hostname_frame,
            font=self.font_std
        )
        self.warning_label_vbox.grid(
            row=1,
            column=1,
            padx=self.padx_std,
            pady=0,
            sticky=self.sticky_warningmsg
        )
        if self.provisions_configs["configurations"]['vbox_name'] in self.vbox_list:
            self.warning_label_vbox.configure(
                text='A box with this name\nalready exists',
                text_color='red'
            )

        hostname_label = ctk.CTkLabel(
            master=self.vbox_hostname_frame,
            text="Hostname:",
            font=self.font_std
        )
        hostname_label.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_title,
            sticky=self.sticky_label
        )

        self.entry_hostname = ctk.CTkEntry(
            master=self.vbox_hostname_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std,
            placeholder_text='Hostname for the new VM'
        )
        if self.provisions_configs["configurations"]['hostname'] != "Hostname":
            self.entry_hostname.insert(
                0,
                self.provisions_configs["configurations"]['hostname']
            )
        self.entry_hostname.grid(
            row=3,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_entry
        )

    def _vbox_name_check(self, event):
        vbox_name_typed = self.entry_vbox_name.get()
        if vbox_name_typed not in self.vbox_list:
            self.entry_vbox_name.configure(border_color=["#979DA2", "#565B5E"])
            self.warning_label_vbox.configure(text='')
        else:
            self.entry_vbox_name.configure(border_color='red')
            self.warning_label_vbox.configure(
                text='A box with this name\nalready exists',
                text_color='red'
            )

    def add_connection_mode_frame(self):
        connection_mode_frame = ctk.CTkFrame(self)

        self.set_general_row_col_conf(
            frame=connection_mode_frame,
            rows=2,
            columns=1
        )

        connection_mode_frame.grid(
            row=1,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_horizontal
        )

        ssh_label = ctk.CTkLabel(
            master=connection_mode_frame,
            text='Connection mode',
            font=self.font_std
        )
        ssh_label.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_label,
        )

        self.connection_mode_var = StringVar()
        if self.provisions_configs["configurations"]["connection"] == 'key':
            self.connection_mode_var.set('key')
        elif self.provisions_configs["configurations"]["connection"] == 'password':
            self.connection_mode_var.set('password')

        ssh_key = ctk.CTkRadioButton(
            master=connection_mode_frame,
            text="ssh_key",
            variable=self.connection_mode_var,
            value='key',
            font=self.font_std
        )
        ssh_key.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_entry
        )

        password = ctk.CTkRadioButton(
            master=connection_mode_frame,
            text="password",
            variable=self.connection_mode_var,
            value='password',
            command=self.set_connection_mode,
            font=self.font_std
        )
        password.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_entry
        )

    def add_credentials_frame(self):
        credentials_frame = ctk.CTkFrame(self)

        self.set_general_row_col_conf(
            frame=credentials_frame,
            rows=6,
            columns=1
        )

        credentials_frame.grid(
            row=4,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )
        
        username_label = ctk.CTkLabel(
            master=credentials_frame,
            text="Username:",
            font=self.font_std
        )
        username_label.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_title,
            sticky=self.sticky_label
        )

        self.entry_default_username = ctk.CTkEntry(
            master=credentials_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std,
            placeholder_text="Existing user on the vagrant box"
        )
        if self.provisions_configs["credentials"]['username'] != "Username":
            self.entry_default_username.insert(
                0,
                self.provisions_configs["credentials"]['username']
            )
        self.entry_default_username.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_entry
        )

        password_label = ctk.CTkLabel(
            master=credentials_frame,
            text="Password:",
            font=self.font_std
        )
        password_label.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_title,
            sticky=self.sticky_label
        )
        
        self.entry_default_password = ctk.CTkEntry(
            master=credentials_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std,
            placeholder_text="Password of the previous user"
        )
        if self.provisions_configs["credentials"]['password'] != "Password":
            self.entry_default_password.insert(
                0,
                self.provisions_configs["credentials"]['password']
            )
        self.entry_default_password.grid(
            row=3,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_entry
        )

        extra_user_label = ctk.CTkLabel(
            master=credentials_frame,
            text="Extra user:",
            font=self.font_std
        )
        extra_user_label.grid(
            row=4,
            column=0,
            padx=self.padx_std,
            pady=self.pady_title,
            sticky=self.sticky_label
        )

        self.entry_extra_user = ctk.CTkEntry(
            master=credentials_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std,
            placeholder_text="An extra user to be created"
        )
        if self.provisions_configs["credentials"]['extra_user']:
            self.entry_extra_user.insert(
                0,
                self.provisions_configs["credentials"]['extra_user']
            )
        self.entry_extra_user.grid(
            row=5,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_entry
        )

    def add_set_provision_button(self):
        set_provision_button_frame = ctk.CTkFrame(
            self,
            fg_color='transparent'
        )

        self.set_general_row_col_conf(
            frame=set_provision_button_frame,
            rows=1,
            columns=1
        )

        set_provision_button_frame.grid(
            row=4,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )

        set_provision_button = ctk.CTkButton(
            master=set_provision_button_frame,
            text='Set Provisions',
            command=self._go_to_provision_page,
            font=self.font_std
        )
        set_provision_button.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button,
            sticky='se'
        )

    def _go_to_provision_page(self):
        project_name = self.entry_project_name.get()
        vbox_name = self.entry_vbox_name.get()
        if not project_name:
            mb.showerror('Error', 'You must choose a name for the project!')
        elif not vbox_name:
            mb.showerror('Error', 'You must choose a name for the virtual box machine!')
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
