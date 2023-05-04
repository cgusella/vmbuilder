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
