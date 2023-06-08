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
        self.update_upgrade = ctk.CTkRadioButton(
            master=self,
            text="Update upgrade",
            variable=self.radio_var,
            value='update_upgrade',
            command=self._active_update_upgrade_edit_button,
            font=self.label_font
        )

        self.update_upgrade_full = ctk.CTkRadioButton(
            master=self,
            text="Update upgrade full",
            variable=self.radio_var,
            value='update_upgrade_full',
            command=self._active_update_upgrade_full_edit_button,
            font=self.label_font
        )
        self.radio_none = ctk.CTkRadioButton(
            self,
            text="None",
            variable=self.radio_var,
            value=None,
            font=self.label_font,
            command=self._disable_both_edit_buttons
        )
        self.edit_update_upgrade_button = ctk.CTkButton(
            master=self,
            text='Edit',
            font=self.label_font,
            width=self.width_button_std,
            state='disabled',
            command=lambda: self._edit_additional_script(self.radio_var)
        )
        self.edit_update_upgrade_full_button = ctk.CTkButton(
            master=self,
            text='Edit',
            font=self.label_font,
            width=self.width_button_std,
            state='disabled',
            command=lambda: self._edit_additional_script(self.radio_var)
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
        self._check_checkbox_clean_status()
        self._check_checkbox_reboot_status()
        self.render()

    def _active_update_upgrade_edit_button(self):
        self.provisions_configs["provisions"]['update_upgrade_full'] = False
        self.provisions_configs["provisions"]['update_upgrade'] = True
        self.edit_update_upgrade_button.configure(
            state='normal'
        )
        self.edit_update_upgrade_full_button.configure(
            state='disabled'
        )

    def _active_update_upgrade_full_edit_button(self):
        self.provisions_configs["provisions"]['update_upgrade'] = False
        self.provisions_configs["provisions"]['update_upgrade_full'] = True
        self.edit_update_upgrade_button.configure(
            state='disabled'
        )
        self.edit_update_upgrade_full_button.configure(
            state='normal'
        )

    def _disable_both_edit_buttons(self):
        self.edit_update_upgrade_button.configure(
            state='disabled'
        )
        self.edit_update_upgrade_full_button.configure(
            state='disabled'
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
            self.edit_clean_button.configure(
                state='normal'
            )
        else:
            self.provisions_configs["provisions"]["clean_packages"] = False
            self.edit_clean_button.configure(
                state='disabled'
            )

    def _check_checkbox_reboot_status(self):
        if self.reboot.get():
            self.provisions_configs["provisions"]["reboot"] = True
            self.edit_reboot_button.configure(
                state='normal'
            )
        else:
            self.provisions_configs["provisions"]["reboot"] = False
            self.edit_reboot_button.configure(
                state='disabled'
            )

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

        self.edit_update_upgrade_button.grid(
            row=2,
            column=0,
        )
        self.edit_update_upgrade_full_button.grid(
            row=2,
            column=1,
        )
        self.edit_clean_button.grid(
            row=2,
            column=3,
        )
        self.edit_reboot_button.grid(
            row=2,
            column=4,
        )
