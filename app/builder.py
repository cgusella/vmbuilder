import abc
import os
import shutil
import json
from error import FlagError
from error import ExistenceProjectError
from error import ExistenceVirtualBoxError
from error import JsonConfigNotFoundError
from error import FileExtesionError
from error import EmptyScriptError
from helper import VAGRANT_FLAGS_TO_ERROR
from helper import PACKER_FLAGS_TO_ERROR
from helper import convert_argv_list_to_dict
from helper import get_local_virtual_boxes
from helper import replace_configs_in_vagrantfile

vmbuilder_path = f'{os.path.dirname(os.path.realpath(__file__))}/..'


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
    def check_folder_vb_json_existence(self):
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
        self.provisions_configs = f'{vmbuilder_path}/templates/vagrant/provisions_configs'
        self.configs: dict = dict()
        self.provisions: dict = dict()

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

        if not self.arguments['-j'].endswith('.json'):
            raise FileExtesionError(f'The config file {self.arguments["-j"]} is not a JSON file!')

    def check_folder_vb_json_existence(self):
        if self.arguments['-n'] in os.listdir(self.machine_path):
            raise ExistenceProjectError("[ERROR] Project already exists!")
        if self.arguments['-vb'] in get_local_virtual_boxes():
            raise ExistenceVirtualBoxError(f'The virtualbox {self.arguments["-vb"]} already exists!')
        if self.arguments['-j'] not in os.listdir(self.provisions_configs):
            shutil.copyfile(
                src=f'{self.provisions_configs}/template.json',
                dst=f'{self.provisions_configs}/{self.arguments["-j"]}'
            )
            raise JsonConfigNotFoundError(
                f'The json file {self.arguments["-j"]} '
                'is created at /templates/vagrant/provisions_configs folder.\n'
                'Fill it up and come back then!'
            )

    def set_configs(self):
        config_provision_file_path = f'{self.provisions_configs}/{self.arguments["-j"]}'
        with open(config_provision_file_path, 'r') as provisions:
            configs = json.loads(provisions.read())["vbox-configs"]
        configs['extra_user'] = self.arguments['-u']
        configs['default_image'] = self.arguments['-i']
        configs['default_hostname'] = self.arguments['-ho']
        configs['default_vbname'] = self.arguments['-vb']
        configs['ssh_insert_key'] = False if self.arguments['-s'] == 'password' else True
        if configs['extra_user'] == configs['default_user']:
            raise FlagError('Default user in provision file is the same as inserted user!')
        self.configs = configs.copy()

    def set_provisions(self):
        config_provision_file_path = f'{self.provisions_configs}/{self.arguments["-j"]}'
        with open(config_provision_file_path, 'r') as provisions:
            self.provisions = json.loads(provisions.read())["vbox-provisions"]

    def create_project_folder(self):
        self.set_configs()
        self.set_provisions()
        project_folder = f'{self.machine_path}/{self.arguments["-n"]}'
        os.mkdir(project_folder)

        vagrant_folder = f'{vmbuilder_path}/templates/vagrant'
        shutil.copyfile(
            src=f'{vagrant_folder}/Vagrantfile',
            dst=f'{project_folder}/Vagrantfile'
        )
        for program in self.provisions['programs']['install']:
            program_folder = f'{vmbuilder_path}/templates/programs/{program}'
            shutil.copytree(
                src=program_folder,
                dst=f'{project_folder}/programs/{program}'
            )
        if self.provisions['upload']:
            shutil.copytree(
                src=f'{vmbuilder_path}/templates/upload/',
                dst=f'{project_folder}/upload'
            )

    def generate_provision_text(self, src, dst, title: str, program: str):
        hash_number = 55
        with open(src) as src_file:
            lines = set(src_file.readlines())

        lines = lines.difference(set(['#!/bin/bash', '#!/bin/bash\n']))
        empty_file = not any(lines)

        if title.lower() in ['config'] and empty_file:
            pass
        else:
            with open(dst, 'a') as vagrantfile:
                vagrantfile.write(f'\n\n{hash_number*"#"}\n')
                pound_number = hash_number - 10 - len(title) - 1 - len(program) - 3
                vagrantfile.write(f'#######   {title} {program}   {pound_number*"#"}')
                vagrantfile.write(f'\n{hash_number*"#"}\n')

                for line in lines:
                    vagrantfile.write(f'{line.strip()}\n')

    def provision(self):
        vagrantfile_path = f'{self.machine_path}/{self.arguments["-n"]}/Vagrantfile'
        custom_scripts_path = f'{vmbuilder_path}/templates/custom-scripts'
        programs_path = f'{vmbuilder_path}/templates/programs'
        update_upgrade = self.provisions['programs']['update-upgrade']
        clean = self.provisions['programs']['clean']
        programs_to_install = self.provisions['programs']['install']
        programs_to_uninstall = self.provisions['programs']['uninstall']
        custom_scripts = self.provisions['custom-scripts']
        with open(vagrantfile_path, 'a') as vagrantfile:
            vagrantfile.write('\nconfig.vm.provision "shell", inline: <<-SHELL\n')
        if self.configs['extra_user']:
            self.generate_provision_text(
                    src=f'{programs_path}/bash/create-extra-user.sh',
                    dst=vagrantfile_path,
                    title=f"CREATE USER {self.configs['extra_user']}",
                    program=''
                )
        if update_upgrade:
            self.generate_provision_text(
                    src=f'{programs_path}/bash/update-upgrade.sh',
                    dst=vagrantfile_path,
                    title="UPDATE and UPGRADE",
                    program='apt'
                )
        if programs_to_install:
            for program in programs_to_install:
                self.generate_provision_text(
                    src=f'{programs_path}/{program}/install.sh',
                    dst=vagrantfile_path,
                    title="INSTALL",
                    program=program
                )
                self.generate_provision_text(
                    src=f'{programs_path}/{program}/configs/config.sh',
                    dst=vagrantfile_path,
                    title="CONFIG",
                    program=program
                )
        if programs_to_uninstall:
            for program in programs_to_uninstall:
                self.generate_provision_text(
                    src=f'{programs_path}/{program}/uninstall.sh',
                    dst=vagrantfile_path,
                    title="UNINSTALL",
                    program=program
                )
        if clean:
            self.generate_provision_text(
                src=f'{programs_path}/bash/clean.sh',
                dst=vagrantfile_path,
                title="CLEAN apt packages",
                program=''
            )
        if custom_scripts:
            for script in custom_scripts:
                self.generate_provision_text(
                    src=f'{custom_scripts_path}/{script}',
                    dst=vagrantfile_path,
                    title="CUSTOM SCRIPT",
                    program=f'{script.split(".")[0]}'
                )

        with open(vagrantfile_path, 'a') as vagrantfile:
            vagrantfile.write('\n\nSHELL\nend')

        replace_configs_in_vagrantfile(self.configs, vagrantfile_path)

    def delete_project(self):
        shutil.rmtree(f'{self.machine_path}/{self.arguments["-n"]}')


class Packer(Builder):
    def __init__(self) -> None:
        self.arguments: dict = convert_argv_list_to_dict()
        self.machine_path: str = vmbuilder_path + '/machines/packer'
        self.provisions_configs = os.listdir(f'{vmbuilder_path}/templates/packer/provision_configs/')

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

    def check_folder_vb_json_existence(self):
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
