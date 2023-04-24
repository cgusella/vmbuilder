#!/usr/bin/python3
import customtkinter
from builder import get_local_vagrant_boxes
import os
import tkinter

dir_path = os.path.dirname(os.path.realpath(__file__))


class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("vagrant")
        self.add("packer")

        # add widgets on vagrant tab
        self.config_label = customtkinter.CTkLabel(
            master=self.tab("vagrant"),
            text='Step 1: Configure'
        )
        self.config_label.grid(row=0, column=0, padx=20, pady=10)

        self.project_name = customtkinter.CTkEntry(
            master=self.tab("vagrant"),
            placeholder_text="Project Name",
            width=240
        )
        self.project_name.grid(row=1, column=0, padx=20, pady=10)

        self.box_name = customtkinter.CTkEntry(
            master=self.tab("vagrant"),
            placeholder_text="Box Name",
            width=240
        )
        self.box_name.grid(row=2, column=0, padx=20, pady=10)

        self.hostname = customtkinter.CTkEntry(
            master=self.tab("vagrant"),
            placeholder_text="Hostname",
            width=240
        )
        self.hostname.grid(row=3, column=0, padx=20, pady=10)

        self.vagrant_boxes = customtkinter.CTkComboBox(
            master=self.tab("vagrant"),
            values=get_local_vagrant_boxes(),
            width=240
        )
        self.vagrant_boxes.grid(row=4, column=0, padx=20, pady=10)

        self.vagrant_provision_configs = customtkinter.CTkComboBox(
            master=self.tab("vagrant"),
            values=os.listdir(
                f'{dir_path}/../templates/vagrant/provision_configs/'
            ),
            width=240
        )
        self.vagrant_provision_configs.grid(row=5, column=0, padx=20, pady=10)

        self.ssh_frame = customtkinter.CTkFrame(self.tab("vagrant"))
        self.ssh_frame.grid(row=6, column=0, padx=(20, 20), pady=(20, 0),
                            sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_ssh_group = customtkinter.CTkLabel(master=self.ssh_frame,
                                                      text="SSH Connection")
        self.label_ssh_group.grid(row=0, column=2, columnspan=1, padx=10,
                                  pady=10, sticky="")
        self.pass_radio_button = customtkinter.CTkRadioButton(
            master=self.ssh_frame,
            variable=self.radio_var,
            value=0,
            text='password'
        )
        self.pass_radio_button.grid(row=1, column=2, pady=10, padx=20,
                                    sticky="n")
        self.key_radio_button = customtkinter.CTkRadioButton(
            master=self.ssh_frame,
            variable=self.radio_var,
            value=1,
            text='key'
        )
        self.key_radio_button.grid(row=2, column=2, pady=10, padx=20,
                                   sticky="n")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('vboxcreator')
        self.geometry("1040x620")
        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)
        self.tab_view.configure(width=1000, height=500)
        self.button_to_provision = customtkinter.CTkButton(
            master=self,
            text="Next",
            command=self.provision
        )
        self.button_to_provision.place(relx=0.5, rely=0.95, anchor=tkinter.S)

    def provision(self):
        self.title('vboxcreator')
        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)
        self.tab_view.configure(width=1000, height=500)
        self.register_btn = customtkinter.CTkButton(
            master=self,
            text="Exit",
            command=exit
        )
        self.register_btn.place(relx=0.5, rely=0.95, anchor=tkinter.S)


if __name__ == '__main__':
    app = App()
    app.mainloop()
