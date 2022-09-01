import pandas as pd
import boto3
from typing import Any, List, Mapping
from time import sleep


if __name__ == '__main__':

    nan_number_replace = -1
    nan_string_replace = "<>"
    replace_nan_values = {
        'Anticipation': nan_number_replace,
        'Disgust': nan_number_replace,
        'Positive': nan_number_replace,
        'Surprise': nan_number_replace,
        'Sadness': nan_number_replace,
        'Joy': nan_number_replace,
        'Negative': nan_number_replace,
        'Anger': nan_number_replace,
        'Trust': nan_number_replace,
        'Fear': nan_number_replace,
        'SPECIAL ABILITY': nan_string_replace,
        'TRINKET': nan_string_replace,
        'PIPE': nan_string_replace,
        'PET': nan_string_replace,
        'SUNGLASSES': nan_string_replace,
        'APEBALL': nan_string_replace,
        'TITLE': nan_string_replace,
        'FLOWER': nan_string_replace,
        'MONOCLE': nan_string_replace,
        'HAT': nan_string_replace,
        'FRIEND': nan_string_replace,
        'ABILITY': nan_string_replace,
        'DRINK': nan_string_replace,
        'CIGAR': nan_string_replace,
        'FOOD': nan_string_replace,
        'SEASON': nan_string_replace,
        'HOME': nan_string_replace,
        'BOWTIE': nan_string_replace,
        'JEWELRY': nan_string_replace,
        'FIREWORKS': nan_string_replace,
        'Perfume': nan_string_replace,
        'Special Trait': nan_string_replace,
        'Curiosity': nan_string_replace,
        'Invention': nan_string_replace,
        'Book': nan_string_replace,
        'Costume': nan_string_replace,
        'World View': nan_string_replace,
        'Hobby': nan_string_replace,
        'Furniture': nan_string_replace,
        'Piece Of Art': nan_string_replace,
        'Vehicle': nan_string_replace,
        'Art Movement': nan_string_replace,
        'Body Feature': nan_string_replace,
        'GROUP': nan_string_replace,
        'PANTS': nan_string_replace,
        'FLAG': nan_string_replace
    }

    # boto3_sesh = boto3.Session(profile_name='Monkeyverse-romeo', region_name='eu-central-1')  # PRODUCTION
    boto3_sesh = boto3.Session(profile_name='MYAWS-sam-affen-app-cris-admin', region_name='us-east-2')  # my testing
    dynamodb = boto3_sesh.resource('dynamodb')
    table = dynamodb.Table('aws-SAM-affen-db')
    all_items = table.scan()

    df = pd.DataFrame(all_items['Items'])

    df.set_index('id', inplace=True)
    df.sort_index(inplace=True)
    df.reset_index(inplace=True)

    df.replace({'':'<>', '<empty>':'<>'}, inplace=True)
    df.fillna(value=replace_nan_values, inplace=True)

    #wr.dynamodb.put_df(df=df, table_name='aws-SAM-affen-db')

    # Code below is not really my own. I extracted much it from the awswrangler library,
    # which was not working reliably every time. I ran into a similar issue when just using
    # the batch writer as-is, but got better results when I asked it to sleep briefly.
    # So I'm basically copy pasting the awswrangler code so I can insert a 'sleep'
    items: List[Mapping[str, Any]] = [v.dropna().to_dict() for k, v in df.iterrows()]
    # validate items
    table_keys = [schema["AttributeName"] for schema in table.key_schema]
    if not all(key in item for item in items for key in table_keys):
        raise Exception("All items need to contain the required keys for the table.")
    # batch-write the items
    try:
        with table.batch_writer() as writer:
            for item in items:
                writer.put_item(Item=item)
                print(f"Putting affe with 'id': {item['id']} into the batch.")
                sleep(0.2)
    except Exception as e:
        print(f"Couldn't load the data. Exception was {repr(e)}")
        raise

