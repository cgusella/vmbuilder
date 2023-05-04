import constants
import json
import os
import shutil
from builder.builder import Builder
from error import (
    FlagError,
    ExistenceProjectError,
    ExistenceVirtualBoxError,
    JsonConfigNotFoundError,
    FileExtesionError,
)
from helper import (
    convert_argv_list_to_dict,
    empty_script,
    get_local_virtual_boxes,
    replace_configs_in_vagrantfile,
    VAGRANT_FLAGS_TO_ERROR,
)


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
            raise JsonConfigNotFoundError(
                f'The json file {self.arguments["-j"]} '
                'is created at /templates/vagrant/provisions_configs folder.\n'
                'Fill it up and come back then!'
            )

    def set_configs(self):
        config_provision_file_path = f'{self.provisions_configs}/{self.arguments["-j"]}'
        with open(config_provision_file_path, 'r') as provisions:
            configs = json.loads(provisions.read())["vbox_configs"]
        configs['extra_user'] = self.arguments['-u']
        configs['default_image'] = self.arguments['-i']
        configs['default_hostname'] = self.arguments['-ho']
        configs['default_vbname'] = self.arguments['-vm']
        configs['ssh_insert_key'] = False if self.arguments['-s'] == 'password' else True
        if configs['extra_user'] == configs['default_user']:
            raise FlagError('Default user in provision file is the same as inserted user!')
        self.configs = configs.copy()

    def set_provisions(self):
        config_provision_file_path = f'{self.provisions_configs}/{self.arguments["-j"]}'
        with open(config_provision_file_path, 'r') as provisions:
            provisions = json.loads(provisions.read())["vbox_provisions"]
        self.provisions = provisions.copy()

    def create_project_folder(self):
        project_folder = f'{self.machine_path}/{self.arguments["-n"]}'
        os.mkdir(project_folder)

        vagrant_folder = constants.vagrant_templates_path
        shutil.copyfile(
            src=f'{vagrant_folder}/Vagrantfile',
            dst=f'{project_folder}/Vagrantfile'
        )
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
        empty_file, lines = empty_script(script=src)

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
        update_upgrade = self.provisions['programs']['update_upgrade']
        clean = self.provisions['programs']['clean']
        programs_to_install = self.provisions['programs']['install']
        programs_to_uninstall = self.provisions['programs']['uninstall']
        custom_scripts = self.provisions['custom_scripts']
        with open(vagrantfile_path, 'a') as vagrantfile:
            vagrantfile.write('\nconfig.vm.provision "shell", inline: <<-SHELL\n')
        if self.configs['extra_user']:
            self._generate_provision_text(
                    src=f'{constants.bash_path}/create-extra-user.sh',
                    dst=vagrantfile_path,
                    title=f"CREATE USER {self.configs['extra_user']}",
                    program=''
                )
        if update_upgrade:
            self._generate_provision_text(
                    src=f'{constants.bash_path}/update-upgrade.sh',
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
                src=f'{constants.bash_path}/clean.sh',
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
