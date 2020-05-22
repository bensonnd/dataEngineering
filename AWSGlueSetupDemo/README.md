## AWS Setup Demo - Provisioning AWS s3 and Glue
Hi! Welcome to my mini datawarehouse for the demobucket game. Please enjoy!

    
init.py will pip install all the necesarry packages, setup temporary access to s3, and start the AWSExtract script.

AWSExtract.py will setup the folder structure in S3, extract the data from source, flatten it, and load to s3 raw, 
deploy job scripts to s3, and then start AWSGlueInit script.

AWSGlueInit.py will setup Glue workflows, triggers, crawlers, and jobs and start the workflows.

Workflows:
    Crawl raw data in s3 => start job to transform raw data and put into lz => crawl lz data in s3 =>
    start job to put data into proc => crawl proc data in s3

Data flow:
    source => raw => lz => proc
