import constants
import json
import tkinter as tk
from gui.views.vagrantview.vagrantconfigsview import VagrantConfigsView
from gui.views.vagrantview.vagrantprovisionsview import VagrantProvisionsView


class MainView(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.rows = 3
        self.columns = 3
        self.set_grid(rows=self.rows, columns=self.columns)
        self.add_machines_types_button()
        self.add_bottom_button()

    def add_machines_types_button(self):
        types_frame = tk.Frame(self)
        types_frame.grid(row=0, column=0, columnspan=self.columns)
        vagrant_button = tk.Button(types_frame, text='Vagrant',
                                   command=self.add_vagrant_configs)
        vagrant_button.pack(side='left')

        packer_button = tk.Button(types_frame, text='Packer',
                                  command=self.add_packer_configs)
        packer_button.pack(side='right')

    def add_bottom_button(self):
        bottom_frame = tk.Frame(self)
        bottom_frame.grid(row=2, column=0, columnspan=3)
        exit_button = tk.Button(bottom_frame, text='exit',
                                command=self.close_window)
        exit_button.pack(side='bottom', anchor='n')

    def set_grid(self, rows: int, columns: int):
        self.grid()
        for i in range(columns):
            weight = 1
            if i in [1]:
                weight = 2
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
        vagrant_configs_view.grid(row=1, column=0, columnspan=5, sticky='wens')

    def add_vagrant_provisions(self):
        vagrant_provs_view = VagrantProvisionsView(
            master=self,
            provisions_configs=self.provisions_configs
        )
        vagrant_provs_view.grid(row=1, column=0, columnspan=5, sticky='wens')

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
