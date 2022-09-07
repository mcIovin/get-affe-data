import logging
from pathlib import Path
from os import getenv
from class_api_interactions_moralis import MoralisAPIinteractions
from helper_functions import setup_logging

setup_logging(destination='both',
              file_logging_level='debug',
              console_logging_level='info',
              full_path_to_log_file=Path(getenv('DATA_PATH')) / 'main.log')


if __name__ == "__main__":
    logging.info(" -------------------- STARTING MAIN PROGRAM -------------------- ")

    museum_address = "0x11f515b85d46ba8aba99cc7a7b385fe9986fe964"

    full_path_data_dir = Path(getenv('DATA_PATH'))

    moralis = MoralisAPIinteractions()
    df = moralis.get_nft_transfers(museum_address, direction="to")

    df.to_csv(full_path_data_dir / "museum_transfers/transfers_to_museum.csv", index=False)
