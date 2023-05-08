#!/usr/bin/python3
import logging
import sys
from provisionsreader import ProvisionConfigReader
from error import (
    NoFileToUploadError,
    FlagError,
    ExistenceProjectError
)
from helper import convert_argv_list_to_dict
from builder.packer import Packer
from builder.vagrant import Vagrant

sys.tracebacklimit = 0


def get_project_class():
    arguments = convert_argv_list_to_dict()
    project_type = arguments['-t']
    if project_type == 'vagrant':
        return Vagrant()
    if project_type == 'packer':
        return Packer()
    else:
        raise FlagError("Select from [packer|vagrant]")


def main():
    builder = get_project_class()
    builder.check_flags()
    try:
        builder.check_new_project_folder_existence()
    except ExistenceProjectError:
        response = input('Project already exists. Delete it?')
        if response.lower() in ['y', 'yes']:
            builder.delete_project()
        exit()
    builder.check_virtualbox_existence()
    builder.check_provision_cfg_json_existence()
    builder.set_configs()
    builder.set_provisions()
    builder.set_credentials()
    provisions_configs_reader = ProvisionConfigReader(
        f'{builder.provisions_configs}/{builder.arguments["-j"]}'
    )
    provisions_configs_reader.check_program_upload_files_existence()
    provisions_configs_reader.check_programs_existence_for(
        provision_key="programs_to_install"
    )
    provisions_configs_reader.check_scripts_emptyness_for(
        provision_key='programs_to_install'
    )
    provisions_configs_reader.check_programs_existence_for(
        provision_key="programs_to_uninstall"
    )
    provisions_configs_reader.check_scripts_emptyness_for(
        provision_key='programs_to_uninstall'
    )
    provisions_configs_reader.check_programs_existence_for(
        provision_key="programs_to_config"
    )
    provisions_configs_reader.check_scripts_emptyness_for(
        provision_key='programs_to_config'
    )
    provisions_configs_reader.check_upload_file_name_duplicates()
    provisions_configs_reader.check_custom_script_existence()

    try:
        builder.create_project_folder()
        builder.generate_main_file()
    except (NoFileToUploadError, KeyError) as exc:
        logging.error(exc.msg)
        builder.delete_project()


if __name__ == '__main__':
    main()
