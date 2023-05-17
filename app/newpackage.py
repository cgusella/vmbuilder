#!/bin/python3
import argparse
import os
import constants


def make_package_folder(packages: list = []):
    if not packages:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-p', '--package-name', dest='packages', required=True,
            help='define new package name to add in template/packages',
            nargs='+'
        )
        arguments = parser.parse_args()
        packages = arguments.packages

    for package in packages:
        new_package_path = f'{constants.packages_path}/{package}'
        # create package folder
        os.mkdir(new_package_path)
        # create config file in configs
        with open(f'{new_package_path}/config.sh', 'w') as config_file:
            config_file.write("#!/bin/bash")
        # create upload folder
        os.mkdir(f'{new_package_path}/upload')
        # create prepare to upload file
        with open(
            file=f'{new_package_path}/upload/prepare_to_upload.sh',
            mode='w'
        ) as upload_file:
            upload_file.write("#!/bin/bash")
        # create install file
        with open(f'{new_package_path}/install.sh', 'w') as install_file:
            install_file.write("#!/bin/bash")
        # create uninstall file
        with open(f'{new_package_path}/uninstall.sh', 'w') as uninstall_file:
            uninstall_file.write("#!/bin/bash")


if __name__ == '__main__':
    make_package_folder()
