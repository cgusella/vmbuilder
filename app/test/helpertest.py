import subprocess
from app.constants import vmbuilder_path
from typing import List

VAGRANT_FLAGS = {"-n": "name", "-vm": "vboxname", "-t": "vagrant",
                 "-u": "user", "-ho": "hostname", "-i": "image",
                 "-j": "provision-file.json", "-s": "key"}

PACKER_FLAGS = {"-n": "name", "-vm": "vboxname", "-t": "packer",
                "-il": "isolink", "-cs": "checksum", "-if": "isofile",
                "-j": "provision-file.json", "-pf": "preseed-kali.cfg"}


def missing_flag_error_test(flags: List[str], vmtype: str):
    """Launch main.py from terminal specifying missing flags.
    It is used to get the error message from terminal.

    Parameters:
        * flags: list of string. Used to specify which flags
        must be missed in order to get relative error message;
        * vmtype: str. Can be "vagrant" or "packer".

    Return:
        * terminal error message.
    """
    if vmtype == 'vagrant':
        command_line_flags = VAGRANT_FLAGS.copy()
    elif vmtype == 'packer':
        command_line_flags = PACKER_FLAGS.copy()
    for flag in flags:
        del command_line_flags[flag]
    argv = list()
    for vagrant_flag in command_line_flags:
        argv.append(vagrant_flag)
        argv.append(command_line_flags[vagrant_flag])
    argv.insert(0, f'{vmbuilder_path}/app/main.py')
    return subprocess.run(
        args=argv,
        capture_output=True
    ).stderr.decode('ascii')


def launch_main_with_custom_arguments(
        new_args: dict,
        vmtype: str,
        error: bool = False
):
    """Launch main.py with custom terminal arguments.

    Parameters:
        * new_args: dict. A dictionary containing flags as
        key and new arguments as values. Then each value in
        predefined vagrant arguments will be override with new
        arguments;
        * vmtype: str. Can be "vagrant" or "packer";
        * error: bool.

        Return:
            * if error = False return terminal message.
            * if error = True return terminal error message
    """
    if vmtype == 'vagrant':
        command_line_flags = VAGRANT_FLAGS.copy()
    elif vmtype == 'packer':
        command_line_flags = PACKER_FLAGS.copy()
    argv = list()
    for key in new_args:
        command_line_flags[key] = new_args[key]
    for vagrant_flag in command_line_flags:
        argv.append(vagrant_flag)
        argv.append(command_line_flags[vagrant_flag])
    argv.insert(0, f'{vmbuilder_path}/app/main.py')
    if error:
        terminal_message = subprocess.run(
            args=argv,
            capture_output=True
        ).stderr.decode('ascii')
    else:
        terminal_message = subprocess.run(
            args=argv,
            capture_output=True
        ).stdout.decode('ascii')
    return terminal_message
