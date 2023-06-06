#!/usr/bin/python3
import constants
import customtkinter as ctk
import json
import os
import shutil
from gui.views.packerview.packerconfigsview import PackerConfigsFrame
from gui.views.vagrantview.vagrantconfigsview import VagrantConfigsFrame
from gui.views.vagrantview.vagrantprovisionspackagesview import VagrantProvisionsPackagesFrame
from gui.widgets.menuwidget import MenuWidget
from tkinter import filedialog
from tkinter import messagebox as mb


dir_path = os.path.dirname(os.path.realpath(__file__))
ctk.set_appearance_mode('light')
# ctk.set_default_color_theme(f'{dir_path}/views/dark_blue.json')


class MainFrame(ctk.CTkFrame):

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)
        self.master = master
        self.rows = 4
        self.columns = 3
        self.family = 'Sans'
        self.title_std = ctk.CTkFont(family=self.family, size=24)
        self.font_std = ctk.CTkFont(family=self.family, size=16)
        self.font_packages = ctk.CTkFont(family=self.family, size=14)
        self.set_dimensions()
        self.set_menu_row_col_conf(rows=self.rows, columns=self.columns)

        self.add_lateral_menu()
        self.add_initial_message()
        self.pack(side="top", fill="both", expand=True)

    def set_dimensions(self):
        self.padx_std = (10, 10)
        self.pady_std = (10, 10)
        self.ipadx = 10
        self.ipady = 10
        self.ipadx_button = 5
        self.ipady_button = 5
        self.width_button_std = 100
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

    def set_menu_row_col_conf(self, rows: int, columns: int):
        # self.grid()
        for i in range(columns):
            weight = 1
            if i > 1:
                # this weight set the menu width respect to the
                # view frame. Larger the weight, smaller the menu
                weight = 20
            self.columnconfigure(i, weight=weight)

        for i in range(rows):
            self.rowconfigure(i, weight=1)

    def add_lateral_menu(self):
        self.menu_frame = MenuWidget(master=self)
        self.menu_frame.grid(row=0, column=0, rowspan=self.rows, sticky='wens')

    def set_general_row_col_conf(self, frame: ctk.CTkFrame, rows: int, columns: int):
        for i in range(columns):
            frame.columnconfigure(i, weight=1)

        for i in range(rows):
            frame.rowconfigure(i, weight=1)

    def add_initial_message(self):
        self.initial_message_frame = ctk.CTkScrollableFrame(self)
        self.initial_message_frame.__init__(self)

        self.set_general_row_col_conf(
            frame=self.initial_message_frame,
            rows=2,
            columns=1
        )

        self.initial_message_frame.grid(
            row=0,
            column=1,
            rowspan=2,
            columnspan=self.columns-1,
            sticky=self.sticky_frame
        )

        title_label = ctk.CTkLabel(
            master=self.initial_message_frame,
            font=self.font_std,
            text='Welcome!'
        )
        title_label.grid(
            row=0,
            column=0,
            sticky=self.sticky_title
        )
        message_label = ctk.CTkLabel(
            master=self.initial_message_frame,
            font=self.font_std,
            text="""
Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque
laudantium, totam rem aperiam eaque ipsa, quae ab illo inventore veritatis et quasi
architecto beatae vitae dicta sunt, explicabo. Nemo enim ipsam voluptatem, quia voluptas
sit, aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos, qui ratione
voluptatem sequi nesciunt, neque porro quisquam est, qui dolorem ipsum, quia dolor sit, amet,
consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt, ut labore et
dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum
exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur?
Quis autem vel eum iure reprehenderit, qui in ea voluptate velit esse, quam nihil molestiae
consequatur, vel illum, qui dolorem eum fugiat, quo voluptas nulla pariatur? [33] At vero eos
et accusamus et iusto odio dignissimos ducimus, qui blanditiis praesentium voluptatum deleniti
atque corrupti, quos dolores et quas molestias excepturi sint, obcaecati cupiditate
"""
        )
        message_label.grid(
            row=1,
            column=0,
            sticky='wens'
        )

    def add_vagrant_configs(self, load=False):
        if not load:
            with open(f'{constants.VAGRANT_PROVS_CONFS_PATH}/template.json') as template_json:
                self.provisions_configs = json.loads(template_json.read())
        for operation in ('install', 'uninstall', 'config'):
            self.provisions_configs["provisions"][f"packages_to_{operation}"] = set(
                self.provisions_configs["provisions"][f"packages_to_{operation}"]
            )

        self.vagrant_configs_frame = VagrantConfigsFrame(
            self,
            self.provisions_configs
        )
        self.vagrant_configs_frame.grid(
            row=0,
            column=1,
            columnspan=self.columns-1,
            rowspan=self.rows,
            sticky=self.sticky_frame
        )

    def add_vagrant_provisions_frame(self):
        self.vagrant_configs_frame.destroy()
        vagrant_configs_view = VagrantProvisionsPackagesFrame(
            master=self,
            provisions_configs=self.provisions_configs
        )
        vagrant_configs_view.grid(
            row=0,
            column=1,
            columnspan=self.columns-1,
            rowspan=self.rows,
            sticky=self.sticky_frame
        )

    def _load_vagrant(self):
        file_to_load = filedialog.askopenfile(
            initialdir=constants.VAGRANT_PROVS_CONFS_PATH
        )
        self.provisions_configs = json.loads(file_to_load.read())
        self.add_vagrant_configs(load=True)

    def _delete_projects(self, vm_type):
        if vm_type == 'packer':
            project_folder = constants.PACKER_MACHINES_PATH
            projects = self.packer_projects.get()
        elif vm_type == 'vagrant':
            project_folder = constants.VAGRANT_MACHINES_PATH
            projects = self.vagrant_projects.get()

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
            self.add_lateral_menu()

    def _up(self):
        project_name = self.vagrant_projects.get()
        if project_name:
            if len(project_name) > 1:
                mb.showerror('Up Error', 'You must select just one project to up')
            else:
                self.destroy()
                self.__init__(self.master)

                terminal_frame = ctk.CTkFrame(self)
                terminal_frame.grid(
                    row=2,
                    column=1,
                    columnspan=self.columns-1,
                    rowspan=2,
                    sticky=self.sticky_frame
                )
                wid = terminal_frame.winfo_id()
                os.chdir(f'{constants.VAGRANT_MACHINES_PATH}/{project_name[0]}')
                # os.system(f'xterm -into {wid} -geometry 218x38 -sb -e "vagrant up ; while true ; do sleep 100 ; done" &')
                os.system(f'xterm -into {wid} -geometry 218x38 -sb -e vagrant up &')
                os.chdir(f'{constants.VMBUILDER_PATH}')

    def _load_packer(self):
        pass

    def _build(self):
        pass

    def add_packer_configs(self):
        with open(f'{constants.PACKER_PROVS_CONFS_PATH}/template.json') as template_json:
            self.provisions_configs = json.loads(template_json.read())
        for operation in ('install', 'uninstall', 'config'):
            self.provisions_configs["provisions"][f"packages_to_{operation}"] = set(
                self.provisions_configs["provisions"][f"packages_to_{operation}"]
            )
        self.initial_message_frame.destroy()
        self.vagrant_configs_frame = PackerConfigsFrame(
            self,
            self.provisions_configs
        )
        self.vagrant_configs_frame.grid(
            row=0,
            column=1,
            columnspan=self.columns-1,
            rowspan=self.rows,
            sticky=self.sticky_frame
        )

    def close_window(self):
        self.master.destroy()


if __name__ == "__main__":
    os.chdir(constants.VMBUILDER_PATH)
    root = ctk.CTk()
    root.wm_geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    main = MainFrame(
        master=root,
    )
    main.master.title('HackTheMonkey')
    root.mainloop()
