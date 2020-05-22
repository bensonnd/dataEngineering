#! /usr/bin/python
from configparser import ConfigParser
import subprocess, sys, json, os

subprocess.call("pip install -r requirements.txt", shell=True)

import awscli

config = ConfigParser()


config['aws'] = {
    'bucketname' : 'demobucketdb',
    'region':   'us-east-1',

    # your own glue arn that should have sts assume role granted arn for devprofile id
    # this profile has admin read/write access to s3, Glue, and Athena
    # I put this here for demo purposes only. You would want to store thois in a much more secure manner.
    'gluerole': 'arn:aws:iam::111111111111:role/service-role/AWSGlueServiceRole-demobucket-data',   

    # this is the user/profile in IAM to give assume privileges so you can create temporary access and secret key
    # this IAM user has no access at all except an assume-role policy
    'devprofile': 'demodevdataengineer', 

     # I put these here for demo purposes only and then later in the code added them to aws config and credentials with a shell command.
     # You would want to store these in a much more secure manner.
    'aws_no_access_key_id': 'ABCD1234567891234567',                                              
    'aws_secret_no_access_key': 'abcd1234abcd1234abcd123abcd123abcd1234a/'
}

config['projectdetails'] = {
    'projectname' : 'demoproject'
}

# these are the different stages/dbs in a workflow. Yours might be setup like 'dev', 'stage', 'prod'
config['db'] = {
    'raw' : 'raw',
    'landingzone' : 'lz',
    'processed' : 'proc'
}

# write you config params to file in the directory
with open('./dev.ini', 'w') as f:
    config.write(f)


# setup for creating temporary AWS credentials
gluerole = config['aws']['gluerole']
region = config['aws']['region']
profile = config['aws']['devprofile']
access_key = config['aws']['aws_no_access_key_id']
secret_key = config['aws']['aws_secret_no_access_key']

# set temporary credentials for AWS in ~/.aws/config or credentials file
commands = [
    f'aws configure set aws_access_key_id {access_key} --profile {profile}',
    f'aws configure set aws_secret_access_key {secret_key} --profile {profile}',
    f'aws configure set region {region} --profile {profile}'
]

for command in commands:
    subprocess.call(command, shell=True)

# use AWS cli to get temp credentials via assume role. Your devprofile will be assuming role of gluerole for temp access
tempcredentials = subprocess.call(f'aws sts assume-role --role-arn {gluerole} --role-session-name'
                                  f' "RoleSession1" --profile {profile} > assume-role-output.txt', shell=True)

# write the temp credentials to a local file
tempvarpath = './assume-role-output.txt'
with open(tempvarpath, 'r') as temps:
    tempvars = json.loads(temps.read())

temps.close()

aws_temp_acces_key = tempvars['Credentials']['AccessKeyId']
aws_temp_secret_key = tempvars['Credentials']['SecretAccessKey']
aws_session_token = tempvars['Credentials']['SessionToken']

# set the temp credentials as environment variables for by othe scripts at runtime
os.environ['AWS_ACCESS_KEY'] = aws_temp_acces_key
os.environ['AWS_SECRET_ACCESS_KEY'] = aws_temp_secret_key
os.environ['AWS_SESSION_TOKEN'] = aws_session_token

# start the s3 provisioning script
pythonpath = sys.executable
subprocess.call(f"{pythonpath} AWSExtract.py", shell=True)


print('Initial setup complete and workflows started')

# clear your temp environment variables
subprocess.call(f'set AWS_ACCESS_KEY=', shell=True)
subprocess.call(f'set AWS_SECRET_ACCESS_KEY=', shell=True)
subprocess.call(f'set AWS_SESSION_TOKEN=', shell=True)