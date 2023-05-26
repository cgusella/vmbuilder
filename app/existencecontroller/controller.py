import abc
import constants
import logging
import json
import os
import shutil
import subprocess
from argparse import Namespace
from existencecontroller.errors import (
    ExistenceProjectError,
    ExistenceVirtualBoxError,
    FileExtesionError
)


def launch_vboxmanage_lst_command():
    """
    Return the virtual machine names list as string.
    """
    result = subprocess.run(
        "VBoxManage list vms",
        shell=True,
        capture_output=True
    ).stdout.decode("ascii")
    lines_list = result.split('\n')
    vmbox_list = [vmbox.split('"')[1] for vmbox in lines_list if vmbox]
    return vmbox_list


class Controller(abc.ABC):

    @abc.abstractmethod
    def check_virtualbox_existence(self):
        pass

    @abc.abstractmethod
    def check_json_existence(self):
        pass

    @abc.abstractmethod
    def check_new_project_folder_existence(self):
        pass

    @abc.abstractmethod
    def get_json_with_flags_values(self):
        pass


class VagrantController(Controller):

    def __init__(self, namespace: Namespace):
        self.namespace = namespace

    def check_virtualbox_existence(self):
        vmbox_list = launch_vboxmanage_lst_command()
        if self.namespace.vm_name in vmbox_list:
            raise ExistenceVirtualBoxError(
                f'The virtualbox {self.namespace.vm_name} already exists!'
            )

    def check_json_existence(self):
        if not self.namespace.json.endswith(".json"):
            raise FileExtesionError('You selected inappropriate JSON file')
        if self.namespace.json not in os.listdir(constants.VAGRANT_PROVS_CONFS_PATH):
            shutil.copyfile(
                src=f'{constants.VAGRANT_PROVS_CONFS_PATH}/template.json',
                dst=f'{constants.VAGRANT_PROVS_CONFS_PATH}/{self.namespace.json}'
            )
            logging.warning(
                f'The json file "{self.namespace.json}" '
                f'is created at {constants.VAGRANT_PROVS_CONFS_PATH} folder.\n'
                'Fill it up and come back then!'
            )
            exit(0)

    def check_new_project_folder_existence(self):
        if self.namespace.name in os.listdir(constants.VAGRANT_MACHINES_PATH):
            raise ExistenceProjectError("Project already exists!")

    def get_json_with_flags_values(self):
        """Set variables in JSON with correspondant namespace values"""
        with open(f'{constants.VAGRANT_PROVS_CONFS_PATH}/template.json', 'w') as json_file:
            self.json_file = json.loads(json_file.read())
        self.json_file["configurations"]["machine_name"] = self.namespace.name
        self.json_file["configurations"]["vbox_name"] = self.namespace.vm_name
        self.json_file["configurations"]["username"] = self.namespace.user
        self.json_file["configurations"]["hostname"] = self.namespace.hostname
        self.json_file["configurations"]["image"] = self.namespace.image
        self.json_file["configurations"]["connection"] = self.namespace.connection
        with open(f'{constants.VAGRANT_PROVS_CONFS_PATH}/{self.namespace.json}') as json_file:
            json_file.write(json.dumps(self.json_file, indent=2))
        return json_file


class PackerController(Controller):

    def __init__(self, namespace: Namespace):
        self.namespace = namespace

    def check_virtualbox_existence(self):
        vmbox_list = launch_vboxmanage_lst_command()
        if self.namespace.vm_name in vmbox_list:
            raise ExistenceVirtualBoxError(
                f'The virtualbox {self.namespace.vm_name} already exists!'
            )

    def check_json_existence(self):
        if not self.namespace.json.endswith(".json"):
            raise FileExtesionError('You selected inappropriate JSON file')
        if self.namespace.json not in os.listdir(constants.PACKER_PROVS_CONFS_PATH):
            shutil.copyfile(
                src=f'{constants.PACKER_PROVS_CONFS_PATH}/template.json',
                dst=f'{constants.PACKER_PROVS_CONFS_PATH}/{self.namespace.json}'
            )
            logging.warning(
                f'The json file "{self.namespace.json}" '
                f'is created at {constants.PACKER_PROVS_CONFS_PATH} folder.\n'
                'Fill it up and come back then!'
            )
            exit(0)

    def check_new_project_folder_existence(self):
        if self.namespace.name in os.listdir(constants.PACKER_MACHINES_PATH):
            raise ExistenceProjectError("Project already exists!")

    def get_json_with_flags_values(self):
        """Set variables in JSON with correspondant namespace values"""
        with open(f'{constants.PACKER_PROVS_CONFS_PATH}/template.json', 'w') as json_file:
            self.json_file = json.loads(json_file.read())
