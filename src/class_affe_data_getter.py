import logging
from os import mkdir
from os.path import exists
import pandas as pd
from pathlib import Path
from class_api_interactions_moralis import MoralisAPIinteractions
from class_selenium_opensea import SeleniumOnOpensea


class AffeDataGetter:
    """This class orchestrates the extraction of Affe data ."""

    def __init__(self, contract_address_with_affe_data, full_path_to_data_dir: Path):
        """
        Initialize the AffeDataGetter class.
        Args:
            full_path_to_data_dir: Path to a directory where this class will output
              intermediate working files, and final output files to. The directory
              should already exist.
        """

        self.affe_contract_address = contract_address_with_affe_data

        # This class will store some files on disk in two directories called
        # 'intermediate_files' and 'output', so we'll check to see if they exist,
        # and if not they will be created.
        self.fullpath_dir_intermediate_files = full_path_to_data_dir / 'intermediate_files'
        self.fullpath_dir_output = full_path_to_data_dir / 'output'
        if not exists(self.fullpath_dir_intermediate_files):
            mkdir(self.fullpath_dir_intermediate_files)
        if not exists(self.fullpath_dir_output):
            mkdir(self.fullpath_dir_output)

        # Intermediate files
        self.fullpath_eoa_nft_transfers = self.fullpath_dir_intermediate_files / 'xlii_transactions.csv'
        self.fullpath_nfts_data = self.fullpath_dir_intermediate_files / 'nfts.csv'
        self.fullpath_nfts_refined_data = self.fullpath_dir_intermediate_files / 'nfts_refined.csv'
        self.fullpath_nfts_extra_data = self.fullpath_dir_intermediate_files / 'nfts_extra_data.csv'
        self.fullpath_combined_nft_data = self.fullpath_dir_intermediate_files / 'combined_data.csv'

        # Finished product files
        self.fullpath_final = self.fullpath_dir_output / 'affe.csv'
    # ------------------------ END FUNCTION ------------------------ #

    def build_affen_data_files(self,
                              output_format: str ="csv",
                              request_moralis_metadata_resync: bool = False):
        """
        This method gets as much data as it can about Affe mit Waffe, compiling the data
        from several sources, and produces an output file in the form of a csv or parquet.
        The output file is saved in a directory called 'output'.
        :param output_format: Can be "csv" or "parquet"
        :param request_moralis_metadata_resync: set this parameter to True if the metadata for some
          NFTs seems to be missing. This will cause a resync of metadata to be requested for each
          token, using the Moralis API.
        """

        logging.info("---------- GETTING NFT TRANSFER TRANSACTIONS ----------")
        df_transfers = self.get_eoa_nft_transfers_from_moralis(do_some_refining=True)

        if request_moralis_metadata_resync:
            logging.info("---------- REQUESTING METADATA RESYNC ----------")
            set_token_ids = set(df_transfers['token_id'])
            self.request_moralis_to_resync_nft_metadata(set_token_ids)

        logging.info("---------- GETTING NFT METADATA FROM TOKEN URIs ----------")
        df_nfts = self.get_nft_metadata_from_moralis(df_transfers)

        logging.info("---------- REFINING NFT METADATA ----------")
        df_refined_nfts = self.refine_nft_data(df_nfts)

        logging.info("---------- GETTING ADDITIONAL NFT METADATA FROM OPENSEA ----------")
        df_extras = self.get_extra_metadata_from_opensea(df_refined_nfts)

        logging.info("---------- COMBINING METADATA ----------")
        df_combined = self.combine_data([df_extras, df_refined_nfts])

        logging.info("---------- REORDERING METADATA ----------")
        list_ordered_columns = ['name', 'CHIMP', 'AK47', 'Anger', 'Anticipation', 'Disgust',
                                'Fear', 'Joy', 'Negative', 'Positive', 'Sadness', 'Surprise',
                                'Trust', 'description', 'SPECIAL ABILITY', 'TRINKET',
                                'FIREWORKS', 'HAT', 'FLOWER', 'SUNGLASSES',
                                'PET', 'MONOCLE', 'APEBALL', 'PIPE', 'JEWELLERY', 'CIGAR',
                                'SEASON', 'BOWTIE', 'SPECIAL ATTRIBUTE', 'DRINK', 'PANTS',
                                'FLAG', 'Damage', 'Parry', 'Speed']
        df_final = self.reorganize_the_data(list_ordered_columns, df_combined)

        logging.info("---------- AFFE DATA PREVIEW ----------")
        self.show_data_on_console(df_final)

        logging.info("FOR THE FULL SET OF DATA see the affe.csv file saved to data/output directory.")
    # ------------------------ END FUNCTION ------------------------ #

    def get_eoa_nft_transfers_from_moralis(self, do_some_refining: bool = False) -> pd.DataFrame:
        """
        This method gets all the NFT transfers that the creator of the Affe has performed
        in the Opensea Storefront contract.
        :param do_some_refining: Refine down to only where the address is the creator (as opposed
          to NFTs that have been SENT to the address, and only include NFT transfers in the Opensea
          Storefront contract where the Affe live.
        :return: Pandas dataframe with the transfers. However, this information will also get saved
          to disk in the 'intermediate_files' directory.
        """
        moralis = MoralisAPIinteractions()

        # the account for which we want to query nft transactions
        # In this case, we are querying the address that creates the Monkeyverse DAO NFTs
        eoa = "0x023a3905E3B33634758871712f4293Ddb919B67F"

        # below get all the NFT transactions done by some address
        df = moralis.get_nft_transfers(eoa, direction='both')

        if do_some_refining:
            # account of interest
            # In this case, we are filtering the address that creates the Monkeyverse DAO NFTs
            # this is, in fact, the same address as above, but the results in the df have lower-case
            # address, so we are re-declaring the same addres, with different case, so the filtering
            # works
            eoa = "0x023a3905e3b33634758871712f4293ddb919b67f"

            # keep only the rows for a certain contract
            df = df[df['token_address'] == self.affe_contract_address]
            # keep only the rows where the eoa is the 'from' address of interest
            df = df[df['from_address'] == eoa]

        df.to_csv(self.fullpath_eoa_nft_transfers, index=False)
        return df
    # ------------------------ END FUNCTION ------------------------ #

    def request_moralis_to_resync_nft_metadata(self, iterable_with_token_ids):
        moralis = MoralisAPIinteractions()
        moralis.resync_many_nft_tokens_metadata(self.affe_contract_address,
                                                iterable_with_token_ids,
                                                log_api_response=True,
                                                sleep_time_between_requests=1)
    # ------------------------ END FUNCTION ------------------------ #

    def get_nft_metadata_from_moralis(self,
                                      df_with_nft_transfers: pd.DataFrame = pd.DataFrame) -> pd.DataFrame:
        """
        This method starts information about NFT transactions that the creator of the Affe
        has sent, and grabs the metadata about each token using the Moralis API.
        :param df_with_nft_transfers: The information about the NFT transfers can be passed
          directly to this method in this parameter. If this parameter is not provided, this
          method will attempt to laod the information from a default location on disk.
        :return:
        """
        df = df_with_nft_transfers
        if df_with_nft_transfers.empty:
            df = pd.read_csv(self.fullpath_eoa_nft_transfers)

        moralis = MoralisAPIinteractions()

        # because the function that gets token metadata takes as an input a particular contract
        # address, we should filter the df (in case it was not done already upstream) to that
        # particular contract
        df = df[df['token_address'] == self.affe_contract_address]

        set_token_ids = set(df['token_id'])

        list_of_metadata_fields_of_interest = ['name', 'description', 'image', 'external_link', 'animation_url']
        df_tokens = moralis.get_many_nft_tokens_metadata(
            self.affe_contract_address,
            set_token_ids,
            list_of_metadata_fields_to_extract=list_of_metadata_fields_of_interest)

        df_tokens.to_csv(self.fullpath_nfts_data, index=False)
        return df_tokens
    # ------------------------ END FUNCTION ------------------------ #

    def refine_nft_data(self, df_with_nft_data: pd.DataFrame = pd.DataFrame) -> pd.DataFrame:
        """
        This method refines the incoming NFT data. For example, it removes all NFTs that
        are not part of the Affe collection.
        :param df_with_nft_data: The information about NFTs can be passed
          directly to this method in this parameter. If this parameter is not provided, this
          method will attempt to laod the information from a default location on disk.
        :return:
        """
        df = df_with_nft_data
        if df_with_nft_data.empty:
            df = pd.read_csv(self.fullpath_nfts_data)

        # the line below can be used to keep only rows that are NOT nan (ie. get rid of the rows
        # that have nan in a column.
        df_without_nans = df[df['metadata'].notna()]

        # keep only rows with a certain substring in the 'name' metadata field of the nft
        substring = "Affe mit"
        df_substring = df_without_nans[df_without_nans['name'].str.startswith(substring)]

        # at this point I hopefully have all the rows that have Affe mit Waffe in the metadata
        # HOWEVER, the moralis api is not returning metadata for all rows so I also need to keep the rows
        # with nans, because some of them are likely to be Affe
        df_nans = df[df['metadata'].isna()]

        df_refined = pd.concat([df_substring, df_nans])

        df_refined.to_csv(self.fullpath_nfts_refined_data, index=False)
        return df_refined
    # ------------------------ END FUNCTION ------------------------ #

    def get_extra_metadata_from_opensea(self, df_with_refined_nft_data: pd.DataFrame = pd.DataFrame) -> pd.DataFrame:
        """
        This method receives a dataframe that has info in it about NFTs, but up to this point
        that data only has the metadata that Opensea stores in the URI location. However, Opensea
        seems to store additional properties about the NFTs offchain AND somewhere that is not at
        the token URI. This method attempts to grab that additional data using Selenium.
        :param df_with_refined_nft_data: The information about NFTs can be passed
          directly to this method in this parameter. If this parameter is not provided, this
          method will attempt to laod the information from a default location on disk containing
          refined nft data.
        :return:
        """
        df = df_with_refined_nft_data
        if df_with_refined_nft_data.empty:
            df = pd.read_csv(self.fullpath_nfts_refined_data)

        # because the function that gets token metadata takes as an input a particular contract
        # address, we should filter the df (in case it was not done already upstream) to that
        # particular contract
        df = df[df['token_address'] == self.affe_contract_address]
        set_token_ids = set(df['token_id'])

        opensea = SeleniumOnOpensea()
        opensea.start_driver()
        df_extra_data = opensea.get_many_nfts_properties(self.affe_contract_address, set_token_ids)
        opensea.close_driver()

        df_extra_data.to_csv(self.fullpath_nfts_extra_data, index=False)
        return df_extra_data
    # ------------------------ END FUNCTION ------------------------ #

    def combine_data(self,
                     list_of_dataframes_with_data_to_combine: list[pd.DataFrame] = []) -> pd.DataFrame:
        """
        This method combines several dataframes that contain relevant data about the NFTs. The
        dataframes are assumed to all contain a column called 'token_id' that can be used for
        the merge.
        :param list_of_dataframes_with_data_to_combine: A list containing the dataframes with NFT data.
        :return: A pandas dataframe with the combined information of all the dataframes that were
          joined based on 'token_id'.
        """
        df_refined = pd.DataFrame
        df_extras = pd.DataFrame
        # If no list was passed, this method will attempt to grab data from the refined NFT data
        # and the extra opensea data on disk.
        if not list_of_dataframes_with_data_to_combine:
            df_refined = pd.read_csv(self.fullpath_nfts_refined_data)
            df_extras = pd.read_csv(self.fullpath_nfts_extra_data)
            list_of_dataframes_with_data_to_combine = [df_extras, df_refined]

        counter = 0
        df_combined = list_of_dataframes_with_data_to_combine[counter]
        df_combined.set_index('token_id', inplace=True)
        num_dfs_to_combine_with = len(list_of_dataframes_with_data_to_combine) - 1
        while counter < num_dfs_to_combine_with:
            counter += 1
            df_to_combine_with = list_of_dataframes_with_data_to_combine[counter]
            df_to_combine_with.set_index('token_id', inplace=True)
            df_combined = df_combined.merge(df_to_combine_with, how='outer', left_index=True, right_index=True)

        df_combined.reset_index(inplace=True)
        df_combined.to_csv(self.fullpath_combined_nft_data, index=False)
        return df_combined
    # ------------------------ END FUNCTION ------------------------ #

    def reorganize_the_data(self,
                            list_with_ordered_column_names: list,
                            df_with_combined_data: pd.DataFrame = pd.DataFrame) -> pd.DataFrame:
        """
        This method receives a dataframe that has info in it about NFTs, and does a bit of
        clean-up, such as reorganizing the columns.
        :param list_with_ordered_column_names: An ordered list containing the column names of the columns that
          should appear first in the re-ordered dataframe.
        :param df_with_combined_data: The information about NFTs can be passed
          directly to this method in this parameter. If this parameter is not provided, this
          method will attempt to laod the information from a default location on disk containing
          refined nft data.
        :return: A pandas dataframe with the data somewhat reorganized.
        """
        df = df_with_combined_data
        if df_with_combined_data.empty:
            df = pd.read_csv(self.fullpath_combined_nft_data)

        counter = 0
        for col_name in list_with_ordered_column_names:
            col = df[col_name]
            df.drop(columns=[col_name], inplace=True)
            df.insert(loc=counter, column=col_name, value=col)
            counter += 1

        df.to_csv(self.fullpath_final, index=False)
        return df
    # ------------------------ END FUNCTION ------------------------ #

    def show_data_on_console(self, df_with_final_data: pd.DataFrame = pd.DataFrame) -> pd.DataFrame:
        """
        This method receives a dataframe that has info in it about NFTs, prints the dataframe to the console.
        :param df_with_final_data: The information about NFTs can be passed
          directly to this method in this parameter. If this parameter is not provided, this
          method will attempt to laod the information from a default location on disk containing
          refined nft data.
        :return: A pandas dataframe with the data somewhat reorganized.
        """
        df = df_with_final_data
        if df_with_final_data.empty:
            df = pd.read_csv(self.fullpath_final)

        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_colwidth", 25)
        pd.set_option("display.width", 1000)
        pd.set_option("display.max_rows", 250)
        print((df.iloc[:, : 14]).head(250))
    # ------------------------ END FUNCTION ------------------------ #

    def load_previously_fetched_data(self) -> pd.DataFrame:
        """
        This method attempts to load from disk a set of 'finalized' (retrieved, filtered, cleaned, etc.)
        Affen data..
        :return: A pandas dataframe with the data somewhat reorganized.
        """
        df = pd.DataFrame
        if  exists(self.fullpath_final):
            df = pd.read_csv(self.fullpath_final)
        return df
    # ------------------------ END FUNCTION ------------------------ #
