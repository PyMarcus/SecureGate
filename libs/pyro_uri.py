import os

import Pyro4

root_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(root_dir, ".pyro_uri")


def set_pyro_uri(uri: Pyro4.URI):
    """
    This function is a setter for the Pyro uri.
    """
    with open(file_path, "w") as file:
        file.write(str(uri))


def get_pyro_uri() -> str:
    """
    This function is a getter for the Pyro uri.
    """
    with open(file_path, "r") as file:
        return file.read()
