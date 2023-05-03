#!/bin/python3
import constants
import json
import os
from error import (
    ProgramNotFoundError,
    ScriptNotFoundError,
    EmptyScriptError,
    NoFileToUploadError
)
from helper import (
    get_upload_files_from_scripts,
    empty_script
)
from newprogram import make_program_folder


class ProvisionConfigReader:
    def __init__(self, provisions_config_file_path: str) -> None:
        self.file_path = provisions_config_file_path
        self.set_provisions()
        self.set_configs()

    def set_provisions(self):
        with open(self.file_path, 'r') as provision_config_file:
            self.provisions = json.loads(provision_config_file.read())["vbox-provisions"]

    def set_configs(self):
        with open(self.file_path, 'r') as provision_config_file:
            self.configs = json.loads(provision_config_file.read())["vbox-configs"]

    def check_programs_existence(self):
        programs = self.provisions["programs"]
        not_found_install_programs = list()
        if programs["install"]:
            for program in programs["install"]:
                if program not in os.listdir(constants.programs_path):
                    not_found_install_programs.append(program)

            if not_found_install_programs:
                make_program_folder(not_found_install_programs)

        not_found_uninstall_programs = list()
        if programs["uninstall"]:
            for program in programs["uninstall"]:
                if program not in os.listdir(constants.programs_path):
                    not_found_uninstall_programs.append(program)

            if not_found_uninstall_programs:
                make_program_folder(not_found_uninstall_programs)

        programs_not_found = (
            not_found_install_programs[:] + not_found_uninstall_programs[:]
        )
        if programs_not_found:
            plural = ('s', 'are')
            singular = ('', 'is')
            numerality = plural if len(programs_not_found) > 1 else singular
            error_msg = (
                'The following program{} '
                f'{", ".join(programs_not_found)} '
                '{} created at /templates/programs folder.\nFill the '
                'appropriate files [install.sh, uninstall.sh, config.sh] '
                'and come back then!'.format(*numerality)
            )
            raise ProgramNotFoundError(error_msg)

    def check_scripts_existence(self):
        scripts = self.provisions["custom-scripts"]
        if scripts:
            not_found_scripts = list()
            for script in scripts:
                if script not in os.listdir(constants.custom_scripts_path):
                    not_found_scripts.append(script)

            if not_found_scripts:
                s = 's' if len(not_found_scripts) > 1 else ''
                raise ScriptNotFoundError(f'Custom script{s} {", ".join(not_found_scripts)} not found!')

    def check_install_scripts_emptyness(self):
        empty_scripts = list()
        for program in self.provisions['programs']['install']:
            empty_file, _ = empty_script(f'{constants.programs_path}/{program}/install.sh')

            if empty_file:
                empty_scripts.append(program)

        if empty_scripts:
            s = 's' if len(empty_scripts) > 1 else ''
            raise EmptyScriptError(f'The script install.sh is empty for program{s} {", ".join(empty_scripts)}')

    def check_uninstall_scripts_emptyness(self):
        empty_scripts = list()
        for program in self.provisions['programs']['uninstall']:
            empty_file, _ = empty_script(f'{constants.programs_path}/{program}/uninstall.sh')

            if empty_file:
                empty_scripts.append(program)

        if empty_scripts:
            raise EmptyScriptError(f'The script "uninstall.sh" is empty for programs {", ".join(empty_scripts)}')

    def check_upload_files_existence(self):
        if self.provisions['upload']:
            if not self.provisions['files-to-upload']:
                raise NoFileToUploadError(
                    'There is no file to upload. Be sure '
                    'to set "upload" to false if you do not '
                    'want to upload any file.'
                )
            files_to_upload = self.provisions['files-to-upload']
            missing_files_to_upload = list()
            for file in files_to_upload:
                if file not in os.listdir(constants.upload_path):
                    missing_files_to_upload.append(file)
            if missing_files_to_upload:
                raise NoFileToUploadError(
                    'The following files are missing from upload folder:\n'
                    f'{", ".join(missing_files_to_upload)}'
                )

    def check_script_dependency_from_file_to_upload(self):
        upload_files_scripts = get_upload_files_from_scripts(
            self.provisions['custom-scripts']
        )
        missing_files_to_upload = list()
        for file in upload_files_scripts:
            if file not in self.provisions['files-to-upload']:
                missing_files_to_upload.append(file)
        err_msg_singular = (
            'The following file is requested by the script.\n'
        )
        err_msg_plural = (
            'The following files are requested by the scripts.\n'
        )
        if upload_files_scripts and not self.provisions['upload']:
            error_msg = err_msg_plural if len(missing_files_to_upload) > 1 else err_msg_singular

            error_msg += '\n'.join(
                [f"--> {file} by\t {upload_files_scripts[file]}"
                 for file in missing_files_to_upload]
            )
            error_msg += '\nBe sure to set "upload" as true in the json file\n'
            raise NoFileToUploadError(error_msg)
        if missing_files_to_upload:
            error_msg = err_msg_plural if len(missing_files_to_upload) > 1 else err_msg_singular

            error_msg += '\n'.join(
                [f'\t--> {file} by\t {upload_files_scripts[file]}'
                 for file in missing_files_to_upload])
            error_msg += '\nBe sure to include them into "files-to-upload" in the json file\n'
            raise NoFileToUploadError(error_msg)
