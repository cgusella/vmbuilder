#!/bin/python3
import constants
import json
import os
from builder.error import (
    ProgramNotFoundError,
    EmptyScriptError,
    UploadNameConflictError
)
from builder.helper import (
    is_empty_script,
    get_programs_upload_files
)
from newprogram import make_program_folder


class ProvisionConfigReader:
    def __init__(self, builder_provisions_config: dict) -> None:
        self.provisions_configs = builder_provisions_config
        self.provisions = self.provisions_configs["provisions"]
        self.configs = self.provisions_configs["virtual_machine_configs"]

    def check_upload_file_name_duplicates(self):
        """
        Ckeck if some upload file names are equal. If it happens,
        then an error is raised.
        """
        program_upload_files = get_programs_upload_files(
            programs=self.provisions['programs_to_config']
        )
        # join all upload file names into one list
        upload_files = list()
        for program in program_upload_files:
            upload_files.extend(program_upload_files[program])

        # check rindondance between names
        duplicates = list()
        for file in upload_files:
            if upload_files.count(file) > 1:
                duplicates.append(file)
        if duplicates:
            # recover program name for duplicate file
            duplicates_dict = dict()
            duplicates = set(duplicates)

            for file in duplicates:
                for program in program_upload_files:
                    if file in program_upload_files[program]:
                        duplicates_dict[program] = list()
                        duplicates_dict[program].append(file)

            # prepare error message
            error_msg = "\n".join(
                [
                    f'{", ".join(duplicates_dict[program])} in {program}'
                    for program in duplicates_dict
                ]
            )
            raise UploadNameConflictError(
                'Upload files are saved under the same folder, so they have '
                'to be unique before copy them into the project folder.\n'
                'Duplicates files are:\n'
                f'{error_msg}'
            )

    def check_programs_existence_for(self, provision_key: str):
        """
        Chack that programs specified exist.
        If it does not, create a program folder and raise an error
        """
        operation = provision_key.split('_')[-1]
        programs = self.provisions[provision_key]
        not_found_provision_programs = list()
        if programs:
            for program in programs:
                if program not in os.listdir(constants.programs_path):
                    not_found_provision_programs.append(program)
            if not_found_provision_programs:
                make_program_folder(not_found_provision_programs)
                plural = ('s', 'are')
                singular = ('', 'is')
                numerality = plural if len(
                    not_found_provision_programs
                ) > 1 else singular
                error_msg = (
                    'The following program{} '
                    f'{", ".join(not_found_provision_programs)} '
                    '{} created at /templates/programs folder.\nFill the '
                    f'appropriate {operation}.sh files '
                    'and come back then!'.format(*numerality)
                )
                raise ProgramNotFoundError(error_msg)

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
                raise ProgramNotFoundError(error_msg)

    def check_scripts_emptyness_for(self, provision_key: str):
        """
        Check if program shell script is empty for selected operation.
        If it does, raise an exception
        """
        operation = provision_key.split('_')[-1]
        empty_scripts = list()
        for program in self.provisions[provision_key]:
            if is_empty_script(
                f'{constants.programs_path}/{program}/{operation}.sh'
            ):
                empty_scripts.append(program)

        if empty_scripts:
            s = 's' if len(empty_scripts) > 1 else ''
            raise EmptyScriptError(
                f'The script {operation}.sh is empty for program{s} '
                f'{", ".join(empty_scripts)}'
            )

    def check_program_upload_files_existence(self):
        """
        Check that upload file called by config scripts exist
        """
        program_upload_files = get_programs_upload_files(
            programs=self.provisions['programs_to_config']
        )
        # initialize not found file dict
        not_found_files = dict()

        for program in program_upload_files:
            not_found_files[program] = list()
            for upload_file in program_upload_files[program]:
                if upload_file not in os.listdir(
                    f'{constants.programs_path}/{program}/upload'
                ):
                    print('upload_file', upload_file)
                    not_found_files[program].append(upload_file)

        error_msg = ''
        for program in not_found_files:
            if not_found_files[program]:
                error_msg += "\n".join(
                    [
                        f'file {file} for {program}\n'
                        for file in not_found_files[program]
                    ]
                )
        if error_msg:
            plural = ('s', 'do')
            singular = ('', 'does')
            numerality = plural if len(
                not_found_files
            ) > 1 else singular
            raise ProgramNotFoundError(
                'The following file{} '
                '{} not exist in:\n'
                f'{error_msg}'.format(*numerality)
            )
