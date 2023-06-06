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
        additional_scripts_label = ctk.CTkLabel(
            master=self,
            text='Additional Scripts',
            font=title_widget_font
        )

        padx_std = (20, 20)
        pady_std = (10, 10)
        pady_title = (10, 2)
        self.width_button_std = 100
        sticky_title = 'wn'

        additional_scripts_label.grid(
            row=0,
            column=0,
            padx=padx_std,
            pady=pady_title,
            sticky=sticky_title
        )

        # add radiobuttons
        self.radio_var = ctk.StringVar(self, value=None)
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
        self.update_upgrade.grid(
            row=1,
            column=0,
            padx=padx_std,
            pady=pady_std,
            sticky=sticky_title
        )

        self.update_upgrade_full = ctk.CTkRadioButton(
            master=self,
            text="Update upgrade full",
            variable=self.radio_var,
            value='update_upgrade_full',
            command=self._add_edit_button,
            font=self.label_font
        )
        self.update_upgrade_full.grid(
            row=2,
            column=0,
            padx=padx_std,
            pady=pady_std,
            sticky=sticky_title
        )
        self.update_upgrade_full = ctk.CTkRadioButton(
            self,
            text="None",
            variable=self.radio_var,
            value=None,
            font=self.label_font,
            command=self._remove_edit_button
        )
        self.update_upgrade_full.grid(
            row=3,
            column=0,
            padx=padx_std,
            pady=pady_std,
            sticky=sticky_title
        )

        # add checkbox for clean packages
        self.clean_var = ctk.StringVar()
        provisions = self.provisions_configs["provisions"]
        default_clean_var = 'clean_packages' if provisions["clean_packages"] else ''
        self.clean_var.set(default_clean_var)
        clean_button = ctk.CTkCheckBox(
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
        clean_button.grid(
            row=4,
            column=0,
            padx=padx_std,
            pady=pady_std,
            sticky=sticky_title
        )
        if self.clean_var.get():
            self._add_edit_clean_button()

        # add checkbox for reboot
        self.reboot = ctk.StringVar()
        provisions = self.provisions_configs["provisions"]
        default_reboot_var = 'reboot' if provisions["reboot"] else ''
        self.reboot.set(default_reboot_var)
        reboot_checkbox = ctk.CTkCheckBox(
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
        reboot_checkbox.grid(
            row=5,
            column=0,
            padx=padx_std,
            pady=pady_std,
            sticky=sticky_title
        )
        if self.reboot.get():
            self._add_edit_reboot_button()

    def _add_edit_button(self):
        if self.radio_var.get() == 'update_upgrade':
            self._remove_edit_button()
            row = 1
            self.provisions_configs["provisions"]['update_upgrade_full'] = False
        elif self.radio_var.get() == 'update_upgrade_full':
            self._remove_edit_button()
            row = 2
            self.provisions_configs["provisions"]['update_upgrade'] = False
        self.provisions_configs["provisions"][f'{self.radio_var.get()}'] = True
        self.edit_upgrade_button = ctk.CTkButton(
            master=self,
            text='Edit',
            font=self.label_font,
            width=self.width_button_std,
            command=lambda: self._edit_additional_script(self.radio_var)
        )
        self.edit_upgrade_button.grid(row=row, column=1)

    def _remove_edit_button(self):
        try:
            self.edit_upgrade_button.destroy()
        except (AttributeError, ValueError):
            pass

    def _add_edit_clean_button(self):
        self.edit_clean_button = ctk.CTkButton(
            master=self,
            text='Edit',
            font=self.label_font,
            width=self.width_button_std,
            command=lambda: self._edit_additional_script(self.clean_var)
        )
        self.edit_clean_button.grid(row=4, column=1)

    def _add_edit_reboot_button(self):
        self.edit_reboot_button = ctk.CTkButton(
            master=self,
            text='Edit',
            font=self.label_font,
            width=self.width_button_std,
            command=lambda: self._edit_additional_script(self.reboot)
        )
        self.edit_reboot_button.grid(row=5, column=1)

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
