#!/usr/bin/python3
from builder import get_project_class


def main():
    project = get_project_class()
    project.check_flags()
    project.check_folder_vb_existence()

    try:
        project.create_project_folder()
        project.provision()
    except (FileNotFoundError, KeyError):
        project.delete_project()


if __name__ == '__main__':
    main()
