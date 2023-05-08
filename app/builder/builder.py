import abc


class Builder(abc.ABC):

    @abc.abstractmethod
    def check_flags(self):
        pass

    @abc.abstractmethod
    def check_new_project_folder_existence(self):
        pass

    @abc.abstractmethod
    def check_virtualbox_existence(self):
        pass

    @abc.abstractmethod
    def check_provision_cfg_json_existence(self):
        pass

    @abc.abstractmethod
    def create_project_folder(self):
        pass

    @abc.abstractmethod
    def generate_main_file(self):
        pass

    @abc.abstractmethod
    def delete_project(self):
        pass
