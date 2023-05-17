import abc


class Builder(abc.ABC):

    @abc.abstractmethod
    def create_project_folder(self):
        pass

    @abc.abstractmethod
    def generate_main_file(self):
        pass

    @abc.abstractmethod
    def delete_project(self):
        pass
