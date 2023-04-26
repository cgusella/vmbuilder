getent passwd extra_user
if [ ! $? -eq 0 ]; # if user does not exist
then
useradd -m extra_user
usermod -a -G sudo extra_user
chsh -s /bin/bash extra_user
fi
