import constants
import os
import shutil
import tkinter as tk
from gui.errors import NotValidOperation
from cli.newpackage import make_package_folder
from tkinter import ttk
from tkinter import messagebox as mb
from builder.helper import is_empty_script


class TextWindowView(tk.Toplevel):
    def __init__(self, master, package, operation, provisions_configs):
        self.package = package
        self.operation = operation
        self.provisions_configs = provisions_configs
        tk.Toplevel.__init__(self, master)
        self.geometry(
            '400x400'
        )
        self.set_grid()
        file_label = tk.Label(self, text=f'You are modifying: {operation}.sh')
        file_label.grid(row=0, column=1)
        file_label = tk.Label(self, text=f'from package: {package}')
        file_label.grid(row=1, column=1)
        self.open_text_box = tk.Text(self, width=40, height=8, state='normal')
        with open(f'{constants.PACKAGES_PATH}/{package}/{operation}.sh') as file:
            text = file.read()
        self.open_text_box.insert('end', text)
        self.open_text_box.grid(row=2, column=1)
        save_button = tk.Button(
            self,
            text='Save',
            command=lambda: self.save_file()
        )
        save_button.grid(row=3, column=1)
        remove_button = tk.Button(
            self,
            text=f'Remove from {operation}',
            command=self.remove_from_operation
        )
        remove_button.grid(row=4, column=1)

    def set_grid(self):
        self.grid()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

    def save_file(self):
        with open(f'{constants.PACKAGES_PATH}/{self.package}/{self.operation}.sh', 'w') as file:
            file.write(self.open_text_box.get("1.0", "end"))
        self.destroy()
        VagrantProvisionsView(self.master)

    def remove_from_operation(self):
        self.provisions_configs[f'packages_to_{self.operation}'].remove(self.package)
        self.destroy()
        VagrantProvisionsView(self.master, self.provisions_configs)


class VagrantProvisionsView(tk.Toplevel):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        tk.Toplevel.__init__(self, master)
        self.wm_geometry(
            f'{self.winfo_screenmmwidth()}x{self.winfo_screenheight()}'
        )
        self.set_grid(rows=8, columns=5)
        self.startcolumn = 1
        self.label = tk.Label(self, text="Vagrant", font='sans 16 bold')
        self.label.grid(row=0, column=0, columnspan=5)
        self.label = tk.Label(self, text="Provisions")
        self.label.grid(row=1, column=0, columnspan=5)

        self.add_separator((2, 0), length=5)
        self.add_label((2, self.startcolumn+1), text='Packages')

        self.add_listbox()
        self.add_install_uninstal_conf_buttons()
        self.add_delete_button()
        self.add_new_package_button()

        self.add_separator((8, 0), length=5)

        self.add_label((8, self.startcolumn), text='Install')
        self.add_label((8, self.startcolumn+1), text='Uninstall')
        self.add_label((8, self.startcolumn+2), text='Config')
        self.add_selected_objects()

        self.add_separator((self.number_of_rows-2, 0), length=5)
        self.add_bottom_button()

    def set_grid(self, rows: int, columns: int):
        self.grid()
        for i in range(columns):
            self.columnconfigure(i, weight=1)

        for i in range(rows):
            self.rowconfigure(i, weight=1)
        number_of_package = [1]
        for operation in ('packages_to_install', 'packages_to_uninstall', 'packages_to_config'):
            number_of_package.append(len(self.master.provisions_configs[operation]))
        for i in range(1, max(number_of_package)+4):
            self.rowconfigure(i+8, weight=1)  
        self.number_of_rows = 8 + max(number_of_package) + 4

    def add_label(self, position: tuple, text: str,):
        label = tk.Label(self, text=text)
        label.grid(row=position[0], column=position[1])

    def add_separator(self, initial_position: tuple, length: int):
        separator = ttk.Separator(
            master=self,
            orient='horizontal',
            style='blue.TSeparator',
            class_=ttk.Separator,
            takefocus=1,
            cursor='plus'
        )
        separator.grid(
            row=initial_position[0],
            column=initial_position[1],
            columnspan=length,
            sticky='EW'
        )

    def _add_packages_for_operation(self, operation: str):
        if operation not in ('install', 'uninstall', 'config'):
            raise NotValidOperation()
        if operation == 'install':
            column_position = self.startcolumn
        elif operation == 'uninstall':
            column_position = self.startcolumn + 1
        elif operation == 'config':
            column_position = self.startcolumn + 2
        try:
            if self.master.provisions_configs[f'packages_to_{operation}']:
                i = 1
                for package in self.master.provisions_configs[f'packages_to_{operation}']:
                    row = 8 + i
                    color = 'black'
                    package_is_empty = is_empty_script(f'{constants.PACKAGES_PATH}/{package}/{operation}.sh')
                    if package_is_empty:
                        color = 'red'
                    package_button = tk.Button(self, text=f'{package}', fg=color,
                                               command=lambda: self.open_text_window(package, operation))
                    package_button.grid(row=row, column=column_position)
                    i += 1
        except KeyError:
            pass

    def add_selected_objects(self):
        self._add_packages_for_operation('install')
        self._add_packages_for_operation('uninstall')
        self._add_packages_for_operation('config')

    def add_listbox(self):
        self.packages_listbox = tk.Listbox(
            self,
            selectmode='multiple',
            width=20,
            height=5,
        )
        packages = [
            package for package in os.listdir(constants.PACKAGES_PATH)
            if package not in ('program-example', 'setup_scripts')
        ]
        for count, package in enumerate(packages):
            self.packages_listbox.insert(count+1, package)
        self.packages_listbox.grid(row=3, column=self.startcolumn+1)

    def save_script(self, package: str, operation: str, file_text: str):
        with open(f'{constants.PACKAGES_PATH}/{package}/{operation}.sh', 'w') as file:
            file.write(file_text)
        self.destroy()
        VagrantProvisionsView(self.master)

    def add_install_uninstal_conf_buttons(self):
        install_button = tk.Button(
            self,
            text='Install',
            command=self.save_install_packages
        )
        install_button.grid(row=4, column=self.startcolumn)
        uninstall_button = tk.Button(
            self,
            text='Uninstall',
            command=self.save_uninstall_packages
        )
        uninstall_button.grid(row=4, column=self.startcolumn+1)
        config_button = tk.Button(
            self,
            text='Config',
            command=self.save_config_packages
        )
        config_button.grid(row=4, column=self.startcolumn+2)

    def add_delete_button(self):
        delete_button = tk.Button(
            self,
            text='Delete Packages',
            command=self.delete_packages
        )
        delete_button.grid(row=5, column=self.startcolumn+1)

    def add_new_package_button(self):
        self.new_package_entry = tk.Entry(self)
        self.new_package_entry.insert(0, 'New Package Name')
        self.new_package_entry.grid(row=6, column=self.startcolumn+1)
        new_package_button = tk.Button(
            self,
            text='Add package',
            command=self.add_package
        )
        new_package_button.grid(row=7, column=self.startcolumn+1)

    def save_install_packages(self):
        packages_to_install = list()
        for pack in self.packages_listbox.curselection():
            packages_to_install.append(
                self.packages_listbox.get(pack)
            )
        self.master.provisions_configs["packages_to_install"] = packages_to_install
        self.destroy()
        VagrantProvisionsView(self.master, self.provisions_configs)

    def save_uninstall_packages(self):
        packages_to_uninstall = list()
        for pack in self.packages_listbox.curselection():
            packages_to_uninstall.append(
                self.packages_listbox.get(pack)
            )
        self.master.provisions_configs["packages_to_uninstall"] = packages_to_uninstall
        self.destroy()
        VagrantProvisionsView(self.master, self.provisions_configs)

    def save_config_packages(self):
        packages_to_config = list()
        for pack in self.packages_listbox.curselection():
            packages_to_config.append(
                self.packages_listbox.get(pack)
            )
        self.master.provisions_configs["packages_to_config"] = packages_to_config
        self.destroy()
        VagrantProvisionsView(self.master, self.provisions_configs)

    def delete_packages(self):
        packages_to_delete = ()
        for pack in self.packages_listbox.curselection():
            packages_to_delete += (self.packages_listbox.get(pack),)
        if packages_to_delete:
            warning_text = 'You choose to delete:\n'
            for package in packages_to_delete:
                warning_text += f'\t- {package}\n'
            warning_text += 'Confirm?'
            yes = mb.askyesno('Confirm Delete', warning_text)
            if yes:
                for package in packages_to_delete:
                    shutil.rmtree(f'{constants.PACKAGES_PATH}/{package}')
            self.destroy()
            VagrantProvisionsView(self.master)
        else:
            mb.showerror('Error Delete', 'You have selected no packages')

    def add_bottom_button(self):
        build_button = tk.Button(
            self,
            text='Back',
            command=self.go_to_configs
        )
        build_button.grid(row=self.number_of_rows-1, column=self.startcolumn)
        build_button = tk.Button(
            self,
            text='Build',
            command=self.destroy
        )
        build_button.grid(row=self.number_of_rows-1, column=3)

    def add_package(self):
        package_name = self.new_package_entry.get()
        if package_name not in os.listdir(constants.PACKAGES_PATH):
            make_package_folder(package_name)
            self.destroy()
            VagrantProvisionsView(self.master, self.provisions_configs)
        else:
            mb.showerror('New Package Error', 'Package already exists')

    def open_text_window(self, package, operation):
        self.destroy()
        TextWindowView(self.master, package=package, operation=operation,
                       provisions_configs=self.provisions_configs)

    def go_to_configs(self):
        self.destroy()
        from gui.views.vagrantview.vagrantconfigsview import VagrantConfigsView
        VagrantConfigsView(self.master)