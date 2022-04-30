from pathlib import Path
from os import getenv
from class_affe_data_orchestrator import AffeDataOrchestrator
from helper_functions import setup_logging

setup_logging()


if __name__ == "__main__":
    # Affe are in Opensea storefront at the following address
    opensea_storefront = "0x495f947276749ce646f68ac8c248420045cb7b5e"
    affe_orch = AffeDataOrchestrator(opensea_storefront, Path(getenv('DATA_PATH')))
    affe_orch.build_affen_data_files(request_moralis_metadata_resync=False)