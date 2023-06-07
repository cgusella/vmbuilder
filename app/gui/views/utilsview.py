import constants
import customtkinter as ctk
import shutil
from builder.helper import is_empty_script
from tkinter import filedialog


class SetUpScriptEdit(ctk.CTkToplevel):
    def __init__(self, master, variable, provisions_configs):
        self.master = master
        self.operation = variable.get()
        self.provisions_configs = provisions_configs
        ctk.CTkToplevel.__init__(self, master)
        self.geometry(
            '800x400'
        )
        self.set_grid()
        file_label = ctk.CTkLabel(
            self,
            text=f'You are modifying "{self.operation}.sh"',
            font=master.font_std
        )
        file_label.grid(row=1, column=1)
        self.open_text_box = ctk.CTkTextbox(
            self,
            width=600,
            font=master.font_std
        )
        with open(f'{constants.SETUP_SCRIPTS_PATH}/{self.operation}.sh') as file:
            text = file.read()
        self.open_text_box.insert('end', text)
        self.open_text_box.grid(row=2, column=1)
        save_button = ctk.CTkButton(
            self,
            text='Save',
            font=master.font_std,
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
        with open(
            f'{constants.SETUP_SCRIPTS_PATH}/{self.operation}.sh', 'w'
        ) as file:
            file.write(self.open_text_box.get("1.0", "end"))
        self.master.__init__(
            master=self.master.master,
            provisions_configs=self.provisions_configs
        )
        self.destroy()


class ScrollableCheckboxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, title, values, select_all=False):
        super().__init__(
            master,
            label_text=title,
            label_font=master.master.master.font_std,
        )
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []

        for count, value in enumerate(self.values):
            checkbox = ctk.CTkCheckBox(
                self,
                text=value,
                font=master.master.master.font_std,
            )
            checkbox.grid(
                row=count,
                column=0,
                padx=10,
                pady=(10, 0),
                sticky="wn"
            )
            self.checkboxes.append(checkbox)
        if select_all:
            for checkbox in self.checkboxes:
                checkbox.select()

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes


class ScrollableButtonFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(
            master,
            label_text=title,
            label_font=master.master.master.font_std,
            border_width=2,
            border_color=['grey64', 'grey34']
        )
        font = ctk.CTkFont(family='Sans', size=15, weight='bold')
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []
        self.operation = title.lower()

        for count, value in enumerate(self.values):
            # color = '#3996D5'
            # btn_color = ['#cfcfcf', '#333333']
            btn_color = 'transparent'
            txt_color = ['#333333', '#cfcfcf']
            package_is_empty = is_empty_script(f'{constants.PACKAGES_PATH}/{value}/{self.operation}.sh')
            if package_is_empty:
                txt_color = 'red'
            checkbox = ctk.CTkButton(
                self,
                height=20,
                text=value,
                font=font,
                command=lambda args=(value, self.operation): master.master._open_text_window(*args),
                fg_color=btn_color,
                text_color=txt_color,
                anchor='wn'
            )
            checkbox.grid(
                row=count,
                column=0,
                padx=10,
                pady=(0, 0),
                sticky="wn",
            )
            self.checkboxes.append(checkbox)


class EditFileWindow(ctk.CTkToplevel):
    def __init__(self, master, package, operation, provisions_configs):
        self.master = master
        self.package = package
        self.operation = operation
        self.provisions_configs = provisions_configs
        ctk.CTkToplevel.__init__(self, master)
        self.geometry(
            '1200x600'
        )
        self.title('Edit File')
        self.font_std = ctk.CTkFont(family='Sans', size=18)
        file_label = ctk.CTkLabel(
            self,
            text=f'You are modifying "{operation}.sh"\nfrom package "{package}"',
            font=self.font_std
        )
        file_label.grid(row=1, column=0, columnspan=3)
        self.open_text_box = ctk.CTkTextbox(
            self,
            width=1100,
            height=400,
            font=self.font_std
        )
        with open(f'{constants.PACKAGES_PATH}/{package}/{operation}.sh') as file:
            text = file.read()
        self.open_text_box.insert('end', text)
        self.open_text_box.grid(row=2, column=0, columnspan=3)

        if self.operation == 'config':
            upload_button = ctk.CTkButton(
                self,
                text='Upload',
                font=self.font_std,
                command=self.upload_file
            )
            upload_button.grid(row=3, column=0)
            save_button = ctk.CTkButton(
                self,
                text='Save',
                font=self.font_std,
                command=self.save_file
            )
            save_button.grid(row=3, column=2)
        else:
            save_button = ctk.CTkButton(
                self,
                text='Save',
                font=self.font_std,
                command=self.save_file
            )
            save_button.grid(row=3, column=1)
        remove_button = ctk.CTkButton(
            self,
            text=f'Remove from {operation}',
            font=self.font_std,
            command=self.remove_from_operation
        )
        remove_button.grid(row=4, column=1)

    def save_file(self):
        with open(f'{constants.PACKAGES_PATH}/{self.package}/{self.operation}.sh', 'w') as file:
            file.write(self.open_text_box.get("1.0", "end"))
        self.master._add_selected_packages_to(self.operation)
        self.destroy()

    def remove_from_operation(self):
        self.provisions_configs["provisions"][f'packages_to_{self.operation}'].remove(self.package)
        self.master.fill_selected_packages_frame()
        self.destroy()

    def upload_file(self):
        filename = filedialog.askopenfilename(
            initialdir=f"{constants.VMBUILDER_PATH}",
            title="Select a File",
            filetypes=(
                ("Text files",
                 "*.txt*"),
                ("all files",
                 "*.*")
            )
        )
        shutil.copy(
            src=filename,
            dst=f'{constants.PACKAGES_PATH}/{self.package}/upload/'
        )
        self.destroy()
