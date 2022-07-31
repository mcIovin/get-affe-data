import logging
from os import mkdir
from os.path import exists
import pandas as pd
import json
from class_affe import Affe
from pathlib import Path
from math import isnan
from typing import Union


class AffeDataManipulator:
    """This class orchestrates manipulation of Affe data."""

    # A list of fields that are considered valid Affen attributes based on text
    fields_all_affen_common_attributes = ['CHIMP', 'AK47']
    # A list of fields that are considered valid Affen NUMERICAL attributes
    fields_all_affen_emotions = ['Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy',
                                 'Negative', 'Positive', 'Sadness', 'Surprise',  'Trust']
    # A list of columns that are not likely to represent valid Affen attributes of any sort
    # OR are already included already in the lists above
    # NOTE that it looks like 'Anticipation' is listed twice, but this is due to a typo in the
    # source data (i.e. a column with the typo in the name DOES exist.)
    fields_to_ignore_as_affen_attributes = ['name', 'CHIMP', 'AK47', 'token_id',
                                            'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy',
                                            'Negative', 'Positive', 'Sadness', 'Surprise', 'Trust', 'description',
                                            'Anticipatioin', 'token_address', 'block_number_minted', 'owner_of',
                                            'block_number', 'token_hash', 'amount', 'contract_type', 'symbol',
                                            'token_uri', 'metadata', 'last_token_uri_sync', 'last_metadata_sync',
                                            'image', 'external_link', 'animation_url']

    def __init__(self, affen_data: pd.DataFrame, full_path_to_data_dir: Path):
        """
        Initialize the AffeDataManipulator class.
        Args:
            affen_data: A pandas dataframe containing information about the Affen as they exist in
            the 1155 Opensea Storefront contract.
        """
        self.df_affen = affen_data

        # Some methods in this class will store files on disk in a directory called 'output',
        # so we'll check to see if it exists, and if not it will be created.
        self.fullpath_dir_output = full_path_to_data_dir / 'output'
        if not exists(self.fullpath_dir_output):
            mkdir(self.fullpath_dir_output)
    # ------------------------ END FUNCTION ------------------------ #

    def dump_all_to_json(self, normal_json: bool = True,
                         opensea_style_json: bool = True,
                         pretty: bool = True):
        """
        Method to dump to disk Affen data in json format.
        :param normal_json: Each Affe object, in a json representation very similar to how each Affe
          object is abstracted in the Affe class.
        :param opensea_style_json: Json formatted in a typical NFT format, in particular following
          the metadata standards of Opensea.
        :return:
        """
        list_with_all_affen_normal = []
        list_with_all_affen_opensea_style = []
        fullpath_dir_normal_json = Path
        fullpath_dir_opensea_json = Path
        kwargs = ({'indent': 2} if pretty else {})

        if normal_json:
            fullpath_dir_normal_json = self.fullpath_dir_output / 'normal_json'
            if not exists(fullpath_dir_normal_json):
                mkdir(fullpath_dir_normal_json)
            for row in self.df_affen.itertuples():
                affe = self.__convert_df_row_to_affe_object(row)
                # In the line below, the method dumps the json to disk, but also returns the dictionary
                # that was used to generate the json, which we then append to the running tally of Affen
                the_ape_as_dict = affe.dump_to_json(fullpath_dir_normal_json, 'normal', pretty)
                list_with_all_affen_normal.append(the_ape_as_dict)
            # Dump the whole list to a single file as well
            full_path_to_collection_file = fullpath_dir_normal_json / '00_all_affen.json'
            with open(full_path_to_collection_file, mode='w') as f:
                json.dump(list_with_all_affen_normal, f, **kwargs)

        if opensea_style_json:
            fullpath_dir_opensea_json = self.fullpath_dir_output / 'opensea_style_json'
            if not exists(fullpath_dir_opensea_json):
                mkdir(fullpath_dir_opensea_json)
            for row in self.df_affen.itertuples():
                affe = self.__convert_df_row_to_affe_object(row)
                # The row below changes some of the metadata from the way it exists in
                # the OpenSea 1155 Storefront contract into the way we want it to be in
                # the 721 contract.
                affe.perform_721_hygene()

                # In the line below, the method dumps the json to disk, but also returns the dictionary
                # that was used to generate the json, which we then append to the running tally of Affen
                the_ape_as_dict = affe.dump_to_json(fullpath_dir_opensea_json, 'nft-style', pretty)
                list_with_all_affen_opensea_style.append(the_ape_as_dict)
            # Dump the whole list to a single file as well
            full_path_to_collection_file = fullpath_dir_opensea_json / '00_all_affen_nft_style.json'
            with open(full_path_to_collection_file, mode='w') as f:
                json.dump(list_with_all_affen_opensea_style, f, **kwargs)
    # ------------------------ END FUNCTION ------------------------ #

    def __convert_df_row_to_affe_object(self, df_rowtuple):
        """
        Convert a pandas row to an individual Affe object.
        :param df_rowtuple: This is the type of object that pandas uses when using the pandas
          itertuples, and represents a row with data about an ape.
        :return: an Affe object
        """
        fields = df_rowtuple
        strict_name = fields[self.__rowtuple_loc('name')]
        id = self.__extract_affe_number_from_strict_name(strict_name)

        affe = Affe(id)
        affe.set_name_strict(strict_name)
        # There is a lot going on in each line below, so lets break it down.
        # The __rowtuple_loc method returns the column number in which to look for the relevant value
        # That integer is then passed as the index for the 'fields' list (although I don't think the
        # object is striclty a list, it is still accessed by integer-index)
        # Then, in order to avoid having NaN in any of the results, the value that is extracted from 'fields'
        # is checked for NaN (and if it is Nan it is converted to an empty string instead
        # by the __check_for_nan method.)
        affe.set_name_friendly(self.__check_for_nan(fields[self.__rowtuple_loc('CHIMP')]))
        affe.set_story(self.__check_for_nan(fields[self.__rowtuple_loc('description')]))
        affe.set_image(self.__check_for_nan(fields[self.__rowtuple_loc('image')]))
        affe.set_website(self.__check_for_nan(fields[self.__rowtuple_loc('external_link')]))

        self.__add_common_attributes_to_affe_obj(affe, fields)
        self.__add_common_emotions_to_affe_obj(affe, fields)
        self.__add_miscellaneous_attributes_to_affe_obj(affe, fields)

        return affe
    # ------------------------ END FUNCTION ------------------------ #

    def __add_common_attributes_to_affe_obj(self, the_affe: Affe, df_rowtuple):
        """This is intended to be a helper function to __convert_df_row_to_affe_object. It extracts
        common attributes from the rowtuple and adds them to the affe in question.
        :param df_rowtuple: This is the type of object that pandas uses when using the pandas
          itertuples, and represents a row with data about an ape.
        :return: nothing is returned, because the Affe object should be modified in-place
        """
        for field in self.fields_all_affen_common_attributes:
            value = df_rowtuple[self.__rowtuple_loc(field)]
            # We only add an attribute if it has a value. If it's returned as 'empty
            # string' we don't add anything.
            if value:
                    the_affe.add_common_attribute(field, value)
    # ------------------------ END FUNCTION ------------------------ #

    def __add_common_emotions_to_affe_obj(self, the_affe: Affe, df_rowtuple):
        """This is intended to be a helper function to __convert_df_row_to_affe_object. It extracts
        common emotions from the rowtuple and adds them to the affe in question.
        :param df_rowtuple: This is the type of object that pandas uses when using the pandas
          itertuples, and represents a row with data about an ape.
        :return: nothing is returned, because the Affe object should be modified in-place
        """
        for field in self.fields_all_affen_emotions:
            value = df_rowtuple[self.__rowtuple_loc(field)]
            # We only add an attribute if it has a value. If it's returned as 'empty
            # string' we don't add anything.
            if value:
                # These values were pulled from OpenSea, so they should come in the format of
                # a string that looks like: X of Y
                if (type(value) is str) and (' of ' in value):
                    num = int(value.split(sep=' of ')[0])
                    the_affe.add_common_emotion(field, num)
                else:
                    logging.debug(f"Field -> '{field}' did not have the expected format of "
                                    f"'X of Y' for Affe -> '{the_affe.name_strict}'")
    # ------------------------ END FUNCTION ------------------------ #

    def __add_miscellaneous_attributes_to_affe_obj(self, the_affe: Affe, df_rowtuple):
        """This is intended to be a helper function to __convert_df_row_to_affe_object. It extracts
        NON common attributes (ie. attributes that are NOT standard across most apes) from the rowtuple
        and adds them to the affe in question.
        :param df_rowtuple: This is the type of object that pandas uses when using the pandas
          itertuples, and represents a row with data about an ape.
        :return: nothing is returned, because the Affe object should be modified in-place
        """
        columns = list(self.df_affen.columns)
        for col in columns:
            # We'll only add miscellaneous attributes to the ape, if the column is not in a list
            # that help to filter non-attribute column names, and if the column name does not
            # contain 'unnamed' (as some previous pandas operations may result in some 'unnamed'
            # columns.)
            if (col not in self.fields_to_ignore_as_affen_attributes) and ('unnamed' not in col.lower()):
                value = df_rowtuple[self.__rowtuple_loc(col)]
                if value:
                    if type(value) is float:
                        if isnan(value):
                            continue
                        else:
                            logging.debug(f"Encountered a non-nan float value for "
                                            f"Affe -> {the_affe.name_strict}")
                    elif type(value) is str:
                        # Because many of the attributes were scraped form Opensea website (rather than a
                        # formal API, if they are numeric, they likely come as a string in the format of
                        # 'X of Y' - so here, we are looking for that format.
                        if ' of ' in value:
                            num = int(value.split(sep=' of ')[0])
                            the_affe.add_rare_numerical_attributes(col, num)
                        else:
                            the_affe.add_rare_textual_attributes(col, value)
                    else:
                        logging.debug(f"Encountered a value that is neither string nor float for "
                                        f"Affe -> {the_affe.name_strict}")
    # ------------------------ END FUNCTION ------------------------ #

    def __extract_affe_number_from_strict_name(self, strict_name: str) -> int:
        str_id = strict_name.split(sep="#")[-1]
        return int(str_id)
    # ------------------------ END FUNCTION ------------------------ #

    def __rowtuple_loc(self, column_name: str) -> int:
        """
        Get the numerical location (ie. the position) of a particular field (column) as it
          should appear in a rowtuple. What is meant here by 'rowtuple' is the type of
          object that is iterated over when using pandas itertuples()
        :param column_name: The name of the column to get the integer index for.
        :return:
        """
        str_to_return = ""
        if column_name in self.df_affen.columns:
            # because the row will have the index as one of its regular columns, the
            # location should be the same as in the dataframe, but moved over by 1
            str_to_return = self.df_affen.columns.get_loc(column_name) + 1

        return str_to_return
    # ------------------------ END FUNCTION ------------------------ #

    def __check_for_nan(self, a_variable: Union[str|int|float]) -> Union[str|int|float]:
        """
        If a value passed is NaN (likely extracted from a pandas dataframe) then
        this function will return an empty string instead.
        :param a_variable: the variable containing the value in question.
        :return: the same a_variable UNLESS it is NaN, in which case return the empty string.
        """
        var_type = type(a_variable)
        if (var_type is float) or (var_type is int):
            if isnan(a_variable):
                return ""
        else:
            return a_variable
    # ------------------------ END FUNCTION ------------------------ #
