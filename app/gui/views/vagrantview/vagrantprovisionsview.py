import constants
import os
import tkinter as tk
from gui.errors import NotValidOperation
from cli.newpackage import make_package_folder
from tkinter import ttk
from builder.helper import is_empty_script


class VagrantProvisionsView(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        self.error_msg_label = None
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.geometry("400x800")
        self.label = tk.Label(self, text="Vagrant")
        self.label.pack(padx=0, pady=20, side='top')
        self.label = tk.Label(self, text="Provisions")
        self.label.pack(padx=0, pady=1, side='top', anchor='w')
        self.add_listbox()
        self.add_new_package_button()
        self.add_selected_objects()
        self.add_install_uninstal_conf_buttons()
        self.add_bottom_button()

    def _add_packages_for_operation(self, operation: str):
        if operation not in ('install', 'uninstall', 'config'):
            raise NotValidOperation()
        try:
            if self.master.provisions_configs[f'packages_to_{operation}']:
                msg_label = tk.Label(self, text=f'{operation.title()}: ')
                msg_label.pack(padx=0, pady=1, side='top', anchor='w')
                for package in self.master.provisions_configs[f'packages_to_{operation}']:
                    color = 'black'
                    if is_empty_script(f'{constants.PACKAGES_PATH}/{package}/{operation}.sh'):
                        color = 'red'
                    label = tk.Label(self, text=package, fg=color)
                    label.pack(padx=0, pady=1, side=tk.TOP, anchor='n')

                    open_text_box = tk.Text(self, width=40, height=3, state='normal')
                    # open_text_box.config(state=editable)
                    with open(f'{constants.PACKAGES_PATH}/{package}/{operation}.sh') as file:
                        text = file.read()
                    open_text_box.insert('end', text)
                    open_text_box.pack(padx=0, pady=1, side=tk.TOP, anchor='n')
        except KeyError:
            pass

    def add_selected_objects(self):
        self._add_packages_for_operation('install')
        self._add_packages_for_operation('uninstall')
        self._add_packages_for_operation('config')

    def add_listbox(self):
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill='x')

        label = tk.Label(self, text='Packages')
        label.pack(padx=0, pady=1, side='top', anchor='w')

        self.packages_listbox = tk.Listbox(
            self,
            selectmode='multiple',
            width=20,
            height=5,
        )
        for count, package in enumerate(os.listdir(constants.PACKAGES_PATH)):
            self.packages_listbox.insert(count+1, package)
        self.packages_listbox.pack(padx=0, pady=1, side='top', anchor='w')

    def open_file(self, package, operation):
        self.destroy()
        VagrantProvisionsView(self.master)

    def add_install_uninstal_conf_buttons(self):
        install_button = tk.Button(
            self,
            text='Install',
            command=self.save_install_packages
        )
        install_button.pack(
            side=tk.LEFT,
            anchor='s',
        )
        uninstall_button = tk.Button(
            self,
            text='Uninstall',
            command=self.save_uninstall_packages
        )
        uninstall_button.pack(
            side=tk.LEFT,
            anchor='s',
        )
        config_button = tk.Button(
            self,
            text='Config',
            command=self.save_config_packages
        )
        config_button.pack(
            side=tk.LEFT,
            anchor='s',
        )

    def add_new_package_button(self):
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill='x')
        self.new_package_entry = tk.Entry(self)
        self.new_package_entry.insert(0, 'Project name')
        self.new_package_entry.pack(padx=0, pady=1, side='top', anchor='w')

        new_package_button = tk.Button(
            self,
            text='Add package',
            command=self.refresh_page_for_packages
        )
        new_package_button.pack(padx=0, pady=1, side='top', anchor='w')

    def save_install_packages(self):
        packages_to_install = list()
        for pack in self.packages_listbox.curselection():
            packages_to_install.append(
                self.packages_listbox.get(pack)
            )
        self.master.provisions_configs["packages_to_install"] = packages_to_install
        self.destroy()
        VagrantProvisionsView(self.master)

    def save_uninstall_packages(self):
        packages_to_uninstall = list()
        for pack in self.packages_listbox.curselection():
            packages_to_uninstall.append(
                self.packages_listbox.get(pack)
            )
        self.master.provisions_configs["packages_to_uninstall"] = packages_to_uninstall
        self.destroy()
        VagrantProvisionsView(self.master)

    def save_config_packages(self):
        packages_to_config = list()
        for pack in self.packages_listbox.curselection():
            packages_to_config.append(
                self.packages_listbox.get(pack)
            )
        self.master.provisions_configs["packages_to_config"] = packages_to_config
        self.destroy()
        VagrantProvisionsView(self.master)

    def add_bottom_button(self):
        build_button = tk.Button(
            self,
            text='Build',
            command=self.destroy
        )
        build_button.pack(
            side='bottom',
            anchor='s',
        )

    def refresh_page_for_packages(self):
        if not self.error_msg_label:
            package_name = self.new_package_entry.get()
            if package_name not in os.listdir(constants.PACKAGES_PATH):
                make_package_folder(package_name)
                self.destroy()
                VagrantProvisionsView(self.master)
            else:
                self.error_msg_label = tk.Label(
                    self,
                    text='Package already exists'
                )
                self.error_msg_label.pack(padx=0, pady=0, side='top',
                                          anchor='w')
        else:
            self.error_msg_label.destroy()
            self.error_msg_label = None
            self.refresh_page_for_packages()
