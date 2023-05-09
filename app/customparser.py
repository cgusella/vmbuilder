import argparse
import logging
import sys
import constants
from helper import (
    get_json_files_for_help,
    get_vagrant_images_for_help,
)

logger = logging.getLogger('vmbuilder')


class CustomArgumentParser:

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            prog='vmbuilder',
            description='Create a virtual machines, Vagrant or Packer'
        )
        if not sys.argv[1:]:
            logger.error('Need arguments. Specify "-h/--help" for more info')
            exit()
        elif sys.argv[1:][0] in ['-h', '--help']:
            self.parse_all_arguments()
            exit()

    def get_namespace(self):
        self.add_common_flags()
        common_namespace, _ = self.parser.parse_known_args()
        if common_namespace.vmtype == 'vagrant':
            self.add_vagrant_args()
        elif common_namespace.vmtype == 'packer':
            self.add_packer_args()

        return self.parser.parse_args()

    def add_common_flags(self):
        """Add flags common with both Vagrant and Packer"""
        self.parser.add_argument(
            '-n', '--name', required=True
        )
        self.parser.add_argument(
            '-vm', '--vboxname', required=True
        )
        self.parser.add_argument(
            '-t', '--vmtype',
            dest='vmtype',
            choices=['vagrant', 'packer'],
            required=True
        )

    def parse_all_arguments(self):
        self.add_common_flags()
        self.add_vagrant_args()
        self.add_packer_args()
        return self.parser.parse_args()

    def add_vagrant_args(self):
        """Parse vagrant argument"""
        vagrant_flags = self.parser.add_argument_group(
            'Vagrant flags',
            'manage vagrant flags'
        )
        vagrant_flags.add_argument('-u', '--user', dest='user', required=False)
        vagrant_flags.add_argument('-o', '--hostname', dest='hostname',
                                   required=True)
        vagrant_flags.add_argument('-i', '--image', dest='image',
                                   help=get_vagrant_images_for_help(),
                                   required=True)
        vagrant_flags.add_argument(
            '-vj',
            '--vagrantjson',
            dest='json',
            help=get_json_files_for_help(
                constants.vagrant_provs_confs_path
            ),
            required=True
        )
        vagrant_flags.add_argument(
            '-s',
            '--ssh',
            dest='connection',
            choices=['password', 'key'],
            required=True
        )

    def add_packer_args(self):
        """Parse vagrant argument"""
        packer_flags = self.parser.add_argument_group(
            'Packer flags',
            'manage packer flags'
        )
        packer_flags.add_argument('-il', '--isolink', dest='isolink',
                                  required=True)
        packer_flags.add_argument('-if', '--isofile', dest='isofile',
                                  required=True)
        packer_flags.add_argument('-cs', '--checksum', dest='checksum',
                                  required=True)
        packer_flags.add_argument(
            '-pj',
            '--packerjson',
            dest='json',
            help=get_json_files_for_help(
                constants.packer_provs_confs_path
            ),
            required=True
        )
        packer_flags.add_argument('-pf', '--preseedfile', dest='preseed')
