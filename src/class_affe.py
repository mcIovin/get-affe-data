import logging
import pandas as pd
import json
from pathlib import Path
from typing import Union


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
        self.story = ""
        self.attributes_common = {}
        self.emotions_common = {}
        self.attributes_rare_textual = {}
        self.attributes_rare_numerical = {}
        self.image_url = ""
        self.website = ""
        # the list below CAN be auto-computed in code with dir() and (not) callable() and getattr(),
        # but the result is sorted alphabetically, so I prefer to keep a list here that tracks the
        # elements of the class in order of preference.
        self.list_of_elements = ['self.id',
                                 'self.name_strict',
                                 'self.name_friendly',
                                 'self.story',
                                 'self.attributes_common',
                                 'self.emotions_common',
                                 'self.attributes_rare_textual',
                                 'self.attributes_rare_numerical',
                                 'self.image_url',
                                 'self.website'
                                 ]
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

    def set_website(self, url: str):
        self.website = url
    # ------------------------ END FUNCTION ------------------------ #

    def add_common_attribute(self, attribute_name: str, attribute_value: str):
        self.attributes_common[attribute_name] = attribute_value
    # ------------------------ END FUNCTION ------------------------ #

    def add_common_emotion(self, emotion_name: str, emotion_value: int):
        self.emotions_common[emotion_name] = emotion_value
    # ------------------------ END FUNCTION ------------------------ #

    def add_rare_textual_attributes(self, attribute_name: str, attribute_value: str):
        self.attributes_rare_textual[attribute_name] = attribute_value
    # ------------------------ END FUNCTION ------------------------ #

    def add_rare_numerical_attributes(self, attribute_name: str, attribute_value: int):
        self.attributes_rare_numerical[attribute_name] = attribute_value
    # ------------------------ END FUNCTION ------------------------ #

    def dump_to_json(self, full_path_to_output_directory: Path, pretty: bool = True) -> dict:
        """
        A method to dump to disk the object represented by this class instance, fairly literally
        (ie. without almost any processing/manipulation.)
        :param full_path_to_output_directory: The directory to save the object to. The filename will
          be based on the ID of the Affe.
        :param pretty: Whether the json should be indented or not
        :return: The dictionary that was used to dump the object to json format.
        """
        dict_to_dump = self.make_dict()

        full_path_to_json_file = full_path_to_output_directory / (str(self.id) + '.json')
        kwargs = {}
        if pretty:
            kwargs = {'indent': 2}
        with open(full_path_to_json_file, mode='w') as f:
            json.dump(dict_to_dump, f, **kwargs)
        return dict_to_dump
    # ------------------------ END FUNCTION ------------------------ #

    def dump_to_opensea_style_json(self, full_path: Path, pretty: bool = True):
        """
        A method to dump to disk the object represented by this class instance, in following the
        opensea metadata standards.
        :param full_path_to_output_directory: The directory to save the object to. The filename will
          be based on the ID of the Affe.
        :param pretty: Whether the json should be indented or not
        """
        pass
    # ------------------------ END FUNCTION ------------------------ #

    def make_dict(self) -> dict:
        """
        A method to 'convert' the instance of the class into a dictionary, whereby each 'self' variable
        in the class is saved as an element in the dictionary.
        :return: A dictionary representing an Affe.
        """
        dict_to_return = {}
        for item in self.list_of_elements:
            element_name = item.replace('self.', '')
            dict_to_return[element_name] = eval(item)
        return dict_to_return
    # ------------------------ END FUNCTION ------------------------ #