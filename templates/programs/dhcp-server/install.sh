#!/bin/bash
apt-get install --yes isc-dhcp-server
# isc-dhcp-server.service is not a native service, so
# in order to enable the service use systemd-sysv-install instead of systemctl
/lib/systemd/systemd-sysv-install enable isc-dhcp-server