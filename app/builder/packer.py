import constants
import json
import os
import shutil
from argparse import Namespace
from builder.builder import Builder
from builder.error import (
    ExistenceProjectError,
    JsonConfigCopiedError,
    ExistenceVirtualBoxError
)
from builder.helper import (
    get_local_virtual_boxes,
    replace_text_in_file,
    get_programs_upload_files
)
from io import TextIOWrapper


class Packer(Builder):
    def __init__(self, namespace) -> None:
        self.arguments: Namespace = namespace
        self.machines_path: str = constants.packer_machines_path
        self.provisions_configs: dict = dict()
        self.configs: dict = dict()
        self.provisions: dict = dict()
        self.credentials: dict = dict()

    def check_new_project_folder_existence(self):
        if self.arguments.name in os.listdir(self.machines_path):
            raise ExistenceProjectError("[ERROR] Project already exists!")

    def check_virtualbox_existence(self):
        if self.arguments.vm_name in get_local_virtual_boxes():
            raise ExistenceVirtualBoxError(
                f'The virtualbox {self.arguments.vm_name} already exists!'
            )

    def check_provision_cfg_json_existence(self):
        if self.arguments.json not in os.listdir(constants.packer_provs_confs_path):
            shutil.copyfile(
                src=f'{constants.packer_provs_confs_path}/template.json',
                dst=f'{constants.packer_provs_confs_path}/{self.arguments.json}'
            )
            raise JsonConfigCopiedError(
                f'The json file "{self.arguments.json}" '
                f'is created at {constants.vagrant_provs_confs_path} folder.\n'
                'Fill it up and come back then!'
            )

    def set_provisions_configs(self):
        """Set provisions_configs attribute"""
        config_provision_file_path = f'{constants.packer_provs_confs_path}/{self.arguments.json}'
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
            - http/
                |
                - chosen_preseed_file
        """
        project_folder = f'{self.machines_path}/{self.arguments.name}'
        os.makedirs(f'{project_folder}/http')

        shutil.copyfile(
            src=f'{constants.packer_http_path}/{self.arguments.preseed}',
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
        programs = self.provisions.get(f"programs_to_{operation}", '')
        if programs:
            for program in programs:
                script_paths.append(
                    f'{constants.programs_path}/{program}/{operation}.sh'
                )
        return script_paths

    def _generate_vars_file(self):
        with open(f'{constants.packer_machines_path}/{self.arguments.name}/vars.pkr.hcl', 'w') as vars_file:
            for var in self.configs:
                if not isinstance(self.configs[var], dict):
                    continue
                if var == 'output_directory':
                    if not self.configs[var]["default"]:
                        self.configs[var]["default"] = constants.packer_builds_path
                if var == 'iso_directory':
                    if not self.configs[var]["default"]:
                        self.configs[var]["default"] = constants.iso_path
                if var == 'boot_command':
                    with open(f'{constants.packer_http_path}/boot_command.txt') as boot_command:
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
        # write local directive on main
        main_file.write(
            'locals {\n'
            f'{self._generate_packer_variable("output_directory")}'
            '}\n\n'
        )
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
        main_file.write(
            'build {\n\n'
            '  sources = ["source.virtualbox-iso.vbox"]\n\n'
        )

        # recover needed upload files for config files
        needed_upload_files = get_programs_upload_files(self.provisions['programs_to_config'])

        # recover upload files
        upload_program_files_path = list()
        for program in needed_upload_files:
            if needed_upload_files[program]:
                upload_program_files_path.extend(
                    [
                        f'{constants.programs_path}/{program}/upload/{file}'
                        for file in os.listdir(f'{constants.programs_path}/{program}/upload')
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
        if needed_upload_files:
            scripts.append(f'{constants.setup_scripts_path}/prepare_to_upload.sh')
        if scripts:
            self._generate_provisioner_shell(
                script_paths=scripts,
                main_file=main_file
            )

        # write upload file into main file
        if upload_program_files_path:
            self._generate_provisioner_file(
                files=upload_program_files_path,
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
                f'{constants.custom_scripts_path}/{script}'
                for script in self.provisions['custom_scripts']
            ]
            self._generate_provisioner_shell(
                scripts=custom_scripts,
                main_file=main_file
            )
        main_file.write('}\n')

    def _add_user_password_preseed(self):
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
        """"""
        self._generate_vars_file()
        with open(f'{constants.packer_machines_path}/{self.arguments.name}/main.pkr.hcl', 'w') as main_file:
            self._add_locals_block(main_file=main_file)
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
