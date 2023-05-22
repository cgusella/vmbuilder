import constants
import json
import tkinter as tk
from tkinter import ttk
from gui.views.vagrantview.vagrantconfigsview import VagrantConfigsView


class MainView(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.rows = 13
        self.columns = 5
        self.set_grid(rows=self.rows, columns=self.columns)
        self.add_main_buttons()

    def add_main_buttons(self):
        self.vagrant_button = tk.Button(self, text='Vagrant',
                                        command=self.add_vagrant_configs)
        self.vagrant_button.grid(row=0, column=1)

        self.packer_button = tk.Button(self, text='Packer',
                                       command=self.add_packer_configs)
        self.packer_button.grid(row=0, column=2)

        exit_button = tk.Button(self, text='exit', command=self.close_window)
        exit_button.grid(row=self.rows-1, column=self.columns-1)

    def set_grid(self, rows: int, columns: int):
        self.grid()
        for i in range(columns):
            self.columnconfigure(i, weight=1)

        for i in range(rows):
            self.rowconfigure(i, weight=1)

    def add_vagrant_configs(self):
        with open(f'{constants.VAGRANT_PROVS_CONFS_PATH}/template.json') as template_json:
            provisions_configs = json.loads(template_json.read())
        # vagrant_configs = tk.Frame(self.master)
        # vagrant_configs.pack(side='top', anchor='s')
        separator = ttk.Separator(
            master=self,
            orient='horizontal',
            style='blue.TSeparator',
            class_=ttk.Separator,
            takefocus=1,
            cursor='plus'
        )
        separator.grid(row=1, column=1, columnspan=3, sticky='EW')
        conf_label = tk.Label(self, text="Vagrant Configurations")
        conf_label.grid(row=1, column=1)
        machine_name_label = tk.Label(self, text="New machine name:")
        machine_name_label.grid(row=2, column=1)
        self.entry_project_name = tk.Entry(self)
        self.entry_project_name.insert(
            0,
            provisions_configs["configurations"]["machine_name"]
        )
        self.entry_project_name.grid(row=3, column=1)

        vbox_name_label = tk.Label(self, text="Virtual box name:")
        vbox_name_label.grid(row=5, column=1)
        self.entry_vbox_name = tk.Entry(self)
        self.entry_vbox_name.insert(
            0,
            provisions_configs["configurations"]['vbox_name']
        )
        self.entry_vbox_name.grid(row=6, column=1)

        username_label = tk.Label(self, text="Username:")
        username_label.grid(row=7, column=1)
        self.entry_default_username = tk.Entry(self)
        self.entry_default_username.insert(
            0,
            provisions_configs["credentials"]['username']
        )
        self.entry_default_username.grid(row=8, column=1)

        machine_name_label = tk.Label(self, text="Password:")
        machine_name_label.grid(row=7, column=2)
        self.entry_default_password = tk.Entry(self)
        self.entry_default_password.insert(
            0,
            provisions_configs["credentials"]['password']
        )
        self.entry_default_password.grid(row=8, column=2)

        machine_name_label = tk.Label(self, text="Extra user:")
        machine_name_label.grid(row=9, column=1)
        self.entry_extra_user = tk.Entry(self)
        self.entry_extra_user.insert(
            0,
            provisions_configs["credentials"]['extra_user']
        )
        self.entry_extra_user.grid(row=10, column=1)

    def add_packer_configs(self):
        pass

    def close_window(self):
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_geometry("800x800")
    main = MainView(root)
    main.master.title('HackTheMonkey')
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
