import constants


def replace_text_in_file(search_phrase, replace_with, file_path):
    replaced_content = ""
    with open(file_path, "r") as file:
        for line in file:
            line = line.rstrip()
            new_line = line.replace(search_phrase, replace_with)
            replaced_content = replaced_content + new_line + '\n'
    with open(file_path, "w") as new_file:
        new_file.write(replaced_content)


def is_empty_script(script: str):
    """
    Return True the given script is empty
    """
    with open(script) as script_file:
        lines = script_file.read().split("\n")

    for line in lines:
        if line in ['#!/bin/bash', '']:
            lines.remove(line)

    return not any(lines)


def get_packages_upload_files(packages: list) -> dict:
    """
    Return a dictionary with packages as keys and list of
    upload file names as value
    """
    package_upload_files = dict()
    for package in packages:
        with open(
            f'{constants.PACKAGES_PATH}/{package}/config.sh', 'r'
        ) as file:
            lines = file.readlines()
        package_upload_files[package] = list()
        for line in lines:
            if line.startswith('cp /vagrant/upload/'):
                upload_file_name = line.strip().split()[1].split('/')[-1]
                package_upload_files[package].append(
                    upload_file_name
                )
    return package_upload_files
