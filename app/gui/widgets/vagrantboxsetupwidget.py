import customtkinter as ctk


class VagrantBoxSetUpWidget(ctk.CTkFrame):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        ctk.CTkFrame.__init__(self, master)

        # add hostname_label
        hostname_label = ctk.CTkLabel(
            master=self,
            text="Hostname:",
            font=self.master.font_std
        )

        self.hostname_entry = ctk.CTkEntry(
            master=self,
            font=self.master.font_std,
            width=self.master.entry_width_std,
            height=self.master.entry_height_std,
            placeholder_text='Hostname for the new VM'
        )
        if self.provisions_configs["configurations"]['hostname']["default"]:
            self.hostname_entry.insert(
                0,
                self.provisions_configs["configurations"]['hostname']["default"]
            )
        vagrant_box_label = ctk.CTkLabel(
            master=self,
            font=self.master.font_std,
            text='Select or Insert Vagrant Box'
        )

        self.vagrant_box = ctk.StringVar(self)
        self.vagrant_box.set(self.provisions_configs["configurations"]["image"]["default"])
        vagrant_drop = ctk.CTkComboBox(
            master=self,
            variable=self.vagrant_box,
            values=self.master.local_vagrant_boxes.split("\n"),
            font=self.master.font_std,
            width=self.master.entry_width_std,
            height=self.master.entry_height_std,
            dropdown_font=self.master.font_std,
        )

        username_label = ctk.CTkLabel(
            master=self,
            text="Username:",
            font=self.master.font_std
        )

        self.username_entry = ctk.CTkEntry(
            master=self,
            font=self.master.font_std,
            width=self.master.entry_width_std,
            height=self.master.entry_height_std,
            placeholder_text="Existing user on the vagrant box"
        )
        if self.provisions_configs["credentials"]['username']:
            self.username_entry.insert(
                0,
                self.provisions_configs["credentials"]['username']
            )

        password_label = ctk.CTkLabel(
            master=self,
            text="Password:",
            font=self.master.font_std
        )
        self.password_entry = ctk.CTkEntry(
            master=self,
            font=self.master.font_std,
            width=self.master.entry_width_std,
            height=self.master.entry_height_std,
            placeholder_text="Password of the previous user"
        )
        if self.provisions_configs["credentials"]['password']:
            self.password_entry.insert(
                0,
                self.provisions_configs["credentials"]['password']
            )

        extra_user_label = ctk.CTkLabel(
            master=self,
            text="Extra user:",
            font=self.master.font_std
        )

        self.extra_user_entry = ctk.CTkEntry(
            master=self,
            font=self.master.font_std,
            width=self.master.entry_width_std,
            height=self.master.entry_height_std,
            placeholder_text="An extra user to be created"
        )
        if self.provisions_configs["credentials"]['extra_user']:
            self.extra_user_entry.insert(
                0,
                self.provisions_configs["credentials"]['extra_user']
            )

        # render widget
        hostname_label.grid(
            row=0,
            column=0,
            padx=self.master.padx_std,
            pady=self.master.pady_title,
            sticky=self.master.sticky_label
        )
        self.hostname_entry.grid(
            row=1,
            column=0,
            padx=self.master.padx_std,
            pady=self.master.pady_entry,
            sticky=self.master.sticky_entry
        )
        vagrant_box_label.grid(
            row=2,
            column=0,
            padx=self.master.padx_std,
            pady=self.master.pady_title,
            sticky=self.master.sticky_label
        )
        vagrant_drop.grid(
            row=3,
            column=0,
            padx=self.master.padx_std,
            pady=self.master.pady_entry,
            sticky=self.master.sticky_entry
        )
        username_label.grid(
            row=4,
            column=0,
            padx=self.master.padx_std,
            pady=self.master.pady_title,
            sticky=self.master.sticky_label
        )
        self.username_entry.grid(
            row=5,
            column=0,
            padx=self.master.padx_std,
            pady=self.master.pady_entry,
            sticky=self.master.sticky_entry
        )
        password_label.grid(
            row=6,
            column=0,
            padx=self.master.padx_std,
            pady=self.master.pady_title,
            sticky=self.master.sticky_label
        )
        self.password_entry.grid(
            row=7,
            column=0,
            padx=self.master.padx_std,
            pady=self.master.pady_entry,
            sticky=self.master.sticky_entry
        )
        extra_user_label.grid(
            row=8,
            column=0,
            padx=self.master.padx_std,
            pady=self.master.pady_title,
            sticky=self.master.sticky_label
        )
        self.extra_user_entry.grid(
            row=9,
            column=0,
            padx=self.master.padx_std,
            pady=self.master.pady_entry,
            sticky=self.master.sticky_entry
        )
