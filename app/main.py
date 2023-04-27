#!/usr/bin/python3
from builder import get_project_class
from provisionsreader import ProvisionConfigReader
import sys

sys.tracebacklimit = 0


def main():
    project = get_project_class()
    project.check_flags()
    project.check_folder_vb_json_existence()
    provisions_configs_reader = ProvisionConfigReader(f'{project.provisions_configs}/{project.arguments["-j"]}')
    provisions_configs_reader.check_programs_existence()
    provisions_configs_reader.check_scripts_existence()
    provisions_configs_reader.check_install_scripts_emptyness()
    provisions_configs_reader.check_uninstall_scripts_emptyness()

    try:
        project.create_project_folder()
        project.provision()
    except (KeyError):
        project.delete_project()


if __name__ == '__main__':
    main()
