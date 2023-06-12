import customtkinter as ctk
from gui.widgets.nicwidget.bridgedwidget import BridgedWidget
from gui.widgets.nicwidget.hostonlywidget import HostOnlyWidget
from gui.widgets.nicwidget.dhcphostonlywidget import DHCPHostOnlyWidget


class NicWidget(ctk.CTkFrame):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        ctk.CTkFrame.__init__(self, master)
        self.font_std = ctk.CTkFont(family='Sans', size=18)
        self.set_std_dimensions()
        self.set_grid()
        self.add_enable_adapter_type_frame()
        self.add_config_adapter_frame()
        self.render()

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)
        self.pady_title = (10, 2)
        self.pady_entry = (2, 10)
        self.ipadx_std = 10
        self.ipady_std = 10
        self.ipadx_button = 5
        self.ipady_button = 5
        self.sticky_title = 'wn'
        self.sticky_label = 'ws'
        self.sticky_entry = 'wn'
        self.sticky_up = 'wen'
        self.sticky_frame = 'wens'
        self.sticky_optionmenu = 'w'
        self.sticky_warningmsg = 'e'
        self.sticky_horizontal = 'ew'

    def set_grid(self):
        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

    def add_enable_adapter_type_frame(self):
        self.enable_adapter_type_frame = ctk.CTkFrame(self)
        self.enable_adapter_type_frame.columnconfigure(0, weight=1)
        self.enable_adapter_type_frame.rowconfigure(0, weight=1)
        self.enable_adapter_type_frame.rowconfigure(1, weight=1)
        self.enable_checkbox = ctk.CTkCheckBox(
            master=self.enable_adapter_type_frame,
            font=self.font_std,
            text='Enable',
            command=self._check_nic_type_optionmenu
        )
        self.enable_checkbox.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_optionmenu
        )
        self.nic_type = ctk.CTkOptionMenu(
            master=self.enable_adapter_type_frame,
            font=self.font_std,
            state='disabled',
            values=['host-only', 'bridged', 'internal', 'nat-network', 'nat'],
            command=self._add_config_adapter_frame
        )
        self.nic_type.set('Select one')
        self.nic_type.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_optionmenu
        )
        self._check_nic_type_optionmenu()

    def _check_nic_type_optionmenu(self):
        if self.enable_checkbox.get():
            self.nic_type.configure(
                state='normal'
            )
            try:
                self.config_adapter_frame.available_bridged_nics.configure(
                    state='normal'
                )
            except AttributeError:
                pass
            try:
                self.hostonly_frame.available_hostonly_networks.configure(
                    state='normal'
                )
                self.hostonly_frame.add_hostonly_network_button.configure(
                    state='normal'
                )
                if self.hostonly_frame.available_hostonly_networks.get() != "Select":
                    self.dhcp_frame.enable_update_dhcp_button.configure(
                        state='normal'
                    )
                    self.dhcp_frame.delete_dhcp_button.configure(
                        state='normal'
                    )
                self.hostonly_frame._active_disactive_delete_update()
            except AttributeError:
                pass
        else:
            self.nic_type.configure(
                state='disabled'
            )
            try:
                self.config_adapter_frame.available_bridged_nics.configure(
                    state='disabled'
                )
            except AttributeError:
                pass
            try:
                self.hostonly_frame.available_hostonly_networks.configure(
                    state='disabled'
                )
                self.hostonly_frame.add_hostonly_network_button.configure(
                    state='disabled'
                )
                self.hostonly_frame.delete_hostonly_network_button.configure(
                    state='disabled'
                )
                self.dhcp_frame.enable_update_dhcp_button.configure(
                    state='disabled'
                )
                self.dhcp_frame.delete_dhcp_button.configure(
                    state='disabled'
                )
            except AttributeError:
                pass

    def _add_config_adapter_frame(self, nic_type_value):
        self.add_config_adapter_frame()

    def add_config_adapter_frame(self):
        self.config_adapter_frame = ctk.CTkFrame(self)
        selected_nic_type = self.nic_type.get()
        if selected_nic_type == 'bridged':
            self._insert_bridged()
        elif selected_nic_type == 'host-only':
            self._insert_hostonly()
        elif selected_nic_type == 'internal':
            self._insert_internal()
        elif selected_nic_type == 'nat-network':
            self._insert_natnetwork()
        elif selected_nic_type == 'nat':
            self._insert_nat()
        self.render()

    def _insert_bridged(self):
        self.config_adapter_frame = BridgedWidget(
            self,
            self.provisions_configs
        )

    def _insert_hostonly(self):
        self.config_adapter_frame = ctk.CTkFrame(self)
        self.config_adapter_frame.columnconfigure(0, weight=1)
        self.config_adapter_frame.columnconfigure(1, weight=1)
        self.config_adapter_frame.rowconfigure(0, weight=1)
        self.hostonly_frame = HostOnlyWidget(
            self.config_adapter_frame,
            self.provisions_configs
        )
        self.dhcp_frame = DHCPHostOnlyWidget(
            self.config_adapter_frame,
            self.provisions_configs
        )
        self.hostonly_frame.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_frame
        )
        self.dhcp_frame.grid(
            row=0,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_frame
        )

    def _insert_internal(self):
        pass

    def _insert_natnetwork(self):
        pass

    def _insert_nat(self):
        pass

    def render(self):
        self.enable_adapter_type_frame.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_frame
        )
        self.config_adapter_frame.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_frame
        )
