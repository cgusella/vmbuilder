import customtkinter as ctk
import subprocess
from tkinter import messagebox as mb


def get_hostonly_infos() -> dict:
    hostonly_infos = subprocess.run(
        (
            "VBoxManage list hostonlyifs | egrep "
            "'^Name|^DHCP|^IPAddress|^NetworkMask"
            "|^HardwareAddress|^Status'"
        ),
        shell=True,
        capture_output=True
    ).stdout.decode("ascii").split('\n')
    number_of_items = 6
    hostonly_configs_dict = dict()
    for count in range(int(len(hostonly_infos)/number_of_items)):
        index_start = number_of_items*count
        hostonly_configs_dict[
                ''.join(hostonly_infos[index_start].split()[1:])
            ] = (
            hostonly_infos[index_start+1],  # dhcp
            hostonly_infos[index_start+2],  # ipaddress
            hostonly_infos[index_start+3],  # netmask
            hostonly_infos[index_start+4],  # macaddress
            hostonly_infos[index_start+5],  # status
        )
    return hostonly_configs_dict


class HostOnlyWidget(ctk.CTkFrame):

    def __init__(self, master, provisions_cofigs):
        self.provisions_configs = provisions_cofigs
        ctk.CTkFrame.__init__(self, master)
        self.font_std = ctk.CTkFont(family='Sans', size=18)
        self.title_font_std = ctk.CTkFont(family='Sans', size=18, weight='bold')
        self.set_std_dimensions()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.grid_propagate(False)
        self.hostonly_configs_dict = get_hostonly_infos()

        self.select_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text='Select among these networks'
        )
        self.available_hostonly_networks = ctk.CTkOptionMenu(
            master=self,
            font=self.font_std,
            values=list(self.hostonly_configs_dict.keys()),
            command=self._show_hostonly_info,
            state='normal'
        )
        self.available_hostonly_networks.set('Select')

        self.add_hostonly_network_button = ctk.CTkButton(
            self,
            font=self.font_std,
            text='Add',
            command=self._add_hostonly_network
        )
        self.delete_hostonly_network_button = ctk.CTkButton(
            self,
            font=self.font_std,
            text='Delete',
            command=self._delete_hostonly_network
        )
        self.update_button = ctk.CTkButton(
            self,
            font=self.font_std,
            text='Update',
            command=self._update_selected_hostonly
        )
        self.dummy_frame = ctk.CTkFrame(self, fg_color='transparent')
        self._show_hostonly_info(self.available_hostonly_networks.get())

    def initialize_main_labels(self):
        self.dhcp_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text='DHCP:'
        )
        self.dhcp_switch_var = ctk.StringVar()
        self.dhcp_state_switch = ctk.CTkSwitch(
            master=self,
            text='',
            font=ctk.CTkFont(family='Sans', size=14),
            variable=self.dhcp_switch_var,
            onvalue='on',
            offvalue='off',
            command=self._configure_dhcp
        )
        self.ip_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text='IP Address:'
        )
        self.ip_entry = ctk.CTkEntry(
            self,
            font=self.font_std,
        )
        self.netmask_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text='Netmask:'
        )
        self.netmask_entry = ctk.CTkEntry(
            self,
            font=self.font_std
        )
        self.macaddress_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text='Mac Address:'
        )
        self.macaddress_value_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text=''
        )
        self.status_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text='Status:'
        )
        self.status_switch_var = ctk.StringVar()
        self.status_state_switch = ctk.CTkSwitch(
            master=self,
            text='',
            font=ctk.CTkFont(family='Sans', size=14),
            variable=self.status_switch_var,
            onvalue='on',
            offvalue='off',
            command=self._configure_status_text
        )

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)

    def render(self):
        self._render_select_among()
        self._render_info()
        self._render_dummy_frame()

    def _render_select_among(self):
        self.select_label.grid(
            row=0,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self.available_hostonly_networks.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self.add_hostonly_network_button.grid(
            row=1,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self.delete_hostonly_network_button.grid(
            row=1,
            column=2,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self.update_button.grid(
            row=1,
            column=3,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )

    def _render_info(self):
        self.dhcp_label.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self.dhcp_state_switch.grid(
            row=2,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self.ip_label.grid(
            row=3,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self.ip_entry.grid(
            row=3,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self.netmask_label.grid(
            row=4,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self.netmask_entry.grid(
            row=4,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self.macaddress_label.grid(
            row=5,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self.macaddress_value_label.grid(
            row=5,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self.status_label.grid(
            row=6,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self.status_state_switch.grid(
            row=6,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )

    def _render_dummy_frame(self):
        self.dummy_frame.grid(
            row=2,
            column=2,
            columnspan=2,
            rowspan=5,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )

    def _configure_dhcp(self):
        dhcp_switch_value = self.dhcp_switch_var.get()
        if dhcp_switch_value == 'on':
            self.dhcp_state_switch.configure(
                text='Enabled'
            )
            self._add_dhcp_configs_frame()
        elif dhcp_switch_value == 'off':
            try:
                self.dhcp_configs_frame.destroy()
            except AttributeError:
                pass
            self.dhcp_state_switch.configure(
                text='Disabled'
            )

    def _configure_status_text(self):
        text = 'Up' if self.status_switch_var.get() == 'on' else 'Down'
        self.status_state_switch.configure(
            text=text
        )

    def _add_dhcp_configs_frame(self):
        self.dhcp_configs_frame = ctk.CTkFrame(self)
        self.dhcp_configs_frame.columnconfigure(0, weight=1)
        self.dhcp_configs_frame.columnconfigure(1, weight=1)
        self.dhcp_configs_frame.rowconfigure(0, weight=1)
        self.dhcp_configs_frame.rowconfigure(1, weight=1)
        self.dhcp_configs_frame.rowconfigure(2, weight=1)
        self.dhcp_configs_frame.rowconfigure(3, weight=1)
        self.dhcp_configs_frame.rowconfigure(4, weight=1)
        self.dhcp_configs_frame.rowconfigure(5, weight=1)
        self.dhcp_configs_frame.rowconfigure(6, weight=1)
        self.dhcp_configs_frame.rowconfigure(7, weight=1)
        self.dhcp_configs_frame.grid_propagate(False)

        self.dhcp_configs_title_label = ctk.CTkLabel(
            master=self.dhcp_configs_frame,
            text='DHCP configs',
            font=self.title_font_std
        )
        lower_ip_label = ctk.CTkLabel(
            master=self.dhcp_configs_frame,
            text='Lower IP',
            font=self.font_std
        )
        self.lower_ip_entry = ctk.CTkEntry(
            master=self.dhcp_configs_frame,
            font=self.font_std,
            placeholder_text='Insert Lower IP'
        )
        upper_ip_label = ctk.CTkLabel(
            master=self.dhcp_configs_frame,
            text='Upper IP',
            font=self.font_std
        )
        self.upper_ip_entry = ctk.CTkEntry(
            master=self.dhcp_configs_frame,
            font=self.font_std,
            placeholder_text='Insert Upper IP'
        )
        server_ip_label = ctk.CTkLabel(
            master=self.dhcp_configs_frame,
            text='Server IP',
            font=self.font_std
        )
        self.server_ip_entry = ctk.CTkEntry(
            master=self.dhcp_configs_frame,
            font=self.font_std,
            placeholder_text='Insert Server IP'
        )
        server_netmask_label = ctk.CTkLabel(
            master=self.dhcp_configs_frame,
            text='Server Netmask',
            font=self.font_std
        )
        self.server_netmask_entry = ctk.CTkEntry(
            master=self.dhcp_configs_frame,
            font=self.font_std,
            placeholder_text='Insert Server Netmask'
        )
        # render subframe
        self.dhcp_configs_title_label.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )
        lower_ip_label.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )
        upper_ip_label.grid(
            row=1,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )
        self.lower_ip_entry.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )
        self.upper_ip_entry.grid(
            row=2,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )
        server_ip_label.grid(
            row=3,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )
        server_netmask_label.grid(
            row=3,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )
        self.server_ip_entry.grid(
            row=4,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )
        self.server_netmask_entry.grid(
            row=4,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )
        # render into main frame
        self.dhcp_configs_frame.grid(
            row=2,
            column=2,
            columnspan=2,
            rowspan=5,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )

    def _add_hostonly_network(self):
        output = subprocess.run(
            'VBoxManage hostonlyif create',
            shell=True,
            capture_output=True
        ).stdout.decode("ascii")
        mb.showinfo(
            'Network created',
            output
        )
        self.set_available_hostonly_networks()
        self._show_hostonly_info(self.available_hostonly_networks.get())

    def _delete_hostonly_network(self):
        selected_network = self.available_hostonly_networks.get()
        delete = mb.askyesno(
            title='Delete Network',
            message=(
                'You confirm to delete the '
                f'"{selected_network}" network?'
            )
        )
        if delete:
            subprocess.run(
                f'VBoxManage hostonlyif remove "{selected_network}"',
                shell=True,
            )
            mb.showinfo(
                title='Delete Network',
                message=(
                    f'The network "{selected_network}" '
                    'is deleted.'
                )
            )
            self.set_available_hostonly_networks()
            self._show_hostonly_info(self.available_hostonly_networks.get())

    def set_available_hostonly_networks(self):
        self.hostonly_configs_dict = get_hostonly_infos()
        values = list(self.hostonly_configs_dict.keys())
        self.available_hostonly_networks.configure(
            values=values,
            state='normal'
        )
        try:
            self.available_hostonly_networks.set(values[-1])
        except IndexError:
            self.available_hostonly_networks.set('Add network')
            self.available_hostonly_networks.configure(
                state='disabled'
            )

    def _update_selected_hostonly(self):
        selected_network = self.available_hostonly_networks.get()
        dhcp_value = self.dhcp_switch_var.get()
        ip_addrss = self.ip_entry.get()
        netmask = self.netmask_entry.get()
        status = self.status_switch_var.get()
        if dhcp_value == 'on':
            lower_ip = self.lower_ip_entry.get()
            upper_ip = self.upper_ip_entry.get()
            server_ip = self.server_ip_entry.get()
            server_netmask = self.server_netmask_entry.get()
            subprocess.run(
                (
                    'VBoxManage dhcpserver modify '
                    f'--ifname "{selected_network}" '
                    f'--enable --ip "{server_ip}" '
                    f'--netmask "{server_netmask}" '
                    f'--lowerip "{lower_ip}" '
                    f'--upperip "{upper_ip}"'
                ),
                shell=True
            )
        subprocess.run(
            (
                f'VBoxManage hostonlyif ipconfig "{selected_network}" '
                f'--ip "{ip_addrss}" --netmask "{netmask}"'
            ),
            shell=True
        )
        # if status == 'on':
        #     subprocess.run(
        #         (
        #             f'VBoxManage hostonlyif set "{selected_network}" '
        #             '--status on'
        #         ),
        #         shell=True
        #     )
        # elif status == 'off':
        #     subprocess.run(
        #         (
        #             f'VBoxManage hostonlyif set "{selected_network}" '
        #             '--status off'
        #         ),
        #         shell=True
        #     )
        mb.showinfo(
            'Update network'
            f'The network {selected_network} has been updated'
        )

    def _show_hostonly_info(self, network):
        if self.available_hostonly_networks.get() == 'Select':
            self._render_select_among()
            self._render_dummy_frame()
        else:
            self.initialize_main_labels()
            # read dhcp state
            dhcp_state = self.hostonly_configs_dict[network][0].split()[1]
            dhcp_switch_value = 'on' if dhcp_state == 'Enabled' else 'off'
            self.dhcp_switch_var.set(dhcp_switch_value)
            self._configure_dhcp()

            # read status network
            status_state = self.hostonly_configs_dict[network][4].split()[1]
            status_switch_value = 'Up' if status_state == 'Up' else 'Down'
            self.status_switch_var.set(status_switch_value)
            self._configure_status_text()

            # insert ip network
            self.ip_entry.insert(
                0,
                f'{self.hostonly_configs_dict[network][1].split()[1]}'
            )
            # insert netmask network
            self.netmask_entry.insert(
                0,
                f'{self.hostonly_configs_dict[network][2].split()[1]}'
            )
            # insert macaddress network
            self.macaddress_value_label.configure(
                text=f'{self.hostonly_configs_dict[network][3].split()[1]}'
            )
            self.render()
