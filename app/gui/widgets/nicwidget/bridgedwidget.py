import customtkinter as ctk
import subprocess


def get_bridged_infos() -> list:
    bridged_infos = subprocess.run(
        (
            "VBoxManage list bridgedifs | egrep "
            "'^Name|^DHCP|^IPAddress|^NetworkMask"
            "|^HardwareAddress|^Status'"
        ),
        shell=True,
        capture_output=True
    ).stdout.decode("ascii").split('\n')
    return bridged_infos


class BridgedWidget(ctk.CTkFrame):

    def __init__(self, master, provisions_configs, num_tab):
        self.provisions_configs = provisions_configs
        self.num_tab = num_tab
        ctk.CTkFrame.__init__(self, master)
        self.font_std = ctk.CTkFont(family='Sans', size=18)
        self.set_std_dimensions()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        bridged_configs_list = get_bridged_infos()
        self.bridged_configs_dict = dict()
        number_of_items = 6
        for count in range(int(len(bridged_configs_list)/number_of_items)):
            index_start = number_of_items*count
            self.bridged_configs_dict[
                    ''.join(bridged_configs_list[index_start].split()[1:])
                ] = (
                bridged_configs_list[index_start+1],  # dhcp
                bridged_configs_list[index_start+2],  # ipaddress
                bridged_configs_list[index_start+3],  # netmask
                bridged_configs_list[index_start+4],  # macaddress
                bridged_configs_list[index_start+5],  # status
            )
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
            text=''
        )
        self.ip_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text=''
        )
        self.netmask_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text=''
        )
        self.macaddress_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text=''
        )
        self.status_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text=''
        )
        self._show_info_if_in_provisions_configs()
        self._show_bridged_info(self.available_bridged_nics.get())
        self.render()

    def _show_info_if_in_provisions_configs(self):
        network_info = self.provisions_configs["configurations"]["networks"]
        if network_info[f"nic{self.num_tab}"]["enable"] and network_info[f"nic{self.num_tab}"]["nic_type"] == 'bridged':
            self.available_bridged_nics.set(
                network_info[f"nic{self.num_tab}"]["settings"]["bridge"]
            )

    def render(self):
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

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)

    def _show_bridged_info(self, nic):
        self.dhcp_label.configure(
            text=f'{self.bridged_configs_dict[nic][0]}'
        )
        self.ip_label.configure(
            text=f'{self.bridged_configs_dict[nic][1]}'
        )
        self.netmask_label.configure(
            text=f'{self.bridged_configs_dict[nic][2]}'
        )
        self.macaddress_label.configure(
            text=f'{self.bridged_configs_dict[nic][3]}'
        )
        self.status_label.configure(
            text=f'{self.bridged_configs_dict[nic][4]}'
        )
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
