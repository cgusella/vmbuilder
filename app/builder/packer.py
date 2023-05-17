import constants
import json
import os
import shutil
from argparse import Namespace
from builder.builder import Builder
from builder.helper import (
    replace_text_in_file,
    get_packages_upload_files
)
from io import TextIOWrapper


class Packer(Builder):
    def __init__(self, namespace: Namespace, json_file: dict) -> None:
        self.arguments: Namespace = namespace
        self.machines_path: str = constants.PACKER_MACHINES_PATH
        self.provisions_configs = json_file
        self.configs: dict = dict()
        self.provisions: dict = dict()
        self.credentials: dict = dict()

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
            - http/
                |
                - chosen_preseed_file
        """
        project_folder = f'{self.machines_path}/{self.arguments.name}'
        os.makedirs(f'{project_folder}/http')

        shutil.copyfile(
            src=f'{constants.PACKER_PRESEEDS_PATH}/{self.arguments.preseed}',
            dst=f'{project_folder}/http/{self.arguments.preseed}'
        )

    def _generate_packer_variable(self, variable: str):
        number = 30
        chars = len(variable)
        space = (number - chars) * ' '
        return f'  {variable}{space}= \"${{var.{variable}}}\"\n'

    def _get_operation_scripts(self, operation: str):
        """
        Return list of scripts for the operation selected.
        Operations available: "install", "uninstall", "config"
        """
        script_paths = list()
        packages = self.provisions.get(f"packages_to_{operation}", '')
        if packages:
            for package in packages:
                script_paths.append(
                    f'{constants.PACKAGES_PATH}/{package}/{operation}.sh'
                )
        return script_paths

    def _generate_vars_file(self):
        """Generate vars file"""
        with open(f'{constants.PACKER_MACHINES_PATH}/{self.arguments.name}/vars.pkr.hcl', 'w') as vars_file:
            for var in self.configs:
                if not isinstance(self.configs[var], dict):
                    continue
                if var == 'output_directory':
                    if not self.configs[var]["default"]:
                        self.configs[var]["default"] = constants.PACKER_BUILDS_PATH
                if var == 'iso_directory':
                    if not self.configs[var]["default"]:
                        self.configs[var]["default"] = constants.ISO_PATH
                if var == 'boot_command':
                    with open(f'{constants.PACKER_PRESEEDS_PATH}/boot_command.txt') as boot_command:
                        lines = boot_command.readlines()
                    for count, line in enumerate(lines):
                        lines[count] = line.replace('preseed-file', self.arguments.preseed)
                    self.configs[var]["default"] = ''.join(lines)
                description = self.configs[var]["description"]
                variable_value = self.configs[var]["default"]
                if isinstance(variable_value, str):
                    variable_type = 'string'
                elif isinstance(variable_value, bool):
                    variable_type = 'bool'
                    variable_value = str(variable_value).lower()
                self.write_variable_directive(
                    variable_file=vars_file,
                    variable_name=var,
                    description=description,
                    variable_type=variable_type,
                    value=variable_value
                    )
            terminal_values = vars(self.arguments)
            for terminal_value in terminal_values:
                if terminal_value in {'iso_file', 'iso_link', 'iso_checksum', 'vm_name'}:
                    variable_value = terminal_values.get(terminal_value)
                    self.write_variable_directive(
                        variable_file=vars_file,
                        variable_name=terminal_value,
                        description="",
                        variable_type="string",
                        value=variable_value
                        )

    def _add_locals_block(self, main_file: TextIOWrapper):
        """
        Write on packer main file the local block and variables
        """
        # write local directive on main
        main_file.write(
            'locals {\n'
            f'{self._generate_packer_variable("output_directory")}'
            '}\n\n'
        )

    def _add_source_block(self, main_file: TextIOWrapper):
        """
        Write the source block on packer main file
        """
        main_file.write('source "virtualbox-iso" "vbox" {\n')
        for var in self.configs:
            if not isinstance(self.configs[var], dict):
                continue
            space = (30 - len(var)) * ' '
            if var in ['start_retry_timeout', 'iso_file']:
                continue
            elif var == 'boot_command':
                main_file.write(f'  {var}{space}= [ var.{var} ]\n')
            elif var == 'iso_directory':
                main_file.write(
                    '  iso_target_path               = '
                    '"${var.iso_directory}/${var.iso_file}"\n'
                )
            elif var == 'ssh_password':
                main_file.write(
                    '  shutdown_command              = "echo '
                    '\'${var.ssh_password}\' | sudo -E -S poweroff"\n'
                )
                main_file.write(self._generate_packer_variable(var))
            else:
                main_file.write(self._generate_packer_variable(var))

        # write iso_urls to main
        main_file.write(
            '  iso_urls = [\n'
            '    "${var.output_directory}/${var.iso_file}",\n'
            '    "${var.iso_link}",\n'
            '  ]\n'
        )

        # write iso_checksum
        main_file.write('  iso_checksum= "${var.iso_checksum}"\n')

        main_file.write(
            '  vboxmanage = [\n'
            '      ["modifyvm", "{{ .Name }}", "--rtcuseutc", "off"],\n'
            '      ["modifyvm", "{{ .Name }}", "--vram", "128"]\n'
            '  ]\n'
            '  virtualbox_version_file       = "/tmp/.vbox_version"\n'
        )
        main_file.write('}\n\n')

    def _add_build_block(self, main_file: TextIOWrapper):
        """
        Write the build block on packer main file
        """
        main_file.write(
            'build {\n\n'
            '  sources = ["source.virtualbox-iso.vbox"]\n\n'
        )

        # recover needed upload files for config files
        needed_upload_files = get_packages_upload_files(self.provisions['packages_to_config'])

        # recover upload files
        upload_package_files_path = list()
        for package in needed_upload_files:
            if needed_upload_files[package]:
                upload_package_files_path.extend(
                    [
                        f'{constants.PACKAGES_PATH}/{package}/upload/{file}'
                        for file in os.listdir(f'{constants.PACKAGES_PATH}/{package}/upload')
                        if file != 'prepare_to_upload.sh'
                    ]
                )

        # recover install scripts
        install_scripts = self._get_operation_scripts(operation='install')

        # recover uninstall scripts
        uninstall_scripts = self._get_operation_scripts(operation='uninstall')

        # write install uninstall scripts into main file; if some needed upload file are found
        # from config files, then the "prepare_to_upload.sh"'s path is added
        scripts = install_scripts[:]+uninstall_scripts[:]
        if self.provisions['update_upgrade_full']:
            scripts.insert(0, f'{constants.SETUP_SCRIPTS_PATH}/update_upgrade_full.sh')
        if self.provisions['update_upgrade']:
            scripts.insert(0, f'{constants.SETUP_SCRIPTS_PATH}/update_upgrade.sh')
        if self.provisions["clean_packages"]:
            scripts.append(f'{constants.SETUP_SCRIPTS_PATH}/clean_packages.sh')
        if needed_upload_files:
            scripts.append(f'{constants.SETUP_SCRIPTS_PATH}/prepare_to_upload.sh')
        if scripts:
            self._generate_provisioner_shell(
                script_paths=scripts,
                main_file=main_file
            )

        # write upload file into main file
        if upload_package_files_path:
            self._generate_provisioner_file(
                files=upload_package_files_path,
                main_file=main_file
            )

        # write config script addresses into main file
        config_scripts = self._get_operation_scripts(operation='config')
        if config_scripts:
            self._generate_provisioner_shell(
                script_paths=config_scripts,
                main_file=main_file
            )

        if self.provisions['custom_scripts']:
            custom_scripts = [
                f'{constants.CUSTOM_SCRIPTS_PATH}/{script}'
                for script in self.provisions['custom_scripts']
            ]
            self._generate_provisioner_shell(
                script_paths=custom_scripts,
                main_file=main_file
            )
        main_file.write('}\n')

    def _add_user_password_preseed(self):
        """
        Replace in preseed file the default user and password
        """
        project_folder = f'{self.machines_path}/{self.arguments.name}'
        replace_text_in_file(
            search_phrase="default_user",
            replace_with=self.credentials['username'],
            file_path=f'{project_folder}/http/{self.arguments.preseed}'
        )
        replace_text_in_file(
            search_phrase="default_pass",
            replace_with=self.credentials['password'],
            file_path=f'{project_folder}/http/{self.arguments.preseed}'
        )

    def generate_main_file(self):
        """Generate main and vars files for packer"""
        self._generate_vars_file()
        with open(f'{constants.PACKER_MACHINES_PATH}/{self.arguments.name}/main.pkr.hcl', 'w') as main_file:
            self._add_locals_block(main_file=main_file)
            self._add_source_block(main_file=main_file)
            self._add_build_block(main_file=main_file)
        self._add_user_password_preseed()

    def _generate_provisioner_shell(
            self,
            script_paths: list,
            main_file: TextIOWrapper
    ):
        main_file.write(
            '\tprovisioner "shell" {\n'
            '\t\tbinary               = false\n'
            '\t\texecute_command      = "echo \'${var.ssh_password}\' | {{ .Vars }} sudo -S -E bash \'{{ .Path }}\'\"\n'
            '\t\texpect_disconnect    = true\n'
            '\t\tvalid_exit_codes     = [0, 2]\n'
            '\t\tscripts = [\n'
        )
        for script in script_paths:
            main_file.write(f'\t\t\t"{script}",\n')
        main_file.write(
            '\t\t]\n'
            f'\t\t{self._generate_packer_variable("start_retry_timeout")}'
            '\t}\n\n'
        )

    def _generate_provisioner_file(self, files: list, main_file: TextIOWrapper):
        main_file.write(
            '\tprovisioner "file" {\n'
            '\t\tsources = [\n'
        )
        for file in files:
            main_file.write(f'\t\t\t"{file}",\n')

        main_file.write(
            '\t\t]\n'
            '\t\tdestination = "/vagrant/upload/"\n'
            '\t}\n\n'
        )

    def write_variable_directive(self, variable_file, variable_name, description, variable_type, value):
        variable_file.write(
            f'variable "{variable_name}" ' + '{\n'
            f'\tdescription\t= "{description}"\n'
            f'\ttype\t= {variable_type}\n'
        )
        if variable_type == 'bool' or variable_name == 'boot_command':
            variable_file.write(
                f'\t\tdefault\t= {value}\n'
            )
        else:
            variable_file.write(
                f'\t\tdefault\t= "{value}"\n'
            )
        variable_file.write(
            '}\n\n'
        )

    def delete_project(self):
        shutil.rmtree(f'{self.machines_path}/{self.arguments.name}')
