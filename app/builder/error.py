class Error(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class PackageNotFoundError(Error):
    pass


class ScriptNotFoundError(Error):
    pass


class JsonConfigCopiedError(Error):
    pass


class EmptyScriptError(Error):
    pass


class NoFileToUploadError(Error):
    pass


class UploadNameConflictError(Error):
    pass
