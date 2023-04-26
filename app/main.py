#!/usr/bin/python3
from builder import get_project_class
from provisionsreader import ProvisionConfigReader
import sys
import logging
import os


sys.tracebacklimit = 0
vmbuilder_path = f'{os.path.dirname(os.path.realpath(__file__))}/..'


def main():
    project = get_project_class()
    project.check_flags()
    project.check_folder_vb_existence()
    provisions_configs_reader = ProvisionConfigReader(f'{project.provisions_configs}/{project.arguments["-j"]}')
    provisions_configs_reader.check_programs_existence()
    provisions_configs_reader.check_scripts_existence()

    try:
        project.create_project_folder()
        project.provision()
    except (FileNotFoundError, KeyError) as error:
        logging.error(error)
        project.delete_project()


if __name__ == '__main__':
    main()
