# vmbuilder

## Description

This project manage and create customized virtual machine.
You can create two kinds of machines: Packer or Vagrant.
The customization is first setted using a JSON object saved in
    * /templates/packer/provisions_configs;
    * /templates/vagrant/provisions_configs.

## Vagrant Machine

First create a new json file you find in the provision
config folder and set the variables. These are:
    * vbox-configs: these variables set the machine configuration
        * default_user: vagrant machine default user;
        * default_pass: vagrant machine default password;
        * api_version:;
        * disk_size: dimension in MB reserved to the machine.
    * vbox-provisions: these set the program installation configuration
        * programs: this contains
            * init: bool. If True, add the apt update command at the top of the Vagrantfile;
            * install: list. It is a list of program names you want to install;
            * uninstall: list. It is a list of program names you want to uninstall from your machine;
            * clean: bool. If True, add the clean, autoremove, autoclean command at the bottom of the Vagrantfile.
        * custom-scripts: list. A list of script name saved in /templates/custom-scripts that you want to add at your Vagrantfile;
        * upload: bool. If True, the folder contenents will be loaded into the machine volume.