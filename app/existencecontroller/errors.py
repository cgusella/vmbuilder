class Error(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ExistenceProjectError(Error):
    pass


class ExistenceVirtualBoxError(Error):
    pass


class FileExtesionError(Error):
    pass
