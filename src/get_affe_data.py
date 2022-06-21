import logging
from pathlib import Path
from os import getenv
from class_affe_data_getter import AffeDataGetter
from class_affe_data_manipulator import AffeDataManipulator
from helper_functions import setup_logging

setup_logging(destination='both',
              file_logging_level='debug',
              console_logging_level='info',
              full_path_to_log_file=Path(getenv('DATA_PATH')) / 'main.log')


if __name__ == "__main__":
    logging.info(" -------------------- STARTING MAIN PROGRAM -------------------- ")
    # Affe are in Opensea storefront at the following address
    opensea_storefront = "0x495f947276749ce646f68ac8c248420045cb7b5e"
    full_path_data_dir = Path(getenv('DATA_PATH'))
    affe_getter = AffeDataGetter(opensea_storefront, full_path_data_dir)
    affe_getter.build_affen_data_files(request_moralis_metadata_resync=False, use_data_already_on_disk=False)
    affe_manip = AffeDataManipulator(affe_getter.load_previously_fetched_data(), full_path_data_dir)
    affe_manip.dump_all_to_json()
