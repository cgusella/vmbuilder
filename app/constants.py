import os

VMBUILDER_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/..'


MACHINE_PATH = f'{VMBUILDER_PATH}/machines'
BUILDS_PATH = f'{VMBUILDER_PATH}/builds'
ISO_PATH = f'{VMBUILDER_PATH}/iso'
PACKAGES_PATH = f'{VMBUILDER_PATH}/packages'
SETUP_SCRIPTS_PATH = f'{VMBUILDER_PATH}/packages/setup_scripts'
CUSTOM_SCRIPTS_PATH = f'{VMBUILDER_PATH}/custom-scripts'


VAGRANT_MACHINES_PATH = f'{VMBUILDER_PATH}/machines/vagrant'
VAGRANT_BUILDS_PATH = f'{VMBUILDER_PATH}/builds/vagrant'
VAGRANT_PROVS_CONFS_PATH = f'{VMBUILDER_PATH}/provisions_configs/vagrant'

PACKER_MACHINES_PATH = f'{VMBUILDER_PATH}/machines/packer'
PACKER_BUILDS_PATH = f'{VMBUILDER_PATH}/builds/packer'
PACKER_PROVS_CONFS_PATH = f'{VMBUILDER_PATH}/provisions_configs/packer'
PACKER_PRESEEDS_PATH = f'{VMBUILDER_PATH}/preseeds'

GUI_PATH = f'{VMBUILDER_PATH}/app/gui'
