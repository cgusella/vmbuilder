import os
import subprocess
import constants


def get_json_files_for_help(path_to_provs_confs: str):
    """
    Return json files available but template.json as string.\n
    Each name is separated by a pipe.
    """
    provision_files = [
            file for file in os.listdir(
                path_to_provs_confs
            ) if file != 'template.json'
        ]
    if not provision_files:
        help_message = (
            'There are no JSON files. '
            'To create a new one is sufficient to specify it '
            'using the relative JSON flag from the main app. '
        )
    else:
        help_message = 'Select among: \n* '
        help_message += '\n* '.join(
            [
                f'{file}' for file in provision_files
            ]
        )
    return help_message


def get_preseed_files_for_help():
    """
    Return preseed file names available in http folder for packer machines
    as string.\n
    Each name is separated by a pipe.
    """
    preseed_file = [
        f'{file}' for file in os.listdir(
            constants.PACKER_PRESEEDS_PATH
        ) if file.startswith('preseed')
    ]
    if not preseed_file:
        help_message = (
            'There are no preseed files. '
            'Add one to http folder in packer template.'
        )
    else:
        help_message = 'Select among: \n* '
        help_message += "\n* ".join(preseed_file)
    return help_message


def get_local_vagrant_boxes():
    """
    Return installed vagrant box list as string.\n
    Each vagrant box name is separated by a pipe.
    """
    output = subprocess.run(
        "vagrant box list",
        shell=True,
        capture_output=True
    ).stdout.decode("ascii")
    boxes = output.split('\n')
    boxes = [box.split(' ')[0] for box in boxes]
    return "\n".join(boxes)
