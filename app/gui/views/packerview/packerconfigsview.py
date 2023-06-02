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
        self.add_iso_file()
        self.add_iso_frame()
        self.add_deatils_column()

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
        self.sticky_title = 'wn'
        self.sticky_label = 'w'
        self.sticky_entry = 'w'
        self.sticky_frame = 'wens'
        self.sticky_optionmenu = 'w'


    def add_title(self):
        title_frame = ctk.CTkFrame(self, fg_color='transparent')
        title_frame.columnconfigure(0, weight=1)
        title_frame.rowconfigure(0, weight=1)
        title_frame.rowconfigure(1, weight=1)

        title_frame.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_frame
        )
        self.vagrant_label = ctk.CTkLabel(
            master=title_frame,
            text="Packer",
            font=self.title_std
        )
        self.vagrant_label.grid(
            row=0,
            column=0,
            sticky=self.sticky_label
        )

        self.conf_label = ctk.CTkLabel(
            master=title_frame,
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

    def add_vboxname(self):
        self.vbox_hostname_frame = ctk.CTkFrame(self)
        # self.vbox_hostname_frame.grid_propagate(False)
        self.vbox_hostname_frame.columnconfigure(0, weight=1)
        self.vbox_hostname_frame.columnconfigure(1, weight=1)
        self.vbox_hostname_frame.rowconfigure(0, weight=1)
        self.vbox_hostname_frame.rowconfigure(1, weight=1)

        self.vbox_hostname_frame.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
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
        if self.provisions_configs["configurations"]['vbox_name']["default"]:
            self.entry_vbox_name.insert(
                0,
                self.provisions_configs["configurations"]['vbox_name']["default"]
            )
        self.entry_vbox_name.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_entry
        )
        self.entry_vbox_name.bind("<Configure>", self._vbox_name_check)
        self.entry_vbox_name.bind("<KeyRelease>", self._vbox_name_check)

        self.warning_label_vbox = ctk.CTkLabel(
            master=self.vbox_hostname_frame,
            font=self.font_std
        )
        self.warning_label_vbox.grid(
            row=1,
            column=1,
            padx=self.padx_std,
            pady=0,
            sticky=self.sticky_label
        )
        if self.provisions_configs["configurations"]['vbox_name'] in self.vbox_list:
            self.warning_label_vbox.configure(
                text='A box with this name\nalready exists',
                text_color='red'
            )

    def _vbox_name_check(self, event):
        vbox_name_typed = self.entry_vbox_name.get()
        if vbox_name_typed not in self.vbox_list:
            self.entry_vbox_name.configure(border_color=["#979DA2", "#565B5E"])
            if self.warning_label_vbox.winfo_exists():
                self.warning_label_vbox.destroy()
        if vbox_name_typed in self.vbox_list:
            self.warning_label_vbox = ctk.CTkLabel(
                master=self.vbox_hostname_frame,
                text='A box with this name\nalready exists',
                text_color='red',
                font=self.font_std
            )
            self.warning_label_vbox.grid(
                row=1,
                column=1,
                padx=self.padx_std,
                pady=0,
                sticky=self.sticky_label
            )
            self.entry_vbox_name.configure(border_color='red')

    def add_iso_file(self):
        iso_file_frame = ctk.CTkFrame(self)
        iso_file_frame.columnconfigure(0, weight=1)
        iso_file_frame.columnconfigure(1, weight=1)
        iso_file_frame.rowconfigure(0, weight=1)
        iso_file_frame.rowconfigure(1, weight=1)
        iso_file_frame.grid(
            row=3,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )

        iso_file_label = ctk.CTkLabel(
            master=iso_file_frame,
            font=self.font_std,
            text='Insert Iso File'
        )
        iso_file_label.grid(
            row=0,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.iso_file_entry = ctk.CTkEntry(
            master=iso_file_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std,
            placeholder_text='Iso File'
        )
        self.iso_file_entry.grid(
            row=1,
            column=0,
            sticky=self.sticky_entry,
            padx=self.padx_std,
            pady=self.pady_title
        )

    def add_iso_frame(self):
        iso_frame = ctk.CTkFrame(self)
        iso_frame.columnconfigure(0, weight=1)
        iso_frame.columnconfigure(1, weight=5)
        iso_frame.columnconfigure(2, weight=5)
        iso_frame.rowconfigure(0, weight=1)
        iso_frame.rowconfigure(1, weight=1)
        iso_frame.rowconfigure(2, weight=1)
        iso_frame.rowconfigure(3, weight=1)

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

        iso_link_label = ctk.CTkLabel(
            master=iso_frame,
            text='Insert Iso Link',
            font=self.font_std
        )
        iso_link_label.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )

        self.iso_link_entry = ctk.CTkEntry(
            master=iso_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std,
            placeholder_text='Iso link'
        )
        if self.provisions_configs["configurations"]["iso_link"]["default"]:
            self.entry_vbox_name.insert(
                0,
                self.provisions_configs["configurations"]["iso_link"]["default"]
            )
        self.iso_link_entry.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_entry
        )

        checksum_label = ctk.CTkLabel(
            master=iso_frame,
            text='Insert Checksum',
            font=self.font_std
        )
        checksum_label.grid(
            row=2,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )

        checksum_subframe = ctk.CTkFrame(
            master=iso_frame,
            fg_color='transparent'
        )
        checksum_subframe.grid(
            row=3,
            column=0,
        )
        self.checksum_types = ctk.CTkOptionMenu(
            master=checksum_subframe,
            font=self.font_std,
            values=['SHA-1', 'SHA-224', 'SHA-256', 'SHA-384', 'SHA-512', 'MD5']
        )
        self.checksum_types.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_optionmenu
        )
        self.checksum_entry = ctk.CTkEntry(
            master=checksum_subframe,
            font=self.font_std,
            width=2*self.entry_width_std,
            height=self.entry_height_std,
            placeholder_text='Checksum'
        )
        self.checksum_entry.grid(
            row=0,
            column=1,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_entry
        )


    def add_deatils_column(self):
        """Add entries for cpus, memory, disk size"""
        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.grid(
            row=1,
            column=1,
            rowspan=3,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame
        )

        # specify cpus
        cpus_label = ctk.CTkLabel(
            master=self.details_frame,
            font=self.font_std,
            text='Specify CPUs number'
        )
        cpus_label.grid(
            row=0,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.cpus_entry = ctk.CTkEntry(
            master=self.details_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std,
            placeholder_text='CPUs'
        )
        self.cpus_entry.grid(
            row=1,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )

        # specify memory
        memory_label = ctk.CTkLabel(
            master=self.details_frame,
            font=self.font_std,
            text='Specify Memory in MB'
        )
        memory_label.grid(
            row=2,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.memory_var = ctk.IntVar()
        self.memory_var.set(8192)
        self.memory_slider = ctk.CTkSlider(
            master=self.details_frame,
            variable=self.memory_var,
            from_=256,
            to=16384,
            number_of_steps=63,
            width=self.entry_width_std,
            command=self._show_slider_value
        )
        self.memory_slider.grid(
            row=3,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self._show_slider_value(self.memory_var.get())

        # specify disk size
        disk_label = ctk.CTkLabel(
            master=self.details_frame,
            font=self.font_std,
            text='Specify Disk Size in MB'
        )
        disk_label.grid(
            row=5,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.disk_entry = ctk.CTkEntry(
            master=self.details_frame,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std,
            placeholder_text='Disk Size'
        )
        self.disk_entry.grid(
            row=6,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )

    def _show_slider_value(self, slider_value):
        self.slider_label = ctk.CTkLabel(
            self.details_frame,
            width=250
        )
        self.slider_label.grid(
            row=4,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std
        )
        if slider_value:
            self.slider_label.configure(
            font=self.font_std,
            text=f'Selected Value: {slider_value}'
        )

    def add_set_provisions(self):
        pass
