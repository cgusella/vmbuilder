#!/usr/bin/python3
from builder import get_project_class
from provisionsreader import ProvisionConfigReader
import sys

sys.tracebacklimit = 0


def main():
    builder = get_project_class()
    builder.check_flags()
    builder.check_folder_vb_json_existence()
    builder.set_configs()
    builder.set_provisions()
    provisions_configs_reader = ProvisionConfigReader(f'{builder.provisions_configs}/{builder.arguments["-j"]}')
    provisions_configs_reader.check_programs_existence()
    provisions_configs_reader.check_scripts_existence()
    provisions_configs_reader.check_install_scripts_emptyness()
    provisions_configs_reader.check_uninstall_scripts_emptyness()

    try:
        builder.create_project_folder()
        builder.provision()
    except (FileNotFoundError, KeyError):
        builder.delete_project()


if __name__ == '__main__':
    main()
