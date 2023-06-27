import customtkinter as ctk
from gui.guistandard import GuiStandard
from gui.widgets.packermanager.packagemanagerwidget import PackageManagerWidget
from gui.widgets.packermanager.selectedpackageswidget import SelectedPackagesWidget


class MainPackageWidget(GuiStandard):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        self.master = master
        ctk.CTkFrame.__init__(self, master)
        self.set_fonts()
        self.set_std_dimensions()
        self.initialize_elements()
        self.render_elements()

    def set_fonts(self):
        family = 'Sans'
        self.little_title = ctk.CTkFont(
            family=family,
            size=20,
            weight='bold'
        )
        self.label_font = ctk.CTkFont(
            family=family,
            size=16,
        )

    def set_std_dimensions(self):
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)
        self.pady_up = (10, 0)
        self.pady_down = (0, 10)
        self.pad_right = (5, 10)
        self.pad_equal = (5, 5)
        self.pady_entry = (2, 10)
        self.entry_height_std = 50
        self.ipadx_std = 10
        self.ipady_std = 10
        self.ipadx_button = 5
        self.ipady_button = 5
        self.width_button_std = 100
        self.sticky_frame = 'wens'
        self.sticky_horizontal = 'ew'

    def initialize_elements(self):
        self.packages_label = ctk.CTkLabel(
            master=self,
            text='Package Manager',
            font=self.little_title
        )
        self.selected_packages_frame = SelectedPackagesWidget(
            self,
            self.provisions_configs
        )
        self.package_manager_frame = PackageManagerWidget(
            self,
            self.provisions_configs
        )

    def render_elements(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.packages_label.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=(20, 20),
            pady=(10, 2),
            sticky='wn'
        )
        self.package_manager_frame.grid(
            row=1,
            column=0,
            rowspan=2,
            padx=self.padx_std,
            pady=self.pady_std,
            ipadx=self.ipadx_std,
            ipady=self.ipady_std,
            sticky=self.sticky_frame,
        )
        self.selected_packages_frame.grid(
            row=1,
            column=1,
            rowspan=2,
            sticky=self.sticky_frame,
        )
