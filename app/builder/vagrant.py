import constants
import json
import os
import shutil
from builder.builder import Builder
from error import (
    FlagError,
    ExistenceProjectError,
    ExistenceVirtualBoxError,
    JsonConfigCopiedError,
    FileExtesionError,
    NoFileToUploadError
)
from helper import (
    convert_argv_list_to_dict,
    get_local_virtual_boxes,
    get_programs_upload_files,
    is_empty_script,
    VAGRANT_FLAGS_TO_ERROR,
)
from typing import List


class Vagrant(Builder):
    def __init__(self) -> None:
        self.arguments: dict = convert_argv_list_to_dict()
        self.machine_path: str = constants.vagrant_machines_path
        self.provisions_configs = constants.vagrant_provs_confs_path
        self.vagrantfile_path = f'{self.machine_path}/{self.arguments["-n"]}/Vagrantfile'
        self.configs: dict = dict()
        self.provisions: dict = dict()
        self.credentials: dict = dict()

    def check_flags(self):
        prompted_flags = set(self.arguments.keys())
        optional_flags = {'-u'}
        necessary_flags = set(VAGRANT_FLAGS_TO_ERROR.keys()).difference(optional_flags)
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
                error_msg += (
                    f'\t\t{forgotten_flag}:\t'
                    f'{VAGRANT_FLAGS_TO_ERROR[forgotten_flag]}\n'
                )
            raise FlagError(error_msg)

        if not self.arguments['-j'].endswith('.json'):
            raise FileExtesionError(
                f'The config file {self.arguments["-j"]} is not a JSON file!'
            )

    def check_new_project_folder_existence(self):
        if self.arguments['-n'] in os.listdir(self.machine_path):
            raise ExistenceProjectError("[ERROR] Project already exists!")

    def check_virtualbox_existence(self):
        if self.arguments['-vm'] in get_local_virtual_boxes():
            raise ExistenceVirtualBoxError(
                f'The virtualbox {self.arguments["-vm"]} already exists!'
            )

    def check_provision_cfg_json_existence(self):
        if self.arguments['-j'] not in os.listdir(self.provisions_configs):
            shutil.copyfile(
                src=f'{self.provisions_configs}/template.json',
                dst=f'{self.provisions_configs}/{self.arguments["-j"]}'
            )
            raise JsonConfigCopiedError(
                f'The json file "{self.arguments["-j"]}" '
                f'is created at {constants.vagrant_provs_confs_path} folder.\n'
                'Fill it up and come back then!'
            )

    def set_configs(self):
        config_provision_file_path = f'{self.provisions_configs}/{self.arguments["-j"]}'
        with open(config_provision_file_path, 'r') as template_json:
            configs = json.loads(template_json.read())["virtual_machine_configs"]
        self.configs = configs.copy()

    def set_provisions(self):
        config_provision_file_path = f'{self.provisions_configs}/{self.arguments["-j"]}'
        with open(config_provision_file_path, 'r') as template_json:
            provisions = json.loads(template_json.read())["provisions"]
        self.provisions = provisions.copy()

    def set_credentials(self):
        config_provision_file_path = f'{self.provisions_configs}/{self.arguments["-j"]}'
        with open(config_provision_file_path, 'r') as template_json:
            credentials = json.loads(template_json.read())["credentials"]
        self.credentials = credentials.copy()

    def create_project_folder(self):
        """
        Create project folder with this structure:
        - project_name/
            |
            - upload/
        """
        project_folder = f'{self.machine_path}/{self.arguments["-n"]}'
        # create project folder
        os.mkdir(project_folder)

        # create upload folder
        os.mkdir(f'{project_folder}/upload')

    def _generate_provision_section(self, src, title: str, program: str):
        """
        Generate provision section in Vagrantfile.
        It titles section as follow
            #######################################################
            #######   OPERATION program   #########################
            #######################################################
        """
        hash_number = 55
        with open(src, 'r') as source_file:
            lines = source_file.readlines()

        if title.lower() in ['config'] and is_empty_script(src):
            pass
        else:
            with open(
                f'{self.machine_path}/{self.arguments["-n"]}/Vagrantfile',
                'a'
            ) as vagrantfile:
                vagrantfile.write(f'\n\n\t{hash_number*"#"}\n')
                pound_number = hash_number - 10 - len(title) - 1 - len(program) - 3
                vagrantfile.write(f'\t#######   {title} {program}   {pound_number*"#"}')
                vagrantfile.write(f'\n\t{hash_number*"#"}\n')

                for line in lines:
                    if line in ['#!/bin/bash', '#!/bin/bash\n']:
                        continue
                    vagrantfile.write(f'\t{line.strip()}\n')

    def _copy_configurations_to_upload(self, programs: List[str]):
        """
        Find needed files from config.sh script and copy them into project
        upload folder
        """
        programs_files_upload = get_programs_upload_files(
            programs=programs
        )
        missing_upload_files = str()
        for program in programs_files_upload:
            for upload_file in programs_files_upload[program]:
                try:
                    shutil.copyfile(
                        src=f'{constants.programs_path}/{program}/upload/{upload_file}',
                        dst=f'{self.machine_path}/{self.arguments["-n"]}/upload/{upload_file}'
                    )
                except FileNotFoundError:
                    missing_upload_files += f'"{upload_file}" from "{program}"\n'
        if missing_upload_files:
            raise NoFileToUploadError(
                'You specify files to upload that does not exist.\n'
                'These are:\n'
                f'{missing_upload_files}'
            )

    def _initialize_vagrantfile(self):
        """Add initial configurations to Vagrantfile"""
        with open(self.vagrantfile_path, 'w') as vagrantfile:
            vagrantfile.write(
                '# -*- mode: ruby -*-\n'
                '# vi: set ft=ruby :\n\n'
            )
            vagrantfile.write(
                'Vagrant.configure("2") do |config|\n'
                f'    config.vm.box = "{self.arguments["-i"]}"\n'
                f'    config.ssh.username = "{self.credentials["username"]}"\n'
                f'    config.ssh.password = "{self.credentials["password"]}"\n'
                f'    config.ssh.insert_key = "{self.arguments["-s"]}"\n'
                f'    config.vm.hostname = "{self.arguments["-ho"]}"\n'
                f'    config.vm.define "{self.arguments["-ho"]}"\n'
                f'    config.vm.provider :{self.configs["provider"]} do |vb|\n'
                f'        vb.name = "{self.arguments["-vm"]}"\n'
                '        vb.customize ["modifyvm", :id, "--uart1", "0x3f8", "4"]\n'
                '    end\n'
            )

    def generate_main_file(self):
        """
        Generate Vagrantfile following the instructions from JSON file
        """
        self._initialize_vagrantfile()
        with open(self.vagrantfile_path, 'a') as vagrantfile:
            vagrantfile.write('\nconfig.vm.provision "shell", inline: <<-SHELL\n')
        if self.arguments['-u']:
            self._generate_provision_section(
                    src=f'{constants.setup_scripts_path}/create_extra_user.sh',
                    title=f"CREATE USER {self.arguments['-u']}",
                    program=''
                )
        if self.provisions['update_upgrade']:
            self._generate_provision_section(
                    src=f'{constants.setup_scripts_path}/update_upgrade.sh',
                    title="UPDATE and UPGRADE",
                    program='apt'
                )
        if self.provisions['programs_to_install']:
            for program in self.provisions['programs_to_install']:
                self._generate_provision_section(
                    src=f'{constants.programs_path}/{program}/install.sh',
                    title="INSTALL",
                    program=program
                )
        if self.provisions['programs_to_config']:
            for program in self.provisions['programs_to_config']:
                self._generate_provision_section(
                    src=f'{constants.programs_path}/{program}/config.sh',
                    title="CONFIG",
                    program=program
                )
            self._copy_configurations_to_upload(
                programs=self.provisions['programs_to_config']
            )
        if self.provisions['programs_to_uninstall']:
            for program in self.provisions['programs_to_uninstall']:
                self._generate_provision_section(
                    src=f'{constants.programs_path}/{program}/uninstall.sh',
                    title="UNINSTALL",
                    program=program
                )
        if self.provisions['clean_packages']:
            self._generate_provision_section(
                src=f'{constants.setup_scripts_path}/clean.sh',
                title="CLEAN apt packages",
                program=''
            )
        if self.provisions['custom_scripts']:
            for script in self.provisions['custom_scripts']:
                self._generate_provision_section(
                    src=f'{constants.custom_scripts_path}/{script}',
                    title="CUSTOM SCRIPT",
                    program=f'{script.split(".")[0]}'
                )

        with open(self.vagrantfile_path, 'a') as vagrantfile:
            vagrantfile.write('\n\nSHELL\nend')

        # replace_configs_in_vagrantfile(self.configs, self.vagrantfile_path)

    def delete_project(self):
        shutil.rmtree(f'{self.machine_path}/{self.arguments["-n"]}')
