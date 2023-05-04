"""
Test file for Vagrant.
To launch these tests, add first
$export PYTHONPATH="${PYTHONPATH}:/path-to-vmbuilder/
"""
import random
import string
import os
import unittest
from app import constants
from helpertest import (
    missing_flag_error_test,
    launch_main_with_custom_arguments
)

VAGRANT_FLAGS = {"-n": "name", "-vm": "vboxname", "-t": "vagrant",
                 "-u": "user", "-ho": "hostname", "-i": "image",
                 "-j": "provision-file.json", "-s": "key"}

VMTYPE = 'vagrant'


class VagrantCheckFlags(unittest.TestCase):

    def test_no_flag_at_all(self):
        """Test correct info are printed when no
        flags are given
        """
        error_msg = missing_flag_error_test(
            flags=["-n", "-vm", "-t", "-u", "-ho", "-i",
                   "-j", "-s"],
            vmtype=VMTYPE
        )
        self.assertIn(
            '-n\t[PROJECT NAME]',
            error_msg
        )
        self.assertIn(
            '-vm\t[VBOXNAME]',
            error_msg
        )
        self.assertIn(
            '-t\tvagrant',
            error_msg
        )
        self.assertIn(
            '-u:\t\t[EXTRA SUDOER USER]',
            error_msg
        )
        self.assertIn(
            '-ho:\t\t[HOSTNAME]',
            error_msg
        )
        self.assertIn(
            '-i:\t\t[VAGRANT IMAGE]',
            error_msg
        )
        self.assertIn(
            '-j:\t\t[VAGRANT PROVISION FILE]',
            error_msg
        )
        self.assertIn(
            '-s:\t\t[VAGRANT SSH CONNECTION TYPE]',
            error_msg
        )
        self.assertIn(
            '-t\tpacker',
            error_msg
        )
        self.assertIn(
            '-il:\t\t[ISO LINK]',
            error_msg
        )
        self.assertIn(
            '-if:\t\t[ISO FILE]',
            error_msg
        )
        self.assertIn(
            '-cs:\t\t[CHECKSUM]',
            error_msg
        )
        self.assertIn(
            '-j:\t\t[PACKER CONFIG FILE]',
            error_msg
        )
        self.assertIn(
            '-pf:\t\t[PRESEED FILE]',
            error_msg
        )

    def test_no_flag_name(self):
        """Test if error message is printed when "-n"
        flag is not specified
        """
        error_msg = missing_flag_error_test(
            flags=["-n"],
            vmtype=VMTYPE
        )
        self.assertEqual(
            'error.FlagError: \n\t-n\t[PROJECT NAME]\n\n',
            error_msg
        )

    def test_no_flag_box(self):
        """Test if error message is printed when "-vm"
        flag is not specified
        """
        error_msg = missing_flag_error_test(
            flags=["-vm"],
            vmtype=VMTYPE
        )
        self.assertEqual(
            'error.FlagError: \n\t-vm\t[VBOXNAME]\n\n',
            error_msg
        )

    def test_no_flag_type(self):
        """Test if error message is printed when "-t"
        flag is not specified
        """
        error_msg = missing_flag_error_test(
            flags=["-t"],
            vmtype=VMTYPE
        )
        self.assertEqual(
            'error.FlagError: \n\t-t\t[vagrant|packer]\n\n',
            error_msg
        )

    def test_no_flag_user(self):
        """Test if error message is printed when "-u"
        flag is not specified
        """
        error_msg = missing_flag_error_test(
            flags=["-u"],
            vmtype=VMTYPE
        )
        self.assertIn(
            '-u:\t[EXTRA SUDOER USER]',
            error_msg,
        )

    def test_no_flag_hostname(self):
        """Test if error message is printed when "-ho"
        flag is not specified
        """
        error_msg = missing_flag_error_test(
            flags=["-ho"],
            vmtype=VMTYPE
        )
        self.assertIn(
            '-ho:\t[HOSTNAME]',
            error_msg,
        )

    def test_no_flag_image(self):
        """Test if error message is printed when "-i"
        flag is not specified
        """
        error_msg = missing_flag_error_test(
            flags=["-i"],
            vmtype=VMTYPE
        )
        self.assertIn(
            '-i:\t[VAGRANT IMAGE]',
            error_msg,
        )

    def test_no_flag_provision_file(self):
        """Test if error message is printed when "-j"
        flag is not specified
        """
        error_msg = missing_flag_error_test(
            flags=["-j"],
            vmtype=VMTYPE
        )
        self.assertIn(
            '-j:\t[VAGRANT PROVISION FILE]',
            error_msg,
        )
        for provision_file in os.listdir(constants.vagrant_provs_confs_path):
            self.assertIn(
                provision_file,
                error_msg
            )

    def test_no_flag_connection(self):
        """Test if error message is printed when "-s"
        flag is not specified
        """
        error_msg = missing_flag_error_test(
            flags=["-s"],
            vmtype=VMTYPE
        )
        self.assertIn(
            '-s:\t[VAGRANT SSH CONNECTION TYPE]',
            error_msg,
        )
        self.assertIn(
            'password|key',
            error_msg,
        )


class VagrantCheckFolderVbJsonExistence(unittest.TestCase):

    def test_check_new_project_folder_existence(self):
        # new_project_name_in_folder = False
        # while not new_project_name_in_folder:
        #     new_project_name = ''.join(
        #         random.choices(string.ascii_lowercase, k=5)
        #     )
        #     created_machines = os.listdir(constants.vagrant_machines_path)
        #     if new_project_name in created_machines:
        #         new_project_name_in_folder = True
        existing_machines = os.listdir(constants.vagrant_machines_path)
        if existing_machines:
            error_msg = launch_main_with_custom_arguments(
                {"-n": f"{existing_machines[0]}"},
                vmtype=VMTYPE
            )
            self.assertIn(
                "ExistenceProjectError",
                error_msg
            )
        else:
            os.mkdir(f"{constants.vagrant_machines_path}/test")
            error_msg = launch_main_with_custom_arguments(
                {"-n": "test"},
                vmtype=VMTYPE
            )
            self.assertIn(
                "ExistenceProjectError",
                error_msg
            )
            os.rmdir(f"{constants.vagrant_machines_path}/test")


if __name__ == '__main__':
    unittest.main()
