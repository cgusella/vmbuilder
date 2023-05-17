import constants
import json
import os
import shutil
from argparse import Namespace
from builder.builder import Builder
from builder.error import (
    ExistenceProjectError,
    ExistenceVirtualBoxError,
    JsonConfigCopiedError,
    NoFileToUploadError
)
from builder.helper import (
    get_local_virtual_boxes,
    get_packages_upload_files,
    is_empty_script,
    replace_text_in_file,
)
from typing import List


class Vagrant(Builder):
    def __init__(self, namespace) -> None:
        self.arguments: Namespace = namespace
        self.machine_path: str = constants.vagrant_machines_path
        self.vagrantfile_path = f'{self.machine_path}/{self.arguments.name}/Vagrantfile'
        self.provisions_configs: dict = dict()
        self.configs: dict = dict()
        self.provisions: dict = dict()
        self.credentials: dict = dict()

    def check_new_project_folder_existence(self):
        if self.arguments.name in os.listdir(self.machine_path):
            raise ExistenceProjectError("[ERROR] Project already exists!")

    def check_virtualbox_existence(self):
        if self.arguments.vm_name in get_local_virtual_boxes():
            raise ExistenceVirtualBoxError(
                f'The virtualbox {self.arguments.vm_name} already exists!'
            )

    def check_provision_cfg_json_existence(self):
        if self.arguments.json not in os.listdir(constants.vagrant_provs_confs_path):
            shutil.copyfile(
                src=f'{constants.vagrant_provs_confs_path}/template.json',
                dst=f'{constants.vagrant_provs_confs_path}/{self.arguments.json}'
            )
            raise JsonConfigCopiedError(
                f'The json file "{self.arguments.json}" '
                f'is created at {constants.vagrant_provs_confs_path} folder.\n'
                'Fill it up and come back then!'
            )

    def set_provisions_configs(self):
        """Set provisions_configs attribute"""
        config_provision_file_path = f'{constants.vagrant_provs_confs_path}/{self.arguments.json}'
        with open(config_provision_file_path, 'r') as provisions_configs:
            self.provisions_configs = json.loads(
                provisions_configs.read()
            )

    def set_configs(self):
        """Set configs attribute"""
        self.configs = self.provisions_configs["virtual_machine_configs"].copy()

    def set_provisions(self):
        """Set provisions attribute"""
        self.provisions = self.provisions_configs["provisions"].copy()

    def set_credentials(self):
        """Set credentials attribute"""
        self.credentials = self.provisions_configs["credentials"].copy()

    def create_project_folder(self):
        """
        Create project folder with this structure:
        - project_name/
            |
            - upload/
        """
        project_folder = f'{self.machine_path}/{self.arguments.name}'
        # create project folder
        os.mkdir(project_folder)

        # create upload folder
        os.mkdir(f'{project_folder}/upload')

    def _generate_provision_section(self, src, title: str, package: str):
        """
        Generate provision section in Vagrantfile.
        It titles section as follow
            ######################################################################
            echo ==OPERATION package==============================================
            ######################################################################
        """
        hash_number = 70
        with open(src, 'r') as source_file:
            lines = source_file.readlines()

        if "create_extra_user.sh" in src:
            lines = [line.replace("extra_user", self.arguments.user) for line in lines]

        if title.lower() in ['config'] and is_empty_script(src):
            pass
        else:
            with open(
                f'{self.machine_path}/{self.arguments.name}/Vagrantfile',
                'a'
            ) as vagrantfile:
                vagrantfile.write(f'\n\n\t\t{hash_number*"#"}\n')
                pound_number = hash_number - 8 - len(title) - len(package)
                # vagrantfile.write(f'\t#######   {title} {package}   {pound_number*"#"}')
                vagrantfile.write(f'\t\techo =={title} {package}{pound_number*"="}')
                vagrantfile.write(f'\n\t\t{hash_number*"#"}\n')

                for line in lines:
                    if line in ['#!/bin/bash', '#!/bin/bash\n']:
                        continue
                    vagrantfile.write(f'\t\t{line.strip()}\n')

    def _copy_configurations_to_upload(self, packages: List[str]):
        """
        Find needed files from config.sh script and copy them into project
        upload folder
        """
        packages_files_upload = get_packages_upload_files(
            packages=packages
        )
        missing_upload_files = str()
        for package in packages_files_upload:
            for upload_file in packages_files_upload[package]:
                try:
                    shutil.copyfile(
                        src=f'{constants.packages_path}/{package}/upload/{upload_file}',
                        dst=f'{self.machine_path}/{self.arguments.name}/upload/{upload_file}'
                    )
                except FileNotFoundError:
                    missing_upload_files += f'"{upload_file}" from "{package}"\n'
                if upload_file == "motd":
                    replace_text_in_file(
                        search_phrase="extra_user",
                        replace_with=self.arguments.user,
                        file_path=f'{self.machine_path}/{self.arguments.name}/upload/{upload_file}'
                    )
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
                f'\tconfig.vm.box = "{self.arguments.image}"\n'
                f'\tconfig.ssh.username = "{self.credentials["username"]}"\n'
                f'\tconfig.ssh.password = "{self.credentials["password"]}"\n'
                f'\tconfig.ssh.insert_key = "{self.arguments.connection}"\n'
                f'\tconfig.vm.hostname = "{self.arguments.hostname}"\n'
                f'\tconfig.vm.define "{self.arguments.hostname}"\n'
                f'\tconfig.vm.provider :{self.configs["provider"]} do |vb|\n'
                f'\t\tvb.name = "{self.arguments.vm_name}"\n'
                '\t\tvb.customize ["modifyvm", :id, "--uart1", "0x3f8", "4"]\n'
                '\tend\n'
            )

    def generate_main_file(self):
        """
        Generate Vagrantfile following the instructions from JSON file
        """
        self._initialize_vagrantfile()
        with open(self.vagrantfile_path, 'a') as vagrantfile:
            vagrantfile.write('\n\tconfig.vm.provision "shell", inline: <<-SHELL\n')
        if self.arguments.user:
            self._generate_provision_section(
                    src=f'{constants.setup_scripts_path}/create_extra_user.sh',
                    title=f"CREATE USER {self.arguments.user}",
                    package=''
                )
        if self.provisions['update_upgrade']:
            self._generate_provision_section(
                    src=f'{constants.setup_scripts_path}/update_upgrade.sh',
                    title="UPDATE and UPGRADE",
                    package='apt'
                )
        if self.provisions['packages_to_install']:
            for package in self.provisions['packages_to_install']:
                self._generate_provision_section(
                    src=f'{constants.packages_path}/{package}/install.sh',
                    title="INSTALL",
                    package=package
                )
        if self.provisions['packages_to_config']:
            for package in self.provisions['packages_to_config']:
                self._generate_provision_section(
                    src=f'{constants.packages_path}/{package}/config.sh',
                    title="CONFIG",
                    package=package
                )
            self._copy_configurations_to_upload(
                packages=self.provisions['packages_to_config']
            )
        if self.provisions['packages_to_uninstall']:
            for package in self.provisions['packages_to_uninstall']:
                self._generate_provision_section(
                    src=f'{constants.packages_path}/{package}/uninstall.sh',
                    title="UNINSTALL",
                    package=package
                )
        if self.provisions['clean_packages']:
            self._generate_provision_section(
                src=f'{constants.setup_scripts_path}/clean_packages.sh',
                title="CLEAN apt packages",
                package=''
            )
        if self.provisions['custom_scripts']:
            for script in self.provisions['custom_scripts']:
                self._generate_provision_section(
                    src=f'{constants.custom_scripts_path}/{script}',
                    title="CUSTOM SCRIPT",
                    package=f'{script.split(".")[0]}'
                )

        with open(self.vagrantfile_path, 'a') as vagrantfile:
            vagrantfile.write('\n\nSHELL\nend')

        if self.arguments.user:
            replace_text_in_file(
                search_phrase='extra_user',
                replace_with=self.arguments.user,
                file_path=f'{constants.machines_path}/vagrant/{self.arguments.name}/Vagrantfile'
            )

    def delete_project(self):
        shutil.rmtree(f'{self.machine_path}/{self.arguments.name}')
