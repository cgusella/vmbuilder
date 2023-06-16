import constants
import customtkinter as ctk
from builder.helper import is_empty_script
from gui.widgets.buttonswidget.editscriptbuttons import EditScriptButtonsWidget


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
    def __init__(self, master, title, values):
        self.font_std = ctk.CTkFont(family='Sans', size=16)
        super().__init__(
            master,
            label_text=title,
            label_font=self.font_std,
        )
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []

        for count, value in enumerate(self.values):
            checkbox = ctk.CTkCheckBox(
                self,
                text=value,
                font=self.font_std,
                # command=lambda: master._active_deactive_operation_buttons(self.get())
            )
            checkbox.grid(
                row=count,
                column=0,
                padx=10,
                pady=(10, 0),
                sticky="wn"
            )
            self.checkboxes.append(checkbox)

    def select_all(self):
        for checkbox in self.checkboxes:
            checkbox.select()

    def deselect_all(self):
        for checkbox in self.checkboxes:
            checkbox.deselect()

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes


class ScrollableButtonFrame(ctk.CTkScrollableFrame):

    def __init__(self, master, title, values, provisions_configs):
        self.provisions_configs = provisions_configs
        self.font = ctk.CTkFont(family='Sans', size=15, weight='bold')
        self.label_font = ctk.CTkFont(family='Sans', size=15)
        super().__init__(
            master,
            label_text=title,
            label_font=self.label_font,
            border_width=2,
            border_color=['grey64', 'grey34']
        )
        self.grid_columnconfigure(0, weight=1)
        self.operation = title.lower()
        self.set_values(values)
        self.add_button_values()

    def set_values(self, values):
        self.values = values

    def add_button_values(self):
        self.checkboxes = []
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
                font=self.font,
                command=lambda args=(value,): self._open_text_window(*args),
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

    def _open_text_window(self, package):
        EditFileWindow(self, package=package, operation=self.operation,
                       provisions_configs=self.provisions_configs)

    def clean(self):
        for checkbox in self.checkboxes:
            checkbox.destroy()


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
        self.set_std_dimensions()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.title('Edit File')
        self.font_std = ctk.CTkFont(family='Sans', size=18)
        file_label = ctk.CTkLabel(
            self,
            text=f'You are modifying "{operation}.sh"\nfrom package "{package}"',
            font=self.font_std
        )
        file_label.grid(row=0, column=0, columnspan=3)
        self.open_text_box = ctk.CTkTextbox(
            self,
            width=1100,
            height=400,
            font=self.font_std
        )
        with open(f'{constants.PACKAGES_PATH}/{package}/{operation}.sh') as file:
            text = file.read()
        self.open_text_box.insert('end', text)
        self.open_text_box.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
        )
        self.bottom_buttons = EditScriptButtonsWidget(
            self,
            package=self.package,
            operation=self.operation,
            provisions_configs=self.provisions_configs
        )
        self.bottom_buttons.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
        )

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)
