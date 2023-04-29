import os

vmbuilder_path = f'{os.path.dirname(os.path.realpath(__file__))}/..'


machines_path       = f'{vmbuilder_path}/machines'
templates_path      = f'{vmbuilder_path}/templates'
builds_path         = f'{vmbuilder_path}/builds'
iso_path            = f'{vmbuilder_path}/iso'
programs_path       = f'{vmbuilder_path}/templates/programs'
custom_scripts_path = f'{vmbuilder_path}/templates/custom-scripts'
upload_path         = f'{vmbuilder_path}/templates/upload'


vagrant_machines_path    = f'{vmbuilder_path}/machines/vagrant'
vagrant_templates_path   = f'{vmbuilder_path}/templates/vagrant'
vagrant_builds_path      = f'{vmbuilder_path}/builds/vagrant'
vagrant_provs_confs_path = f'{vmbuilder_path}/templates/vagrant/provisions_configs'

packer_machines_path    = f'{vmbuilder_path}/machines/packer'
packer_templates_path   = f'{vmbuilder_path}/templates/packer'
packer_builds_path      = f'{vmbuilder_path}/builds/packer'
packer_provs_confs_path = f'{vmbuilder_path}/templates/packer/provisions_configs'
packer_http_path = f'{vmbuilder_path}/templates/packer/http'
