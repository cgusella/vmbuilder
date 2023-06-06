import constants
import customtkinter as ctk
import os
from gui.views.utilsview import ScrollableCheckboxFrame
from PIL import Image


class MenuWidget(ctk.CTkFrame):

    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, *args, **kwargs)
        family_font = 'Sans'
        title_font = ctk.CTkFont(family=family_font, size=20)
        label_font = ctk.CTkFont(family=family_font, size=16)
        ipadx = 10
        ipady = 10
        padx_std = (10, 10)
        pady_std = (10, 10)
        ipadx_button = 5
        ipady_button = 5
        width_button_std = 100
        pad_left = (10, 5)
        pad_right = (5, 10)
        pad_five = (5, 5)
        padx_btn_left = (5, 0)
        sticky_frame = 'wens'

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        # add menu title
        project_title = ctk.CTkLabel(
            master=self,
            text='Projects',
            font=title_font
        )
        project_title.grid(
            row=0,
            column=0,
            padx=padx_std,
            pady=pady_std,
            ipadx=ipadx,
            ipady=ipady
        )

        # add packer frame to menu
        packer_menu_frame = ctk.CTkFrame(self)
        packer_menu_frame.rowconfigure(0, weight=1)
        packer_menu_frame.rowconfigure(1, weight=1)
        packer_menu_frame.rowconfigure(2, weight=1)

        packer_menu_frame.grid(
            row=1,
            column=0,
            rowspan=2,
            padx=padx_std,
            pady=pad_left,
            sticky=sticky_frame
        )

        self.packer_projects = ScrollableCheckboxFrame(
            master=packer_menu_frame,
            title='Packer Projects',
            values=sorted([
                folder for folder in os.listdir(
                    f'{constants.PACKER_MACHINES_PATH}'
                )
                if os.path.isdir(f'{constants.PACKER_MACHINES_PATH}/{folder}')
            ])
        )
        self.packer_projects.grid(
            row=0,
            column=0,
            columnspan=4,
            rowspan=2,
            padx=padx_std,
            pady=pad_five,
            sticky=sticky_frame
        )

        plus_icon = ctk.CTkImage(
            light_image=Image.open(f'{constants.IMAGES_PATH}/plus_light.png'),
            dark_image=Image.open(f'{constants.IMAGES_PATH}/plus_dark.png'),
            size=(40, 40)
        )
        remove_icon = ctk.CTkImage(
            light_image=Image.open(f'{constants.IMAGES_PATH}/remove_light.png'),
            dark_image=Image.open(f'{constants.IMAGES_PATH}/remove_dark.png'),
            size=(40, 40)
        )

        add_packer_button = ctk.CTkButton(
            master=packer_menu_frame,
            text='',
            image=plus_icon,
            width=10,
            height=10,
            fg_color=['grey86', 'grey17'],
            hover_color=['grey76', 'grey7'],
            command=self.master.add_packer_configs
        )
        add_packer_button.grid(
            row=2,
            column=0,
            padx=padx_btn_left,
            pady=pad_right,
            ipadx=0,
            ipady=0,
        )

        packer_delete_button = ctk.CTkButton(
            master=packer_menu_frame,
            text='',
            image=remove_icon,
            width=10,
            height=10,
            fg_color=['grey86', 'grey17'],
            hover_color=['grey76', 'grey7'],
            command=lambda: self.master._delete_projects('packer')
        )
        packer_delete_button.grid(
            row=2,
            column=1,
            padx=padx_btn_left,
            pady=pad_right,
            ipadx=0,
            ipady=0,
        )

        packer_load_button = ctk.CTkButton(
            master=packer_menu_frame,
            text='Load',
            font=label_font,
            width=width_button_std,
            command=self.master._load_packer
        )
        packer_load_button.grid(
            row=2,
            column=2,
            padx=padx_std,
            pady=pad_right,
            ipadx=ipadx_button,
            ipady=ipady_button,
        )

        packer_build_button = ctk.CTkButton(
            master=packer_menu_frame,
            text='Build',
            font=label_font,
            width=width_button_std,
            command=self.master._build
        )
        packer_build_button.grid(
            row=2,
            column=3,
            padx=padx_std,
            pady=pad_right,
            ipadx=ipadx_button,
            ipady=ipady_button,
        )

        # add vagrant frame to menu
        vagrant_menu_frame = ctk.CTkFrame(self)

        vagrant_menu_frame.rowconfigure(0, weight=1)
        vagrant_menu_frame.rowconfigure(1, weight=1)
        vagrant_menu_frame.rowconfigure(2, weight=1)

        vagrant_menu_frame.grid(
            row=3,
            column=0,
            rowspan=2,
            padx=padx_std,
            pady=pad_left,
            sticky=sticky_frame
        )

        self.vagrant_projects = ScrollableCheckboxFrame(
            master=vagrant_menu_frame,
            title='Vagrant Projects',
            values=sorted([
                folder for folder in os.listdir(
                    f'{constants.VAGRANT_MACHINES_PATH}'
                )
                if os.path.isdir(f'{constants.VAGRANT_MACHINES_PATH}/{folder}')
            ])
        )
        self.vagrant_projects.grid(
            row=0,
            column=0,
            rowspan=2,
            columnspan=4,
            padx=padx_std,
            pady=pad_five,
            sticky=sticky_frame
        )

        add_vagrant_button = ctk.CTkButton(
            master=vagrant_menu_frame,
            text='',
            command=self.master.add_vagrant_configs,
            font=label_font,
            image=plus_icon,
            width=10,
            height=10,
            fg_color=['grey86', 'grey17'],
            hover_color=['grey76', 'grey7']
        )
        add_vagrant_button.grid(
            row=2,
            column=0,
            padx=padx_btn_left,
            pady=pad_right,
            ipadx=0,
            ipady=0
        )

        delete_vagrant_button = ctk.CTkButton(
            master=vagrant_menu_frame,
            text='',
            image=remove_icon,
            width=10,
            height=10,
            fg_color=['grey86', 'grey17'],
            hover_color=['grey76', 'grey7'],
            command=lambda: self.master._delete_projects('vagrant')
        )
        delete_vagrant_button.grid(
            row=2,
            column=1,
            padx=padx_btn_left,
            pady=pad_right,
            ipadx=0,
            ipady=0
        )

        load_vagrant_button = ctk.CTkButton(
            master=vagrant_menu_frame,
            text='Load',
            font=label_font,
            width=width_button_std,
            command=self.master._load_vagrant
        )
        load_vagrant_button.grid(
            row=2,
            column=2,
            padx=padx_std,
            pady=pad_right,
            ipadx=ipadx_button,
            ipady=ipady_button
        )

        vagrant_up_button = ctk.CTkButton(
            master=vagrant_menu_frame,
            text='Up',
            font=label_font,
            width=width_button_std,
            command=self.master._up
        )
        vagrant_up_button.grid(
            row=2,
            column=3,
            padx=padx_std,
            pady=pad_right,
            ipadx=ipadx_button,
            ipady=ipady_button
        )

        self.off_on_switch_frame = ctk.CTkFrame(
            master=self,
            width=50,
            fg_color='transparent'
        )

        self.off_on_switch_frame.grid(
            row=5,
            column=0,
            padx=padx_std,
            pady=0
        )

        off_title = ctk.CTkLabel(
            master=self.off_on_switch_frame,
            text='OFF',
            font=ctk.CTkFont(family=family_font, size=14)
        )
        off_title.grid(
            row=0,
            column=0,
            padx=(10, 0),
            pady=(5, 5),
            ipadx=0,
            ipady=0,
            sticky='e'
        )

        # add switch light/dark mode
        self.switch_var = ctk.StringVar(value="on")
        swith_light_dark_mode = ctk.CTkSwitch(
            master=self.off_on_switch_frame,
            text='ON',
            font=ctk.CTkFont(family=family_font, size=14),
            variable=self.switch_var,
            onvalue='on',
            offvalue='off',
            command=self._swith_light_dark_mode
        )
        swith_light_dark_mode.grid(
            row=0,
            column=1,
            padx=(0, 10),
            pady=(5, 5),
            ipadx=0,
            ipady=0,
            sticky='w'
        )

    def _swith_light_dark_mode(self):
        if self.switch_var.get() == 'on':
            ctk.set_appearance_mode('light')
        elif self.switch_var.get() == 'off':
            ctk.set_appearance_mode('dark')
