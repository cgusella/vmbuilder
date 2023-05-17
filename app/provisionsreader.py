#!/bin/python3
import constants
import json
import os
from argparse import Namespace
from builder.error import (
    PackageNotFoundError,
    EmptyScriptError,
    UploadNameConflictError
)
from builder.helper import (
    is_empty_script,
    get_packages_upload_files
)
from newpackage import make_package_folder


class ProvisionConfigReader:
    def __init__(self, namespace: Namespace) -> None:
        if namespace.vm_type == 'vagrant':
            provision_config_file_path = constants.vagrant_provs_confs_path
        elif namespace.vm_type == 'packer':
            provision_config_file_path = constants.packer_provs_confs_path
        with open(f'{provision_config_file_path}/{namespace.json}') as provs_confs_file:
            self.json_file = json.loads(provs_confs_file.read())
        self.provisions = self.json_file["provisions"]
        self.configs = self.json_file["virtual_machine_configs"]

    def check_upload_file_name_duplicates(self):
        """
        Ckeck if some upload file names are equal. If it happens,
        then an error is raised.
        """
        package_upload_files = get_packages_upload_files(
            packages=self.provisions['packages_to_config']
        )
        # join all upload file names into one list
        upload_files = list()
        for package in package_upload_files:
            upload_files.extend(package_upload_files[package])

        # check rindondance between names
        duplicates = list()
        for file in upload_files:
            if upload_files.count(file) > 1:
                duplicates.append(file)
        if duplicates:
            # recover package name for duplicate file
            duplicates_dict = dict()
            duplicates = set(duplicates)

            for file in duplicates:
                for package in package_upload_files:
                    if file in package_upload_files[package]:
                        duplicates_dict[package] = list()
                        duplicates_dict[package].append(file)

            # prepare error message
            error_msg = "\n".join(
                [
                    f'{", ".join(duplicates_dict[package])} in {package}'
                    for package in duplicates_dict
                ]
            )
            raise UploadNameConflictError(
                'Upload files are saved under the same folder, so they have '
                'to be unique before copy them into the project folder.\n'
                'Duplicates files are:\n'
                f'{error_msg}'
            )

    def check_packages_existence_for(self):
        """
        Chack that packages specified exist.
        If it does not, create a package folder and raise an error
        """
        provisions_to_check = {"packages_to_install", "packages_to_uninstall", "packages_to_config"}
        operation_packages = dict()
        for provision_to_check in provisions_to_check:
            operation = provision_to_check.split('_')[-1]
            operation_packages[operation] = list()
            packages = self.provisions[provision_to_check]
            if packages:
                for package in packages:
                    if package not in os.listdir(constants.packages_path):
                        operation_packages[operation].append(package)

        if any(operation_packages.values()):
            error_msg = 'The following scripts are empty: \n'
            for operation in operation_packages:
                if operation_packages[operation]:
                    error_msg += f'{operation}.sh for {", ".join(operation_packages[operation])}\n'
                    make_package_folder(operation_packages[operation])
            raise PackageNotFoundError(error_msg)

    def check_custom_script_existence(self):
        """
        Check if custom scripts specified into the JSON exist. If it is not,
        raise an error
        """
        scripts = self.provisions["custom_scripts"]
        not_found_scripts = list()
        if scripts:
            for script in scripts:
                if script not in os.listdir(constants.custom_scripts_path):
                    not_found_scripts.append(script)
            if not_found_scripts:
                plural = ('s', 'do')
                singular = ('', 'does')
                numerality = plural if len(
                    not_found_scripts
                ) > 1 else singular
                error_msg = (
                    'The following script{} '
                    f'{", ".join(not_found_scripts)} '
                    '{} not exist.'.format(*numerality)
                )
                raise PackageNotFoundError(error_msg)

    def check_scripts_emptyness_for(self, provision_key: str):
        """
        Check if package shell script is empty for selected operation.
        If it does, raise an exception
        """
        operation = provision_key.split('_')[-1]
        empty_scripts = list()
        for package in self.provisions[provision_key]:
            if is_empty_script(
                f'{constants.packages_path}/{package}/{operation}.sh'
            ):
                empty_scripts.append(package)

        if empty_scripts:
            s = 's' if len(empty_scripts) > 1 else ''
            raise EmptyScriptError(
                f'The script {operation}.sh is empty for package{s} '
                f'{", ".join(empty_scripts)}'
            )

    def check_package_upload_files_existence(self):
        """
        Check that upload file called by config scripts exist
        """
        package_upload_files = get_packages_upload_files(
            packages=self.provisions['packages_to_config']
        )
        # initialize not found file dict
        not_found_files = dict()

        for package in package_upload_files:
            not_found_files[package] = list()
            for upload_file in package_upload_files[package]:
                if upload_file not in os.listdir(
                    f'{constants.packages_path}/{package}/upload'
                ):
                    not_found_files[package].append(upload_file)

        error_msg = ''
        for package in not_found_files:
            if not_found_files[package]:
                error_msg += "\n".join(
                    [
                        f'file {file} for {package}\n'
                        for file in not_found_files[package]
                    ]
                )
        if error_msg:
            plural = ('s', 'do')
            singular = ('', 'does')
            numerality = plural if len(
                not_found_files
            ) > 1 else singular
            raise PackageNotFoundError(
                'The following file{} '
                '{} not exist in:\n'
                f'{error_msg}'.format(*numerality)
            )
