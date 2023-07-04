import customtkinter as ctk
import gui.settings as settings
from gui.guistandard import GuiStandard
from gui.widgets.nicwidget.bridgedwidget import BridgedWidget
from gui.widgets.nicwidget.hostonlywidget import HostOnlyWidget
from gui.widgets.nicwidget.dhcpwidget import DHCPWidget
from gui.widgets.nicwidget.natnetworkwidget import NatNetworkWidget


class NicWidget(GuiStandard):

    def __init__(self, master, provisions_configs, num_tab: int):
        self.provisions_configs = provisions_configs
        self.num_tab = num_tab
        self.network_info = self.provisions_configs["configurations"]["networks"][f"nic{num_tab}"]
        ctk.CTkFrame.__init__(self, master, fg_color='transparent')
        self.set_fonts()
        self.set_std_dimensions()
        self.initialize_elements()
        self.render_elements()

    def set_fonts(self):
        self.font_std = ctk.CTkFont(**settings.FONT_STD)

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

    """     initialize elements     """

    def initialize_elements(self):
        self._initialize_subframes()
        self._initialize_enable_adapter_subframe_elemets()
        self._initialize_config_adapter_subframe_elements()
        self._check_nic_type_optionmenu()

    def _initialize_subframes(self):
        self.enable_adapter_type_frame = ctk.CTkFrame(self)
        self.config_adapter_frame = ctk.CTkFrame(self)

    def _initialize_enable_adapter_subframe_elemets(self):
        self.enable_checkbox = ctk.CTkCheckBox(
            master=self.enable_adapter_type_frame,
            font=self.font_std,
            text='Enable',
            command=self._check_nic_type_optionmenu
        )
        self.nic_type = ctk.CTkOptionMenu(
            master=self.enable_adapter_type_frame,
            font=self.font_std,
            state='disabled',
            values=['hostonly', 'bridged', 'internal', 'natnetwork', 'nat'],
            command=self._reload_config_adapter_subframe
        )
        self.nic_type.set('Select one')
        if self.network_info["enable"] or self.network_info["settings"]:
            self._show_nic_info_if_in_provisions_configs()

    def _initialize_config_adapter_subframe_elements(self):
        selected_nic_type = self.nic_type.get()
        if selected_nic_type == 'bridged':
            self.config_adapter_frame = BridgedWidget(
                self,
                self.provisions_configs,
                self.num_tab
            )
        elif selected_nic_type == 'hostonly':
            self._initialize_hostonly_elements()
        elif selected_nic_type == 'internal':
            pass
        elif selected_nic_type == 'natnetwork':
            self._initialize_natnetwork_subframe_elements()
        elif selected_nic_type == 'nat':
            pass

    def _initialize_hostonly_elements(self):
        # HostOnlyWidget uses methods in DHCPWidget,
        # so do not invert their initialization order
        self.dhcp_frame = DHCPWidget(
            self.config_adapter_frame,
            self.provisions_configs,
            self.num_tab,
            nic_type='hostonly'
        )
        self.hostonly_frame = HostOnlyWidget(
            self.config_adapter_frame,
            self.provisions_configs,
            self.num_tab
        )

    def _initialize_natnetwork_subframe_elements(self):
        # NatNetwork uses methods in DHCPWidget,
        # so do not invert their initialization order
        self.dhcp_frame = DHCPWidget(
            self.config_adapter_frame,
            self.provisions_configs,
            self.num_tab,
            nic_type='natnetwork'
        )
        self.natnetwork_frame = NatNetworkWidget(
            self.config_adapter_frame,
            self.provisions_configs,
            self.num_tab
        )

    """    render elements     """

    def _render_enable_adapter_subframe_elements(self):
        self.enable_adapter_type_frame.columnconfigure(0, weight=1)
        self.enable_adapter_type_frame.rowconfigure(0, weight=1)
        self.enable_adapter_type_frame.rowconfigure(1, weight=1)
        self.enable_checkbox.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_optionmenu
        )
        self.nic_type.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_optionmenu
        )

    def _render_hostonly_elements(self):
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

    def _render_natnetwork_subframe_elements(self):
        self.natnetwork_frame.grid(
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

    def _render_config_adapter_subframe_elements(self):
        self.config_adapter_frame.columnconfigure(0, weight=1)
        self.config_adapter_frame.columnconfigure(1, weight=1)
        self.config_adapter_frame.rowconfigure(0, weight=1)
        selected_nic_type = self.nic_type.get()
        # bridged does not need two subframes, so it does not need
        # to be rendered
        if selected_nic_type == 'hostonly':
            self._render_hostonly_elements()
        elif selected_nic_type == 'internal':
            pass
        elif selected_nic_type == 'natnetwork':
            self._render_natnetwork_subframe_elements()
        elif selected_nic_type == 'nat':
            pass

    def _render_subframes(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
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

    def render_elements(self):
        self._render_enable_adapter_subframe_elements()
        self._render_config_adapter_subframe_elements()
        self._render_subframes()

    """     button commands     """

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
            self.provisions_configs["configurations"]["networks"][f"nic{self.num_tab}"]["enable"] = False

    def _show_nic_info_if_in_provisions_configs(self):
        if self.network_info["enable"]:
            self.enable_checkbox.select()
        else:
            self.enable_checkbox.deselect()
        self.nic_type.set(
            self.network_info["nic_type"]
        )
        self.nic_type.configure(state='normal')

    def _reload_config_adapter_subframe(self, nic_type_value):
        self.config_adapter_frame = ctk.CTkFrame(self)
        self._initialize_config_adapter_subframe_elements()
        self._render_config_adapter_subframe_elements()
        self._render_subframes()
