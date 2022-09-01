import awswrangler as wr
import pandas as pd
import boto3


if __name__ == '__main__':

    file_with_museum_tokens =\
        "/home/mclovin/my_projects_github_mcIovin/get-affe-data/data/output/museum_tokens/" \
        "2022-08-29_tokens_in_museum.csv"

    df_tokens = pd.read_csv(file_with_museum_tokens)
    list_museum_tokens = list(df_tokens['name'].apply(lambda x: x.split(sep='#', maxsplit=1)[1]))
    #
    # dynamodb = boto3.resource('dynamodb')
    # table = dynamodb.Table('aws-SAM-affen-db')
    # all_items = table.scan()
    #
    # df = pd.DataFrame(all_items['Items'])
    #
    # df.set_index('id', inplace=True)
    # df.sort_index(inplace=True)
    # df.reset_index(inplace=True)
    #
    # #df.iloc[4, df.columns.get_loc('Trusts in Humanity')] = True
    # #df.rename(columns={"Birth Order": "Birthday"}, inplace=True)
    #
    # wr.dynamodb.put_df(df=df, table_name='sam-stack-affen-TableAffeMitWaffe-1BC7SQWQPNJK2')
    #
    # print('here')
