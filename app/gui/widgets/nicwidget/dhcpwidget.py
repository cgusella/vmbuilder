import customtkinter as ctk
import gui.settings as settings
import subprocess
from gui.guistandard import GuiStandard
from tkinter import messagebox as mb


def get_dhcp_infos() -> dict:
    dhcp_infos = subprocess.run(
        (
            "VBoxManage list dhcpservers | egrep '^NetworkName|^Dhcpd IP"
            "|^LowerIPAddress|^UpperIPAddress|^NetworkMask|^Enabled'"
        ),
        shell=True,
        capture_output=True
    ).stdout.decode("ascii").split('\n')
    number_of_items = 6
    dhcp_configs_dict = dict()
    for count in range(int(len(dhcp_infos)/number_of_items)):
        index_start = number_of_items*count
        # if dhcp server is not a part of hostonlyif, ignore it
        # if 'HostInterfaceNetworking' not in dhcp_infos[index_start]:
        #     continue
        dhcp_configs_dict[
                ''.join(dhcp_infos[index_start].split()[1:]).split('-')[-1]
            ] = (
            dhcp_infos[index_start+1],  # dhcpd ip
            dhcp_infos[index_start+2],  # lower ip
            dhcp_infos[index_start+3],  # upper ip
            dhcp_infos[index_start+4],  # network mask
            dhcp_infos[index_start+5],  # enabled/disabled
        )
    return dhcp_configs_dict


class DHCPWidget(GuiStandard):

    def __init__(self, master, provisions_cofigs, num_tab, nic_type):
        self.provisions_configs = provisions_cofigs
        self.num_tab = num_tab
        self.nic_type = nic_type
        ctk.CTkFrame.__init__(self, master)
        self.set_fonts()
        self.set_std_dimensions()
        self.initialize_elements()
        self.render_elements()

    def set_fonts(self):
        self.font_std = ctk.CTkFont(**settings.FONT_STD)
        self.title_font_std = ctk.CTkFont(**settings.SUBTITLE_VIEW_FONT_BOLD)

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)

    def initialize_elements(self):
        self.dhcp_configs_title_label = ctk.CTkLabel(
            master=self,
            text='DHCP configs',
            font=self.title_font_std
        )
        self.enable_update_dhcp_button = ctk.CTkButton(
            self,
            font=self.font_std,
            text='Enable',
            state='disabled'
        )
        self.delete_dhcp_button = ctk.CTkButton(
            self,
            font=self.font_std,
            text='Delete',
            state='disabled',
            command=self._delete_dhcp
        )
        self.lower_ip_label = ctk.CTkLabel(
            master=self,
            text='Lower IP',
            font=self.font_std
        )
        self.lower_ip_entry = ctk.CTkEntry(
            master=self,
            font=self.font_std,
            placeholder_text='Insert Lower IP'
        )
        self.upper_ip_label = ctk.CTkLabel(
            master=self,
            text='Upper IP',
            font=self.font_std
        )
        self.upper_ip_entry = ctk.CTkEntry(
            master=self,
            font=self.font_std,
            placeholder_text='Insert Upper IP'
        )
        self.server_ip_label = ctk.CTkLabel(
            master=self,
            text='Server IP',
            font=self.font_std
        )
        self.server_ip_entry = ctk.CTkEntry(
            master=self,
            font=self.font_std,
            placeholder_text='Insert Server IP'
        )
        self.server_netmask_label = ctk.CTkLabel(
            master=self,
            text='Server Netmask',
            font=self.font_std
        )
        self.server_netmask_entry = ctk.CTkEntry(
            master=self,
            font=self.font_std,
            placeholder_text='Insert Server Netmask'
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
        self.rowconfigure(7, weight=1)
        self.grid_propagate(False)
        self.enable_update_dhcp_button.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )
        self.delete_dhcp_button.grid(
            row=1,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )
        self.dhcp_configs_title_label.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )
        self.lower_ip_label.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )
        self.upper_ip_label.grid(
            row=2,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )
        self.lower_ip_entry.grid(
            row=3,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='we'
        )
        self.upper_ip_entry.grid(
            row=3,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='we'
        )
        self.server_ip_label.grid(
            row=4,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )
        self.server_netmask_label.grid(
            row=4,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )
        self.server_ip_entry.grid(
            row=5,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='we'
        )
        self.server_netmask_entry.grid(
            row=5,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='we'
        )

    def _show_dhcp_values(self, selected_dhcp: str):
        self.selected_dhcp = selected_dhcp
        self.set_enable_or_update_button()
        # fill the entries with the information from dhcp server
        try:
            dhcp_infos = get_dhcp_infos()[selected_dhcp]
            self.lower_ip_entry.insert(
                0,
                dhcp_infos[1].split()[-1]
            )
            self.upper_ip_entry.insert(
                0,
                dhcp_infos[2].split()[-1]
            )
            self.server_ip_entry.insert(
                0,
                dhcp_infos[0].split()[-1]
            )
            self.server_netmask_entry.insert(
                0,
                dhcp_infos[3].split()[-1]
            )
            self.delete_dhcp_button.configure(
                state='normal'
            )
        except KeyError:
            # self.delete_dhcp_button.configure(
            #     state='disabled'
            # )
            pass

    def set_enable_or_update_button(self):
        # check if dhcp exists; if it does not, then you need a enable button
        self.enable_update_dhcp_button.configure(
            state='normal'
        )
        try:
            if all(get_dhcp_infos()[self.selected_dhcp]):
                self.enable_update_dhcp_button.configure(
                    text='Update',
                    command=self._update_selected_dhcp
                )
            else:
                self.enable_update_dhcp_button.configure(
                    text='Enable',
                    command=self._enable_dhcp
                )
        except KeyError:
            self.enable_update_dhcp_button.configure(
                text='Enable',
                command=self._enable_dhcp
            )

    def _delete_dhcp(self):
        delete = mb.askyesno(
            title='Delete DHCP',
            message=(
                'Are you sure you want to delete '
                f'DHCP server from the "{self.selected_dhcp}" network?'
            )
        )
        if delete:
            subprocess.run(
                f'VBoxManage dhcpserver remove --network=HostInterfaceNetworking-{self.selected_dhcp}',
                shell=True,
            )
            mb.showinfo(
                title='Delete DHCP',
                message=(
                    'The DHCP server has been deleted '
                    f'from "{self.selected_dhcp}" network.'
                )
            )
            self._show_dhcp_values(self.selected_dhcp)

    def _enable_dhcp(self):
        lower_ip = self.lower_ip_entry.get()
        upper_ip = self.upper_ip_entry.get()
        server_ip = self.server_ip_entry.get()
        server_netmask = self.server_netmask_entry.get()
        if not all((lower_ip, upper_ip, server_ip, server_netmask)):
            mb.showerror(
                'Enable error',
                'To enable a DHCP server, you need to fill all the required fields.'
            )
        else:
            if self.nic_type == 'hostonly':
                network_name = f'HostInterfaceNetworking-{self.selected_dhcp} '
            else:
                network_name = self.selected_dhcp

            subprocess.run(
                (
                    'VBoxManage dhcpserver add '
                    f'--network={network_name} '
                    f'--server-ip={server_ip} '
                    f'--netmask={server_netmask} '
                    f'--lower-ip={lower_ip} '
                    f'--upper-ip={upper_ip} '
                    '--enable'
                ),
                shell=True
            )
            mb.showinfo(
                title='Enable DHCP',
                message=f'The DHCP server has been enabled for the {self.selected_dhcp} network.'
            )
        self._show_dhcp_values(selected_dhcp=self.selected_dhcp)
        self.set_enable_or_update_button()

    def _update_selected_dhcp(self):
        print(self.selected_dhcp)
        if self.nic_type == 'hostonly':
            network = f'HostInterfaceNetworking-{self.selected_dhcp}'
        elif self.nic_type == 'natnetwork':
            network = self.selected_dhcp
        lower_ip = self.lower_ip_entry.get()
        upper_ip = self.upper_ip_entry.get()
        server_ip = self.server_ip_entry.get()
        server_netmask = self.server_netmask_entry.get()

        subprocess.run(
            (
                'VBoxManage dhcpserver modify '
                f'--network={network} '
                f'--server-ip={server_ip} '
                f'--netmask={server_netmask} '
                f'--lower-ip={lower_ip} '
                f'--upper-ip={upper_ip} '
                '--enable'
            ),
            shell=True
        )
        if self.nic_type == 'hostonly':
            # get the status of the network adapter
            hostonly_network_status = subprocess.run(
                (
                    "VBoxManage list hostonlyifs | grep "
                    f"HostInterfaceNetworking-{self.selected_dhcp} "
                    "-B1"
                ),
                shell=True,
                capture_output=True
            ).stdout.decode("ascii").split('\n')[0].split()[-1]
            # reset the dhcpserver after update only if its status is up
            if hostonly_network_status.lower() == 'up':
                subprocess.run(
                    (
                        'VBoxManage dhcpserver restart '
                        f'--network=HostInterfaceNetworking-{self.selected_dhcp}'
                    ),
                    shell=True
                )
        elif self.nic_type == 'natnetwork':
            natnetwork_status = subprocess.run(
                (
                    "VBoxManage list natnetworks | egrep "
                    f"{self.selected_dhcp} "
                    "-A6 | tail -1"
                ),
                shell=True,
                capture_output=True
            ).stdout.decode("ascii").split()[-1]

            # reset the dhcpserver after update only if its status is up
            if natnetwork_status.lower() == 'yes':
                subprocess.run(
                    (
                        'VBoxManage natnetwork stop '
                        f'--netname {self.selected_dhcp}'
                    ),
                    shell=True
                )
                subprocess.run(
                    (
                        'VBoxManage natnetwork start '
                        f'--netname {self.selected_dhcp}'
                    ),
                    shell=True
                )
        mb.showinfo(
            title='Update DHCP',
            message=f'The DHCP configs has been updated for the {self.selected_dhcp} network.'
        )
