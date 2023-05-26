import constants
import customtkinter as ctk
import json
import os
import shutil
from gui.views.utilsview import ScrollableCheckboxFrame
from gui.views.vagrantview.vagrantconfigsview import VagrantConfigsFrame
from gui.views.vagrantview.vagrantprovisionspackagesview import VagrantProvisionsPackagesFrame
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
        self.font_std = ctk.CTkFont(family=self.family, size=20)
        self.set_dimensions()
        self.set_grid(rows=self.rows, columns=self.columns)

        # we separate the main frame into 2 parts:
        # the menu frame and the view frame.

        # add menu frame
        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.grid(row=0, column=0, rowspan=self.rows, sticky='wens')
        self.add_lateral_menu()

        self.add_initial_message()
        self.pack(side="top", fill="both", expand=True)

    def set_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)
        self.ipadx = 10
        self.ipady = 10
        self.ipadx_button = 5
        self.ipady_button = 5
        self.width_button_std = 100
        self.pady_up = (10, 5)
        self.pady_down = (5, 10)
        self.pady_equal = (5, 5)

    def set_grid(self, rows: int, columns: int):
        self.grid()
        for i in range(columns):
            weight = 1
            if i > 1:
                # this weight set the menu width respect to the
                # view frame. Larger the weight, smaller the menu
                weight = 15
            self.columnconfigure(i, weight=weight)

        for i in range(rows):
            self.rowconfigure(i, weight=1)

    def add_lateral_menu(self):
        # configure menu frame
        self.menu_frame.columnconfigure(0, weight=1)
        self.menu_frame.rowconfigure(0, weight=1)
        self.menu_frame.rowconfigure(1, weight=1)
        self.menu_frame.rowconfigure(2, weight=1)
        self.menu_frame.rowconfigure(3, weight=1)

        # add menu title
        project_title = ctk.CTkLabel(
            self.menu_frame,
            text='Projects',
            font=self.title_std
        )
        project_title.grid(row=0, column=0, padx=self.padx_std,
                           pady=self.pady_std)

        # add packer frame to menu
        packer_menu_frame = ctk.CTkFrame(self.menu_frame)
        packer_menu_frame.grid(row=1, column=0)
        packer_menu_frame.columnconfigure(0, weight=1)
        packer_menu_frame.columnconfigure(1, weight=1)
        packer_menu_frame.rowconfigure(0, weight=1)
        packer_menu_frame.rowconfigure(1, weight=1)
        packer_menu_frame.rowconfigure(2, weight=1)
        add_packer_button = ctk.CTkButton(
            packer_menu_frame,
            text='Add Packer Project',
            command=self.add_packer_configs,
            font=self.font_std
        )
        add_packer_button.grid(row=1, column=0, columnspan=2,
                               pady=self.pady_up,
                               ipadx=self.ipadx_button,
                               ipady=self.ipady_button)
        self.packer_projects = ScrollableCheckboxFrame(
            master=packer_menu_frame,
            title='Packer Projects',
            values=sorted([
                folder for folder in os.listdir(f'{constants.PACKER_MACHINES_PATH}')
                if os.path.isdir(f'{constants.PACKER_MACHINES_PATH}/{folder}')
            ])
        )
        self.packer_projects.grid(row=2, column=0, columnspan=2, padx=self.padx_std,
                             pady=self.pady_equal)
        packer_delete_button = ctk.CTkButton(
            packer_menu_frame,
            text='Delete',
            font=self.font_std,
            width=self.width_button_std,
            command=lambda: self._delete_projects('packer')
        )
        packer_delete_button.grid(row=3, column=0,
                                  padx=self.padx_std, pady=self.pady_down,
                                  ipadx=self.ipadx_button,
                                  ipady=self.ipady_button)
        packer_load_button = ctk.CTkButton(
            packer_menu_frame,
            text='Load',
            font=self.font_std,
            width=self.width_button_std,
        )
        packer_load_button.grid(row=3, column=1,
                                padx=self.padx_std, pady=self.pady_down,
                                ipadx=self.ipadx_button,
                                ipady=self.ipady_button)

        # add vagrant frame to menu
        vagrant_menu_frame = ctk.CTkFrame(self.menu_frame)
        vagrant_menu_frame.grid(row=2, column=0)
        vagrant_menu_frame.columnconfigure(0, weight=1)
        vagrant_menu_frame.columnconfigure(1, weight=1)
        vagrant_menu_frame.rowconfigure(0, weight=1)
        vagrant_menu_frame.rowconfigure(1, weight=1)
        vagrant_menu_frame.rowconfigure(2, weight=1)
        add_vagrant_button = ctk.CTkButton(
            vagrant_menu_frame,
            text='Add Vagrant Project',
            command=self.add_vagrant_configs,
            font=self.font_std,
        )
        add_vagrant_button.grid(row=1, column=0, columnspan=2,
                                pady=self.pady_up,
                                ipadx=self.ipadx_button,
                                ipady=self.ipady_button)
        self.vagrant_projects = ScrollableCheckboxFrame(
            master=vagrant_menu_frame,
            title='Vagrant Projects',
            values=[
                folder for folder in os.listdir(f'{constants.VAGRANT_MACHINES_PATH}')
                if os.path.isdir(f'{constants.VAGRANT_MACHINES_PATH}/{folder}')
            ]
        )
        self.vagrant_projects.grid(row=2, column=0, columnspan=2, padx=self.padx_std,
                              pady=self.pady_equal)
        vagrant_delete_button = ctk.CTkButton(
            vagrant_menu_frame,
            text='Delete',
            font=self.font_std,
            width=self.width_button_std,
            command=lambda: self._delete_projects('vagrant')
        )
        vagrant_delete_button.grid(row=3, column=0,
                                   padx=self.padx_std, pady=self.pady_down,
                                   ipadx=self.ipadx_button,
                                   ipady=self.ipady_button)
        vagrant_load_button = ctk.CTkButton(
            vagrant_menu_frame,
            text='Load',
            font=self.font_std,
            width=self.width_button_std,
            command=self._load_vagrant
        )
        vagrant_load_button.grid(row=3, column=1,
                                 padx=self.padx_std, pady=self.pady_down,
                                 ipadx=self.ipadx_button,
                                 ipady=self.ipady_button)

        # add switch light/dark mode
        self.switch_var = ctk.StringVar(value="on")
        swith_light_dark_mode = ctk.CTkSwitch(
            self.menu_frame,
            text='Switch theme',
            variable=self.switch_var,
            onvalue='on',
            offvalue='off',
            command=self._swith_light_dark_mode
        )
        swith_light_dark_mode.grid(row=3, column=0, columnspan=2)

    def _swith_light_dark_mode(self):
        if self.switch_var.get() == 'on':
            ctk.set_appearance_mode('light')
        elif self.switch_var.get() == 'off':
            ctk.set_appearance_mode('dark')

    def add_initial_message(self):
        self.initial_message_frame = ctk.CTkScrollableFrame(self)
        self.initial_message_frame.__init__(self)
        self.initial_message_frame.grid(row=0, column=1, rowspan=self.rows,
                                        columnspan=self.columns-1,
                                        sticky='wnes')
        self.initial_message_frame.columnconfigure(0, weight=1)
        self.initial_message_frame.rowconfigure(0, weight=1)
        self.initial_message_frame.rowconfigure(1, weight=1)
        title_label = ctk.CTkLabel(
            self.initial_message_frame,
            font=self.font_std,
            text='Welcome!'
        )
        title_label.grid(row=0, column=0, sticky='wens')
        message_label = ctk.CTkLabel(
            self.initial_message_frame,
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
non provident, similique sunt in culpa, qui officia deserunt mollitia animi, id est
laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio.
Nam libero tempore, cum soluta nobis est eligendi optio, cumque nihil impedit,
quo minus id, quod maxime placeat, facere possimus, omnis voluptas assumenda est,
omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut
rerum necessitatibus saepe eveniet, ut et voluptates repudiandae sint et molestiae
non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis
"""
        )
        message_label.grid(row=1, column=0, sticky='wens')

    def add_vagrant_configs(self, load=False):
        if not load:
            with open(f'{constants.VAGRANT_PROVS_CONFS_PATH}/template.json') as template_json:
                self.provisions_configs = json.loads(template_json.read())
        for operation in ('install', 'uninstall', 'config'):
            self.provisions_configs["provisions"][f"packages_to_{operation}"] = set(
                self.provisions_configs["provisions"][f"packages_to_{operation}"]
            )
        self.initial_message_frame.destroy()
        self.vagrant_configs_frame = VagrantConfigsFrame(
            self,
            self.provisions_configs
        )
        self.vagrant_configs_frame.grid(row=0, column=1,
                                        columnspan=self.columns-1,
                                        rowspan=self.rows, sticky='wens')

    def add_vagrant_provisions_frame(self):
        self.vagrant_configs_frame.destroy()
        vagrant_configs_view = VagrantProvisionsPackagesFrame(
            master=self,
            provisions_configs=self.provisions_configs
        )
        vagrant_configs_view.grid(row=0, column=1, columnspan=self.columns-1,
                                  rowspan=self.rows, sticky='wens')

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

    def add_packer_configs(self):
        pass

    def close_window(self):
        self.master.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    root.wm_geometry("1800x1100")
    main = MainFrame(root)
    main.master.title('HackTheMonkey')
    root.mainloop()
