import json
import boto3
import logging
from math import isnan
from botocore.exceptions import ClientError
from time import sleep


if __name__ == '__main__':
    affen_json_file = "/home/mclovin/my_projects_github_mcIovin/" \
                      "get-affe-data/data/output/flat_json/00_all_affen_flat.json"
    list_of_affen = []
    with open(affen_json_file, mode='r') as f:
        list_of_affen = json.load(f)

    # One of the Affe is missing a name and AK47, which will cause an error, so we manually
    # populate them here...
    index_of_affe_13 = 12
    if list_of_affen[index_of_affe_13]['name'] == '':
        list_of_affen[index_of_affe_13]['name'] = "PR1M473 D0NN4"
    ak47ofNo13 = list_of_affen[index_of_affe_13]['AK47']
    if type(ak47ofNo13) is float and isnan(ak47ofNo13):
        list_of_affen[index_of_affe_13]['AK47'] = ''

    # For some reason, one of the Affe ends-up without an image URL, so we manually
    # populate it here...
    index_of_affe_93 = 92
    if list_of_affen[index_of_affe_93]['image'] == '':
        list_of_affen[index_of_affe_93]['image'] = "https://lh3.googleusercontent.com/bcowHA7QAB-evBtHrnFxtzCsdDmoytpHmNjbF6r9JNbzxkGPOcjE2I6OEzWo31RWSrPL_7A5nBsaDjaK3TJQU4MnsH5l0M6SPQdA2i4=w600"

    # Moving #97's 'special attribute' to the 'SPECIAL ABILITY' column
    index_of_affe_97 = 96
    list_of_affen[index_of_affe_97]['SPECIAL ABILITY'] = list_of_affen[index_of_affe_97].pop('SPECIAL ATTRIBUTE')

    # Affe #47 Has a typo in the Anticipation column, and doesn't get populated so correcting that here
    index_of_affe_47 = 46
    list_of_affen[index_of_affe_47]['Anticipation'] = 2

    # Add an Affe that won't be part of the collection to the end of the list, which allows
    # the addition of some additional traits.
    dummy_affe = {
        'id': 0,
        'name': 'Tina Fape',
        'description': 'Tina was arguably, the funniest Primate of all time.',
        'Birth Order': 'zero',
        'AK47': 'Urine Piss-tol',
        'Special Trait': 'Super Humour',
        'Perfume': 'Ten Thousand Nuns',
        'Hobby': 'Laughing',
        'Art Movement': 'Pop',
        'World View': 'Apetimistic',
        'Costume': 'Lemon',
        'Body Feature': 'Plain',
        'Vehicle': 'Bone Crusher',
        'Invention': 'Banana Umbrella',
        'Book': "Apehiker's Guide to the Sañctuary",
        'Curiosity': 'cat',
        'Piece Of Art': 'Girl With a Banana Earring',
        'Furniture': 'FJÄDERMOLN'
    }
    list_of_affen.append(dummy_affe)

    #boto3_sesh = boto3.Session(profile_name='Monkeyverse-romeo', region_name='eu-central-1')  # PRODUCTION
    boto3_sesh = boto3.Session(profile_name='MYAWS-sam-affen-app-cris-admin', region_name='us-east-2')  # my testing
    dynamodb = boto3_sesh.resource('dynamodb')
    table = dynamodb.Table('aws-SAM-affen-db')

    try:
        with table.batch_writer() as writer:
            for item in list_of_affen:
                #if item['id'] in [0]:  # TO RUN for specific Affe (edit the items in the list accordingly)
                if item['id'] not in [0]:  # TO RUN FOR ALL (no need to modify this line; it works for all as is)

                    # We also want to rename 'JEWELLERY' to 'JEWELRY'
                    if 'JEWELLERY' in item:
                        item['JEWELRY'] = item.pop('JEWELLERY')

                    writer.put_item(Item=item)
                    print(f"Putting affe with 'id': {item['id']} into the batch.")
                    #sleep(0.25)

    except ClientError:
        print("Couldn't load data into table %s.", table.name)
        raise
