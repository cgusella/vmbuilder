import abc
import customtkinter as ctk
from gui.guistandard import GuiStandard
from existencecontroller.controller import launch_vboxmanage_lst_command


class MainButtonsWidget(GuiStandard):
    """This class define the buttons to add at each view.
    Buttons are the following:
        * build (mandatory)
        * save (mandatory)
        * configs (optional)
        * provisions (optional)
        * networks (optional)

    'configs', 'provisions' and 'networks' must be specified in 'wanted_buttons'
    if you want to add a 'set ####' button to the main button widget,
    while build and save are added by default without specifications.
    """

    def __init__(self, master, provisions_configs, wanted_buttons: list):
        self.provisions_configs = provisions_configs
        self.wanted_buttons = wanted_buttons
        self.master = master
        self.vbox_list = launch_vboxmanage_lst_command()
        ctk.CTkFrame.__init__(self, master, fg_color='transparent')
        self.set_fonts()
        self.set_std_dimensions()
        self.initialize_elements()
        self.render_elements()

    def set_fonts(self):
        self.font_std = ctk.CTkFont(family='Sans', size=18)

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)
        self.width_button_std = 40
        self.ipadx_button = 5
        self.ipady_button = 5
        self.sticky_frame = 'wens'

    def initialize_elements(self):
        self.build_button = ctk.CTkButton(
            master=self,
            text='Build',
            font=self.font_std,
            width=self.width_button_std,
            command=self._build
        )

        self.save_button = ctk.CTkButton(
            master=self,
            text='Save',
            font=self.font_std,
            width=self.width_button_std,
            command=self._save
        )

        if 'configs' in self.wanted_buttons:
            self.set_configs_button = ctk.CTkButton(
                master=self,
                text='Set Configs',
                font=self.font_std,
                width=self.width_button_std,
                command=self._save_state_and_go_to_configs
            )

        if 'provisions' in self.wanted_buttons:
            self.set_provision_button = ctk.CTkButton(
                master=self,
                text='Set Provisions',
                command=self._save_state_and_go_to_provisions,
                font=self.font_std
            )
        if 'networks' in self.wanted_buttons:
            self.set_network_button = ctk.CTkButton(
                master=self,
                text='Set Network',
                font=self.font_std,
                width=self.width_button_std,
                command=self._save_state_and_go_to_networks
            )

    def render_elements(self):
        # The order here is important. Reading down means add buttons
        # to the left, so choose the packing accordingly
        self.build_button.pack(
            side='right',
            anchor='ne',
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        self.save_button.pack(
            side='right',
            anchor='ne',
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        if 'configs' in self.wanted_buttons:
            self.set_configs_button.pack(
                side='right',
                anchor='ne',
                padx=self.padx_std,
                pady=self.pady_std,
                ipadx=self.ipadx_button,
                ipady=self.ipady_button
            )
        if 'provisions' in self.wanted_buttons:
            self.set_provision_button.pack(
                side='right',
                anchor='ne',
                padx=self.padx_std,
                pady=self.pady_std,
                ipadx=self.ipadx_button,
                ipady=self.ipady_button
            )
        if 'networks' in self.wanted_buttons:
            self.set_network_button.pack(
                side='right',
                anchor='ne',
                padx=self.padx_std,
                pady=self.pady_std,
                ipadx=self.ipadx_button,
                ipady=self.ipady_button
            )

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
