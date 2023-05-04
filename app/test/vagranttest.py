"""
Test file for Vagrant.
To launch these tests, add first
$export PYTHONPATH="${PYTHONPATH}:/path-to-vmbuilder/
"""
import os
import unittest
from app import constants
from helpertest import missing_flag_error_test

VAGRANT_FLAGS = {"-n": "name", "-vm": "vboxname", "-t": "vagrant",
                 "-u": "user", "-ho": "hostname", "-i": "image",
                 "-j": "provision-file.json", "-s": "key"}


class VagrantCheckFlags(unittest.TestCase):

    def setUp(self) -> None:
        self.vmtype = 'vagrant'

    def test_no_flag_at_all(self):
        """Test correct info are printed when no
        flags are given
        """
        error_msg = missing_flag_error_test(
            flags=["-n", "-vm", "-t", "-u", "-ho", "-i",
                   "-j", "-s"],
            vmtype=self.vmtype
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
            vmtype=self.vmtype
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
            vmtype=self.vmtype
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
            vmtype=self.vmtype
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
            vmtype=self.vmtype
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
            vmtype=self.vmtype
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
            vmtype=self.vmtype
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
            vmtype=self.vmtype
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
            vmtype=self.vmtype
        )
        self.assertIn(
            '-s:\t[VAGRANT SSH CONNECTION TYPE]',
            error_msg,
        )
        self.assertIn(
            'password|key',
            error_msg,
        )


if __name__ == '__main__':
    unittest.main()
