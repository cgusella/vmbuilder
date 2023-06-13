import customtkinter as ctk
from gui.widgets.titlewidget import TitleWidget
from gui.widgets.nicwidget.mainnicwidget import NicWidget


class VagrantNetworkView(ctk.CTkFrame):

    def __init__(self, master, provisions_configs):
        self.frame_name = 'networks'
        self.provisons_configs = provisions_configs
        ctk.CTkFrame.__init__(self, master)
        self.set_std_dimensions()
        self.set_grid()
        self.add_title()
        self.add_main_buttons()
        self.add_nic_tabs()
        self.render()

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)
        self.sticky_frame = 'wens'

    def set_grid(self):
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)

    def add_title(self):
        self.title_frame = TitleWidget(
            master=self,
            title='Vagrant',
            subtitle='Networks'
        )

    def add_nic_tabs(self):
        self.nic_tabs = ctk.CTkTabview(self)
        self.nic_tab_1 = self.nic_tabs.add('nic 1')
        self.nic_tab_2 = self.nic_tabs.add('nic 2')
        self.nic_tab_3 = self.nic_tabs.add('nic 3')
        self.nic_tab_4 = self.nic_tabs.add('nic 4')
        self.nic_widget_1 = NicWidget(
            master=self.nic_tab_1,
            provisions_configs=self.provisons_configs
        )
        self.nic_tab_1.columnconfigure(0, weight=1)
        self.nic_tab_1.rowconfigure(0, weight=1)
        self.nic_widget_2 = NicWidget(
            master=self.nic_tab_2,
            provisions_configs=self.provisons_configs
        )
        self.nic_tab_2.columnconfigure(0, weight=1)
        self.nic_tab_2.rowconfigure(0, weight=1)
        self.nic_widget_3 = NicWidget(
            master=self.nic_tab_3,
            provisions_configs=self.provisons_configs
        )
        self.nic_tab_3.columnconfigure(0, weight=1)
        self.nic_tab_3.rowconfigure(0, weight=1)
        self.nic_widget_4 = NicWidget(
            master=self.nic_tab_4,
            provisions_configs=self.provisons_configs
        )
        self.nic_tab_4.columnconfigure(0, weight=1)
        self.nic_tab_4.rowconfigure(0, weight=1)
        self.nic_widget_1.grid(row=0, column=0, sticky=self.sticky_frame)
        self.nic_widget_2.grid(row=0, column=0, sticky=self.sticky_frame)
        self.nic_widget_3.grid(row=0, column=0, sticky=self.sticky_frame)
        self.nic_widget_4.grid(row=0, column=0, sticky=self.sticky_frame)

    def add_main_buttons(self):
        pass

    def render(self):
        self.title_frame.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_frame
        )
        self.nic_tabs.grid(
            row=1,
            column=0,
            columnspan=2,
            rowspan=7,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_frame
        )
        self.nic_tabs.grid_propagate(False)
