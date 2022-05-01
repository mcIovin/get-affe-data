import logging
from os import mkdir
import pandas as pd
from pathlib import Path


class Affe:
    """Each instance of this class represents and individual ape."""

    def __init__(self, id: int):
        """
        Method to initialize an object representing an ape.
        :param id: The numerical id of the Affe (should be between 1 and 250, but is not enforced.)
        """

        self.id = id
        self.name_strict = ""
        self.name_friendly = ""
        self.name_strict = ""
        self.story = ""
        self.image_url = ""
        self.attributes = []
        self.emotions = []
        self.attributes_other_textual = []
        self.attributes_other_numerical = []
    # ------------------------ END FUNCTION ------------------------ #

    def set_name_strict(self, name_with_number: str):
        self.name_strict = name_with_number
    # ------------------------ END FUNCTION ------------------------ #

    def set_name_friendly(self, nice_name: str):
        self.name_friendly = nice_name
    # ------------------------ END FUNCTION ------------------------ #

    def set_story(self, story: str):
        self.story = story
    # ------------------------ END FUNCTION ------------------------ #

    def set_image(self, image_location: str):
        self.image_url = image_location
    # ------------------------ END FUNCTION ------------------------ #

    def dump_to_nftstyle_json(self, full_path: Path):
        pass
    # ------------------------ END FUNCTION ------------------------ #
