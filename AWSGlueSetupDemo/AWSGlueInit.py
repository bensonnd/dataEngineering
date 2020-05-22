#! /usr/bin/python
print('Beginning AWS Glue Setup')

import boto3, os, base64
from configparser import ConfigParser
from botocore.exceptions import ClientError


parser = ConfigParser()
parser.read('dev.ini')

# get config values
AWS_KEY_ID = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SESSION = os.getenv('AWS_SESSION_TOKEN')
region = parser.get('aws', 'region')
bucket = parser.get('aws', 'bucketname')
gluerole = parser.get('aws', 'gluerole')
sourcedata = ['gamedata', 'playerdata']
s3targets = {'gamedata': {
    'raw': ['games'],
    'lz': ['games'],
    'proc': ['games']},
            'playerdata': {
        'raw': ['player'],
        'lz': ['player', 'contactinfo', 'login', 'pictures'],
        'proc': ['player', 'contactinfo', 'login', 'pictures']}
}

# list the dbs in config file
dbs = []
for i in parser.items('db'):
    dbs.append(i[1])

# Generate the boto3 client for interacting with Glue
glue = boto3.client('glue', region_name=region,
                    aws_access_key_id=AWS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET,
                    aws_session_token=AWS_SESSION)


# list crawlers function
def crawler_list():
    crawlerlist = []
    crawlers = glue.get_crawlers(
        MaxResults=100)
    for crawler in crawlers['Crawlers']:
        crawlerlist.append(crawler['Name'])
    return crawlerlist


# create crawlers function
def create_crawlers(role, bucket, path, db, source, target):
    """Function to create crawlers in AWS
    :param str name: The name of your crawler ex. 'crawlmysourcempgdata'
    :param str role: The AWS arn
    :param str bucket: The AWS bucket your crawlers will point to ex. 'uniquebucketname'
    :param str path: The AWS key/folder your ex. s3://{bucket}/{db}/{name}/
    :param str db: ex. 'dev', 'stg', 'prod'
    """

    response = glue.create_crawler(
        Name=f'{source}_{db}_{target}_crawler',
        Role=role,
        DatabaseName=bucket,
        Description=f'Crawls the {source} {db} {target} data',
        Targets={
            'S3Targets': [
                {
                    'Path': path,
                    'Exclusions': ['*__committed_*']
                },
            ],
            'JdbcTargets': [],
            'DynamoDBTargets': [],
            'CatalogTargets': []
        },
        # Schedule='string',
        Classifiers=[],
        TablePrefix=f'{db}_',
        SchemaChangePolicy={
            'UpdateBehavior': 'UPDATE_IN_DATABASE',
            'DeleteBehavior': 'DEPRECATE_IN_DATABASE'
        },
        Configuration='{"Version":1.0,"Grouping":{"TableGroupingPolicy":"CombineCompatibleSchemas"}}',
        # CrawlerSecurityConfiguration='string',
        Tags={
            'source': source,
            'db': db,
            'target': target
        }
    )
    return response


# list jobs function
def jobs_list():
    joblist = []
    jobs = glue.get_jobs(
        MaxResults=100)
    for job in jobs['Jobs']:
        joblist.append(job['Name'])
    return joblist


# create jobs function
def create_jobs(bucket, role, db, source):
    response = glue.create_job(
        Name=f'{source}_to_{db}_job',
        Description=f'Job to put {source} data in {db}',
        Role=role,
        ExecutionProperty={
            'MaxConcurrentRuns': 1
        },
        Command={
            'Name': 'glueetl',
            'ScriptLocation': f's3://{bucket}/{db}/{source}/scripts/{source}_to_{db}.py',
            'PythonVersion': '3'
        },
        DefaultArguments={
        },
        NonOverridableArguments={
        },
        # Connections={
        #     'Connections': [
        #         's3',
        #     ]
        # },
        MaxRetries=3,
        # AllocatedCapacity=10, #depracated
        Timeout=2880,
        MaxCapacity=10,
        # SecurityConfiguration='string',
        Tags={
            'source': source,
            'db': db
        },
        NotificationProperty={
            'NotifyDelayAfter': 60
        },
        GlueVersion='1.0',
        # NumberOfWorkers=8,
        # WorkerType='Standard'
    )
    return response


# list workflows function
def wf_list():
    wflist = []
    wfs = glue.list_workflows(
        MaxResults=25)
    for wf in wfs['Workflows']:
        wflist.append(wf)
    return wflist


# create workflows function
def create_wf(name, source):
    response = glue.create_workflow(
        Name=name,
        Description=f'Move {name} from source to target.',
        DefaultRunProperties={
            # 'key': 'value'
        },
        Tags={
            'source': source,
        }
    )
    return response


# start workflows function
def start_wf(workflow):
    response = glue.start_workflow_run(
        Name=workflow
    )
    return response


# create triggers function
def create_triggers(workflow, source, logical, conditions, actions, name, type):
    if type == 'ON_DEMAND':
        StartOnCreationBool = False
    else:
        StartOnCreationBool = True
    response = glue.create_trigger(
        Name=name,
        WorkflowName=workflow,
        Type=type,
        Predicate={
            'Logical': logical,
            'Conditions': conditions
        },
        Actions=actions,
        Description='string',
        StartOnCreation=StartOnCreationBool,
        Tags={
            'source': source
        }
    )
    return response


# list triggers function
def trigger_list():
    triggerlist = []
    triggers = glue.list_triggers(
        MaxResults=25
    )
    for trigger in triggers['TriggerNames']:
        triggerlist.append(trigger)
    return triggerlist


# list the existing glue objects
crawlerlist = crawler_list()
workflowlist = wf_list()
trigger_list = trigger_list()

# create workflows
for source in sourcedata:
    workflowname = f'{source}_wf'
    if workflowname not in workflowlist:
        create_wf(workflowname, source)

print('Workflows created')

# create jobs
for db in dbs:
    for source in sourcedata:
        jobname = f'{source}_to_{db}_job'
        joblist = jobs_list()
        if db != 'raw' and jobname not in joblist:
            create_jobs(bucket, gluerole, db, source)

print('Jobs created')

# create crawlers
for db in dbs:
    for source in sourcedata:
        for target in s3targets[source][db]:
            path = f's3://{bucket}/{db}/{source}/{source}_{target}/'
            crawlername = f'{source}_{db}_{target}_crawler'

            # create crawlers
            if crawlername not in crawlerlist:
                create_crawlers(gluerole, bucket, path, db, source, target)

print('Crawlers created')

# create trigger conditions and actions from this dictionary
# TODO: The creation of this dictionary may be automated
triggerstocreate = [
    {
        'name': 'gamedata_raw_games_crawler_trig',
        'type': 'OnDemandActivateCrawler',
        'awstype': 'ON_DEMAND',
        'conditions': [],
        'actions': [{'CrawlerName': 'gamedata_raw_games_crawler'}],
        'source': 'gamedata',
        'workflow': 'gamedata_wf',
        'target': 'games'
    },
    {
        'name': 'gamedata_to_lz_job_trig',
        'type': 'CrawlercompleteActivateJob',
        'awstype': 'CONDITIONAL',
        'conditions': [
            {'LogicalOperator': 'EQUALS', 'CrawlerName': 'gamedata_raw_games_crawler', 'CrawlState': 'SUCCEEDED'}],
        'actions': [{'JobName': 'gamedata_to_lz_job', 'Arguments': {}, 'Timeout': 2880,
                     'NotificationProperty': {'NotifyDelayAfter': 60}}],
        'source': 'gamedata',
        'workflow': 'gamedata_wf',
        'target': 'games'
    },
    {
        'name': 'gamedata_lz_games_crawler_trig',
        'type': 'JobCompleteActivateCrawler',
        'awstype': 'CONDITIONAL',
        'conditions': [{'LogicalOperator': 'EQUALS', 'JobName': 'gamedata_to_lz_job', 'State': 'SUCCEEDED'}],
        'actions': [{'CrawlerName': 'gamedata_lz_games_crawler'}],
        'source': 'gamedata',
        'workflow': 'gamedata_wf',
        'target': 'games'
    },
    {
        'name': 'gamedata_to_proc_job_trig',
        'type': 'CrawlercompleteActivateJob',
        'awstype': 'CONDITIONAL',
        'conditions': [
            {'LogicalOperator': 'EQUALS', 'CrawlerName': 'gamedata_lz_games_crawler', 'CrawlState': 'SUCCEEDED'}],
        'actions': [{'JobName': 'gamedata_to_proc_job', 'Arguments': {}, 'Timeout': 2880,
                     'NotificationProperty': {'NotifyDelayAfter': 60}}],
        'source': 'gamedata',
        'workflow': 'gamedata_wf',
        'target': 'games'
    },
    {
        'name': 'gamedata_proc_games_crawler_trig',
        'type': 'JobCompleteActivateCrawler',
        'awstype': 'CONDITIONAL',
        'conditions': [{'LogicalOperator': 'EQUALS', 'JobName': 'gamedata_to_proc_job', 'State': 'SUCCEEDED'}],
        'actions': [{'CrawlerName': 'gamedata_proc_games_crawler'}],
        'source': 'gamedata',
        'workflow': 'gamedata_wf',
        'target': 'games'
    },
    {
        'name': 'playerdata_raw_player_crawler_trig',
        'type': 'OnDemandActivateCrawler',
        'awstype': 'ON_DEMAND',
        'conditions': [],
        'actions': [{'CrawlerName': 'playerdata_raw_player_crawler'}],
        'source': 'playerdata',
        'workflow': 'playerdata_wf',
        'target': 'player'
    },
    {
        'name': 'playerdata_to_lz_job_trig',
        'type': 'CrawlercompleteActivateJob',
        'awstype': 'CONDITIONAL',
        'conditions': [
            {'LogicalOperator': 'EQUALS', 'CrawlerName': 'playerdata_raw_player_crawler', 'CrawlState': 'SUCCEEDED'}],
        'actions': [{'JobName': 'playerdata_to_lz_job', 'Arguments': {}, 'Timeout': 2880,
                     'NotificationProperty': {'NotifyDelayAfter': 60}}],
        'source': 'playerdata',
        'workflow': 'playerdata_wf',
        'target': ['player', 'contactinfo', 'login', 'pictures']
    },
    {
        'name': 'playerdata_lz_crawler_trig_1',
        'type': 'JobCompleteActivateCrawler',
        'awstype': 'CONDITIONAL',
        'conditions': [{'LogicalOperator': 'EQUALS', 'JobName': 'playerdata_to_lz_job', 'State': 'SUCCEEDED'}],
        'actions': [{'CrawlerName': 'playerdata_lz_pictures_crawler'}, {'CrawlerName': 'playerdata_lz_player_crawler'}],
        'source': 'playerdata',
        'workflow': 'playerdata_wf',
        'target': ['player', 'pictures']
    },
    {
        'name': 'playerdata_lz_crawler_trig_2',
        'type': 'JobCompleteActivateCrawler',
        'awstype': 'CONDITIONAL',
        'conditions': [{'LogicalOperator': 'EQUALS', 'JobName': 'playerdata_to_lz_job', 'State': 'SUCCEEDED'}],
        'actions': [{'CrawlerName': 'playerdata_lz_login_crawler'},
                    {'CrawlerName': 'playerdata_lz_contactinfo_crawler'}],
        'source': 'playerdata',
        'workflow': 'playerdata_wf',
        'target': ['contactinfo', 'login']
    },
    {
        'name': 'playerdata_to_proc_job_trig',
        'type': 'CrawlercompleteActivateJob',
        'awstype': 'CONDITIONAL',
        'conditions': [{'LogicalOperator': 'EQUALS', 'CrawlerName': 'playerdata_lz_contactinfo_crawler',
                        'CrawlState': 'SUCCEEDED'},
                       {'LogicalOperator': 'EQUALS', 'CrawlerName': 'playerdata_lz_login_crawler',
                        'CrawlState': 'SUCCEEDED'},
                       {'LogicalOperator': 'EQUALS', 'CrawlerName': 'playerdata_lz_pictures_crawler',
                        'CrawlState': 'SUCCEEDED'},
                       {'LogicalOperator': 'EQUALS', 'CrawlerName': 'playerdata_lz_player_crawler',
                        'CrawlState': 'SUCCEEDED'}],
        'actions': [{'JobName': 'playerdata_to_proc_job', 'Arguments': {}, 'Timeout': 2880,
                     'NotificationProperty': {'NotifyDelayAfter': 60}}],
        'source': 'playerdata',
        'workflow': 'playerdata_wf',
        'target': ['player', 'contactinfo', 'login', 'pictures']
    },
    {
        'name': 'playerdata_proc_crawler_1',
        'type': 'JobCompleteActivateCrawler',
        'awstype': 'CONDITIONAL',
        'conditions': [{'LogicalOperator': 'EQUALS', 'JobName': 'playerdata_to_proc_job', 'State': 'SUCCEEDED'}],
        'actions': [{'CrawlerName': 'playerdata_proc_pictures_crawler'},
                    {'CrawlerName': 'playerdata_proc_player_crawler'}],
        'source': 'playerdata',
        'workflow': 'playerdata_wf',
        'target': ['player', 'pictures']
    },
    {
        'name': 'playerdata_proc_crawler_2',
        'type': 'JobCompleteActivateCrawler',
        'awstype': 'CONDITIONAL',
        'conditions': [{'LogicalOperator': 'EQUALS', 'JobName': 'playerdata_to_proc_job', 'State': 'SUCCEEDED'}],
        'actions': [{'CrawlerName': 'playerdata_proc_login_crawler'},
                    {'CrawlerName': 'playerdata_proc_contactinfo_crawler'}],
        'source': 'playerdata',
        'workflow': 'playerdata_wf',
        'target': ['contactinfo', 'login']
    }
]

# create triggers
for trigger in triggerstocreate:
    create_triggers(trigger['workflow'], trigger['source'], 'AND', trigger['conditions'], trigger['actions'],
                    trigger['name'], trigger['awstype'])

print('Triggers created')

print('Starting workflows')

# Start workflows
workflowlist = wf_list()
for wf in workflowlist:
    start_wf(wf)

print('Workflows started')

print('AWS Glue setup complete')
