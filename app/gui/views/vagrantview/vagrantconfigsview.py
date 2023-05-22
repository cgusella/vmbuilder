import constants
import os
import tkinter as tk
from argumentparser.helper import get_local_vagrant_boxes
from gui.views.vagrantview.vagrantprovisionsview import VagrantProvisionsView
from tkinter import ttk
from tkinter import messagebox as mb


class VagrantConfigsView(tk.Toplevel):
    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        tk.Toplevel.__init__(self, master)
        self.geometry("600x600")
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
        machine_name_label = tk.Label(self, text="New machine name:")
        machine_name_label.grid(row=3, column=startcolumn)
        self.entry_project_name = tk.Entry(self)
        self.entry_project_name.insert(
            0,
            self.provisions_configs["configurations"]["machine_name"]
        )
        self.entry_project_name.grid(row=4, column=startcolumn)

        vbox_name_label = tk.Label(self, text="Virtual box name:")
        vbox_name_label.grid(row=5, column=1)
        self.entry_vbox_name = tk.Entry(self)
        self.entry_vbox_name.insert(
            0,
            self.provisions_configs["configurations"]['vbox_name']
        )
        self.entry_vbox_name.grid(row=6, column=startcolumn)

        username_label = tk.Label(self, text="Username:")
        username_label.grid(row=7, column=startcolumn)
        self.entry_default_username = tk.Entry(self)
        self.entry_default_username.insert(
            0,
            self.provisions_configs["credentials"]['username']
        )
        self.entry_default_username.grid(row=8, column=startcolumn)

        machine_name_label = tk.Label(self, text="Password:")
        machine_name_label.grid(row=7, column=startcolumn+1)
        self.entry_default_password = tk.Entry(self)
        self.entry_default_password.insert(
            0,
            self.provisions_configs["credentials"]['password']
        )
        self.entry_default_password.grid(row=8, column=startcolumn+1)

        machine_name_label = tk.Label(self, text="Extra user:")
        machine_name_label.grid(row=9, column=startcolumn)
        self.entry_extra_user = tk.Entry(self)
        self.entry_extra_user.insert(
            0,
            self.provisions_configs["credentials"]['extra_user']
        )
        self.entry_extra_user.grid(row=10, column=startcolumn)

        self.vagrant_box = tk.StringVar(self)
        self.vagrant_box.set('Select Vagrant Box')
        vagrant_drop = tk.OptionMenu(self, self.vagrant_box,
                                     *get_local_vagrant_boxes().split("\n"))
        vagrant_drop.grid(row=11, column=startcolumn, sticky="ew")

        exit_button = tk.Button(self, text='Back', command=self.destroy)
        exit_button.grid(row=12, column=startcolumn)

        save_button = tk.Button(
            self,
            text='Next',
            command=self.go_to_provision_page
        )
        save_button.grid(row=12, column=startcolumn+1)

    def set_grid(self):
        self.grid()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        # title row
        self.rowconfigure(0, weight=2)
        # config row
        self.rowconfigure(1, weight=2)
        # separator row
        self.rowconfigure(2, weight=1)
        # label name
        self.rowconfigure(3, weight=1)
        # entry name
        self.rowconfigure(4, weight=1)
        # vbox label
        self.rowconfigure(5, weight=1)
        # vbox entry
        self.rowconfigure(6, weight=1)
        # username label, password label
        self.rowconfigure(7, weight=1)
        # username entry, password entry
        self.rowconfigure(8, weight=2)
        # extra user label
        self.rowconfigure(9, weight=2)
        # extra user entry
        self.rowconfigure(10, weight=2)
        # select vagrant box
        self.rowconfigure(11, weight=2)
        # back, next buttons
        self.rowconfigure(12, weight=2)

    def go_to_provision_page(self):
        machine_name = self.entry_project_name.get()
        if machine_name in os.listdir(constants.VAGRANT_MACHINES_PATH):
            mb.showerror('Error', 'A machine with this name already exists')
        else:
            self.provisions_configs["configurations"]["machine_name"] = machine_name
            self.provisions_configs["configurations"]["vbox_name"] = self.entry_vbox_name.get()
            self.provisions_configs["credentials"]["username"] = self.entry_default_username.get()
            self.provisions_configs["credentials"]["password"] = self.entry_default_password.get()
            self.provisions_configs["credentials"]["extra_user"] = self.entry_extra_user.get()
            self.provisions_configs["configurations"]["image"] = self.vagrant_box.get()
            self.destroy()
            VagrantProvisionsView(self.master, self.provisions_configs)

    def get_vagrant_configs(self):
        return self.provisions_configs
