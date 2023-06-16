import customtkinter as ctk


class IsoWidget(ctk.CTkFrame):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        ctk.CTkFrame.__init__(self, master)
        self.font_std = ctk.CTkFont(family='Sans', size=18)
        self.warning_font = ctk.CTkFont(family='Sans', size=11)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.padx_std = (20, 20)
        self.pady_title = (10, 2)
        self.pady_entry = (2, 10)
        self.entry_height_std = 50
        self.entry_width_std = 380
        self.sticky_label = 'w'
        self.sticky_entry = 'w'
        self.sticky_frame = 'wens'
        self.sticky_optionmenu = 'w'

        iso_link_label = ctk.CTkLabel(
            master=self,
            text='Insert Iso Link',
            font=self.font_std
        )
        iso_link_label.grid(
            row=0,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )

        self.iso_link_entry = ctk.CTkEntry(
            master=self,
            font=self.font_std,
            placeholder_text='Iso link'
        )
        if self.provisions_configs["configurations"]["iso_link"]["default"]:
            self.iso_link_entry.insert(
                0,
                self.provisions_configs["configurations"]["iso_link"]["default"]
            )
        self.iso_link_entry.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_frame
        )

        iso_file_label = ctk.CTkLabel(
            master=self,
            font=self.font_std,
            text='Insert Iso File'
        )
        iso_file_label.grid(
            row=0,
            column=2,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.iso_file_entry = ctk.CTkEntry(
            master=self,
            font=self.font_std,
            placeholder_text='Iso File'
        )
        if self.provisions_configs["configurations"]["iso_file"]["default"]:
            self.iso_file_entry.insert(
                0,
                self.provisions_configs["configurations"]["iso_file"]["default"]
            )
        self.iso_file_entry.grid(
            row=1,
            column=2,
            sticky=self.sticky_frame,
            padx=self.padx_std,
            pady=self.pady_entry
        )

        # add iso_checksum subframe
        self.iso_checksum_subframe = ctk.CTkFrame(
            master=self,
            fg_color='transparent'
        )
        self.iso_checksum_subframe.columnconfigure(0, weight=0)
        self.iso_checksum_subframe.columnconfigure(1, weight=1)
        self.iso_checksum_subframe.rowconfigure(0, weight=0)
        self.iso_checksum_subframe.rowconfigure(1, weight=1)
        self.iso_checksum_subframe.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky=self.sticky_frame
        )
        algorithm_label = ctk.CTkLabel(
            master=self.iso_checksum_subframe,
            text='Algorithm',
            font=self.font_std
        )
        algorithm_label.grid(
            row=0,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.iso_checksum_algorithm = ctk.CTkOptionMenu(
            master=self.iso_checksum_subframe,
            font=self.font_std,
            values=['SHA-1', 'SHA-224', 'SHA-256', 'SHA-384', 'SHA-512', 'MD5']
        )
        self.iso_checksum_algorithm.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_optionmenu
        )
        iso_checksum_label = ctk.CTkLabel(
            master=self.iso_checksum_subframe,
            text='Insert Checksum',
            font=self.font_std
        )
        iso_checksum_label.grid(
            row=0,
            column=1,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.iso_checksum_entry = ctk.CTkEntry(
            master=self.iso_checksum_subframe,
            font=self.font_std,
            placeholder_text='Checksum'
        )
        self.iso_checksum_entry.grid(
            row=1,
            column=1,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_frame
        )
        if self.provisions_configs["configurations"]["iso_checksum"]["default"]:
            self.iso_checksum_algorithm.set(
                self.provisions_configs["configurations"]["iso_checksum"]["default"].split(':')[0]
            )
            self.iso_checksum_entry.insert(
                0,
                self.provisions_configs["configurations"]["iso_checksum"]["default"].split(':')[1]
            )
