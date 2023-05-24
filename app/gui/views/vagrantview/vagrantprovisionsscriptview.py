import constants
import customtkinter as ctk
from tkinter import ttk
from tkinter import StringVar


class TextWindowView(ctk.CTkToplevel):
    def __init__(self, master, operation, provisions_configs):
        self.master = master
        self.operation = operation
        self.provisions_configs = provisions_configs
        ctk.CTkToplevel.__init__(self, master)
        self.geometry(
            '800x400'
        )
        self.set_grid()
        file_label = ctk.CTkLabel(
            self,
            text=f'You are modifying "{operation}.sh"'
        )
        file_label.grid(row=1, column=1)
        self.open_text_box = ctk.CTkTextbox(self, width=600)
        with open(f'{constants.SETUP_SCRIPTS_PATH}/{operation}.sh') as file:
            text = file.read()
        self.open_text_box.insert('end', text)
        self.open_text_box.grid(row=2, column=1)
        save_button = ctk.CTkButton(
            self,
            text='Save',
            command=self.save_file
        )
        save_button.grid(row=3, column=1)

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
        with open(f'{constants.SETUP_SCRIPTS_PATH}/{self.operation}.sh', 'w') as file:
            file.write(self.open_text_box.get("1.0", "end"))
        self.master.add_vagrant_provisions_frame()
        self.destroy()


class VagrantProvisionsScriptView(ctk.CTkFrame):

    def __init__(self, master, provisions_configs):
        self.startcolumn = 1
        self.provisions_configs = provisions_configs
        provisions = provisions_configs["provisions"]
        ctk.CTkFrame.__init__(self, master)
        self.set_grid(rows=7, columns=5)

        my_font = ctk.CTkFont(
            family='DejaVu Sans',
            size=16
        )

        title_label = ctk.CTkLabel(self, text="Vagrant", font=my_font)
        title_label.grid(row=0, column=0, columnspan=5)
        provisions_label = ctk.CTkLabel(self, text="Provisions", font=my_font)
        provisions_label.grid(row=1, column=0, columnspan=5)
        separator = ttk.Separator(
            master=self,
            orient='horizontal',
            style='blue.TSeparator',
            class_=ttk.Separator,
            takefocus=1,
            cursor='plus'
        )
        separator.grid(
            row=2,
            column=0,
            columnspan=5,
            sticky='we'
        )
        packages_label = ctk.CTkLabel(self, text="Additional scripts")
        packages_label.grid(row=2, column=0, columnspan=5)

        self.radio_var = StringVar(self, value=None)
        if self.provisions_configs["provisions"]['update_upgrade']:
            self.radio_var.set('update_upgrade')
            self.add_edit_upgrade_button()
        if self.provisions_configs["provisions"]['update_upgrade_full']:
            self.radio_var.set('update_upgrade_full')
            self.add_edit_upgrade_button()

        self.update_upgrade = ctk.CTkRadioButton(
            self,
            text="Update upgrade",
            variable=self.radio_var,
            value='update_upgrade',
            command=self.add_edit_upgrade_button
        )
        self.update_upgrade.grid(row=3, column=2)

        self.update_upgrade_full = ctk.CTkRadioButton(
            self,
            text="Update upgrade full",
            variable=self.radio_var,
            value='update_upgrade_full',
            command=self.add_edit_upgrade_button
        )
        self.update_upgrade_full.grid(row=4, column=2)

        deselect_button = ctk.CTkButton(self, text='Deselect', command=self.deselect)
        deselect_button.grid(row=5, column=2)

        self.clean_var = StringVar()
        default_clean_var = 'clean_packages' if provisions["clean_packages"] else ''
        self.clean_var.set(default_clean_var)
        clean_button = ctk.CTkCheckBox(
            self, text="Clean packages",
            variable=self.clean_var,
            onvalue='clean_packages',
            offvalue='',
            height=1,
            width=15,
            command=self.check_checkbox_status
        )
        clean_button.grid(row=6, column=2)
        if self.clean_var.get():
            self.add_edit_clean_button()

    def set_grid(self, rows: int, columns: int):
        self.grid()
        for i in range(columns):
            self.columnconfigure(i, weight=1)
        for i in range(rows):
            self.rowconfigure(i, weight=1)

    def add_edit_clean_button(self):
        self.edit_clean_button = ctk.CTkButton(self, text='Edit', command=self.edit_clean_script)
        self.edit_clean_button.grid(row=6, column=3)

    def edit_update_script(self):
        TextWindowView(self.master, operation=self.radio_var.get(),
                       provisions_configs=self.provisions_configs)

    def edit_clean_script(self):
        TextWindowView(self.master, operation=self.clean_var.get(),
                       provisions_configs=self.provisions_configs)

    def deselect(self):
        self.edit_upgrade_button.destroy()
        self.provisions_configs["provisions"]['update_upgrade'] = False
        self.provisions_configs["provisions"]['update_upgrade_full'] = False
        self.update_upgrade.deselect()
        self.update_upgrade_full.deselect()

    def check_checkbox_status(self):
        if self.clean_var.get():
            self.provisions_configs["provisions"]["clean_packages"] = True
            self.add_edit_clean_button()
        else:
            self.provisions_configs["provisions"]["clean_packages"] = False
            self.edit_clean_button.destroy()

    def add_edit_upgrade_button(self):
        if self.radio_var.get() == 'update_upgrade':
            self.provisions_configs["provisions"]['update_upgrade_full'] = False
        elif self.radio_var.get() == 'update_upgrade_full':
            self.provisions_configs["provisions"]['update_upgrade'] = False
        self.provisions_configs["provisions"][f'{self.radio_var.get()}'] = True
        self.edit_upgrade_button = ctk.CTkButton(self, text='Edit', command=self.edit_update_script)
        self.edit_upgrade_button.grid(row=3, column=3, rowspan=2)
