import subprocess
import timeit


def get_local_virtual_boxes_popen():
    bash_command = "VBoxManage list vms"
    process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    items = output.decode("utf-8").split('\n')
    return [item.split()[0].replace('"', '') for item in items if item]


def get_local_virtual_boxes_run():
    bash_command = "VBoxManage list vms"
    process = subprocess.run(bash_command, shell=True, capture_output=True)
    items = process.stdout.decode("ascii").split('\n')
    return [item.split()[0].replace('"', '') for item in items if item]


if __name__ == '__main__':
    print(
        "popen = ",
        timeit.timeit(
            'get_local_virtual_boxes_popen()',
            setup="from __main__ import get_local_virtual_boxes_popen",
            number=1000
        )
    )
    print(
        "run =",
        timeit.timeit(
            'get_local_virtual_boxes_run()',
            setup="from __main__ import get_local_virtual_boxes_run",
            number=1000
        )
    )
