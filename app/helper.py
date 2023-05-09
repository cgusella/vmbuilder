import subprocess
import os
import constants


def get_json_files_for_help(path_to_provs_confs: str):
    provision_files = [
            file for file in os.listdir(
                path_to_provs_confs
            ) if file != 'template.json'
        ]
    if not provision_files:
        message = (
            "\t\t\t\tThere are no provision files.\n"
            "\t\t\t\tTo create a new one just specify it\n"
            "\t\t\t\tusing \"-j\""
        )
    else:
        message = '\n'.join(
            [
                f'\t\t\t\t--> {file}' for file in provision_files
            ]
        )
    return message


def get_preseed_files_for_error():
    return '\n'.join(
        [
            '\t\t\t\t--> ' + file for file in os.listdir(
                constants.packer_http_path
            ) if file.startswith('preseed')
        ]
    )


def get_local_vagrant_boxes():
    bash_command = "vagrant box list"
    process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    items = output.decode("utf-8").split('\n')
    return [item.split()[0] for item in items if item]


def get_vagrant_images_for_help():
    return '\n'.join(
        [
            '\t\t\t\t--> ' + file for file in get_local_vagrant_boxes()
        ]
    )


def replace_text_in_file(search_phrase, replace_with, file_path):
    replaced_content = ""
    with open(file_path, "r") as file:
        for line in file:
            line = line.rstrip()
            new_line = line.replace(search_phrase, replace_with)
            replaced_content = replaced_content + new_line + '\n'
    with open(file_path, "w") as new_file:
        new_file.write(replaced_content)


def get_local_virtual_boxes():
    bash_command = "VBoxManage list vms"
    process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    items = output.decode("utf-8").split('\n')
    return [item.split()[0].replace('"', '') for item in items if item]


def replace_configs_in_vagrantfile(configs: dict, file_path: str):
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


def is_empty_script(script: str):
    """
    Return True the given script is empty
    """
    with open(script) as script_file:
        lines = script_file.readlines()

    for line in lines:
        if line in ['#!/bin/bash', '#!/bin/bash\n']:
            lines.remove(line)

    return not any(lines)


def get_programs_upload_files(programs: list) -> dict:
    """
    Return a dictionary with programs as keys and list of
    upload file names as value
    """
    program_upload_files = dict()
    for program in programs:
        with open(
            f'{constants.programs_path}/{program}/config.sh', 'r'
        ) as file:
            lines = file.readlines()
        program_upload_files[program] = list()
        for line in lines:
            if line.startswith('cp '):
                upload_file_name = line.strip().split()[1].split('/')[-1]
                program_upload_files[program].append(
                    upload_file_name
                )
    return program_upload_files
