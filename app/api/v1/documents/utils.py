from .exceptions import NoFileNameError


def get_file_extension(filename: str | None = None) -> str:
    if filename is None or filename.strip() == "":
        raise NoFileNameError("No filename provided")
    return filename.split(".")[-1].lower()
