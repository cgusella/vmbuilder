#!/bin/bash
if [ ! -d "/home/extra_user/.config/terminator" ];
then
mkdir -p /home/extra_user/.config/terminator
fi
cp /vagrant/programs/terminator/config /home/extra_user/.config/terminator/