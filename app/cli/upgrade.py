import constants
import os

packages = os.listdir(constants.packages_path)

for package in packages:
    old_upload_folder = f'{constants.packages_path}/{package}/configs/upload'
    old_config_script = f'{constants.packages_path}/{package}/configs/config.sh'
    new_upload_folder = f'{constants.packages_path}/{package}/upload'
    if package in ['package-example']:
        continue
    if 'upload' not in os.listdir(f'{constants.packages_path}/{package}/'):
        os.mkdir(new_upload_folder)
    if 'upload' in os.listdir(f'{constants.packages_path}/{package}/config/'):
        os.rmdir(old_upload_folder)

    # if os.path.isdir(upload_folder):
    #     continue
    # os.mkdir(upload_folder)
