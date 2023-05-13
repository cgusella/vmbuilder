"""
Test file for Vagrant.
To launch these tests, add first
$export PYTHONPATH="${PYTHONPATH}:/path-to-app/
"""
import constants
import os
import random
import string
import unittest
from argparse import Namespace
from argumentparser.customparser import CustomArgumentParser
from builder.error import ExistenceProjectError
from builder.vagrant import Vagrant


def generate_name_in_folder(folder_path: str):
    """Generate and return a string which mock the name
    of a file or folder that does not exist in the given folder
    """
    name_in_folder = False
    while not name_in_folder:
        random_file_name = f"""{''.join(
            random.choices(string.ascii_lowercase, k=5)
        )}.json"""
        if random_file_name not in os.listdir(folder_path):
            name_in_folder = True
    return random_file_name


class VagrantTest(unittest.TestCase):

    def test_check_new_project_folder_existence(self):
        """
        Test that an error is raised when a project with a given
        name already exists
        """
        namespace_test = Namespace()
        project_name = generate_name_in_folder(
            folder_path=constants.vagrant_machines_path
        )
        namespace_test.name = project_name
        self.vagrant = Vagrant(namespace_test)
        os.mkdir(f'{constants.vagrant_machines_path}/{project_name}')
        with self.assertRaises(ExistenceProjectError):
            self.vagrant.check_new_project_folder_existence()
        os.rmdir(f'{constants.vagrant_machines_path}/{project_name}')


if __name__ == '__main__':
    unittest.main()
