#!/bin/python3
import argparse
import os

vmbuilder_path = f'{os.getcwd()}/..'


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
    open(f'{new_program_path}/configs/config.sh', 'w')
    # create install file
    open(f'{new_program_path}/install.sh', 'w')


if __name__ == '__main__':
    main()
