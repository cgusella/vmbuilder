import constants
import os

programs = os.listdir(constants.programs_path)

for program in programs:
    old_upload_folder = f'{constants.programs_path}/{program}/configs/upload'
    old_config_script = f'{constants.programs_path}/{program}/configs/config.sh'
    new_upload_folder = f'{constants.programs_path}/{program}/upload'
    if program in ['program-example']:
        continue
    if 'upload' not in os.listdir(f'{constants.programs_path}/{program}/'):
        os.mkdir(new_upload_folder)
    if 'upload' in os.listdir(f'{constants.programs_path}/{program}/config/'):
        os.rmdir(old_upload_folder)
    
    # if os.path.isdir(upload_folder):
    #     continue
    # os.mkdir(upload_folder)