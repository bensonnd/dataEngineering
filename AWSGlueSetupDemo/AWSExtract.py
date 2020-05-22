#! /usr/bin/python
import boto3, subprocess, requests, json, os, sys
import pyarrow as pa
import pandas as pd
from io import BytesIO, StringIO
from configparser import ConfigParser
from datetime import datetime
import base64
from botocore.exceptions import ClientError


def dataframe_to_s3(s3_client, input_datafame, bucket_name, filepath, format):
    """This function gets parquet output in a buffer and then writes
        buffer.values() to S3 without saving parquet locally
    """
    if format == 'parquet':
        out_buffer = BytesIO()
        input_datafame.to_parquet(out_buffer, index=False)

    elif format == 'csv':
        out_buffer = StringIO()
        input_datafame.to_parquet(out_buffer, index=False)

    s3_client.put_object(Bucket=bucket_name, Key=filepath, Body=out_buffer.getvalue())


def get_json(endpoint) -> list:
    """
    A function to iterate through a paginated API in JSON format.
    :param str endpoihnt: The JSON endpoint that you would like to extract
    :return results - a list of dictionaries of the JSON data records.
    """
    headers = {'Content-Type':'application/json',}
    page_num = 0
    PARAMS = {'page': page_num}
    session = requests.Session()
    response = session.get(endpoint, params=PARAMS, headers=headers)
    results = []
    while int(response.headers["Content-Length"]) > 2:
    # while page_num < 2:
        response = session.get(endpoint, params=PARAMS, headers=headers)
        resp_json = response.json()
        for i in resp_json:
            results.append(i)
        page_num += 1
        PARAMS = {'page': page_num}
    return results


parser = ConfigParser()
parser.read('dev.ini')


# get aws credentials and region set in init file
AWS_KEY_ID = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SESSION = os.getenv('AWS_SESSION_TOKEN')
region = parser.get('aws','region')

# Generate the boto3 client for interacting with S3
s3 = boto3.client('s3', region_name=region,
                  aws_access_key_id=AWS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET,
                  aws_session_token=AWS_SESSION)

# Generate the boto3 client for interacting with S3
s3Resource = boto3.resource('s3', region_name=region,
                  aws_access_key_id=AWS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET,
                  aws_session_token=AWS_SESSION)

# list the dbs from config file
dbs = []
for (each_key, each_val) in parser.items('db'):
    dbs.append(each_val)


# TODO: this can be abstracted and used in audit process/ETLControl - with JobID, BatchID and RunID
batchID = datetime.now().strftime('%Y%m%d%H%M%S') # ('%Y%m%d%H%M%S')


# List the buckets
buckets = s3.list_buckets()
bucketlist = [i['Name'] for i in buckets['Buckets']]


# create s3 buckets
bucket = parser.get('aws','bucketname')
sourcedata = ['gamedata','playerdata']
s3targets = {'gamedata': {
                'raw': ['games'],
                'lz': ['games'],
                'proc': ['games']},
             'playerdata': {
                 'raw': ['player'],
                 'lz': ['player', 'contactinfo', 'login', 'pictures'],
                 'proc': ['player', 'contactinfo', 'login', 'pictures']}
             }

if bucket not in bucketlist:
    s3.create_bucket(Bucket=f'{bucket}')


buckettoempty = s3Resource.Bucket(bucket)
buckettoempty.objects.all().delete()

print(f'S3 Bucket {bucket} created')

# Read the raw game data from the CSV into a dataframe
gamedataurl = 'https://s3-us-west-2.amazonaws.com/<yoursourcefilehere>/game_data.csv'
gamedf = pd.read_csv(gamedataurl)

print('CSV extracted')

print('JSON extracting')
# Get JSON paginated player data into a dataframe
playerprofileurl = 'https://x37sv76kth.execute-api.us-west-1.amazonaws.com/prod/<yoursourceapihere>'
playerdf = pd.DataFrame(get_json(playerprofileurl), columns=['id', 'data'])
json_struct = json.loads(playerdf.to_json(orient="records"))
df_flat = pd.json_normalize(json_struct)                                    # flatten out the JSON object
cols = list(df_flat.columns)
for col in cols:
    if col != 'id':
        colname = col.split('.', 1)[1]
        colname = colname.replace('.','_')
        df_flat.rename(columns={f'{col}': f'{colname}'}, inplace=True)      # rename the columns
        df_flat[f'{colname}'] = df_flat[f'{colname}'].astype(str)           # set as type str

print('Paginated JSON extracted and flattened')

# deploy job scripts to s3
for db in dbs:
    for source in sourcedata:
        if db != 'raw':
            s3.put_object(Bucket=f'{bucket}', Key=f'{db}/{source}/scripts/')
            s3.upload_file(Bucket=f'{bucket}', Key=f'{db}/{source}/scripts/{source}_to_{db}.py', Filename=f'./GlueJobScripts/{source}_to_{db}.py')

print(f'Job scripts deployed to s3')

# create the AWS keys/folders for parquet files and put the parquet files in s3 for JSON and CSV
for db in dbs:
    for source in sourcedata:
        for target in s3targets[source][db]:
            s3.put_object(Bucket=f'{bucket}', Key=f'{db}/{source}/{source}_{target}/')

            # Write CSV to Parquet in S3 Raw
            if db == 'raw' and source == 'gamedata':
                gamepathraw = f'{db}/{source}/{source}_{target}/{source}_{target}.parquet'
                dataframe_to_s3(s3, gamedf, bucket, gamepathraw, 'parquet')
                print(f'CSV extracted to s3://{bucket}/{db}/{source}/{source}_{target}/{source}_{target}.parquet')

            # Write JSON to Parquet in S3 Raw
            if db == 'raw' and source == 'playerdata':
                playerpathraw = f'{db}/{source}/{source}_{target}/{source}_{target}.parquet'
                dataframe_to_s3(s3, df_flat, bucket, playerpathraw, 'parquet')
                print(f'JSON extracted to s3://{bucket}/{db}/{source}/{source}_{target}/{source}_{target}.parquet')

print(f'S3 data folders created')

pythonpath = sys.executable
subprocess.call(f"{pythonpath} AWSGlueInit.py", shell=True)