# import boto3
#
#
# if __name__ == '__main__':
#     dynamodb = boto3.resource('dynamodb')
#
#     table = dynamodb.create_table(
#         TableName='Affe_mit_Waffe',
#         KeySchema=[
#             {
#                 'AttributeName': 'id',
#                 'KeyType': 'HASH'
#             }#,
#             # {
#             #     'AttributeName': 'name',
#             #     'KeyType': 'RANGE'
#             # }
#         ],
#         AttributeDefinitions=[
#             {
#                 'AttributeName': 'id',
#                 'AttributeType': 'N'
#             }#,
#             # {
#             #     'AttributeName': 'name',
#             #     'AttributeType': 'S'
#             # }
#         ],
#         ProvisionedThroughput={
#             'ReadCapacityUnits': 5,
#             'WriteCapacityUnits': 5
#         }
#
#     )
#     print(table)
