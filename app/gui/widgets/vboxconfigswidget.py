import customtkinter as ctk
from existencecontroller.controller import launch_vboxmanage_lst_command


class VboxConfigsWidget(ctk.CTkFrame):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        self.vbox_list = launch_vboxmanage_lst_command()
        ctk.CTkFrame.__init__(self, master)
        self.font_std = ctk.CTkFont(family='Sans', size=18)
        self.warning_font = ctk.CTkFont(family='Sans', size=11)
        self.padx_std = (20, 20)
        self.pady_std = (10, 10)
        self.pady_title = (10, 2)
        self.pady_entry = (2, 10)
        self.ipadx_std = 10
        self.ipady_std = 10
        self.entry_height_std = 50
        self.entry_width_std = 380
        self.sticky_title = 'wn'
        self.sticky_label = 'w'
        self.sticky_entry = 'w'
        self.sticky_frame = 'wens'

        # vbox name
        self.vbox_subframe = ctk.CTkFrame(
            self,
            height=150
        )
        self.vbox_subframe.grid(
            row=0,
            column=0,
            sticky=self.sticky_frame,
            padx=self.padx_std,
            pady=self.pady_std
        )
        self.vbox_subframe.grid_propagate(False)
        vbox_name_label = ctk.CTkLabel(
            master=self.vbox_subframe,
            text="Virtual box name:",
            font=self.font_std
        )
        vbox_name_label.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_title,
            sticky=self.sticky_label
        )
        self.entry_vbox_name = ctk.CTkEntry(
            master=self.vbox_subframe,
            font=self.font_std,
            width=self.entry_width_std,
            height=self.entry_height_std,
            placeholder_text='Virtualbox name to be created'
        )
        if self.provisions_configs["configurations"]['vbox_name']["default"]:
            self.entry_vbox_name.insert(
                0,
                self.provisions_configs["configurations"]['vbox_name']["default"]
            )
        self.entry_vbox_name.grid(
            row=1,
            column=0,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_entry
        )
        self.entry_vbox_name.bind("<Configure>", self._vbox_name_check)
        self.entry_vbox_name.bind("<KeyRelease>", self._vbox_name_check)
        self.warning_label_vbox = ctk.CTkLabel(
            master=self.vbox_subframe,
            font=self.warning_font,
            text_color='red',
            text=""
        )
        self.warning_label_vbox.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=0,
            sticky=self.sticky_label
        )
        if self.provisions_configs["configurations"]['vbox_name'] in self.vbox_list:
            self.warning_label_vbox.configure(
                text='A box with this name already exists',
            )

        # cpus subframe
        self.cpus_subframe = ctk.CTkFrame(self)
        self.cpus_subframe.grid(
            row=1,
            column=0,
            sticky=self.sticky_frame,
            padx=self.padx_std,
            pady=self.pady_std

        )
        cpus_label = ctk.CTkLabel(
            master=self.cpus_subframe,
            font=self.font_std,
            text='Specify CPUs number'
        )
        cpus_label.grid(
            row=0,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.cpus_value = ctk.IntVar()
        self.cpus_value.set(2)
        self.cpus_slider = ctk.CTkSlider(
            master=self.cpus_subframe,
            variable=self.cpus_value,
            from_=1,
            to=8,
            number_of_steps=7,
            width=self.entry_width_std,
            command=self._show_cpus_slider_value
        )
        self.cpus_slider.grid(
            row=1,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self._show_cpus_slider_value(self.cpus_slider.get())

        # add memory subframe
        self.memory_subframe = ctk.CTkFrame(self)
        self.memory_subframe.grid(
            row=3,
            column=0,
            sticky=self.sticky_frame,
            padx=self.padx_std,
            pady=self.pady_std
        )
        memory_label = ctk.CTkLabel(
            master=self.memory_subframe,
            font=self.font_std,
            text='Specify Memory in MB'
        )
        memory_label.grid(
            row=0,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.memory_var = ctk.IntVar()
        self.memory_var.set(8192)
        self.memory_slider = ctk.CTkSlider(
            master=self.memory_subframe,
            variable=self.memory_var,
            from_=2,
            to=16384,
            number_of_steps=8191,
            width=self.entry_width_std,
            command=self._show_memory_slider_value
        )
        self.memory_slider.grid(
            row=1,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self._show_memory_slider_value(self.memory_slider.get())

        self.combo_value_memory = ctk.CTkComboBox(
            master=self.memory_subframe,
            variable=self.memory_var,
            font=self.font_std,
            values=["2", "4", "8", "16", "32", "64", "128", "256", "512",
                    "1024", "2048", "4096", "8192", "16384"],
            command=self._show_memory_slider_value
        )
        self.combo_value_memory.grid(
            row=1,
            column=1,
            sticky=self.sticky_entry,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.combo_value_memory.bind(
            '<KeyRelease>',
            self._show_memory_value_with_keyrelease
        )

        # specify disk size
        self.disk_size_subframe = ctk.CTkFrame(self)
        self.disk_size_subframe.grid(
            row=4,
            column=0,
            sticky=self.sticky_frame,
            padx=self.padx_std,
            pady=self.pady_std
        )
        disk_label = ctk.CTkLabel(
            master=self.disk_size_subframe,
            font=self.font_std,
            text='Specify Disk Size in MB'
        )
        disk_label.grid(
            row=0,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.disk_slider_value = ctk.IntVar()
        self.disk_slider_value.set(30)
        self.disk_slider = ctk.CTkSlider(
            master=self.disk_size_subframe,
            variable=self.disk_slider_value,
            from_=4,
            to=2048,
            number_of_steps=2044,
            width=self.entry_width_std,
            command=self._show_disk_size_value
        )
        self.disk_slider.grid(
            row=1,
            column=0,
            sticky=self.sticky_label,
            padx=self.padx_std,
            pady=self.pady_title
        )
        self.disk_entry = ctk.CTkEntry(
            master=self.disk_size_subframe,
            font=self.font_std,
        )
        self.disk_entry.grid(
            row=1,
            column=1,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_entry
        )
        self._show_disk_size_value(self.disk_slider_value.get())
        self.disk_entry.bind(
            '<KeyRelease>',
            self._show_disk_size_value_with_keyrelease
        )
        self.disk_slider.bind(
            '<Button-1>',
            self._set_disk_size_entry
        )
        self.disk_slider.bind(
            '<Motion>',
            self._set_disk_size_entry
        )

    def _show_memory_slider_value(self, memory_value):
        self.slider_memory_label = ctk.CTkLabel(
            self.memory_subframe,
            text="",
            width=400
        )
        self.slider_memory_label.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std
        )
        if memory_value:
            self.slider_memory_label.configure(
                font=self.font_std,
                text=f'Selected Value: {int(self.memory_var.get())} MB'
            )

    def _show_memory_value_with_keyrelease(self, event):
        self._show_memory_slider_value(self.memory_var.get())

    def _show_disk_size_value(self, disk_value):
        self.disk_slider_label = ctk.CTkLabel(
            master=self.disk_size_subframe,
            text="",
            width=250
        )
        self.disk_slider_label.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std
        )
        if disk_value:
            value_text = f'{self.disk_slider_value.get()} MB'
            if self.disk_slider_value.get() >= 1024:
                disk_value = self.disk_slider_value.get() / 1_024
                value_text = f'{disk_value:.2f} GB'
            if disk_value >= 1024:
                disk_value = self.disk_slider_value.get() / 1_048_576
                value_text = f'{disk_value:.2f} TB'
            self.disk_slider_label.configure(
                font=self.font_std,
                text=f'Disk Size: {value_text}'
            )

    def _show_cpus_slider_value(self, cpus_value):
        self.cpus_slider_label = ctk.CTkLabel(
            master=self.cpus_subframe,
            text="",
            width=250
        )
        self.cpus_slider_label.grid(
            row=2,
            column=0,
            padx=self.padx_std,
            pady=self.pady_std
        )
        if cpus_value:
            self.cpus_slider_label.configure(
                font=self.font_std,
                text=f'CPUs Selected: {int(cpus_value)}'
            )

    def _set_disk_size_entry(self, event):
        self.disk_entry.delete(0, 100)
        self.disk_entry.insert(0, self.disk_slider_value.get())

    def _show_disk_size_value_with_keyrelease(self, event):
        self.disk_slider_value.set(int(self.disk_entry.get()))
        self._show_disk_size_value(int(self.disk_entry.get()))

    def _vbox_name_check(self, event):
        vbox_name_typed = self.entry_vbox_name.get()
        if vbox_name_typed not in self.vbox_list:
            self.entry_vbox_name.configure(border_color=["#979DA2", "#565B5E"])
            if self.warning_label_vbox.winfo_exists():
                self.warning_label_vbox.destroy()
        if vbox_name_typed in self.vbox_list:
            self.warning_label_vbox = ctk.CTkLabel(
                master=self.vbox_subframe,
                text='A box with this name already exists',
                text_color='red',
                font=self.warning_font
            )
            self.warning_label_vbox.grid(
                row=2,
                column=0,
                padx=self.padx_std,
                pady=0,
                sticky=self.sticky_label
            )
            self.entry_vbox_name.configure(border_color='red')
