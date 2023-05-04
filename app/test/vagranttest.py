"""
Test file for Vagrant.
To launch these tests, add first
$export PYTHONPATH="${PYTHONPATH}:/path-to-vmbuilder/
"""

import subprocess
import unittest
from app.constants import vmbuilder_path
from helpertest import missing_flag_error_test

VAGRANT_FLAGS = {"-n": "name", "-vm": "vboxname", "-t": "vagrant",
                 "-u": "user", "-ho": "hostname", "-i": "image",
                 "-j": "provision-file.json", "-s": "key"}


class VagrantCheckFlags(unittest.TestCase):

    def setUp(self) -> None:
        self.vmtype = 'vagrant'

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
