import logging
from os import mkdir
from os.path import exists
import pandas as pd
from class_affe import Affe
from pathlib import Path
from class_api_interactions_moralis import MoralisAPIinteractions
from class_selenium_opensea import SeleniumOnOpensea


class AffeDataManipulator:
    """This class orchestrates manipulation of Affe data."""

    # A list of typical top-level NFT metadata, such as ID, name, description, etc.
    fields_nft_toplevel = ['id', 'name', 'description', 'image']
    # A list of fields that are considered valid Affen attributes based on text
    fields_nft_attributes_txt = []
    # A list of fields that are considered valid Affen NUMERICAL attributes
    fields_nft_attributes_num = []

    def __init__(self, affen_data: pd.DataFrame):
        """
        Initialize the AffeDataManipulator class.
        Args:
            affen_data: A pandas dataframe containing information about the Affen as they exist in
            the 1155 Opensea Storefront contract.
        """
        self.df_affen = affen_data

    # ------------------------ END FUNCTION ------------------------ #




    def dump_all_to_nftstyled_json(self):


        list_with_all_affen = []

        for row in self.df_affen.itertuples():
            affe = self.__convert_df_row_to_affe_object(row)
            list_with_all_affen.append(affe)
            affe.dump_to_nftstyle_json(Path())
    # ------------------------ END FUNCTION ------------------------ #



    def __convert_df_row_to_affe_object(self, df_rowtuple):
        """
        Convert a pandas row to an individual Affe object.
        :param df_rowtuple: This is the type of object that pandas uses when using the pandas
          itertuples.
        :return: an Affe object
        """
        fields = df_rowtuple
        strict_name = fields[self.__rowtuple_loc('name')]
        id = self.__extract_affe_number_from_strict_name(strict_name)

        affe = Affe(id)
        affe.set_name_strict(strict_name)
        affe.set_name_friendly(fields[self.__rowtuple_loc('CHIMP')])
        affe.set_story(fields[self.__rowtuple_loc('description')])
        affe.set_image(fields[self.__rowtuple_loc('image')])


        return affe
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