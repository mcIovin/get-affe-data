import logging
from os import mkdir
from os.path import exists
import pandas as pd
from pathlib import Path
from class_api_interactions_moralis import MoralisAPIinteractions


class AffeDataOrchestrator:
    """This class orchestrates the extraction of Affe data ."""

    def __init__(self, full_path_to_data_dir: Path):
        """
        Initialize the AffeDataOrchestrator class.
        Args:
            full_path_to_data_dir: Path to a directory where this class will output
              intermediate working files, and final output files to. The directory
              should already exist.
        """
        self.fullpath_intermediate_files = full_path_to_data_dir / 'intermediate_files'
        self.fullpath_output = full_path_to_data_dir / 'output'
        # This class will store some files on disk in two directories called
        # 'intermediate_files' and 'output', so we'll check to see if they exist,
        # and if not they will be created.
        if not exists(self.fullpath_intermediate_files):
            mkdir(self.fullpath_intermediate_files)
        if not exists(self.fullpath_output):
            mkdir(self.fullpath_output)
    # ------------------------ END FUNCTION ------------------------ #

    def build_affen_data_file(self, output_format="csv"):
        """
        This method gets as much data as it can about Affe mit Waffe, compiling the data
        from several sources, and produces an output file in the form of a csv or parquet.
        The output file is saved in a directory called 'output'.
        :param output_format: Can be "csv" or "parquet"
        """

        df = self.get_eoa_nft_transfers_from_moralis(do_some_refining=True)

        print(df)
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
            # contract of interest
            # the opensea storefront address we are interested in
            contract = "0x495f947276749ce646f68ac8c248420045cb7b5e"
            # account of interest
            # In this case, we are filtering the address that creates the Monkeyverse DAO NFTs
            # this is, in fact, the same address as above, but the results in the df have lower-case
            # address, so we are re-declaring the same addres, with different case, so the filtering
            # works
            eoa = "0x023a3905e3b33634758871712f4293ddb919b67f"

            # keep only the rows for a certain contract
            df = df[df['token_address'] == contract]
            # keep only the rows where the eoa is the 'from' address of interest
            df = df[df['from_address'] == eoa]

        output_file = self.fullpath_intermediate_files / 'xlii_transactions.csv'
        df.to_csv(output_file, index=False)
        return df
    # ------------------------ END FUNCTION ------------------------ #
