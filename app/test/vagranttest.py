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
from builder.error import ExistenceProjectError
from builder.error import JsonConfigCopiedError
from builder.vagrant import Vagrant


def generate_new_name_in(folder_path: str):
    """Generate and return a string which mock the name
    of a file or folder that does not exist in the given
    folder
    """
    name_in_folder = False
    while not name_in_folder:
        random_file_name = f"""{''.join(
            random.choices(string.ascii_lowercase, k=5)
        )}.json"""
        if random_file_name not in os.listdir(folder_path):
            name_in_folder = True
    return random_file_name


class VagrantCommonFlagsTest(unittest.TestCase):

    def setUp(self):
        """
        Set namespace with name attribute only.
        If there are not vagrant machine, a new name is generated.
        """
        self.namespace = Namespace()
        self.created_new_project_folder = False
        try:
            self.namespace.name = os.listdir(constants.vagrant_machines_path)[0]
        except IndexError:
            self.namespace.name = generate_new_name_in(
                constants.vagrant_machines_path
            )
            os.mkdir(
                f'{constants.vagrant_machines_path}/{self.namespace.name}'
            )
            self.created_new_project_folder = True

    def tearDown(self):
        """Delete project folder if it was created in setUp."""
        if self.created_new_project_folder:
            os.rmdir(
                f'{constants.vagrant_machines_path}/{self.namespace.name}'
            )

    def test_check_new_project_folder_existence(self):
        """
        Test that an error is raised when a project with a given
        name already exists
        """
        vagrant = Vagrant(self.namespace)
        with self.assertRaises(ExistenceProjectError):
            vagrant.check_new_project_folder_existence()

    def test_check_provision_cfg_json_existence(self):
        """
        Test that an error is raised and a new json is created when a
        non existing json file is specified
        """
        json_name = generate_new_name_in(
            constants.vagrant_provs_confs_path
        )
        self.namespace.json = f'{json_name}.json'
        vagrant = Vagrant(self.namespace)
        with self.assertRaises(JsonConfigCopiedError):
            vagrant.check_provision_cfg_json_existence()

        self.assertIn(
            f'{json_name}.json',
            os.listdir(constants.vagrant_provs_confs_path)
        )
        os.remove(f'{constants.vagrant_provs_confs_path}/{json_name}.json')


class VagrantAllFlagsTest(unittest.TestCase):

    def setUp(self):
        self.namespace = Namespace()
        self.namespace.name = generate_new_name_in(
            constants.vagrant_machines_path
        )

    def test_create_project_folder(self):
        """Test that a new project is generated with the wanted structure"""
        vagrant = Vagrant(self.namespace)
        vagrant.create_project_folder()
        self.assertIn(
            self.namespace.name,
            os.listdir(constants.vagrant_machines_path)
        )
        self.assertIn(
            "upload",
            os.listdir(
                f'{constants.vagrant_machines_path}/{self.namespace.name}'
            )
        )
        vagrant.delete_project()



if __name__ == '__main__':
    unittest.main()
