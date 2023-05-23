import constants
import os
import shutil
import tkinter as tk
from builder.vagrant import Vagrant
from gui.errors import NotValidOperation
from cli.newpackage import make_package_folder
from tkinter import ttk
from tkinter import messagebox as mb
from builder.helper import is_empty_script


def new_vagrant_config_frame(master, provisions_configs):
    vagrant_configs_view = VagrantProvisionsView(
        master=master,
        provisions_configs=provisions_configs
    )
    vagrant_configs_view.grid(row=1, column=0, columnspan=5, sticky='wens')


class TextWindowView(tk.Toplevel):
    def __init__(self, master, package, operation, provisions_configs):
        self.master = master
        self.package = package
        self.operation = operation
        self.provisions_configs = provisions_configs
        tk.Toplevel.__init__(self, master)
        self.geometry(
            '400x400'
        )
        self.set_grid()
        file_label = tk.Label(
            self,
            text=f'You are modifying "{operation}.sh"\nfrom package "{package}"'
        )
        file_label.grid(row=1, column=1)
        self.open_text_box = tk.Text(self, width=40, height=8, state='normal')
        with open(f'{constants.PACKAGES_PATH}/{package}/{operation}.sh') as file:
            text = file.read()
        self.open_text_box.insert('end', text)
        self.open_text_box.grid(row=2, column=1)
        save_button = tk.Button(
            self,
            text='Save',
            command=self.save_file
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
        new_vagrant_config_frame(self.master, self.provisions_configs)
        self.destroy()

    def remove_from_operation(self):
        self.provisions_configs["provisions"][f'packages_to_{self.operation}'].remove(self.package)
        new_vagrant_config_frame(self.master, self.provisions_configs)
        self.destroy()


class VagrantProvisionsView(tk.Frame):

    def __init__(self, master, provisions_configs):
        self.startcolumn = 1
        self.provisions_configs = provisions_configs
        tk.Frame.__init__(self, master)
        self.set_grid(rows=9, columns=5)
        self.startcolumn = 1
        title_label = tk.Label(self, text="Vagrant", font='sans 16 bold')
        title_label.grid(row=0, column=0, columnspan=5)
        provisions_label = tk.Label(self, text="Provisions")
        provisions_label.grid(row=1, column=0, columnspan=5)
        self.add_separator((2, 0), length=5)
        packages_label = tk.Label(self, text="Packages")
        packages_label.grid(row=2, column=0, columnspan=5)

        self.add_listbox()
        self.add_install_uninstal_conf_buttons()
        self.add_delete_button()
        self.add_new_package_button()

        self.add_separator((8, 0), length=5)

        self.add_label((9, self.startcolumn), text='Install')
        self.add_label((9, self.startcolumn+1), text='Uninstall')
        self.add_label((9, self.startcolumn+2), text='Config')
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
        for operation in ('install', 'uninstall', 'config'):
            number_of_package.append(
                len(self.provisions_configs["provisions"][f'packages_to_{operation}'])
            )
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
            sticky='wens'
        )

    def add_selected_objects(self):
        for operation in ('install', 'uninstall', 'config'):
            if operation == 'install':
                column_position = self.startcolumn
            elif operation == 'uninstall':
                column_position = self.startcolumn + 1
            elif operation == 'config':
                column_position = self.startcolumn + 2
            if self.provisions_configs["provisions"][f'packages_to_{operation}']:
                for count, package in enumerate(self.provisions_configs["provisions"][f'packages_to_{operation}']):
                    row = 9 + count + 1
                    color = 'black'
                    package_is_empty = is_empty_script(f'{constants.PACKAGES_PATH}/{package}/{operation}.sh')
                    if package_is_empty:
                        color = 'red'
                    package_button = tk.Button(
                        self,
                        text=f'{package}',
                        fg=color,
                        command=lambda args=(package, operation): self.open_text_window(*args)
                    )
                    package_button.grid(row=row, column=column_position)

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
        for count, package in enumerate(sorted(packages)):
            self.packages_listbox.insert(count+1, package)
        self.packages_listbox.grid(row=3, column=self.startcolumn+1)

    def add_install_uninstal_conf_buttons(self):
        for count, operation in enumerate(('install', 'uninstall', 'config')):
            operation_button = tk.Button(
                self,
                text=operation.title(),
                command=lambda operation=operation: self.save_packages(operation)
            )
            operation_button.grid(row=4, column=self.startcolumn+count)

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

    def save_packages(self, operation: str):
        packages = list()
        for pack in self.packages_listbox.curselection():
            packages.append(
                self.packages_listbox.get(pack)
            )
        for package in packages:
            self.provisions_configs["provisions"][f"packages_to_{operation}"].add(package)
        new_vagrant_config_frame(self.master, self.provisions_configs)

    def delete_packages(self):
        packages_to_delete = ()
        for pack in self.packages_listbox.curselection():
            packages_to_delete += (self.packages_listbox.get(pack),)
        if packages_to_delete:
            warning_text = 'This operation is irreversible.\nYou choose to delete:\n'
            for package in packages_to_delete:
                warning_text += f'\t- {package}\n'
            warning_text += 'Confirm?'
            yes = mb.askyesno('Confirm Delete', warning_text)
            if yes:
                for package in packages_to_delete:
                    shutil.rmtree(f'{constants.PACKAGES_PATH}/{package}')
                new_vagrant_config_frame(
                    self.master, self.provisions_configs
                )
        else:
            mb.showerror('Error Delete', 'You have selected no packages')

    def add_bottom_button(self):
        build_button = tk.Button(
            self,
            text='Set Configs',
            command=self.set_configs,
            width=7
        )
        build_button.grid(row=self.number_of_rows-1, column=self.startcolumn)
        build_button = tk.Button(
            self,
            text='Build',
            command=self.build
        )
        build_button.grid(row=self.number_of_rows-1, column=3)

    def add_package(self):
        package_name = self.new_package_entry.get()
        if package_name not in os.listdir(constants.PACKAGES_PATH):
            confirm = mb.askyesnocancel("Add package",
                                        f'You want to add "{package_name}" '
                                        'as package?')
            if confirm:
                make_package_folder(package_name)
                self.add_listbox()
        else:
            mb.showerror('New Package Error', 'Package already exists')

    def open_text_window(self, package, operation):
        TextWindowView(self.master, package=package, operation=operation,
                       provisions_configs=self.provisions_configs)

    def set_configs(self):
        from gui.views.vagrantview.vagrantconfigsview import VagrantConfigsView
        vagrant_configs_view = VagrantConfigsView(
            master=self.master,
            provisions_configs=self.provisions_configs
        )
        vagrant_configs_view.grid(row=1, column=0, columnspan=5, sticky='wens')

    def build(self):
        vagrant_builder = Vagrant(self.provisions_configs)
        vagrant_builder.set_configs()
        vagrant_builder.set_provisions()
        vagrant_builder.set_credentials()
        vagrant_builder.create_project_folder()
        vagrant_builder.generate_main_file()
        info = mb.showinfo(
            title='Well done!',
            message=(
                f'Your new "{self.provisions_configs["configurations"]["machine_name"]}" machine '
                'was succesfully created'
            )
        )
        if info == 'ok':
            exit()
