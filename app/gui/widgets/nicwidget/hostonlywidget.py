import customtkinter as ctk
import subprocess
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


class HostOnlyWidget(ctk.CTkFrame):

    def __init__(self, master, provisions_cofigs):
        self.provisions_configs = provisions_cofigs
        ctk.CTkFrame.__init__(self, master)
        self.font_std = ctk.CTkFont(family='Sans', size=18)
        self.title_font_std = ctk.CTkFont(family='Sans', size=18, weight='bold')
        self.set_std_dimensions()
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
        hostonly_configs_dict = get_hostonly_infos()

        self.select_label = ctk.CTkLabel(
            master=self,
            font=self.title_font_std,
            text='HostOnly Adapters'
        )
        self.available_hostonly_networks = ctk.CTkOptionMenu(
            master=self,
            font=self.font_std,
            values=list(hostonly_configs_dict.keys()),
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
        self._render_select_among()

        # add network labels
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
        self._render_info()

    def _show_network_values(self, network):
        hostonly_configs_dict = get_hostonly_infos()
        self.ip_value_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text=f'{hostonly_configs_dict[network][0].split()[1]}',
        )
        self.ip_value_label.grid(
            row=3,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self.netmask_value_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text=f'{hostonly_configs_dict[network][1].split()[1]}'
        )
        self.netmask_value_label.grid(
            row=4,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )

        # insert macaddress network
        self.macaddress_value_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text=f'{hostonly_configs_dict[network][2].split()[1]}'
        )
        self.macaddress_value_label.grid(
            row=5,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
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
        self.status_state_switch.grid(
            row=6,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        # read status network
        status_state = hostonly_configs_dict[network][3].split()[1]
        status_switch_value = 'on' if status_state == 'Up' else 'off'
        self.status_switch_var.set(status_switch_value)
        self._configure_status_text()
        self._active_disactive_delete_update()
        mainnicwidget_class = self.master.master
        mainnicwidget_class.dhcp_frame._show_dhcp_values(network)

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)

    def _render_select_among(self):
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
            row=7,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wn'
        )
        self._active_disactive_delete_update()

    def _active_disactive_delete_update(self):
        if self.available_hostonly_networks.get() == 'Select':
            self.delete_hostonly_network_button.configure(
                state='disabled'
            )
        else:
            self.delete_hostonly_network_button.configure(
                state='normal'
            )

    def _render_info(self):
        self.ip_label.grid(
            row=3,
            column=0,
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
        self.macaddress_label.grid(
            row=5,
            column=0,
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

    # def _configure_dhcp(self):
    #     dhcp_switch_value = self.dhcp_switch_var.get()
    #     if dhcp_switch_value == 'on':
    #         self.dhcp_state_switch.configure(
    #             text='Enabled'
    #         )
    #         self._add_dhcp_configs_frame()
    #     elif dhcp_switch_value == 'off':
    #         try:
    #             self.dhcp_configs_frame.destroy()
    #         except AttributeError:
    #             pass
    #         self.dhcp_state_switch.configure(
    #             text='Disabled'
    #         )

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
        hostonly_configs_dict = get_hostonly_infos()
        values = list(hostonly_configs_dict.keys())
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
