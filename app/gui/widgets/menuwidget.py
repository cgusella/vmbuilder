import constants
import customtkinter as ctk
import os
import json
import shutil
from gui.guistandard import GuiStandard
from gui.views.utilsview import ScrollableCheckboxFrame
from PIL import Image
from tkinter import filedialog
from tkinter import messagebox as mb


class MenuWidget(GuiStandard):

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)
        self.set_fonts()
        self.set_std_dimensions()
        self.set_icons()
        self.initialize_elements()
        self.render_elements()

    def set_fonts(self):
        family_font = 'Sans'
        self.title_font = ctk.CTkFont(family=family_font, size=20)
        self.label_font = ctk.CTkFont(family=family_font, size=16)
        self.switch_font = ctk.CTkFont(family=family_font, size=14)

    def set_std_dimensions(self):
        self.padx_std = (5, 5)
        self.pady_std = (5, 5)
        self.width_button_std = 80
        self.ipadx_button = 5
        self.ipady_button = 5
        self.pad_up = (5, 0)
        self.pad_down = (0, 5)
        self.pad_five = (5, 5)
        self.padx_btn_left = (5, 0)
        self.sticky_frame = 'wens'

    def set_icons(self):
        self.plus_icon = ctk.CTkImage(
            light_image=Image.open(f'{constants.IMAGES_PATH}/plus_light.png'),
            dark_image=Image.open(f'{constants.IMAGES_PATH}/plus_dark.png'),
            size=(40, 40)
        )
        self.remove_icon = ctk.CTkImage(
            light_image=Image.open(f'{constants.IMAGES_PATH}/remove_light.png'),
            dark_image=Image.open(f'{constants.IMAGES_PATH}/remove_dark.png'),
            size=(40, 40)
        )

    def initialize_elements(self):
        self._initialize_subframes()
        self._initialize_packer_menu()
        self._initialize_vagrant_menu()
        self._initialize_switch_theme()

    def _initialize_subframes(self):
        self.project_title = ctk.CTkLabel(
            master=self,
            text='Projects',
            font=self.title_font
        )
        self.packer_menu_frame = ctk.CTkFrame(self)
        self.vagrant_menu_frame = ctk.CTkFrame(self)
        self.off_on_switch_frame = ctk.CTkFrame(self, fg_color='transparent')

    def _initialize_packer_menu(self):
        self.packer_projects = ScrollableCheckboxFrame(
            master=self.packer_menu_frame,
            title='Packer Projects',
            values=sorted([
                folder for folder in os.listdir(
                    f'{constants.PACKER_MACHINES_PATH}'
                )
                if os.path.isdir(f'{constants.PACKER_MACHINES_PATH}/{folder}')
            ])
        )
        self.add_packer_button = ctk.CTkButton(
            master=self.packer_menu_frame,
            text='',
            image=self.plus_icon,
            width=10,
            height=10,
            fg_color=['grey86', 'grey17'],
            hover_color=['grey76', 'grey7'],
            command=self.master.add_packer_configs
        )
        self.packer_delete_button = ctk.CTkButton(
            master=self.packer_menu_frame,
            text='',
            image=self.remove_icon,
            width=10,
            height=10,
            fg_color=['grey86', 'grey17'],
            hover_color=['grey76', 'grey7'],
            command=self._delete_packer_projects
        )
        self.packer_load_button = ctk.CTkButton(
            master=self.packer_menu_frame,
            text='Load',
            width=self.width_button_std,
            font=self.label_font,
            command=self._load_packer
        )
        self.packer_build_button = ctk.CTkButton(
            master=self.packer_menu_frame,
            text='Build',
            font=self.label_font,
            width=self.width_button_std,
            command=self._build
        )

    def _initialize_vagrant_menu(self):
        self.vagrant_projects = ScrollableCheckboxFrame(
            master=self.vagrant_menu_frame,
            title='Vagrant Projects',
            values=sorted([
                folder for folder in os.listdir(
                    f'{constants.VAGRANT_MACHINES_PATH}'
                )
                if os.path.isdir(f'{constants.VAGRANT_MACHINES_PATH}/{folder}')
            ])
        )
        self.add_vagrant_button = ctk.CTkButton(
            master=self.vagrant_menu_frame,
            text='',
            command=self.master.add_vagrant_configs,
            font=self.label_font,
            image=self.plus_icon,
            width=10,
            height=10,
            fg_color=['grey86', 'grey17'],
            hover_color=['grey76', 'grey7']
        )
        self.delete_vagrant_button = ctk.CTkButton(
            master=self.vagrant_menu_frame,
            text='',
            image=self.remove_icon,
            width=10,
            height=10,
            fg_color=['grey86', 'grey17'],
            hover_color=['grey76', 'grey7'],
            command=self._delete_vagrant_projects
        )
        self.load_vagrant_button = ctk.CTkButton(
            master=self.vagrant_menu_frame,
            text='Load',
            font=self.label_font,
            width=self.width_button_std,
            command=self._load_vagrant
        )
        self.vagrant_up_button = ctk.CTkButton(
            master=self.vagrant_menu_frame,
            text='Up',
            width=self.width_button_std,
            font=self.label_font,
            command=self._up
        )

    def _initialize_switch_theme(self):
        self.off_title = ctk.CTkLabel(
            master=self.off_on_switch_frame,
            text='OFF',
            font=self.switch_font
        )
        self.switch_var = ctk.StringVar(value="on")
        self.swith_light_dark_mode = ctk.CTkSwitch(
            master=self.off_on_switch_frame,
            text='ON',
            font=self.switch_font,
            variable=self.switch_var,
            onvalue='on',
            offvalue='off',
            command=self._swith_light_dark_mode
        )

    def render_elements(self):
        self._render_packer_menu()
        self._render_vagrant_menu()
        self._render_switch_theme()
        self._render_subframes()

    def _render_packer_menu(self):
        self.packer_menu_frame.columnconfigure(0, weight=1)
        self.packer_menu_frame.rowconfigure(0, weight=1)
        self.packer_menu_frame.rowconfigure(1, weight=1)
        self.packer_menu_frame.rowconfigure(2, weight=1)
        self.packer_projects.grid(
            row=0,
            column=0,
            columnspan=4,
            rowspan=2,
            padx=self.padx_std,
            pady=self.pad_five,
            sticky=self.sticky_frame
        )
        self.add_packer_button.grid(
            row=2,
            column=0,
            padx=self.padx_btn_left,
            pady=self.pad_down,
            ipadx=0,
            ipady=0,
        )
        self.packer_delete_button.grid(
            row=2,
            column=1,
            padx=self.padx_btn_left,
            pady=self.pad_down,
            ipadx=0,
            ipady=0,
        )
        self.packer_load_button.grid(
            row=2,
            column=2,
            padx=self.padx_std,
            pady=self.pad_down,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button,
        )
        self.packer_build_button.grid(
            row=2,
            column=3,
            padx=self.padx_std,
            pady=self.pad_down,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button,
        )

    def _render_vagrant_menu(self):
        self.vagrant_menu_frame.columnconfigure(0, weight=1)
        self.vagrant_menu_frame.rowconfigure(0, weight=1)
        self.vagrant_menu_frame.rowconfigure(1, weight=1)
        self.vagrant_menu_frame.rowconfigure(2, weight=1)
        self.vagrant_projects.grid(
            row=0,
            column=0,
            rowspan=2,
            columnspan=4,
            padx=self.padx_std,
            pady=self.pad_five,
            sticky=self.sticky_frame
        )
        self.add_vagrant_button.grid(
            row=2,
            column=0,
            padx=self.padx_btn_left,
            pady=self.pad_down,
            ipadx=0,
            ipady=0
        )
        self.delete_vagrant_button.grid(
            row=2,
            column=1,
            padx=self.padx_btn_left,
            pady=self.pad_down,
            ipadx=0,
            ipady=0
        )
        self.load_vagrant_button.grid(
            row=2,
            column=2,
            padx=self.padx_std,
            pady=self.pad_down,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        self.vagrant_up_button.grid(
            row=2,
            column=3,
            padx=self.padx_std,
            pady=self.pad_down,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )

    def _render_switch_theme(self):
        self.off_on_switch_frame.columnconfigure(0, weight=1)
        self.off_on_switch_frame.columnconfigure(1, weight=1)
        self.off_on_switch_frame.rowconfigure(0, weight=1)
        self.off_title.grid(
            row=0,
            column=0,
            padx=(10, 0),
            pady=(5, 5),
            ipadx=0,
            ipady=0,
            sticky='e'
        )
        self.swith_light_dark_mode.grid(
            row=0,
            column=1,
            padx=(0, 10),
            pady=(5, 5),
            ipadx=0,
            ipady=0,
            sticky='w'
        )

    def _render_subframes(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        self.project_title.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pad_up,
        )
        self.packer_menu_frame.grid(
            row=1,
            column=0,
            rowspan=2,
            padx=self.padx_std,
            pady=self.pad_down,
            sticky=self.sticky_frame
        )

        self.vagrant_menu_frame.grid(
            row=3,
            column=0,
            rowspan=2,
            padx=self.padx_std,
            pady=self.pad_down,
            sticky=self.sticky_frame
        )

        self.off_on_switch_frame.grid(
            row=5,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std
        )

    def _swith_light_dark_mode(self):
        if self.switch_var.get() == 'on':
            ctk.set_appearance_mode('light')
        elif self.switch_var.get() == 'off':
            ctk.set_appearance_mode('dark')

    def _delete_vagrant_projects(self):
        projects = self.vagrant_projects.get()
        if projects:
            message = (
                'This operation in irreversible.\n'
                'You choose to delete the following projects:\n'
            )
            for project in projects:
                message += f'\t- {project}\n'
            yes = mb.askyesnocancel(
                title='Delete Confirm',
                message=message
            )
            if yes:
                for project in projects:
                    shutil.rmtree(f'{constants.VAGRANT_MACHINES_PATH}/{project}')
                self.vagrant_projects.clean()
                self.vagrant_projects.set_values(
                    sorted(
                        [
                            folder for folder in os.listdir(
                                f'{constants.VAGRANT_MACHINES_PATH}'
                            )
                            if os.path.isdir(f'{constants.VAGRANT_MACHINES_PATH}/{folder}')
                        ]
                    )
                )
                self.vagrant_projects.add_checkboxes()

    def _delete_packer_projects(self):
        project_folder = constants.PACKER_MACHINES_PATH
        projects = self.packer_projects.get()

        if projects:
            message = (
                'This operation in irreversible.\n'
                'You choose to delete the following projects:\n'
            )
            for project in projects:
                message += f'\t- {project}\n'
            yes = mb.askyesnocancel(
                title='Delete Confirm',
                message=message
            )
            if yes:
                for project in projects:
                    shutil.rmtree(f'{project_folder}/{project}')
                self.packer_projects.clean()
                self.packer_projects.set_values(
                    sorted(
                        [
                            folder for folder in os.listdir(
                                f'{constants.PACKER_MACHINES_PATH}'
                            )
                            if os.path.isdir(f'{constants.PACKER_MACHINES_PATH}/{folder}')
                        ]
                    )
                )
                self.packer_projects.add_checkboxes()

    def _load_vagrant(self):
        file_to_load = filedialog.askopenfile(
            initialdir=constants.VAGRANT_PROVS_CONFS_PATH
        )
        if file_to_load:
            self.master.provisions_configs = json.loads(file_to_load.read())
            self.master.add_vagrant_configs(load=True)

    def _load_packer(self):
        file_to_load = filedialog.askopenfile(
            initialdir=constants.PACKER_PROVS_CONFS_PATH
        )
        self.master.set_provisions_configs(json.loads(file_to_load.read()))
        self.master.add_packer_configs(load=True)

    def _build(self):
        pass

    def _up(self):
        pass
