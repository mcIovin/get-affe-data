from pathlib import Path
from os import getenv
from class_affe_data_orchestrator import AffeDataOrchestrator
from helper_functions import setup_logging

setup_logging()


if __name__ == "__main__":
    affe_orch = AffeDataOrchestrator(Path(getenv('DATA_PATH')))
    affe_orch.build_affen_data_file()
