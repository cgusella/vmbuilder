import abc
import subprocess
import os
import sys
import shutil
import json
import logging
from error import FlagError
from error import ExistenceProjectError
from error import ExistenceVirtualBoxError


sys.tracebacklimit = 0
vmbuilder_path = f'{os.path.dirname(os.path.realpath(__file__))}/..'
logger = logging.getLogger('')


def get_vagrant_provision_for_error():
    return '\n'.join(
        [
            '\t\t\t\t--> ' + file for file in os.listdir(
                f"{vmbuilder_path}/templates/vagrant/vbox_confs_provs"
            )
        ]
    )


def get_packer_provision_for_error():
    return '\n'.join(
        [
            '\t\t\t\t--> ' + file for file in os.listdir(
                f'{vmbuilder_path}/templates/packer/vbox_confs_provs'
            )
        ]
    )


def replace_text_in_file(search_phrase, replace_with, file_path):
    replaced_content = ""
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            new_line = line.replace(search_phrase, replace_with)
            replaced_content = replaced_content + new_line + '\n'
    with open(file_path, "w") as new_file:
        new_file.write(replaced_content)


def get_local_vagrant_boxes():
    bash_command = "vagrant box list"
    process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    items = output.decode("utf-8").split('\n')
    return [item.split()[0] for item in items if item]


def get_vagrant_images_for_error():
    return '\n'.join(
        [
            '\t\t\t\t--> ' + file for file in get_local_vagrant_boxes()
        ]
    )


COMMON_FLAGS_TO_ERROR = {
    '-n': '[PROJECT NAME]',
    '-vb': '[VBOXNAME]',
    '-t': '[vagrant|packer]'
}
VAGRANT_FLAGS_TO_ERROR = {
    '-u': '[EXTRA USER]',
    '-ho': '[HOSTNAME]',
    '-i': f'[VAGRANT IMAGE]\n{get_vagrant_images_for_error()}',
    '-j': f'[VAGRANT PROVISION FILE]\n{get_vagrant_provision_for_error()}',
    '-s': '[VAGRANT SSH CONNECTION TYPE]\n\t\t\t\t[password|key]'
}
PACKER_FLAGS_TO_ERROR = {
    '-il': '[ISO LINK]',
    '-if': '[ISO FILE]',
    '-cs': '[CHECKSUM]',
    '-j': f'[PACKER CONFIG FILE]\n{get_packer_provision_for_error()}'
}
COMMON_VALID_FLAGS = ('-n', '-vb', '-t')


def get_local_virtual_boxes():
    bash_command = "VBoxManage list vms"
    process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    items = output.decode("utf-8").split('\n')
    return [item.split()[0].replace('"', '') for item in items if item]


def replace_configs_in_file(configs: dict, file_path):
    with open(file_path, "r") as file:
        lines = [line for line in file]

    for default_key in configs:
        if isinstance(configs[default_key], str):
            for count, line in enumerate(lines):
                lines[count] = line.replace(default_key, configs[default_key])
        elif isinstance(configs[default_key], bool):
            bool_value = "true" if configs[default_key] else "false"
            for count, line in enumerate(lines):
                if "SSH_INSERT_KEY" in line:
                    lines[count] = line.replace(default_key, bool_value)
                    lines[count] = ''.join(lines[count].split('"'))

    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line)


def convert_argv_list_to_dict():
    arguments = sys.argv[1:]
    if not arguments:
        error_msg = '''
        build_lab
          -n\t[PROJECT NAME]
          -vb\t[VBOXNAME]
          -t\tvagrant\n{}
          ---------------------------
          -t\tpacker\n{}
        '''
        vagrant_error_str = ''
        packer_error_str = ''
        for vagrant_flag in VAGRANT_FLAGS_TO_ERROR:
            vagrant_error_str += f'\t\t{vagrant_flag}:\t\t{VAGRANT_FLAGS_TO_ERROR[vagrant_flag]}\n'
        for packer_flag in PACKER_FLAGS_TO_ERROR:
            packer_error_str += f'\t\t{packer_flag}:\t\t{PACKER_FLAGS_TO_ERROR[packer_flag]}\n'
        raise FlagError(
            error_msg.format(vagrant_error_str, packer_error_str)
        )

    good_arguments = dict()
    for count, arg in enumerate(arguments):
        if arg.startswith('-'):
            try:
                if arguments[count + 1].startswith('-'):
                    good_arguments[arg] = ''
                else:
                    good_arguments[arg] = arguments[count + 1]
            except IndexError:
                good_arguments[arg] = ''

    undefined_args = ()
    for good_argument in ('-n', '-vb', '-t'):
        if not good_arguments[good_argument]:
            undefined_args += (good_argument,)
    for flag in COMMON_VALID_FLAGS:
        if flag not in good_arguments.keys():
            undefined_args += (flag,)
    error_msg = '\n'
    if undefined_args:
        for undefined_flag in undefined_args:
            error_msg += f'\t{undefined_flag}\t{COMMON_FLAGS_TO_ERROR[undefined_flag]}\n'
        raise FlagError(error_msg)
    return good_arguments


def get_project_class():
    arguments = convert_argv_list_to_dict()
    project_type = arguments['-t']
    if project_type == 'vagrant':
        return Vagrant()
    if project_type == 'packer':
        return Packer()
    else:
        raise FlagError("Select from [packer|vagrant]")


class Creator(abc.ABC):

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


class Vagrant(Creator):
    def __init__(self) -> None:
        self.arguments: dict = convert_argv_list_to_dict()
        self.machine_path: str = vmbuilder_path + '/machines/vagrant'
        self.vbox_confs_provs = os.listdir(f'{vmbuilder_path}/templates/vagrant/vbox_confs_provs')

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

    def create_project_folder(self):
        project_folder = f'{self.machine_path}/{self.arguments["-n"]}'
        os.mkdir(project_folder)

        vagrant_folder = f'{vmbuilder_path}/templates/vagrant'
        shutil.copyfile(
            src=f'{vagrant_folder}/Vagrantfile',
            dst=f'{project_folder}/Vagrantfile'
        )
        # with open(f'{vmbuilder_path}/templates/vagrant/vbox_confs_provs/{self.arguments["-j"]}') as config_file:
        #     programs = json.loads(config_file.read())['programs']['install']
        # for program in programs:
        #     shutil.copytree(
        #         src=f'{vmbuilder_path}/templates/programs/{program}',
        #         dst=f'{project_folder}/programs/{program}/'
        #     )

    def provision(self):
        # provisions_folder_path = f'{self.machine_path}/{self.arguments["-n"]}/provision'
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

        vagrantfile_path = f'{self.machine_path}/{self.arguments["-n"]}/Vagrantfile'
        programs_path = f'{vmbuilder_path}/templates/programs'
        with open(vagrantfile_path, 'a') as vagrantfile:
            vagrantfile.write('\nconfig.vm.provision "shell", inline: <<-SHELL\n')
            for program in configs['programs']['install']:
                with open(f'{programs_path}/{program}/install.sh') as install_file:
                    vagrantfile.write(f'\n#######   INSTALL {program}     #######\n')
                    vagrantfile.write(f'{install_file.read()}\n')
                with open(f'{programs_path}/{program}/configs/config.sh') as config_file:
                    vagrantfile.write(f'\n#######   CONFIG {program}     #######\n')
                    vagrantfile.write(f'{config_file.read()}\n')
            for program in configs['programs']['uninstall']:
                with open(f'{programs_path}/{program}/uninstall.sh') as uninstall_file:
                    vagrantfile.write(f'\n#######   UNINSTALL {program}     #######\n')
                    vagrantfile.write(f'{uninstall_file.read()}\n')
            vagrantfile.write('\nSHELL\nend')

        replace_configs_in_file(configs, vagrantfile_path)

    def delete_project(self):
        shutil.rmtree(f'{self.machine_path}/{self.arguments["-n"]}')


class Packer(Creator):
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
