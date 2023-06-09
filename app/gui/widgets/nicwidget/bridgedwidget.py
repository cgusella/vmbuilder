import customtkinter as ctk
import subprocess


class BridgedWidget(ctk.CTkFrame):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        ctk.CTkFrame.__init__(self, master)
        self.font_std = ctk.CTkFont(family='Sans', size=18)
        self.set_std_dimensions()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        bridged_configs_list = subprocess.run(
            "VBoxManage list bridgedifs | egrep '^Name|^DHCP|^IPAddress|^NetworkMask'",
            shell=True,
            capture_output=True
        ).stdout.decode("ascii").split('\n')
        self.bridged_configs_dict = dict()
        for count in range(int(len(bridged_configs_list)/4)):
            index_start = 4*count
            self.bridged_configs_dict[''.join(bridged_configs_list[index_start].split()[1:])] = (
                bridged_configs_list[index_start+1],  # dhcp
                bridged_configs_list[index_start+2],  # ipaddress
                bridged_configs_list[index_start+3],  # netmask
            )
        select_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text='Select among these bridges'
        )
        select_label.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
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
        self._show_bridged_info(self.available_bridged_nics.get())
        # render config frame
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
