#!/bin/bash
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get --yes -o Dpkg::Options::="--force-confnew" upgrade





