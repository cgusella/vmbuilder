"""
Test file for Vagrant.
To launch these tests, add first
$export PYTHONPATH="${PYTHONPATH}:/path-to-vmbuilder/
"""

import unittest
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
            error_msg,
            'error.FlagError: \n\t-n\t[PROJECT NAME]\n\n'
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
            error_msg,
            'error.FlagError: \n\t-vm\t[VBOXNAME]\n\n'
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
            error_msg,
            'error.FlagError: \n\t-t\t[vagrant|packer]\n\n'
        )


if __name__ == '__main__':
    unittest.main()
