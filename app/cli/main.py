#!/usr/bin/python3
import sys
from argparse import Namespace
from argumentparser.customparser import CustomArgumentParser
from cli.provisionsreader import ProvisionConfigReader
from builder.packer import Packer
from builder.vagrant import Vagrant
from builder.builder import Builder
from existencecontroller.controller import VagrantController, PackerController


def get_project_class(namespace: Namespace, json_file: dict) -> Builder:
    project_type = namespace.vm_type
    if project_type == 'vagrant':
        return Vagrant(
            json_file=json_file
        )
    if project_type == 'packer':
        return Packer(
            namespace=namespace,
            json_file=json_file
        )


def get_controller_class(namespace: Namespace):
    if namespace.vm_type == 'vagrant':
        return VagrantController(namespace=namespace)
    elif namespace.vm_type == 'packer':
        return PackerController(namespace=namespace)


def main():
    # flags parsing
    namespace = CustomArgumentParser().get_namespace()

    # debug mode to see traceback errors
    if not namespace.debug:
        sys.tracebacklimit = 0

    # start control
    controller = get_controller_class(namespace=namespace)
    controller.check_virtualbox_existence()
    controller.check_json_existence()
    controller.check_new_project_folder_existence()
    json_file = controller.get_json_with_flags_values()

    # read selected json
    provisions_configs_reader = ProvisionConfigReader(json_file)
    provisions_configs_reader.check_packages_existence_for()

    provisions_configs_reader.check_package_upload_files_existence()
    provisions_configs_reader.check_upload_file_name_duplicates()
    provisions_configs_reader.check_custom_script_existence()
    provisions_configs_reader.check_update_upgrade_type()
    provisions_configs_reader.check_if_clean_is_selected()

    # build new project
    builder = get_project_class(
        json_file=provisions_configs_reader.json_file
    )
    builder.set_configs()
    builder.set_provisions()
    builder.set_credentials()
    builder.create_project_folder()
    builder.generate_main_file()


if __name__ == '__main__':
    main()
