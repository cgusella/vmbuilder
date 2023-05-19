import tkinter as tk
from argumentparser.helper import get_local_vagrant_boxes
from gui.views.vagrantview.vagrantprovisionsview import VagrantProvisionsView
from tkinter import ttk


class VagrantConfigsView(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        self.provisions_configs = dict()
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.geometry("600x400")
        self.set_grid()
        self.vagrant_label = tk.Label(self, text="Vagrant", font='sans 16 bold')
        self.vagrant_label.grid(row=0, column=0, columnspan=4)

        self.conf_label = tk.Label(self, text="Configurations")
        self.conf_label.grid(row=1, column=0, columnspan=4)

        separator = ttk.Separator(
            master=self,
            orient='horizontal',
            style='blue.TSeparator',
            class_=ttk.Separator,
            takefocus=1,
            cursor='plus'
        )
        separator.grid(row=2, column=0, columnspan=4, sticky='EW')

        startcolumn = 1
        self.entry_project_name = tk.Entry(self)
        self.entry_project_name.insert(0, 'Project name')
        self.entry_project_name.grid(row=3, column=startcolumn)

        self.entry_vbox_name = tk.Entry(self)
        self.entry_vbox_name.insert(0, 'Virtualbox name')
        self.entry_vbox_name.grid(row=4, column=startcolumn)

        self.entry_default_username = tk.Entry(self)
        self.entry_default_username.insert(0, 'Default username')
        self.entry_default_username.grid(row=5, column=startcolumn)

        self.entry_default_password = tk.Entry(self)
        self.entry_default_password.insert(0, 'Dafult password')
        self.entry_default_password.grid(row=5, column=startcolumn+1)

        self.entry_extra_user = tk.Entry(self)
        self.entry_extra_user.insert(0, 'Extra username')
        self.entry_extra_user.grid(row=6, column=startcolumn)

        self.vagrant_box = tk.StringVar(self)
        self.vagrant_box.set('Select Vagrant Box')
        vagrant_drop = tk.OptionMenu(self, self.vagrant_box,
                                     *get_local_vagrant_boxes().split("\n"))
        vagrant_drop.grid(row=7, column=startcolumn, sticky="ew")

        exit_button = tk.Button(self, text='Back', command=self.destroy)
        exit_button.grid(row=8, column=startcolumn)

        save_button = tk.Button(
            self,
            text='Next',
            command=self.go_to_provision_page
        )
        save_button.grid(row=8, column=startcolumn+1)

    def set_grid(self):
        self.grid()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=2)

    def go_to_provision_page(self):
        self.master.provisions_configs["name"] = self.entry_project_name.get()
        self.master.provisions_configs["vm_name"] = self.entry_vbox_name.get()
        self.master.provisions_configs["username"] = self.entry_default_username.get()
        self.master.provisions_configs["password"] = self.entry_default_password.get()
        self.master.provisions_configs["user"] = self.entry_extra_user.get()
        self.master.provisions_configs["vm_name"] = self.vagrant_box.get()
        self.destroy()
        self.master.vagrant_provision = VagrantProvisionsView(self.master)

    def get_vagrant_configs(self):
        return self.provisions_configs
