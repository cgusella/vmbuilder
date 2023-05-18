import tkinter as tk
from argumentparser.helper import get_local_vagrant_boxes
from gui.views.vagrantview.vagrantprovisionsview import VagrantProvisionsView
from tkinter import ttk


class VagrantConfigsView(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        self.provisions_configs = dict()
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.geometry("400x400")
        self.label = tk.Label(self, text="Vagrant")
        self.label.pack(padx=0, pady=20, side='top')

        self.label = tk.Label(self, text="Configurations")
        self.label.pack(padx=0, pady=1, side='top', anchor='w')

        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill='x')

        self.entry_project_name = tk.Entry(self)
        self.entry_project_name.insert(0, 'Project name')
        self.entry_project_name.pack(padx=0, pady=1, side='top', anchor='w')

        self.entry_vbox_name = tk.Entry(self)
        self.entry_vbox_name.insert(0, 'Virtualbox name')
        self.entry_vbox_name.pack(padx=0, pady=1, side='top', anchor='w')

        self.entry_default_username = tk.Entry(self)
        self.entry_default_username.insert(0, 'Default username')
        self.entry_default_username.pack(padx=0, pady=1, side='top', anchor='w')

        self.entry_default_password = tk.Entry(self)
        self.entry_default_password.insert(0, 'Dafult password')
        self.entry_default_password.pack(padx=0, pady=1, side='top', anchor='w')

        self.entry_extra_user = tk.Entry(self)
        self.entry_extra_user.insert(0, 'Extra username')
        self.entry_extra_user.pack(padx=0, pady=1, side='top', anchor='w')

        vagrant_boxes = get_local_vagrant_boxes().strip()
        self.vagrant_box = tk.StringVar(self)
        self.vagrant_box.set('Select Vagrant Box')
        vagrant_drop = tk.OptionMenu(self, self.vagrant_box,
                                     *[vagrant_boxes])
        vagrant_drop.pack(padx=0, pady=1, side='top', anchor='w')

        exit_button = tk.Button(self, text='Back', command=self.destroy)
        exit_button.pack(padx=0, pady=1, side=tk.LEFT, anchor='w')

        save_button = tk.Button(
            self,
            text='Next',
            command=self.go_to_provision_page
        )
        save_button.pack(padx=0, pady=1, side=tk.RIGHT, anchor='w')

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
