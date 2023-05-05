#!/usr/bin/python3
import sys
from provisionsreader import ProvisionConfigReader
from error import (
    NoFileToUploadError,
    FlagError,
)
from helper import convert_argv_list_to_dict
from builder.packer import Packer
from builder.vagrant import Vagrant

# sys.tracebacklimit = 0


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
    builder.check_new_project_folder_existence()
    builder.check_virtualbox_existence()
    builder.check_provision_cfg_json_existence()
    builder.set_configs()
    builder.set_provisions()
    provisions_configs_reader = ProvisionConfigReader(f'{builder.provisions_configs}/{builder.arguments["-j"]}')
    provisions_configs_reader.check_programs_existence()
    provisions_configs_reader.check_scripts_existence()
    provisions_configs_reader.check_install_scripts_emptyness()
    provisions_configs_reader.check_uninstall_scripts_emptyness()
    provisions_configs_reader.check_config_scripts_for_upload()
    provisions_configs_reader.check_upload_files_existence()
    provisions_configs_reader.check_name_conflicts_in_upload_files()
    provisions_configs_reader.check_script_dependency_from_file_to_upload()

    try:
        builder.create_project_folder()
        builder.provision()
    except (NoFileToUploadError, KeyError):
        builder.delete_project()


if __name__ == '__main__':
    main()
