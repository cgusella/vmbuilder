import customtkinter as ctk
from argumentparser.helper import get_local_vagrant_boxes
from existencecontroller.controller import launch_vboxmanage_lst_command
from gui.widgets.projectnamewidget import VagrantProjectNameWidget
from gui.widgets.titlewidget import TitleWidget
from gui.widgets.vagrantboxsetupwidget import VagrantBoxSetUpWidget
from gui.widgets.vboxconfigswidget import VboxConfigsWidget
from tkinter import messagebox as mb
from tkinter import StringVar


class VagrantConfigsView(ctk.CTkFrame):
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
        self.warning_font = ctk.CTkFont(family=self.master.family, size=11)
        self.font_std = ctk.CTkFont(family=self.master.family, size=18)
        self.set_grid()
        self.set_std_dimensions()
        self.add_titles()
        self.add_project_name()
        self.add_vagrant_box_setup()
        self.add_vbox_configs()
        self.add_connection_mode_frame()
        self.add_set_provision_button()
        self.render()

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)
        self.pady_title = (10, 2)
        self.pady_entry = (2, 10)
        self.ipadx_std = 10
        self.ipady_std = 10
        self.ipadx_button = 5
        self.ipady_button = 5
        self.sticky_title = 'wn'
        self.sticky_label = 'ws'
        self.sticky_entry = 'wn'
        self.sticky_up = 'wen'
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
        # project name, connection mode
        self.rowconfigure(1, weight=1)
        # vbox_host, # username_password,
        self.rowconfigure(2, weight=1)
        # select vagrant box, set provision button
        self.rowconfigure(3, weight=1)

    def set_general_row_col_conf(self, frame:ctk.CTkFrame, rows: int, columns: int):
        # self.grid()
        for i in range(columns):
            frame.columnconfigure(i, weight=1)

        for i in range(rows):
            frame.rowconfigure(i, weight=1)

    def add_titles(self):
        self.title_frame = TitleWidget(
            master=self,
            title='Vagrant',
            subtitle='Configurations'
        )

    def add_project_name(self):
        self.project_name_frame = VagrantProjectNameWidget(
            master=self,
            provisions_configs=self.provisions_configs
        )

    def add_vagrant_box_setup(self):
        self.vagrant_box_setup_frame = VagrantBoxSetUpWidget(
            master=self,
            provisions_configs=self.provisions_configs
        )

    def add_vbox_configs(self):
        self.vbox_configs_frame = VboxConfigsWidget(
            master=self,
            provisions_configs=self.provisions_configs
        )

    def add_connection_mode_frame(self):
        self.connection_mode_frame = ctk.CTkFrame(self)

        self.set_general_row_col_conf(
            frame=self.connection_mode_frame,
            rows=2,
            columns=1
        )

        ssh_label = ctk.CTkLabel(
            master=self.connection_mode_frame,
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
        self.connection_mode_var.set('key')
        if self.provisions_configs["configurations"]["connection"]["default"]:
            self.connection_mode_var.set(
                self.provisions_configs["configurations"]["connection"]["default"]
            )

        ssh_key = ctk.CTkRadioButton(
            master=self.connection_mode_frame,
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
            master=self.connection_mode_frame,
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

    def add_set_provision_button(self):
        self.set_provision_button_frame = ctk.CTkFrame(
            self,
            height=100,
            fg_color='transparent'
        )

        self.set_general_row_col_conf(
            frame=self.set_provision_button_frame,
            rows=1,
            columns=1
        )
        set_provision_button = ctk.CTkButton(
            master=self.set_provision_button_frame,
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

    def render(self):
        self.title_frame.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_frame
        )
        self.project_name_frame.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )
        self.vagrant_box_setup_frame.grid(
            row=2,
            column=0,
            rowspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame,
        )
        self.vbox_configs_frame.grid(
            row=1,
            column=1,
            rowspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )
        self.connection_mode_frame.grid(
            row=4,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )
        self.set_provision_button_frame.grid(
            row=4,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )

    def _go_to_provision_page(self):
        project_name = self.project_name_frame.project_name_entry.get()
        vbox_name = self.vbox_configs_frame.vbox_name_entry.get()
        if not project_name:
            mb.showerror('Error', 'You must choose a name for the project!')
        elif not vbox_name:
            mb.showerror('Error', 'You must choose a name for the virtual box machine!')
        elif not self.vagrant_box_setup_frame.username_entry.get():
            mb.showerror('Error', 'You must specify the existing username of the vagrant box for vagrant to be able to connect to the machine!')
        elif not self.vagrant_box_setup_frame.password_entry.get():
            mb.showerror('Error', 'You must specify the password of the specified user for vagrant to be able to connect to the machine!')
        elif not self.vagrant_box_setup_frame.vagrant_box.get():
            mb.showerror('Error', 'You must choose a Vagrant box!')
        else:
            self.provisions_configs["configurations"]["project_name"]["default"] = project_name
            self.provisions_configs["configurations"]["vbox_name"]["default"] = vbox_name
            self.provisions_configs["configurations"]["hostname"]["default"] = self.vagrant_box_setup_frame.hostname_entry.get()
            self.provisions_configs["credentials"]["username"] = self.vagrant_box_setup_frame.username_entry.get()
            self.provisions_configs["credentials"]["password"] = self.vagrant_box_setup_frame.password_entry.get()
            self.provisions_configs["credentials"]["extra_user"] = self.vagrant_box_setup_frame.extra_user_entry.get()
            self.provisions_configs["configurations"]["image"]["default"] = self.vagrant_box_setup_frame.vagrant_box.get()
            self.provisions_configs["configurations"]["cpus"]["default"] = self.vbox_configs_frame.cpus_value.get()
            self.provisions_configs["configurations"]["memory"]["default"] = int(self.vbox_configs_frame.memory_slider.get())
            self.provisions_configs["configurations"]["disk_size"]["default"] = self.vbox_configs_frame.disk_slider_value.get()
            self.destroy()
            self.master.add_vagrant_provisions_frame()

    def get_vagrant_configs(self):
        return self.provisions_configs

    def set_connection_mode(self):
        self.provisions_configs["configurations"]["connection"]["default"] = self.connection_mode_var.get()
