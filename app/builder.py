import abc
import os
import shutil
import json
from error import FlagError
from error import ExistenceProjectError
from error import ExistenceVirtualBoxError
from error import JsonConfigNotFoundError
from error import FileExtesionError
from helper import VAGRANT_FLAGS_TO_ERROR
from helper import PACKER_FLAGS_TO_ERROR
from helper import convert_argv_list_to_dict
from helper import get_local_virtual_boxes
from helper import replace_configs_in_vagrantfile
import constants


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
    def provision(self):
        pass

    @abc.abstractmethod
    def delete_project(self):
        pass


class Vagrant(Builder):
    def __init__(self) -> None:
        self.arguments: dict = convert_argv_list_to_dict()
        self.machine_path: str = constants.vagrant_machines_path
        self.provisions_configs = constants.vagrant_provs_confs_path
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
            provisions = json.loads(provisions.read())["vbox-provisions"]
        self.provisions = provisions.copy()

    def create_project_folder(self):
        self.set_provisions()
        project_folder = f'{self.machine_path}/{self.arguments["-n"]}'
        os.mkdir(project_folder)

        vagrant_folder = constants.vagrant_templates_path
        shutil.copyfile(
            src=f'{vagrant_folder}/Vagrantfile',
            dst=f'{project_folder}/Vagrantfile'
        )
        print(self.provisions)
        for program in self.provisions['programs']['install']:
            program_folder = f'{constants.programs_path}/{program}'
            shutil.copytree(
                src=program_folder,
                dst=f'{project_folder}/programs/{program}'
            )
        if self.provisions['upload']:
            shutil.copytree(
                src=f'{constants.upload_path}/',
                dst=f'{project_folder}/upload'
            )

    def _generate_provision_text(self, src, dst, title: str, program: str):
        hash_number = 55
        with open(src) as src_file:
            lines = src_file.readlines()

        for line in lines:
            if line in ['#!/bin/bash', '#!/bin/bash\n']:
                lines.remove(line)

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
        update_upgrade = self.provisions['programs']['update-upgrade']
        clean = self.provisions['programs']['clean']
        programs_to_install = self.provisions['programs']['install']
        programs_to_uninstall = self.provisions['programs']['uninstall']
        custom_scripts = self.provisions['custom-scripts']
        with open(vagrantfile_path, 'a') as vagrantfile:
            vagrantfile.write('\nconfig.vm.provision "shell", inline: <<-SHELL\n')
        if self.configs['extra_user']:
            self._generate_provision_text(
                    src=f'{constants.programs_path}/bash/create-extra-user.sh',
                    dst=vagrantfile_path,
                    title=f"CREATE USER {self.configs['extra_user']}",
                    program=''
                )
        if update_upgrade:
            self._generate_provision_text(
                    src=f'{constants.programs_path}/bash/update-upgrade.sh',
                    dst=vagrantfile_path,
                    title="UPDATE and UPGRADE",
                    program='apt'
                )
        if programs_to_install:
            for program in programs_to_install:
                self._generate_provision_text(
                    src=f'{constants.programs_path}/{program}/install.sh',
                    dst=vagrantfile_path,
                    title="INSTALL",
                    program=program
                )
                self._generate_provision_text(
                    src=f'{constants.programs_path}/{program}/configs/config.sh',
                    dst=vagrantfile_path,
                    title="CONFIG",
                    program=program
                )
        if programs_to_uninstall:
            for program in programs_to_uninstall:
                self._generate_provision_text(
                    src=f'{constants.programs_path}/{program}/uninstall.sh',
                    dst=vagrantfile_path,
                    title="UNINSTALL",
                    program=program
                )
        if clean:
            self._generate_provision_text(
                src=f'{constants.programs_path}/bash/clean.sh',
                dst=vagrantfile_path,
                title="CLEAN apt packages",
                program=''
            )
        if custom_scripts:
            for script in custom_scripts:
                self._generate_provision_text(
                    src=f'{constants.custom_scripts_path}/{script}',
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
        self.machine_path: str = constants.vmbuilder_path + '/machines/packer'
        self.provisions_configs = constants.packer_provs_confs_path
        self.configs: dict = dict()
        self.provisions: dict = dict()

    def set_configs(self):
        config_provision_file_path = f'{self.provisions_configs}/{self.arguments["-j"]}'
        with open(config_provision_file_path, 'r') as provisions:
            configs = json.loads(provisions.read())["vbox-configs"]
        configs['iso_file'] = self.arguments['-if']
        configs['iso_link'] = self.arguments['-il']
        configs['iso_checksum'] = self.arguments['-cs']
        configs['vb_name'] = self.arguments['-vb']
        self.configs = configs.copy()

    def set_provisions(self):
        config_provision_file_path = f'{self.provisions_configs}/{self.arguments["-j"]}'
        with open(config_provision_file_path, 'r') as provisions:
            self.provisions = json.loads(provisions.read())["vbox-provisions"].copy()

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
        project_folder = f'{self.machine_path}/{self.arguments["-n"]}'
        os.mkdir(project_folder)

        # packer_folder = f'{constants.vmbuilder_path}/templates/packer'
        # for element in os.listdir(packer_folder):
        #     element_path = f'{packer_folder}/{element}'
        #     if os.path.isdir(element_path):
        #         shutil.copytree(src=element_path, dst=f'{project_folder}/{element}')
        #     else:
        #         shutil.copy(src=element_path, dst=project_folder)
        print(self.provisions)
        if self.provisions['upload']:
            shutil.copytree(
                src=f'{constants.upload_path}/',
                dst=f'{project_folder}/upload'
            )

    def _generate_vars_file(self, json_file: dict):
        with open(f'{constants.packer_machines_path}/{self.arguments["-n"]}/vars.pkr.hcl', 'w') as vars_file:
            for var in json_file['vbox-configs']:
                if var in {'iso_file', 'iso_link', 'iso_checksum', 'vb_name'}:
                    json_file['vbox-configs'][var]["default"] = self.configs[var]
                if isinstance(json_file['vbox-configs'][var]["default"], str):
                    default_type = 'string'
                elif isinstance(json_file['vbox-configs'][var]["default"], bool):
                    default_type = 'bool'
                vars_file.write(
                    f'variable "{var}" ' + '{\n'
                    f'  description\t= "{json_file["vbox-configs"][var]["description"]}"\n'
                    f'  type\t= {default_type}\n'
                    f'  default\t= "{json_file["vbox-configs"][var]["default"]}"\n'
                    '}\n\n'
                )

    def provision(self):
        with open(f'{constants.packer_provs_confs_path}/{self.arguments["-j"]}') as provisions:
            json_provision = json.loads(provisions.read())
        self._generate_vars_file(json_provision)

    def delete_project(self):
        shutil.rmtree(f'{self.machine_path}/{self.arguments["-n"]}')
