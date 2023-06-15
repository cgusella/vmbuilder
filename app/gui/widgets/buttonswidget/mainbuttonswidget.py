import abc
import customtkinter as ctk
from existencecontroller.controller import launch_vboxmanage_lst_command


class MainButtonsWidget(abc.ABC, ctk.CTkFrame):

    def __init__(self, master, provisions_configs, wanted_buttons: list):
        self.provisions_configs = provisions_configs
        self.master = master
        self.vbox_list = launch_vboxmanage_lst_command()
        ctk.CTkFrame.__init__(self, master, fg_color='transparent')
        self.font_std = ctk.CTkFont(family='Sans', size=18)
        self.set_std_dimensions()
        # The order here is important.
        # Do not change the order between build, save, and set configs
        build_button = ctk.CTkButton(
            master=self,
            text='Build',
            font=self.font_std,
            width=self.width_button_std,
            command=self._build
        )
        build_button.pack(
            side='right',
            anchor='ne',
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        save_button = ctk.CTkButton(
            master=self,
            text='Save',
            font=self.font_std,
            width=self.width_button_std,
            command=self._save
        )
        save_button.pack(
            side='right',
            anchor='ne',
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        if 'configs' in wanted_buttons:
            set_configs_button = ctk.CTkButton(
                master=self,
                text='Set Configs',
                font=self.font_std,
                width=self.width_button_std,
                command=self._save_state_and_go_to_configs
            )
            set_configs_button.pack(
                side='right',
                anchor='ne',
                padx=self.padx_std,
                pady=self.pady_std,
                ipadx=self.ipadx_button,
                ipady=self.ipady_button
            )
        if 'provisions' in wanted_buttons:
            set_provision_button = ctk.CTkButton(
                master=self,
                text='Set Provisions',
                command=self._save_state_and_go_to_provisions,
                font=self.font_std
            )
            set_provision_button.pack(
                side='right',
                anchor='ne',
                padx=self.padx_std,
                pady=self.pady_std,
                ipadx=self.ipadx_button,
                ipady=self.ipady_button
            )
        if 'networks' in wanted_buttons:
            set_network_button = ctk.CTkButton(
                master=self,
                text='Set Network',
                font=self.font_std,
                width=self.width_button_std,
                command=self._save_state_and_go_to_networks
            )
            set_network_button.pack(
                side='right',
                anchor='ne',
                padx=self.padx_std,
                pady=self.pady_std,
                ipadx=self.ipadx_button,
                ipady=self.ipady_button
            )

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)
        self.width_button_std = 40
        self.ipadx_button = 5
        self.ipady_button = 5
        self.sticky_frame = 'wens'

    @abc.abstractmethod
    def _save(self):
        pass

    @abc.abstractmethod
    def _build(self):
        pass

    @abc.abstractmethod
    def _save_state_and_go_to_configs(self):
        pass

    @abc.abstractmethod
    def _save_state_and_go_to_provisions(self):
        pass
