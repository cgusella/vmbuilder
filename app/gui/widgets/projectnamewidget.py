import abc
import constants
import customtkinter as ctk
import os


class ProjectNameWidget(abc.ABC, ctk.CTkFrame):

    def __init__(self, master, provisions_configs):
        self.provisions_configs = provisions_configs
        ctk.CTkFrame.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.warning_font = ctk.CTkFont(family='Sans', size=11)
        self.font_std = ctk.CTkFont(family='Sans', size=18)

        self.padx_std = (20, 20)
        self.pady_std = (10, 10)
        self.pady_title = (10, 2)
        self.pady_entry = (2, 10)
        self.entry_height_std = 40
        self.sticky_label = 'w'
        self.sticky_horizontal = 'we'

        project_name_label = ctk.CTkLabel(
            master=self,
            text="New Project Name:",
            font=self.font_std
        )
        project_name_label.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_title,
            sticky=self.sticky_label
        )

        self.project_name_entry = ctk.CTkEntry(
            master=self,
            height=self.entry_height_std,
            font=self.font_std,
            placeholder_text='Project name to be created'
        )
        self.project_name_entry.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=self.pady_entry,
            sticky=self.sticky_horizontal
        )
        self.project_name_entry.bind("<Configure>", self._project_name_check)
        self.project_name_entry.bind("<KeyRelease>", self._project_name_check)

        self.warning_label_project = ctk.CTkLabel(
            master=self,
            font=self.warning_font
        )
        self.warning_label_project.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=self.padx_std,
            pady=0,
            sticky=self.sticky_label
        )
        self._set_project_name()

    @abc.abstractmethod
    def _set_project_name(self):
        pass

    @abc.abstractmethod
    def _project_name_check(self):
        pass


class PackerProjectNameWidget(ProjectNameWidget):

    def __init__(self, master, provisions_configs):
        self.project_name_widget = super()
        self.project_name_widget.__init__(
            master=master,
            provisions_configs=provisions_configs
        )

    def _set_project_name(self):
        if self.provisions_configs["configurations"]["project_name"]["default"]:
            self.project_name_entry.insert(
                0,
                self.provisions_configs["configurations"]["project_name"]["default"]
            )

    def _project_name_check(self, event):
        project_name_typed = self.project_name_entry.get()
        if project_name_typed not in os.listdir(f'{constants.PACKER_MACHINES_PATH}/'):
            self.project_name_entry.configure(border_color=["#979DA2", "#565B5E"])
            self.warning_label_project.configure(
                text=''
            )
        else:
            self.project_name_entry.configure(border_color='red')
            self.warning_label_project.configure(
                text='A project with this name already exists',
                text_color='red'
            )


class VagrantProjectNameWidget(ProjectNameWidget):

    def __init__(self, master, provisions_configs):
        self.project_name_widget = super()
        self.project_name_widget.__init__(
            master=master,
            provisions_configs=provisions_configs
        )

    def _set_project_name(self):
        if self.provisions_configs["configurations"]["project_name"]["default"]:
            self.project_name_entry.insert(
                0,
                self.provisions_configs["configurations"]["project_name"]["default"]
            )

    def _project_name_check(self, event):
        project_name_typed = self.project_name_entry.get()
        if project_name_typed not in os.listdir(f'{constants.VAGRANT_MACHINES_PATH}/'):
            self.project_name_entry.configure(border_color=["#979DA2", "#565B5E"])
            self.warning_label_project.configure(
                text=''
            )
        else:
            self.project_name_entry.configure(border_color='red')
            self.warning_label_project.configure(
                text='A project with this name already exists',
                text_color='red'
            )
        if project_name_typed.lower() == 'vagrant':
            self.project_name_entry.configure(border_color='red')
            self.warning_label_project.configure(
                text='The project name cannot be "vagrant"',
                text_color='red'
            )
