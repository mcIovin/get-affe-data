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

    def perform_721_hygene(self):
        """
        This method takes an affen object and makes sure its data is in
        the form we want it to be for the 721 contract, rather than the form
        it exists as in the 1155 Storefront contract. For example, we may
        to store the 'name' as the Chimp's name rather than the number, and
        the number as an attribute. This function would take care of such
        :return:
        """
        self.name_strict = self.name_friendly
        self.add_common_attribute("Birth Order", f"Affe mit Waffe #{str(self.id)}")
    # ------------------------ END FUNCTION ------------------------ #

    def dump_to_json(self, full_path_to_output_directory: Path, style: str, pretty: bool = True) -> dict:
        """
        A method to dump to disk the object
        :param full_path_to_output_directory: The directory to save the object to. The filename will
          be based on the ID of the Affe.
        :param style: Acceptable values are 'normal' and 'nft-style'.
          - 'normal' will dump to disc a json file that represents an instance of this class instance, fairly
            literally - not much processing/manipulation. Each self.variable of the class is dumped 'as is' to
            the dictionary/json.
          - 'nft-style' will organize and rename the fields slightly so that places like OpenSea will 'understand'
            the metadata. Eg. 'story' will be renamed to 'description' in the json output.
        :param pretty: Whether the json should be indented or not
        :return: The dictionary that was used to dump the object to json format.
        """
        dict_to_dump = {}
        if style == 'normal':
            dict_to_dump = self.make_dict()
        if style == 'nft-style':
            dict_to_dump = self.make_dict_nft_style()

        full_path_to_json_file = full_path_to_output_directory / (str(self.id) + '.json')
        kwargs = {}
        if pretty:
            kwargs = {'indent': 2}
        with open(full_path_to_json_file, mode='w') as f:
            json.dump(dict_to_dump, f, **kwargs)
        return dict_to_dump
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

    def make_dict_nft_style(self) -> dict:
        """
        A method to 'convert' the instance of the class into a dictionary that can be dumped as json which
        generally adheres to metadata/opensea standards.
        :return: A dictionary representing an Affe.
        """
        dict_to_return = {}
        list_of_attributes = []

        # The loops below build the list of attributes

        for item in self.attributes_common:
            dict_attrib_to_add = {
                'trait_type': item,
                'value': self.attributes_common[item]
            }
            list_of_attributes.append(dict_attrib_to_add)

        for item in self.attributes_rare_textual:
            dict_attrib_to_add = {
                'trait_type': item,
                'value': self.attributes_rare_textual[item]
            }
            list_of_attributes.append(dict_attrib_to_add)

        for item in self.emotions_common:
            dict_attrib_to_add = {
                'display_type': 'number',
                'trait_type': item,
                'value': self.emotions_common[item],
                'max_value': 5
            }
            list_of_attributes.append(dict_attrib_to_add)

        for item in self.attributes_rare_numerical:
            dict_attrib_to_add = {
                'display_type': 'number',
                'trait_type': item,
                'value': self.attributes_rare_numerical[item],
                'max_value': 5
            }
            list_of_attributes.append(dict_attrib_to_add)

        # Now all the pieces are ready to compile the metadata
        dict_to_return['name'] = self.name_strict
        dict_to_return['description'] = self.story
        dict_to_return['image'] = self.image_url
        dict_to_return['external_url'] = self.website
        dict_to_return['attributes'] = list_of_attributes

        return dict_to_return
    # ------------------------ END FUNCTION ------------------------ #
