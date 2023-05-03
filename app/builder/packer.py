import constants
import json
import os
import shutil
from builder.builder import Builder
from error import (
    FlagError,
    ExistenceProjectError,
)
from helper import (
    convert_argv_list_to_dict,
    PACKER_FLAGS_TO_ERROR,
    replace_text_in_file
)


class Packer(Builder):
    def __init__(self) -> None:
        self.arguments: dict = convert_argv_list_to_dict()
        # self.machines_path: str = constants.vmbuilder_path + '/machines/packer'
        self.machines_path: str = constants.packer_machines_path
        self.provisions_configs = constants.packer_provs_confs_path
        self.configs: dict = dict()
        self.provisions: dict = dict()

    def set_configs(self):
        config_provision_file_path = f'{self.provisions_configs}/{self.arguments["-j"]}'
        with open(config_provision_file_path, 'r') as file:
            configs = json.loads(file.read())["vbox-configs"]
        configs['iso_file'] = self.arguments['-if']
        configs['iso_link'] = self.arguments['-il']
        configs['iso_checksum'] = self.arguments['-cs']
        configs['vm_name'] = self.arguments['-vm']
        self.configs = configs.copy()

    def set_provisions(self):
        config_provision_file_path = f'{self.provisions_configs}/{self.arguments["-j"]}'
        with open(config_provision_file_path, 'r') as file:
            self.provisions = json.loads(file.read())["vbox-provisions"].copy()

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
        if self.arguments['-n'] in os.listdir(self.machines_path):
            raise ExistenceProjectError(
                f"Project {self.arguments['-n']} already exists!"
            )

    def create_project_folder(self):
        project_folder = f'{self.machines_path}/{self.arguments["-n"]}'
        os.makedirs(f'{project_folder}/http')

        shutil.copyfile(
            src=f'{constants.packer_http_path}/{self.arguments["-pf"]}',
            dst=f'{project_folder}/http/{self.arguments["-pf"]}'
        )

    def _generate_packer_variable(self, variable: str):
        number = 30
        chars = len(variable)
        space = (number - chars) * ' '
        return f'  {variable}{space}= \"${{var.{variable}}}\"\n'

    def _get_provisions_scripts(self):
        scripts = list()
        for key in self.provisions['programs']:
            value = self.provisions['programs'][key]
            if value:
                if isinstance(value, bool):
                    script = f'{constants.bash_path}/{key}.sh'
                    scripts.append(script)
                elif isinstance(value, list):
                    for program in value:
                        scripts.append(
                            f'{constants.programs_path}/{program}/{key}.sh'
                        )
        if self.provisions['upload']:
            scripts.append(
                f'{constants.bash_path}/prepare-for-upload.sh'
            )
        return scripts

    def _generate_vars_file(self, json_file: dict):
        with open(f'{constants.packer_machines_path}/{self.arguments["-n"]}/vars.pkr.hcl', 'w') as vars_file:
            for var in json_file:
                if not isinstance(json_file[var], dict):
                    continue
                if var in {'iso_file', 'iso_link', 'iso_checksum', 'vm_name'}:
                    json_file[var]["default"] = self.configs[var]
                if var == 'output_directory':
                    if not json_file[var]["default"]:
                        json_file[var]["default"] = constants.packer_builds_path
                if var == 'iso_directory':
                    if not json_file[var]["default"]:
                        json_file[var]["default"] = constants.iso_path
                if var == 'boot_command':
                    with open(f'{constants.packer_http_path}/boot_command.txt') as boot_command:
                        lines = boot_command.readlines()
                    for count, line in enumerate(lines):
                        lines[count] = line.replace('preseed-file', self.arguments['-pf'])
                    json_file[var]["default"] = ''.join(lines)

                description = json_file[var]["description"]
                variable_value = json_file[var]["default"]
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

    def _generate_main_file(self, json_file: dict):
        with open(f'{constants.packer_machines_path}/{self.arguments["-n"]}/main.pkr.hcl', 'w') as main_file:
            main_file.write(
                'locals {\n'
                f'{self._generate_packer_variable("output_directory")}'
                '}\n\n'
            )
            main_file.write('source "virtualbox-iso" "vbox" {\n')
            for var in json_file['vbox-configs']:
                if not isinstance(json_file['vbox-configs'][var], dict):
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
                elif var == 'iso_link':
                    main_file.write(
                        '  iso_urls = [\n'
                        '    "${var.output_directory}/${var.iso_file}",\n'
                        '    "${var.iso_link}",\n'
                        '  ]\n'
                    )
                elif var == 'ssh_password':
                    main_file.write(
                        '  shutdown_command              = "echo '
                        '\'${var.ssh_password}\' | sudo -E -S poweroff"\n'
                    )
                    main_file.write(self._generate_packer_variable(var))
                else:
                    main_file.write(self._generate_packer_variable(var))
            main_file.write(
                '  vboxmanage = [\n'
                '      ["modifyvm", "{{ .Name }}", "--rtcuseutc", "off"],\n'
                '      ["modifyvm", "{{ .Name }}", "--vram", "128"]\n'
                '  ]\n'
                '  virtualbox_version_file       = "/tmp/.vbox_version"\n'
            )
            main_file.write('}\n\n')

            main_file.write(
                'build {\n\n'
                '  sources = ["source.virtualbox-iso.vbox"]\n\n'
            )

            provision_scripts = self._get_provisions_scripts()

            self.provisioner_shell(
                scripts=provision_scripts,
                main_file=main_file
            )
            if self.provisions['upload']:
                upload_files = list()
                for file in self.provisions['files-to-upload']:
                    upload_files.append(
                        f'{constants.upload_path}/{file}'
                    )
                self.provisioner_file(upload_files, main_file)
            if self.provisions['custom-scripts']:
                custom_scripts = [
                    f'{constants.custom_scripts_path}/{script}'
                    for script in self.provisions['custom-scripts']
                ]
                self.provisioner_shell(
                    scripts=custom_scripts,
                    main_file=main_file
                )
            main_file.write('}\n')

    def _add_user_password_preseed(self, credentials: dict):
        project_folder = f'{self.machines_path}/{self.arguments["-n"]}'
        replace_text_in_file(
            search_phrase="default_user",
            replace_with=credentials['default_user'],
            file_path=f'{project_folder}/http/{self.arguments["-pf"]}'
        )
        replace_text_in_file(
            search_phrase="default_pass",
            replace_with=credentials['default_pass'],
            file_path=f'{project_folder}/http/{self.arguments["-pf"]}'
        )

    def provision(self):
        with open(f'{constants.packer_provs_confs_path}/{self.arguments["-j"]}') as provisions:
            json_provision = json.loads(provisions.read())
        vbox_configs = json_provision['vbox-configs']
        self._generate_vars_file(vbox_configs)
        self._generate_main_file(json_provision)
        credentials = {
            key: value for (key, value) in vbox_configs.items()
            if key in ("default_user", "default_pass")
        }
        self._add_user_password_preseed(credentials)

    def provisioner_shell(self, scripts, main_file):
        main_file.write(
            '  provisioner "shell" {\n'
            '    binary               = false\n'
            '    execute_command      = "echo \'${var.ssh_password}\' | {{ .Vars }} sudo -S -E bash \'{{ .Path }}\'\"\n'
            '    expect_disconnect    = true\n'
            '    valid_exit_codes     = [0, 2]\n'
            '    scripts = [\n'
        )
        for script in scripts:
            main_file.write(f'      "{script}",\n')
        main_file.write(
            '    ]\n'
            f'  {self._generate_packer_variable("start_retry_timeout")}'
            '  }\n\n'
        )

    def provisioner_file(self, files, main_file):
        main_file.write(
            '  provisioner "file" {\n'
            '    sources = [\n'
        )
        for file in files:
            main_file.write(f'      "{file}",\n')
        with open(f'{constants.bash_path}/prepare-for-upload.sh', 'r') as preparer:
            lines = preparer.readlines()
        for line in lines:
            if line.startswith('mkdir '):
                upload_folder_path = line.strip().split()[-1]

        main_file.write(
            '    ]\n'
            f'    destination = "{upload_folder_path}"\n'
            '  }\n\n'
        )

    def write_variable_directive(self, variable_file, variable_name, description, variable_type, value):
        variable_file.write(
            f'variable "{variable_name}" ' + '{\n'
            f'  description\t= "{description}"\n'
            f'  type\t= {variable_type}\n'
        )
        if variable_type == 'bool' or variable_name == 'boot_command':
            variable_file.write(
                f'  default\t= {value}\n'
            )
        else:
            variable_file.write(
                f'  default\t= "{value}"\n'
            )
        variable_file.write(
            '}\n\n'
        )

    def delete_project(self):
        shutil.rmtree(f'{self.machines_path}/{self.arguments["-n"]}')
