import pandas as pd
from pathlib import Path
from datetime import datetime

if __name__ == '__main__':

    address_of_museum = "0x11f515b85d46ba8aba99cc7a7b385fe9986fe964"

    input_file = "/home/mclovin/my_projects_github_mcIovin/get-affe-data/data/output/affe.csv"
    output_dir = Path("/home/mclovin/my_projects_github_mcIovin/get-affe-data/data/output/museum_tokens")

    df = pd.read_csv(input_file)
    df = df[df['owner_of'] == address_of_museum]

    df.to_csv(output_dir / f"{datetime.now().strftime('%Y-%m-%d')}_tokens_in_museum.csv", index=False)
