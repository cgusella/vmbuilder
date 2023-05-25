import constants
import customtkinter as ctk
import json
import os
from gui.views.vagrantview.vagrantconfigsview import VagrantConfigsView
from gui.views.vagrantview.vagrantprovisionspackagesview import VagrantProvisionsPackagesView
from gui.views.vagrantview.vagrantprovisionsscriptview import VagrantProvisionsScriptView


dir_path = os.path.dirname(os.path.realpath(__file__))
ctk.set_appearance_mode('light')
# ctk.set_default_color_theme(f'{dir_path}/views/dark_blue.json')


class ScrollableCheckboxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []

        for count, value in enumerate(self.values):
            checkbox = ctk.CTkCheckBox(self, text=value)
            checkbox.grid(row=count, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes


class MainFrame(ctk.CTkFrame):

    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master)
        self.master = master
        self.rows = 4
        self.columns = 3
        self.padx_std = (10, 10)
        self.pady_std = (10, 10)
        self.family = 'Sans'
        self.title_std = ctk.CTkFont(family=self.family, size=20)
        self.font_std = ctk.CTkFont(family=self.family, size=16)
        self.set_grid(rows=self.rows, columns=self.columns)

        # we separate the main frame into 2 parts:
        # the menu frame and the view frame.

        # add menu frame
        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.grid(row=0, column=0, rowspan=self.rows,
                             sticky='wens', padx=(0, 0))
        self.add_lateral_menu()
        # add view frame
        self.view_frame = ctk.CTkFrame(self)
        self.view_frame.grid(row=0, column=1, rowspan=self.rows,
                             columnspan=self.columns-1,
                             sticky='wens', padx=(0, 0))

        self.add_initial_message()
        # self.add_machines_types_button()
        # self.add_bottom_button()
        self.pack(side="top", fill="both", expand=True)

    def add_lateral_menu(self):
        # configure menu frame
        self.menu_frame.columnconfigure(0, weight=1)
        self.menu_frame.rowconfigure(0, weight=1)
        self.menu_frame.rowconfigure(1, weight=1)
        self.menu_frame.rowconfigure(2, weight=1)
        self.menu_frame.rowconfigure(3, weight=1)

        # add menu title
        project_title = ctk.CTkLabel(self.menu_frame, text='Projects',
                                     font=self.title_std)
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
                               padx=self.padx_std, pady=self.pady_std)
        packer_projects = ScrollableCheckboxFrame(
            master=packer_menu_frame,
            title='Packer Projects',
            values=[
                folder for folder in os.listdir(f'{constants.PACKER_MACHINES_PATH}')
                if os.path.isdir(f'{constants.PACKER_MACHINES_PATH}/{folder}')
            ]
        )
        packer_projects.grid(row=2, column=0, columnspan=2, padx=self.padx_std,
                             pady=self.pady_std)
        packer_delete_button = ctk.CTkButton(
            packer_menu_frame,
            text='Delete',
            font=self.font_std
        )
        packer_delete_button.grid(row=3, column=0, padx=self.padx_std,
                                  pady=self.pady_std)
        packer_load_button = ctk.CTkButton(
            packer_menu_frame,
            text='Load',
            font=self.font_std
        )
        packer_load_button.grid(row=3, column=1, padx=self.padx_std,
                                pady=self.pady_std)

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
            font=self.font_std
        )
        add_vagrant_button.grid(row=1, column=0, columnspan=2,
                                padx=self.padx_std, pady=self.pady_std)
        vagrant_projects = ScrollableCheckboxFrame(
            master=vagrant_menu_frame,
            title='Vagrant Projects',
            values=[
                folder for folder in os.listdir(f'{constants.VAGRANT_MACHINES_PATH}')
                if os.path.isdir(f'{constants.VAGRANT_MACHINES_PATH}/{folder}')
            ]
        )
        vagrant_projects.grid(row=2, column=0, columnspan=2, padx=self.padx_std,
                              pady=self.pady_std)
        vagrant_delete_button = ctk.CTkButton(
            vagrant_menu_frame,
            text='Delete',
            font=self.font_std
        )
        vagrant_delete_button.grid(row=3, column=0, padx=self.padx_std,
                                   pady=self.pady_std)
        vagrant_load_button = ctk.CTkButton(
            vagrant_menu_frame,
            text='Load',
            font=self.font_std
        )
        vagrant_load_button.grid(row=3, column=1, padx=self.padx_std,
                                 pady=self.pady_std)

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
        initial_message_frame = ctk.CTkScrollableFrame(
            self,
            label_text='Welcome!',
        )
        initial_message_frame.grid(row=0, column=1, rowspan=self.rows,
                                   columnspan=self.columns-1, sticky='wnes')
        initial_message_frame.columnconfigure(0, weight=1)
        initial_message_frame.rowconfigure(0, weight=1)
        message_label = ctk.CTkLabel(
            initial_message_frame,
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
        message_label.pack(padx=(0, 0))

    def add_machines_types_button(self):
        self.types_frame = ctk.CTkFrame(self)
        self.types_frame.grid(row=0, column=0, columnspan=self.columns)
        vagrant_button = ctk.CTkButton(self.types_frame, text='Vagrant',
                                       command=self.add_vagrant_configs)
        vagrant_button.pack(side='left', padx=(10, 100), pady=10)

    def add_bottom_button(self, back: bool = False):
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.grid(row=self.rows-1, column=0, columnspan=3)
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(1, weight=1)
        self.bottom_frame.columnconfigure(2, weight=1)
        self.bottom_frame.columnconfigure(3, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)
        if not back:
            exit_button = ctk.CTkButton(self.bottom_frame, text='exit',
                                        command=self.close_window)
            exit_button.grid(row=0, column=1, columnspan=2)
        else:
            exit_button = ctk.CTkButton(self.bottom_frame, text='exit',
                                        command=self.close_window)
            exit_button.grid(row=0, column=2)
            back_button = ctk.CTkButton(self.bottom_frame, text='Back',
                                        command=lambda args=(self, back): start(*args))
            back_button.grid(row=0, column=1)

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

    def add_vagrant_configs(self):
        with open(f'{constants.VAGRANT_PROVS_CONFS_PATH}/template.json') as template_json:
            self.provisions_configs = json.loads(template_json.read())
        for operation in ('install', 'uninstall', 'config'):
            self.provisions_configs["provisions"][f"packages_to_{operation}"] = set()
        vagrant_configs_view = VagrantConfigsView(
            master=self,
            provisions_configs=self.provisions_configs
        )
        vagrant_configs_view.grid(row=0, column=1, rowspan=self.rows,
                                  columnspan=self.columns-1,
                                  sticky='wens')
        self.add_bottom_button(back=True)
        self.types_frame.destroy()

    def add_vagrant_provisions_frame(self):
        vagrant_configs_view = VagrantProvisionsScriptView(
            master=self,
            provisions_configs=self.provisions_configs
        )
        vagrant_configs_view.grid(row=1, column=0, columnspan=3, sticky='wens')
        vagrant_configs_view = VagrantProvisionsPackagesView(
            master=self,
            provisions_configs=self.provisions_configs
        )
        vagrant_configs_view.grid(row=2, column=0, columnspan=5, sticky='wens')

    def add_packer_configs(self):
        pass

    def close_window(self):
        self.master.destroy()


def start(mainview=None, back=False):
    if back:
        mainview.destroy()
        mainview.__init__(master=mainview.master)
    else:
        root = ctk.CTk()
        root.wm_geometry("1400x900")
        main = MainFrame(root)
        main.master.title('HackTheMonkey')
        root.mainloop()


if __name__ == "__main__":
    start()
