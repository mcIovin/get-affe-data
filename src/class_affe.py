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
        self.name = ""
        self.story = ""
        self.image_url = ""
        self.attributes = ""
        self.emotions = ""

    # ------------------------ END FUNCTION ------------------------ #

    def set_name(self, name: str):
        self.name = name
    # ------------------------ END FUNCTION ------------------------ #

    def set_story(self, story: str):
        self.story = story
    # ------------------------ END FUNCTION ------------------------ #

    def set_image(self, image_location: str):
        self.image_url = image_location
    # ------------------------ END FUNCTION ------------------------ #
