import customtkinter as ctk
from gui.guistandard import GuiStandard
from gui.views.utilsview import ScrollableButtonFrame


class SelectedPackagesWidget(GuiStandard):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        ctk.CTkFrame.__init__(self, master, fg_color='transparent')
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
        self.install_scrollable = ScrollableButtonFrame(
            master=self,
            title='Install',
            values=sorted(
                self.provisions_configs["provisions"]["packages_to_install"]
            ),
            provisions_configs=self.provisions_configs
        )
        self.clean_install_button = ctk.CTkButton(
            master=self,
            font=self.label_font,
            text='Clean',
            command=self._clean_install_packages
        )
        self.uninstall_scrollable = ScrollableButtonFrame(
            master=self,
            title='Uninstall',
            values=sorted(
                self.provisions_configs["provisions"]["packages_to_uninstall"]
            ),
            provisions_configs=self.provisions_configs
        )
        self.clean_uninstall_button = ctk.CTkButton(
            master=self,
            font=self.label_font,
            text='Clean',
            command=self._clean_uninstall_packages
        )
        self.config_scrollable = ScrollableButtonFrame(
            master=self,
            title='Config',
            values=sorted(
                self.provisions_configs["provisions"]["packages_to_config"]
            ),
            provisions_configs=self.provisions_configs
        )
        self.clean_config_button = ctk.CTkButton(
            master=self,
            font=self.label_font,
            text='Clean',
            command=self._clean_config_packages
        )

    def render_elements(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=0)
        self.install_scrollable.grid(
            row=0,
            column=0,
            padx=(3, 3),
            pady=self.pady_up,
            sticky=self.sticky_frame
        )
        self.uninstall_scrollable.grid(
            row=0,
            column=1,
            padx=(3, 3),
            pady=self.pady_up,
            sticky=self.sticky_frame
        )
        self.config_scrollable.grid(
            row=0,
            column=2,
            padx=(3, 3),
            pady=self.pady_up,
            sticky=self.sticky_frame
        )
        self.clean_install_button.grid(
            row=1,
            column=0,
            pady=self.pady_std,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        self.clean_uninstall_button.grid(
            row=1,
            column=1,
            pady=self.pady_std,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )
        self.clean_config_button.grid(
            row=1,
            column=2,
            pady=self.pady_std,
            ipadx=self.ipadx_button,
            ipady=self.ipady_button
        )

    def _clean_install_packages(self):
        self.provisions_configs["provisions"]["packages_to_install"] = set()
        self.install_scrollable.clean()

    def _clean_uninstall_packages(self):
        self.provisions_configs["provisions"]["packages_to_uninstall"] = set()
        self.uninstall_scrollable.clean()

    def _clean_config_packages(self):
        self.provisions_configs["provisions"]["packages_to_config"] = set()
        self.config_scrollable.clean()
