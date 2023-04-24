import logging

log = logging.getLogger(__name__)


class Error(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class FlagError(Error):
    pass


class ExistenceProjectError(Error):
    pass


class ExistenceVirtualBoxError(Error):
    pass
