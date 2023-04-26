#!/bin/python3
import json
import os
from error import ProgramNotFoundError
from error import ScriptNotFoundError


vmbuilder_path = f'{os.getcwd()}/..'


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
        if programs["install"]:
            not_found_programs = list()
            for program in programs["install"]:
                if program not in os.listdir(f'{vmbuilder_path}/templates/programs'):
                    not_found_programs.append(program)

            if not_found_programs:
                raise ProgramNotFoundError(f'Programs {", ".join(not_found_programs)} not found!')
        if programs["uninstall"]:
            not_found_programs = list()
            for program in programs["uninstall"]:
                if program not in os.listdir(f'{vmbuilder_path}/templates/programs'):
                    not_found_programs.append(program)

            if not_found_programs:
                raise ProgramNotFoundError(f'Programs {", ".join(not_found_programs)} not found!')

    def check_scripts_existence(self):
        scripts = self.provisions["custom-scripts"]
        if scripts:
            not_found_scripts = list()
            for script in scripts:
                if script not in os.listdir(f'{vmbuilder_path}/templates/custom-scripts'):
                    not_found_scripts.append(script)

            if not_found_scripts:
                raise ScriptNotFoundError(f'Scripts {", ".join(not_found_scripts)} not found!')
