import customtkinter as ctk
import gui.settings as settings
import subprocess
from gui.guistandard import GuiStandardValues
from tkinter import messagebox as mb


def get_hostonly_infos() -> dict:
    hostonly_infos = subprocess.run(
        (
            "VBoxManage list hostonlyifs | egrep "
            "'^Name|^IPAddress|^NetworkMask"
            "|^HardwareAddress|^Status'"
        ),
        shell=True,
        capture_output=True
    ).stdout.decode("ascii").split('\n')
    number_of_items = 5
    hostonly_configs_dict = dict()
    for count in range(int(len(hostonly_infos)/number_of_items)):
        index_start = number_of_items*count
        hostonly_configs_dict[
                ''.join(hostonly_infos[index_start].split()[1:])
            ] = (
            hostonly_infos[index_start+1],  # ipaddress
            hostonly_infos[index_start+2],  # netmask
            hostonly_infos[index_start+3],  # macaddress
            hostonly_infos[index_start+4],  # status
        )
    return hostonly_configs_dict


class HostOnlyWidget(GuiStandardValues):

    def __init__(self, master, provisions_cofigs, num_tab):
        self.provisions_configs = provisions_cofigs
        self.num_tab = num_tab
        self.hostonly_configs_dict = get_hostonly_infos()
        ctk.CTkFrame.__init__(self, master)
        self.set_fonts()
        self.set_std_dimensions()
        self.initialize_elements()
        self.render_elements()

    def set_fonts(self):
        self.font_std = ctk.CTkFont(**settings.FONT_STD)
        self.title_font_std = ctk.CTkFont(**settings.TITLE_WIDGET_FONT_BOLD)

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)

    def initialize_elements(self):
        self.select_label = ctk.CTkLabel(
            master=self,
            font=self.title_font_std,
            text='HostOnly Adapters'
        )
        self.available_hostonly_networks = ctk.CTkOptionMenu(
            master=self,
            font=self.font_std,
            values=list(self.hostonly_configs_dict.keys()),
            command=self._show_network_values,
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
        self.ip_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text='IP Address:'
        )
        self.netmask_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text='Netmask:'
        )
        self.macaddress_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text='Mac Address:'
        )
        self.status_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text='Status:'
        )
        self._show_info_if_in_provisions_configs()

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
        self.select_label.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )
        self.available_hostonly_networks.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='we'
        )
        self.add_hostonly_network_button.grid(
            row=1,
            column=1,
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
        self.delete_hostonly_network_button.grid(
            row=7,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )
        self._active_disactive_delete_update()

    def initialize_values(self, network):
        self.ip_value_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text=f'{self.hostonly_configs_dict[network][0].split()[1]}',
        )
        self.netmask_value_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text=f'{self.hostonly_configs_dict[network][1].split()[1]}'
        )
        self.macaddress_value_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text=f'{self.hostonly_configs_dict[network][2].split()[1]}'
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
        # read status network
        status_state = self.hostonly_configs_dict[network][3].split()[1]
        status_switch_value = 'on' if status_state == 'Up' else 'off'
        self.status_switch_var.set(status_switch_value)
        self._configure_status_text()
        self._active_disactive_delete_update()
        mainnicwidget_class = self.master.master
        mainnicwidget_class.dhcp_frame._show_dhcp_values(network)
        self.save_in_provisions_configs(
            network,
            self.hostonly_configs_dict[network]
        )

    def render_values(self):
        self.ip_value_label.grid(
            row=3,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )
        self.netmask_value_label.grid(
            row=4,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )
        self.macaddress_value_label.grid(
            row=5,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )
        self.status_state_switch.grid(
            row=6,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )

    def _show_network_values(self, network):
        self.initialize_values(network)
        self.render_values()

    def _show_info_if_in_provisions_configs(self):
        network_info = self.provisions_configs["configurations"]["networks"]
        if network_info[f"nic{self.num_tab}"]["nic_type"] == 'hostonly':
            if network_info[f"nic{self.num_tab}"]["settings"]:
                self.available_hostonly_networks.set(
                    network_info[f"nic{self.num_tab}"]["settings"]["hostonly"]
                )
                self._show_network_values(
                    network_info[f"nic{self.num_tab}"]["settings"]["hostonly"]
                )

    def _active_disactive_delete_update(self):
        if self.available_hostonly_networks.cget("state") == 'disabled':
            self.delete_hostonly_network_button.configure(
                state='disabled'
            )
        else:
            self.delete_hostonly_network_button.configure(
                state='normal'
            )

    def _configure_status_text(self):
        text = 'Up' if self.status_switch_var.get() == 'on' else 'Down'
        self.status_state_switch.configure(
            text=text
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
        self._show_network_values(self.available_hostonly_networks.get())

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
            # consider also deleting the probable dhcp connected to the hostonly adapter
            subprocess.run(
                'VBoxManage dhcpserver remove '
                f'--network=HostInterfaceNetworking-{selected_network}',
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
            self._show_network_values(self.available_hostonly_networks.get())

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

    def save_in_provisions_configs(self, hostonly_name, hostonly_info):
        network_set_up = self.provisions_configs["configurations"]["networks"]
        network_set_up[f"nic{self.num_tab}"]["enable"] = True
        network_set_up[f"nic{self.num_tab}"]["nic_type"] = "hostonly"
        network_set_up[f"nic{self.num_tab}"]["settings"] = {
            "hostonly": hostonly_name,
            "ipaddress": hostonly_info[0].split()[-1],
            "netmask": hostonly_info[1].split()[-1],
            "macaddress": hostonly_info[2].split()[-1],
            "status": hostonly_info[3].split()[-1]
        }
