import logging
from pathlib import Path
from os import getenv
from class_selenium_opensea import SeleniumOnOpensea
from helper_functions import setup_logging

setup_logging(destination='both',
              file_logging_level='debug',
              console_logging_level='info',
              full_path_to_log_file=Path(getenv('DATA_PATH')) / 'main.log')


if __name__ == "__main__":
    logging.info(" -------------------- STARTING MAIN PROGRAM -------------------- ")
    # Affe are in Opensea storefront at the following address
    #contract = "0xf77efd6810a8547543e7fcb1f6713f09e3a5df8e"  #GOERLI TEST ADDRESS
    #network = "goerli"
    contract = "0x732efbe05dabe70185c96a7efa3f12dd70d5703c"  #RINKEBY TEST ADDRESS
    network = "rinkeby"
    iterable_with_token_ids = range(1, 238)

    opensea = SeleniumOnOpensea(contract)
    opensea.start_driver()
    opensea.refresh_many_nfts(iterable_with_token_ids, network, wait_x_seconds_per_request=0.5)
    opensea.close_driver()
