import customtkinter as ctk
from gui.widgets.titlewidget import TitleWidget
from gui.widgets.nicwidget import NicWidget


class VagrantNetworkView(ctk.CTkFrame):

    def __init__(self, master, provisions_configs):
        self.frame_name = 'networks'
        self.provisons_configs = provisions_configs
        ctk.CTkFrame.__init__(self, master)
        self.set_std_dimensions()
        self.set_grid()
        self.add_title()
        self.add_main_buttons()
        self.add_nic_frame()
        self.render()

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

    def set_grid(self):
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

    def add_title(self):
        self.title_frame = TitleWidget(
            master=self,
            title='Vagrant',
            subtitle='Networks'
        )

    def add_nic_frame(self):
        self.nic_frame = NicWidget(
            master=self,
            provisions_configs=self.provisons_configs
        )

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
        self.nic_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            rowspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            sticky=self.sticky_frame
        )
