#!/bin/python3
import constants
import json
import os
from error import ProgramNotFoundError
from error import ScriptNotFoundError
from error import EmptyScriptError
from error import NoFileToUploadError
from helper import get_upload_files_from_scripts
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
        stop = False
        programs = self.provisions["programs"]
        if programs["install"]:
            not_found_install_programs = list()
            for program in programs["install"]:
                if program not in os.listdir(constants.programs_path):
                    not_found_install_programs.append(program)

            if not_found_install_programs:
                make_program_folder(not_found_install_programs)
                stop = True

        if programs["uninstall"]:
            not_found_uninstall_programs = list()
            for program in programs["uninstall"]:
                if program not in os.listdir(constants.programs_path):
                    not_found_uninstall_programs.append(program)

            if not_found_uninstall_programs:
                make_program_folder(not_found_uninstall_programs)
                stop = True
        if stop:
            programs = not_found_install_programs[:] + not_found_uninstall_programs[:]
            raise ProgramNotFoundError(
                f'The programs {", ".join(programs)} '
                'are created at /templates/programs folder.\nFill the '
                'appropriate files [install.sh, uninstall.sh, config.sh] '
                'and come back then!'
            )

    def check_scripts_existence(self):
        scripts = self.provisions["custom-scripts"]
        if scripts:
            not_found_scripts = list()
            for script in scripts:
                if script not in os.listdir(constants.custom_scripts_path):
                    not_found_scripts.append(script)

            if not_found_scripts:
                raise ScriptNotFoundError(f'Scripts {", ".join(not_found_scripts)} not found!')

    def check_install_scripts_emptyness(self):
        empty_scripts = list()
        for program in self.provisions['programs']['install']:
            with open(f'{constants.programs_path}/{program}/install.sh') as install_script:
                lines = set(install_script.readlines())

            lines = lines.difference(set(['#!/bin/bash', '#!/bin/bash\n']))
            empty_file = not any(lines)

            if empty_file:
                empty_scripts.append(program)

        if empty_scripts:
            raise EmptyScriptError(f'The script install.sh is empty for programs {", ".join(empty_scripts)}')

    def check_uninstall_scripts_emptyness(self):
        empty_scripts = list()
        for program in self.provisions['programs']['uninstall']:
            with open(f'{constants.programs_path}/{program}/uninstall.sh') as uninstall_script:
                lines = set(uninstall_script.readlines())

            lines = lines.difference(set(['#!/bin/bash', '#!/bin/bash\n']))
            empty_file = not any(lines)

            if empty_file:
                empty_scripts.append(program)

        if empty_scripts:
            raise EmptyScriptError(f'The script uninstall.sh is empty for programs {", ".join(empty_scripts)}')

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
                    'The missing files to upload are '
                    f'{", ".join(missing_files_to_upload)}'
                )

    def check_script_dependency_from_file_to_upload(self):
        upload_files = get_upload_files_from_scripts(
            self.provisions['custom-scripts']
        )
        missing_files_to_upload = list()
        for file in upload_files:
            if file not in self.provisions['files-to-upload']:
                missing_files_to_upload.append(file)
        if upload_files and not self.provisions['upload']:
            raise NoFileToUploadError(
                f'Files {", ".join(upload_files)} '
                'are requested by scripts. Be sure to set "upload" as true '
                'in json file'
            )
        if missing_files_to_upload:
            raise NoFileToUploadError(
                f'Files {", ".join(missing_files_to_upload)} '
                'are requested by scripts. Be sure to include them '
                'into "files-to-upload"'
            )
