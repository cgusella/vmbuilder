# Create extra_user user
getent passwd extra_user
if [ ! $? -eq 0 ]; # if user does not exist
then
useradd -m extra_user
usermod -a -G sudo extra_user
chsh -s /bin/bash extra_user
fi

# Configure terminal/prompt/bash for extra_user
chsh -s /bin/bash extra_user
cp /vagrant/configurations/bash-terminator/bashrc /home/extra_user/.bashrc

# Configure nano for extra_user
cp /vagrant/configurations/nanorc /home/extra_user/.nanorc
chown extra_user:extra_user /home/extra_user/.nanorc

# Configure keyboard for extra_user
if [ ! -d "/home/extra_user/Scripts" ];
then
mkdir /home/extra_user/Scripts
fi
cp /vagrant/configurations/keyboard.config.sh /home/extra_user/Scripts/
chown -R extra_user:extra_user /home/extra_user/Scripts

# Configure terminator for extra_user
if [ ! -d "/home/extra_user/.config/terminator" ];
then
mkdir -p /home/extra_user/.config/terminator
fi
cp /vagrant/configurations/bash-terminator/config /home/extra_user/.config/terminator/
