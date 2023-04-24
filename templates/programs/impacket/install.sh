#!/bin/bash
# Impacket is a collection of Python classes for working with network protocols. 
# In order to install impacket first install pipx
apt-get install -y pipx
python3 -m pipx install impacket
# Automatically add /root/.local/bin to PATH environment variable
pipx ensurepath