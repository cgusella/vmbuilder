import subprocess
import sys
import logging
import os
from error import FlagError

vmbuilder_path = f'{os.path.dirname(os.path.realpath(__file__))}/..'
logger = logging.getLogger('')


def get_vagrant_provision_for_error():
    return '\n'.join(
        [
            '\t\t\t\t--> ' + file for file in os.listdir(
                f"{vmbuilder_path}/templates/vagrant/provisions_configs"
            )
        ]
    )


def get_packer_provision_for_error():
    return '\n'.join(
        [
            '\t\t\t\t--> ' + file for file in os.listdir(
                f'{vmbuilder_path}/templates/packer/provisions_configs'
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
    '-u': '[EXTRA SUDOER USER]',
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


def replace_configs_in_vagrantfile(configs: dict, file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

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
        vmbuilder
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
        if not good_arguments.get(good_argument, ''):
            undefined_args += (good_argument,)
    error_msg = '\n'
    if undefined_args:
        for undefined_flag in undefined_args:
            error_msg += f'\t{undefined_flag}\t{COMMON_FLAGS_TO_ERROR[undefined_flag]}\n'
        raise FlagError(error_msg)
    return good_arguments
