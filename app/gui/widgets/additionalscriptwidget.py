import customtkinter as ctk
from gui.views.utilsview import SetUpScriptEdit


class AdditionalScriptWidget(ctk.CTkFrame):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        ctk.CTkFrame.__init__(self, master)
        family_font = 'Sans'
        title_widget_font = ctk.CTkFont(
            family=family_font,
            size=20,
            weight='bold'
        )
        self.label_font = ctk.CTkFont(family=family_font, size=18)
        self.additional_scripts_label = ctk.CTkLabel(
            master=self,
            text='Additional Scripts',
            font=title_widget_font
        )
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.padx_std = (20, 20)
        self.pady_std = (10, 10)
        self.pady_title = (10, 2)
        self.width_button_std = 100
        self.sticky_title = 'wn'

        # add radiobuttons
        self.radio_var = ctk.StringVar(self, value=None)
        self.edit_upgrade_button = ctk.CTkButton(
            master=self,
            fg_color='transparent',
            text='',
            font=self.label_font,
            width=self.width_button_std,
            command=lambda: self._edit_additional_script(self.radio_var)
        )
        if self.provisions_configs["provisions"]['update_upgrade']:
            self.radio_var.set('update_upgrade')
            self._add_edit_button()
        if self.provisions_configs["provisions"]['update_upgrade_full']:
            self.radio_var.set('update_upgrade_full')
            self._add_edit_button()

        self.update_upgrade = ctk.CTkRadioButton(
            master=self,
            text="Update upgrade",
            variable=self.radio_var,
            value='update_upgrade',
            command=self._add_edit_button,
            font=self.label_font
        )

        self.update_upgrade_full = ctk.CTkRadioButton(
            master=self,
            text="Update upgrade full",
            variable=self.radio_var,
            value='update_upgrade_full',
            command=self._add_edit_button,
            font=self.label_font
        )
        self.radio_none = ctk.CTkRadioButton(
            self,
            text="None",
            variable=self.radio_var,
            value=None,
            font=self.label_font,
            command=self._remove_edit_button
        )

        # add checkbox for clean packages
        self.clean_var = ctk.StringVar()
        provisions = self.provisions_configs["provisions"]
        default_clean_var = 'clean_packages' if provisions["clean_packages"] else ''
        self.clean_var.set(default_clean_var)
        self.clean_button = ctk.CTkCheckBox(
            master=self,
            text="Clean packages",
            variable=self.clean_var,
            onvalue='clean_packages',
            offvalue='',
            height=1,
            width=15,
            font=self.label_font,
            command=self._check_checkbox_clean_status
        )
        self.edit_clean_button = ctk.CTkButton(
            master=self,
            text='Edit',
            font=self.label_font,
            width=self.width_button_std,
            command=lambda: self._edit_additional_script(self.clean_var)
        )
        if self.clean_var.get():
            self._add_edit_clean_button()

        # add checkbox for reboot
        self.reboot = ctk.StringVar()
        provisions = self.provisions_configs["provisions"]
        default_reboot_var = 'reboot' if provisions["reboot"] else ''
        self.reboot.set(default_reboot_var)
        self.reboot_checkbox = ctk.CTkCheckBox(
            master=self,
            text="Reboot",
            variable=self.reboot,
            onvalue='reboot',
            offvalue='',
            height=1,
            width=15,
            font=self.label_font,
            command=self._check_checkbox_reboot_status
        )
        self.edit_reboot_button = ctk.CTkButton(
            master=self,
            text='Edit',
            font=self.label_font,
            width=self.width_button_std,
            command=lambda: self._edit_additional_script(self.reboot)
        )
        if self.reboot.get():
            self._add_edit_reboot_button()
        self.render()

    def _add_edit_button(self):
        if self.radio_var.get() == 'update_upgrade':
            column = 0
            self.provisions_configs["provisions"]['update_upgrade_full'] = False
        elif self.radio_var.get() == 'update_upgrade_full':
            column = 1
            self.provisions_configs["provisions"]['update_upgrade'] = False
        self.provisions_configs["provisions"][f'{self.radio_var.get()}'] = True
        self.edit_upgrade_button.configure(
            fg_color=["#3a7ebf", "#1f538d"],
            text='Edit',
            state='normal'
        )
        self.edit_upgrade_button.grid(
            row=2,
            column=column,
        )

    def _remove_edit_button(self):
        self.edit_upgrade_button.configure(
            fg_color='transparent',
            text='',
            state='disabled'
        )

    def _add_edit_clean_button(self):
        self.edit_clean_button.grid(
            row=2,
            column=3,
        )

    def _add_edit_reboot_button(self):
        self.edit_reboot_button.grid(
            row=2,
            column=4,
        )

    def _edit_additional_script(self, variable):
        SetUpScriptEdit(
            self.master,
            variable=variable,
            provisions_configs=self.provisions_configs
        )

    def _check_checkbox_clean_status(self):
        if self.clean_var.get():
            self.provisions_configs["provisions"]["clean_packages"] = True
            self._add_edit_clean_button()
        else:
            self.provisions_configs["provisions"]["clean_packages"] = False
            self.edit_clean_button.destroy()

    def _check_checkbox_reboot_status(self):
        if self.reboot.get():
            self.provisions_configs["provisions"]["reboot"] = True
            self._add_edit_reboot_button()
        else:
            self.provisions_configs["provisions"]["reboot"] = False
            self.edit_reboot_button.destroy()

    def render(self):
        self.additional_scripts_label.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_title,
            sticky=self.sticky_title
        )
        self.update_upgrade.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
        )
        self.update_upgrade_full.grid(
            row=1,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
        )
        self.radio_none.grid(
            row=1,
            column=2,
            padx=self.padx_std,
            pady=self.pady_std,
        )

        self.clean_button.grid(
            row=1,
            column=3,
            padx=self.padx_std,
            pady=self.pady_std,
        )
        self.reboot_checkbox.grid(
            row=1,
            column=4,
            padx=self.padx_std,
            pady=self.pady_std,
        )
        empty_label = ctk.CTkLabel(
            self,
            text=''
        )
        empty_label.grid(
            row=2,
            column=1,
            columnspan=5
        )
