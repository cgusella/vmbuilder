#!/bin/python3
import argparse
import os


vmbuilder_path = f'{os.path.dirname(os.path.realpath(__file__))}/..'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--program-name', dest='program', required=True,
        help='define new program name to add in template/programs'
    )
    arguments = parser.parse_args()

    new_program_path = f'{vmbuilder_path}/templates/programs/{arguments.program}'
    # create program folder
    os.mkdir(new_program_path)
    # create configs folder
    os.mkdir(f'{new_program_path}/configs')
    # create config file in configs
    with open(f'{new_program_path}/configs/config.sh', 'w') as config_file:
        config_file.write("#!/bin/bash")
    # create install file
    with open(f'{new_program_path}/install.sh', 'w') as install_file:
        install_file.write("#!/bin/bash")
    # create uninstall file
    with open(f'{new_program_path}/uninstall.sh', 'w') as uninstall_file:
        uninstall_file.write("#!/bin/bash")


if __name__ == '__main__':
    main()
