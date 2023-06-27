import customtkinter as ctk
import subprocess
from gui.guistandard import GuiStandardValues
from tkinter import messagebox as mb


def get_natnetwork_infos() -> dict:
    natnetwork_infos = subprocess.run(
        (
            "VBoxManage list natnetworks | egrep "
            "'^NetworkName|^Network|^Enabled'"
        ),
        shell=True,
        capture_output=True
    ).stdout.decode("ascii").split('\n')
    number_of_items = 3
    natnetwork_configs_dict = dict()
    for count in range(int(len(natnetwork_infos)/number_of_items)):
        index_start = number_of_items*count
        natnetwork_configs_dict[
                ''.join(natnetwork_infos[index_start].split()[1:])
            ] = (
            natnetwork_infos[index_start+1],  # network
            natnetwork_infos[index_start+2],  # enable
        )
    natnetwork_configs_dict['New Network'] = tuple()
    return natnetwork_configs_dict


class NatNetworkWidget(GuiStandardValues):

    def __init__(self, master, provisions_configs, num_tab):
        self.provisions_configs = provisions_configs
        self.num_tab = num_tab
        ctk.CTkFrame.__init__(self, master)
        self.set_fonts()
        self.set_std_dimensions()
        self.initialize_elements()
        self.render_elements()

    def set_fonts(self):
        family = 'Sand'
        self.font_std = ctk.CTkFont(family=family, size=18)
        self.title_font_std = ctk.CTkFont(family=family, size=18, weight='bold')

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)

    """     INITIALIZE ELEMENTS      """

    def initialize_elements(self):
        self.natnetwork_infos_dict = get_natnetwork_infos()
        self.select_label = ctk.CTkLabel(
            master=self,
            font=self.title_font_std,
            text='Nat Network Configs'
        )
        self.available_natnetworks = ctk.CTkOptionMenu(
            master=self,
            font=self.font_std,
            values=list(self.natnetwork_infos_dict.keys()),
            command=self._show_natnetwork_values,
            state='normal'
        )
        self.available_natnetworks.set('Select')

        self.add_natnetwork_button = ctk.CTkButton(
            self,
            font=self.font_std,
            text='Add',
            command=self._add_natnetwork
        )
        self.delete_natnetwork_button = ctk.CTkButton(
            self,
            font=self.font_std,
            text='Delete',
            command=self._delete_natnetwork
        )
        self.update_natnetwork_button = ctk.CTkButton(
            self,
            font=self.font_std,
            text='Update',
            command=self._update_natnetwork
        )

        self.name_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text='Name:'
        )
        self.netmask_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text='Netmask:'
        )
        self.status_label = ctk.CTkLabel(
            self,
            font=self.font_std,
            text='Status:'
        )
        self._show_info_if_in_provisions_configs()

    """     RENDER ELEMENTS     """

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
        self.grid_propagate(False)
        self.select_label.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='wens'
        )
        self.available_natnetworks.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='we'
        )
        self.add_natnetwork_button.grid(
            row=1,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )
        self.name_label.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )
        self.netmask_label.grid(
            row=3,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )
        self.status_label.grid(
            row=4,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )
        self.delete_natnetwork_button.grid(
            row=5,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )
        self.update_natnetwork_button.grid(
            row=5,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )
        self._active_disactive_delete()

    """     INITIALIZE VALUES       """

    def initialize_values(self, natnetwork):
        self.name_value_entry = ctk.CTkEntry(
            self,
            font=self.font_std,
            placeholder_text='Insert Name'
        )
        self.netmask_value_entry = ctk.CTkEntry(
            self,
            font=self.font_std,
            placeholder_text='Insert Netmask'
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
        mainnicwidget_class = self.master.master
        mainnicwidget_class.dhcp_frame._show_dhcp_values(natnetwork)
        self.update_natnetwork_button.configure(
            state="disabled"
        )
        self.add_natnetwork_button.configure(
            state='disabled'
        )
        if natnetwork == 'New Network':
            self.add_natnetwork_button.configure(
                state='normal'
            )
            self.delete_natnetwork_button.configure(
                state='disabled'
            )
            self.name_value_entry.configure(
                state='normal'
            )
        else:
            # read status network
            status_state = self.natnetwork_infos_dict[natnetwork][1].split()[1]
            status_switch_value = 'on' if status_state == 'Yes' else 'off'
            self.status_switch_var.set(status_switch_value)
            self._configure_status_text()
            self._active_disactive_delete()
            self.name_value_entry.insert(
                0,
                natnetwork
            )
            self.netmask_value_entry.insert(
                0,
                f'{self.natnetwork_infos_dict[natnetwork][0].split()[1]}'
            )
            self.update_natnetwork_button.configure(
                state="normal"
            )
            self.name_value_entry.configure(
                state='disabled'
            )
            self.save_in_provisions_configs(
                natnetwork_name=natnetwork,
                natnetwork_info=self.natnetwork_infos_dict[natnetwork]
            )

    """     RENDER VALUES       """

    def render_values(self):
        self.name_value_entry.grid(
            row=2,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='we'
        )
        self.netmask_value_entry.grid(
            row=3,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='we'
        )
        self.status_state_switch.grid(
            row=4,
            column=1,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky='w'
        )

    """     BUTTON COMMANDS AND OTHER METHODS   """

    def _show_natnetwork_values(self, natnetwork):
        self.initialize_values(natnetwork)
        self.render_values()

    def _configure_status_text(self):
        text = 'Up' if self.status_switch_var.get() == 'on' else 'Down'
        self.status_state_switch.configure(
            text=text
        )

    def _active_disactive_delete(self):
        if self.available_natnetworks.cget("state") == 'disabled':
            self.delete_natnetwork_button.configure(
                state='disabled'
            )
        else:
            self.delete_natnetwork_button.configure(
                state='normal'
            )

    def save_in_provisions_configs(self, natnetwork_name, natnetwork_info):
        network_set_up = self.provisions_configs["configurations"]["networks"]
        network_set_up[f"nic{self.num_tab}"]["enable"] = True
        network_set_up[f"nic{self.num_tab}"]["nic_type"] = "natnetwork"
        network_set_up[f"nic{self.num_tab}"]["settings"] = {
            "natnetwork": natnetwork_name,
            "netmask": natnetwork_info[0].split()[-1],
            "status": natnetwork_info[1].split()[-1]
        }

    def _add_natnetwork(self):
        name = self.name_value_entry.get()
        netmask = self.netmask_value_entry.get()
        output = subprocess.run(
            f'VBoxManage natnetwork add --netname={name} --network={netmask}',
            shell=True,
            capture_output=True
        ).stdout.decode("ascii")
        if output:
            text = output
        else:
            text = f'Natnetwork {name} has been created'
        mb.showinfo(
            'Network created',
            text
        )
        self.set_available_natnetworks()
        self._show_natnetwork_values(self.available_natnetworks.get())

    def _show_info_if_in_provisions_configs(self):
        network_info = self.provisions_configs["configurations"]["networks"]
        if network_info[f"nic{self.num_tab}"]["nic_type"] == 'natnetwork':
            if network_info[f"nic{self.num_tab}"]["settings"]:
                self.available_natnetworks.set(
                    network_info[f"nic{self.num_tab}"]["settings"]["natnetwork"]
                )
                self._show_natnetwork_values(
                    network_info[f"nic{self.num_tab}"]["settings"]["natnetwork"]
                )

    def set_available_natnetworks(self):
        self.natnetwork_infos_dict = get_natnetwork_infos()
        values = list(self.natnetwork_infos_dict.keys())
        self.available_natnetworks.configure(
            values=values,
            state='normal'
        )
        try:
            self.available_natnetworks.set(values[-1])
        except IndexError:
            self.available_natnetworks.set('Add network')
            self.available_natnetworks.configure(
                state='disabled'
            )

    def _delete_natnetwork(self):
        selected_network = self.available_natnetworks.get()
        delete = mb.askyesno(
            title='Delete Network',
            message=(
                'You confirm to delete the '
                f'"{selected_network}" network?'
            )
        )
        if delete:
            subprocess.run(
                f'VBoxManage natnetwork remove --netname {selected_network}',
                shell=True,
            )
            # consider also deleting the probable dhcp connected to the
            # natnetwork adapter
            subprocess.run(
                'VBoxManage dhcpserver remove '
                f'--network={selected_network}',
                shell=True,
            )
            mb.showinfo(
                title='Delete Network',
                message=(
                    f'The network "{selected_network}" '
                    'is deleted.'
                )
            )
            self.provisions_configs["configurations"]["networks"][f"nic{self.num_tab}"] = {
                "enable": False,
                "nic_type": "",
                "settings": {}
            }
            self.set_available_natnetworks()
            self._show_natnetwork_values(self.available_natnetworks.get())

    def _update_natnetwork(self):
        name = self.name_value_entry.get()
        netmask = self.netmask_value_entry.get()
        output = subprocess.run(
            'VBoxManage natnetwork modify '
            f'--netname={name} '
            f'--network={netmask}',
            shell=True,
            capture_output=True
        ).stderr
        if output:
            text = output.decode('utf-8')
        else:
            text = f'Natnetwork {name} has been updated'
        mb.showinfo(
            'Update natnetwork',
            text
        )
        self.set_available_natnetworks()
        self._show_natnetwork_values(self.available_natnetworks.get())
