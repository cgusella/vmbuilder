"""
Test file for Vagrant.
To launch these tests, add first
$export PYTHONPATH="${PYTHONPATH}:/path-to-vmbuilder/
"""

import subprocess
import unittest
from app.constants import vmbuilder_path

VAGRANT_FLAGS = {"-n": "name", "-vm": "vboxname", "-t": "vagrant",
                 "-u": "user", "-ho": "hostname", "-i": "image",
                 "-j": "provision-file.json", "-s": "key"}


class VagrantCheckFlags(unittest.TestCase):

    def no_common_flag_test(self, flag: str, msg: str):
        vagrant_flags = VAGRANT_FLAGS.copy()
        del vagrant_flags[flag]
        argv = list()
        for vagrant_flag in vagrant_flags:
            argv.append(vagrant_flag)
            argv.append(vagrant_flags[vagrant_flag])
        argv.insert(0, f'{vmbuilder_path}/app/main.py')
        result = subprocess.run(
            args=argv,
            capture_output=True
        )
        self.assertEqual(
            result.stderr.decode('ascii'),
            f'error.FlagError: \n\t{flag}\t[{msg}]\n\n'
        )

    def test_no_flag_name(self):
        self.no_common_flag_test(
            flag="-n",
            msg="PROJECT NAME"
        )

    def test_no_flag_box(self):
        self.no_common_flag_test(
            flag="-vm",
            msg="VBOXNAME"
        )

    def test_no_flag_type(self):
        self.no_common_flag_test(
            flag="-t",
            msg="vagrant|packer"
        )


if __name__ == '__main__':
    unittest.main()
