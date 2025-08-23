"""
Model definitions
"""

class FileReader:
    """
    A FileReader. Contains the method for reading in a file.
    """
    def __init__(
        self, file_path
    ):
        self.file_path = file_path
    def read_file(self):
        """
        Read the contents of the file_path
        """
        return NotImplemented
    def sequence(self):
        """
        Return a sequence
        """
        return NotImplemented
