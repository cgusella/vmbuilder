#!/usr/bin/python3
import constants
import customtkinter as ctk
import json
import os
from gui.guistandard import GuiStandard
from gui.views.packerview.packerconfigsview import PackerConfigsFrame
from gui.views.vagrantview.vagrantconfigsview import VagrantConfigsView
from gui.widgets.menuwidget import MenuWidget


dir_path = os.path.dirname(os.path.realpath(__file__))
ctk.set_appearance_mode('system')


class MainFrame(GuiStandard):

    def __init__(self, master):
        self.frame_name = 'main'
        ctk.CTkFrame.__init__(self, master)
        self.master = master
        self.set_fonts()
        self.set_std_dimensions()
        self.initialize_elements()
        self.render_elements()
        self.pack(side="top", fill="both", expand=True)

    def set_provisions_configs(self, provisions_configs: dict):
        self.provisions_configs = provisions_configs

    def set_fonts(self):
        family = 'Sans'
        self.title_std = ctk.CTkFont(family=family, size=24)
        self.font_std = ctk.CTkFont(family=family, size=16)
        self.font_packages = ctk.CTkFont(family=family, size=14)

    def set_std_dimensions(self):
        self.padx_std = (10, 10)
        self.pady_std = (10, 10)
        self.ipadx = 10
        self.ipady = 10
        self.ipadx_button = 5
        self.ipady_button = 5
        self.pad_left = (10, 5)
        self.pad_right = (5, 10)
        self.pad_five = (5, 5)
        self.padx_btn_right = (0, 5)
        self.padx_btn_left = (5, 0)
        self.sticky_title = 'wn'
        self.sticky_label = 'ws'
        self.sticky_entry = 'wn'
        self.sticky_frame = 'wens'
        self.sticky_optionmenu = 'w'

    def initialize_elements(self):
        self._initialize_subframes()
        self._initialize_first_page()

    def _initialize_subframes(self):
        self.menu_frame = MenuWidget(self)
        self.operative_frame = ctk.CTkScrollableFrame(self)

    def _initialize_first_page(self):
        self.message_label = ctk.CTkLabel(
            master=self.operative_frame,
            font=self.font_std,
            text='welcome!'
        )

    def render_elements(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.menu_frame.grid(
            row=0,
            column=0,
            rowspan=4,
            sticky=self.sticky_frame
        )
        self._render_operative_frame()

    def _render_operative_frame(self):
        self.operative_frame.grid(
            row=0,
            column=1,
            columnspan=4,
            rowspan=4,
            sticky=self.sticky_frame
        )

    def add_vagrant_configs(self, load=False):
        if not load:
            with open(f'{constants.VAGRANT_PROVS_CONFS_PATH}/template.json') as template_json:
                self.provisions_configs = json.loads(template_json.read())
        for operation in ('install', 'uninstall', 'config'):
            self.provisions_configs["provisions"][f"packages_to_{operation}"] = set(
                self.provisions_configs["provisions"][f"packages_to_{operation}"]
            )
        self.operative_frame = VagrantConfigsView(
            self,
            self.provisions_configs
        )
        self._render_operative_frame()

    def add_packer_configs(self, load=False):
        if not load:
            with open(f'{constants.PACKER_PROVS_CONFS_PATH}/template.json') as template_json:
                self.provisions_configs = json.loads(template_json.read())
        for operation in ('install', 'uninstall', 'config'):
            self.provisions_configs["provisions"][f"packages_to_{operation}"] = set(
                self.provisions_configs["provisions"][f"packages_to_{operation}"]
            )
        self.operative_frame = PackerConfigsFrame(
            self,
            self.provisions_configs
        )
        self._render_operative_frame()


if __name__ == "__main__":
    os.chdir(constants.VMBUILDER_PATH)
    root = ctk.CTk()
    root.wm_geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    main = MainFrame(
        master=root,
    )
    main.master.title('HackTheMonkey')
    root.mainloop()
