import customtkinter as ctk
import gui.settings as settings
import subprocess
from gui.guistandard import GuiStandardValues


def get_bridged_infos() -> dict:
    bridged_infos = subprocess.run(
        (
            "VBoxManage list bridgedifs | egrep "
            "'^Name|^DHCP|^IPAddress|^NetworkMask"
            "|^HardwareAddress|^Status'"
        ),
        shell=True,
        capture_output=True
    ).stdout.decode("ascii").split('\n')
    number_of_items = 6
    bridged_configs_dict = dict()
    for count in range(int(len(bridged_infos)/number_of_items)):
        index_start = number_of_items*count
        bridged_configs_dict[
                ''.join(bridged_infos[index_start].split()[1:])
            ] = (
            bridged_infos[index_start+1],  # dhcp
            bridged_infos[index_start+2],  # ipaddress
            bridged_infos[index_start+3],  # netmask
            bridged_infos[index_start+4],  # macaddress
            bridged_infos[index_start+5],  # status
        )
    return bridged_configs_dict


class BridgedWidget(GuiStandardValues):

    def __init__(self, master, provisions_configs, num_tab):
        self.provisions_configs = provisions_configs
        self.num_tab = num_tab
        self.bridged_configs_dict = get_bridged_infos()
        ctk.CTkFrame.__init__(self, master, fg_color=["gray81", "gray21"])
        self.set_fonts()
        self.set_std_dimensions()
        self.initialize_elements()
        self.render_elements()

    def set_fonts(self):
        self.font_std = ctk.CTkFont(**settings.FONT_STD)

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)
        self.sticky_horizontal = 'we'

    def initialize_elements(self):
        self.select_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text='Select among these bridges'
        )
        self.available_bridged_nics = ctk.CTkOptionMenu(
            master=self,
            font=self.font_std,
            values=list(self.bridged_configs_dict.keys()),
            command=self._show_bridged_info,
            state='normal'
        )
        self.dhcp_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text='DHCP'
        )
        self.ip_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text='IP Address'
        )
        self.netmask_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text='NetworkMask'
        )
        self.macaddress_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text='MacAddress'
        )
        self.status_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text='Status'
        )

    def render_elements(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.select_label.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self.available_bridged_nics.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self.dhcp_label.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )
        self.ip_label.grid(
            row=3,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )
        self.netmask_label.grid(
            row=4,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )
        self.macaddress_label.grid(
            row=5,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )
        self.status_label.grid(
            row=6,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )

    def initialize_values(self, nic):
        self.dhcp_value_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text=self.bridged_configs_dict[nic][0].split()[-1]
        )
        self.ip_value_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text=self.bridged_configs_dict[nic][1].split()[-1]
        )
        self.netmask_value_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text=self.bridged_configs_dict[nic][2].split()[-1]
        )
        self.macaddress_value_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text=self.bridged_configs_dict[nic][3].split()[-1]
        )
        self.status_value_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text=self.bridged_configs_dict[nic][4].split()[-1]
        )

    def render_values(self):
        self.dhcp_value_label.grid(
            row=2,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_horizontal
        )
        self.ip_value_label.grid(
            row=3,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_horizontal
        )
        self.netmask_value_label.grid(
            row=4,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_horizontal
        )
        self.macaddress_value_label.grid(
            row=5,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_horizontal
        )
        self.status_value_label.grid(
            row=6,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_horizontal
        )

    def _show_info_if_in_provisions_configs(self):
        network_info = self.provisions_configs["configurations"]["networks"]
        if network_info[f"nic{self.num_tab}"]["enable"] and network_info[f"nic{self.num_tab}"]["nic_type"] == 'bridged':
            self.available_bridged_nics.set(
                network_info[f"nic{self.num_tab}"]["settings"]["bridge"]
            )

    def _show_bridged_info(self, nic):
        self.initialize_values(nic)
        self.render_values()
        self.save_in_provisions_configs()

    def save_in_provisions_configs(self):
        network_set_up = self.provisions_configs["configurations"]["networks"]
        network_set_up[f"nic{self.num_tab}"]["enable"] = True
        network_set_up[f"nic{self.num_tab}"]["nic_type"] = "bridged"
        network_set_up[f"nic{self.num_tab}"]["settings"] = {
            "bridge": self.available_bridged_nics.get(),
            "dhcp": self.bridged_configs_dict[self.available_bridged_nics.get()][0].split()[-1],
            "ipaddress": self.bridged_configs_dict[self.available_bridged_nics.get()][1].split()[-1],
            "netmask": self.bridged_configs_dict[self.available_bridged_nics.get()][2].split()[-1],
            "macaddress": self.bridged_configs_dict[self.available_bridged_nics.get()][3].split()[-1],
            "status": self.bridged_configs_dict[self.available_bridged_nics.get()][4].split()[-1]
        }
