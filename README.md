# vmbuilder
## Work in progress.
If you want to try, launch   
>$ ./main.py -h  

or  
 >$ python3 main.py -h  
 
to let you be surprised!

## Purpose
This application wants to make easier the building for a virtual machine.
The aim is to specify the main configs using the same JSON structure for Vagrant
and Packer.
Programs are organized inside "templates/programs/" and there are share between Vagrant e Packer.
Each programs contains file for install, configure, and uninstall commands you want to add to the Vagrantfile or the main file for Packer.
