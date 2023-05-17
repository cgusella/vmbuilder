"""
Test file for controller.
To launch these tests, add first
$export PYTHONPATH="${PYTHONPATH}:/path-to-app/
"""
import constants
import os
import shutil
import unittest
from argparse import Namespace
from builder.vagrant import Vagrant
from existencecontroller.test import generate_new_name_in


class VagrantBuilder(unittest.TestCase):

    def test_create_project_folder(self):
        """Test that a project folder with the wanted structure is created"""
        new_project_folder = generate_new_name_in(constants.VAGRANT_MACHINES_PATH)
        namespace = Namespace()
        namespace.name = new_project_folder
        vagrant = Vagrant(namespace=namespace, json_file=dict())
        vagrant.create_project_folder()

        self.assertIn(
            new_project_folder,
            os.listdir(constants.VAGRANT_MACHINES_PATH)
        )
        self.assertIn(
            'upload',
            os.listdir(f'{constants.VAGRANT_MACHINES_PATH}/{new_project_folder}')
        )
        shutil.rmtree(f'{constants.VAGRANT_MACHINES_PATH}/{new_project_folder}')


if __name__ == '__main__':
    unittest.main()
