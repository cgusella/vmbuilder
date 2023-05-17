import abc
import constants
import logging
import os
import shutil
import subprocess
from argparse import Namespace
from controller.errors import (
    ExistenceProjectError,
    ExistenceVirtualBoxError,
    FileExtesionError
)


def launch_vboxmanage_lst_command():
    """
    Return the virtual machine names list as string.
    """
    vmbox_list = subprocess.run(
        "VBoxManage list vms",
        shell=True,
        capture_output=True
    ).stdout.decode("ascii")
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
        if self.namespace.json not in os.listdir(constants.vagrant_provs_confs_path):
            shutil.copyfile(
                src=f'{constants.vagrant_provs_confs_path}/template.json',
                dst=f'{constants.vagrant_provs_confs_path}/{self.namespace.json}'
            )
            logging.warning(
                f'The json file "{self.namespace.json}" '
                f'is created at {constants.vagrant_provs_confs_path} folder.\n'
                'Fill it up and come back then!'
            )
            exit(0)

    def check_new_project_folder_existence(self):
        if self.namespace.name in os.listdir(constants.vagrant_machines_path):
            raise ExistenceProjectError("Project already exists!")


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
        if self.namespace.json not in os.listdir(constants.packer_provs_confs_path):
            shutil.copyfile(
                src=f'{constants.packer_provs_confs_path}/template.json',
                dst=f'{constants.packer_provs_confs_path}/{self.namespace.json}'
            )
            logging.warning(
                f'The json file "{self.namespace.json}" '
                f'is created at {constants.packer_provs_confs_path} folder.\n'
                'Fill it up and come back then!'
            )
            exit(0)

    def check_new_project_folder_existence(self):
        if self.namespace.name in os.listdir(constants.packer_machines_path):
            raise ExistenceProjectError("Project already exists!")
