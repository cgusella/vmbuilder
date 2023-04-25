import abc
import os
import shutil
import json
from error import FlagError
from error import ExistenceProjectError
from error import ExistenceVirtualBoxError
from  helper import vmbuilder_path
from  helper import VAGRANT_FLAGS_TO_ERROR
from  helper import PACKER_FLAGS_TO_ERROR
from  helper import convert_argv_list_to_dict
from  helper import get_local_virtual_boxes
from  helper import replace_configs_in_file


def get_project_class():
    arguments = convert_argv_list_to_dict()
    project_type = arguments['-t']
    if project_type == 'vagrant':
        return Vagrant()
    if project_type == 'packer':
        return Packer()
    else:
        raise FlagError("Select from [packer|vagrant]")

class Builder(abc.ABC):

    @abc.abstractmethod
    def check_flags(self):
        pass

    @abc.abstractmethod
    def check_folder_vb_existence(self):
        pass

    @abc.abstractmethod
    def create_project_folder(self):
        pass

    @abc.abstractmethod
    def delete_project(self):
        pass


class Vagrant(Builder):
    def __init__(self) -> None:
        self.arguments: dict = convert_argv_list_to_dict()
        self.machine_path: str = vmbuilder_path + '/machines/vagrant'
        self.vbox_confs_provs = os.listdir(f'{vmbuilder_path}/templates/vagrant/vbox_confs_provs')
        self.configs: dict = dict()

    def check_flags(self):
        prompted_flags = set(self.arguments.keys())
        necessary_flags = set(VAGRANT_FLAGS_TO_ERROR.keys())
        forgotten_flags = set()

        # Check missing flags
        if not necessary_flags.issubset(prompted_flags):
            forgotten_flags = {
                flag for flag in necessary_flags if flag not in prompted_flags
            }

        # Check if some flags are written but without value
        for key in self.arguments:
            if not self.arguments[key]:
                forgotten_flags.add(key)

        if forgotten_flags:
            error_msg = '\n'
            for forgotten_flag in forgotten_flags:
                error_msg += f'\t\t{forgotten_flag}:\t{VAGRANT_FLAGS_TO_ERROR[forgotten_flag]}\n'
            raise FlagError(error_msg)

    def check_folder_vb_existence(self):
        if self.arguments['-n'] in os.listdir(self.machine_path):
            raise ExistenceProjectError("[ERROR] Project already exists!")
        if self.arguments['-vb'] in get_local_virtual_boxes():
            raise ExistenceVirtualBoxError(f'The virtualbox {self.arguments["-vb"]} already exists!')

    def set_configs(self):
        config_provision_file_path = f'{vmbuilder_path}/templates/vagrant/vbox_confs_provs/{self.arguments["-j"]}'
        with open(config_provision_file_path, 'r') as provisions:
            configs = json.loads(provisions.read())
        configs['extra_user'] = self.arguments['-u']
        configs['default_image'] = self.arguments['-i']
        configs['default_hostname'] = self.arguments['-ho']
        configs['default_vbname'] = self.arguments['-vb']
        configs['ssh_insert_key'] = False if self.arguments['-s'] == 'password' else True
        if configs['extra_user'] == configs['default_user']:
            raise FlagError('Default user in provision file is the same as inserted user!')
        self.configs = configs.copy()

    def create_project_folder(self):
        self.set_configs()
        project_folder = f'{self.machine_path}/{self.arguments["-n"]}'
        os.mkdir(project_folder)

        vagrant_folder = f'{vmbuilder_path}/templates/vagrant'
        shutil.copyfile(
            src=f'{vagrant_folder}/Vagrantfile',
            dst=f'{project_folder}/Vagrantfile'
        )
        for program in self.configs['programs']['install']:
            program_folder = f'{vmbuilder_path}/templates/programs/{program}'
            shutil.copytree(
                src=program_folder,
                dst=f'{project_folder}/{program}'
            )
        if self.configs['upload']:
            upload_folder = f'{project_folder}/upload'
            os.mkdir(upload_folder)

    def generate_provision_text(self, src, dst, title: str, program: str):
        hash_number = 55

        lines = src.readlines()
        # if file has only hash bang line, exit
        if len(lines) == 1 and lines[0].startswith('#!'):
            return
        # if file contains only empty lines after hash bang line, exit
        empty_lines = 0
        for line in lines:
            if line in ['\n']:
                # count empty lines
                empty_lines += 1
        # take hash bang line into consideration
        if len(lines) == empty_lines + 1:
            return

        dst.write(f'\n\n{hash_number*"#"}\n')
        pound_number = hash_number - 10 - len(title) - 1 - len(program) - 3 
        dst.write(f'#######   {title} {program}   {pound_number*"#"}')
        dst.write(f'\n{hash_number*"#"}\n')

        for line in lines:
            if line.startswith('#!'):
                continue
            else:
                dst.write(f'{line}')

    def provision(self):
        vagrantfile_path = f'{self.machine_path}/{self.arguments["-n"]}/Vagrantfile'
        custom_scripts_path = f'{vmbuilder_path}/templates/custom-scripts'
        programs_path = f'{vmbuilder_path}/templates/programs'
        init = self.configs['programs']['init']
        end = self.configs['programs']['end']
        programs_to_install = self.configs['programs']['install']
        programs_to_uninstall = self.configs['programs']['uninstall']
        custom_scripts = self.configs['custom-scripts']
        with open(vagrantfile_path, 'a') as vagrantfile:
            vagrantfile.write('\nconfig.vm.provision "shell", inline: <<-SHELL\n')
            if init:
                with open(f'{programs_path}/init.sh') as init_file:
                    self.generate_provision_text(
                            src=init_file,
                            dst=vagrantfile,
                            title="UPDATE and UPGRADE",
                            program='apt'
                        )
            if programs_to_install:
                for program in programs_to_install:
                    with open(f'{programs_path}/{program}/install.sh') as install_file:
                        self.generate_provision_text(
                            src=install_file,
                            dst=vagrantfile,
                            title="INSTALL",
                            program=program
                        )
                    with open(f'{programs_path}/{program}/configs/config.sh') as config_file:
                        self.generate_provision_text(
                            src=config_file,
                            dst=vagrantfile,
                            title="CONFIG",
                            program=program
                        )
            if programs_to_uninstall:
                for program in programs_to_uninstall:
                    with open(f'{programs_path}/{program}/uninstall.sh') as uninstall_file:
                        self.generate_provision_text(
                            src=uninstall_file,
                            dst=vagrantfile,
                            title="UNINSTALL",
                            program=program
                        )
            if end:
                with open(f'{programs_path}/clean.sh') as clean_file:
                    self.generate_provision_text(
                        src=clean_file,
                        dst=vagrantfile,
                        title="CLEAN apt packages",
                        program=''
                    )
            if custom_scripts:
                for script in custom_scripts:
                    with open(f'{custom_scripts_path}/{script}') as script_file:
                        self.generate_provision_text(
                            src=script_file,
                            dst=vagrantfile,
                            title="CUSTOM script",
                            program=f'{script.split(".")[0]}'
                        )
            vagrantfile.write('\n\nSHELL\nend')

        replace_configs_in_file(self.configs, vagrantfile_path)

    def delete_project(self):
        shutil.rmtree(f'{self.machine_path}/{self.arguments["-n"]}')


class Packer(Builder):
    def __init__(self) -> None:
        self.arguments: dict = convert_argv_list_to_dict()
        self.machine_path: str = vmbuilder_path + '/machines/packer'
        self.vbox_confs_provs = os.listdir(f'{vmbuilder_path}/templates/packer/provision_configs/')

    def check_flags(self):
        prompted_flags = set(self.arguments.keys())
        necessary_flags = set(PACKER_FLAGS_TO_ERROR.keys())
        forgotten_flags = set()

        # Check missing flags
        if not necessary_flags.issubset(prompted_flags):
            forgotten_flags = {
                flag for flag in necessary_flags if flag not in prompted_flags
            }

        # Check if some flags are written but without value
        for key in self.arguments:
            if not self.arguments[key]:
                forgotten_flags.add(key)

        if forgotten_flags:
            error_msg = '\n'
            for forgotten_flag in forgotten_flags:
                error_msg += f'\t\t{forgotten_flag}:\t{PACKER_FLAGS_TO_ERROR[forgotten_flag]}\n'
            raise FlagError(error_msg)

    def check_folder_vb_existence(self):
        if self.arguments['-n'] in os.listdir(self.machine_path):
            raise ExistenceProjectError("[ERROR] Project already exists!")

    def create_project_folder(self):
        configurations_folder = f'{vmbuilder_path}/configurations/'
        project_folder = f'{self.machine_path}/{self.arguments["-n"]}'
        os.mkdir(project_folder)
        shutil.copytree(src=configurations_folder, dst=f'{project_folder}/configurations')

        packer_folder = f'{vmbuilder_path}/packer'
        for element in os.listdir(packer_folder):
            element_path = f'{packer_folder}/{element}'
            if os.path.isdir(element_path):
                shutil.copytree(src=element_path, dst=f'{project_folder}/{element}')
            else:
                shutil.copy(src=element_path, dst=project_folder)

    def delete_project(self):
        shutil.rmtree(f'{self.machine_path}/{self.arguments["-n"]}')
