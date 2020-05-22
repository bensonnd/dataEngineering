## AWS Setup Demo - Provisioning AWS s3 and Glue Using Python
Hi! Welcome to my mini datawarehouse for a demo game. Please enjoy!

The overall project extracts data from s3 in CSV and paginated JSON format, and will move to various stage keys in target s3 for RAW, LZ, and PROC. The data is initially transformed using Pandas, then passed to Glue jobs to transform the data using Spark and Python. 

The project provisions the s3 bucket structure, deploys the Glue job scripts, builds out the workflows, crawlers, triggers, and jobs in Glue. Finally, the workflows created move all the data from RAW => LZ => PROC and finish by crawling the data to add to the metastore so that the data can be queried in Athena. The entire process is mostly automated, except executing the init.py script. 
    
### init.py 
will pip install all the necesarry packages, setup temporary access to s3, and start the AWSExtract script.

### AWSExtract.py 
will setup the folder structure in S3, extract the data from source, flatten it, and load to s3 raw, 
deploy job scripts to s3, and then start AWSGlueInit script.

### AWSGlueInit.py 
will setup Glue workflows, triggers, crawlers, and jobs and start the workflows.

### Workflows
Crawl raw data in s3 => start job to transform raw data and put into lz => crawl lz data in s3 =>
start job to put data into proc => crawl proc data in s3

### Data flow
source => raw => lz => proc
    
### Data warehouse tables to query:
RAW:    raw_gamedata_games	
    	raw_playerdata_player

LZ:     lz_gamedata_games
	lz_playerdata_contactinfo
	lz_playerdata_login
    	lz_playerdata_pictures
    	lz_playerdata_player

PROC:    proc_gamedata_games
	proc_playerdata_contactinfo
    	proc_playerdata_login	
    	proc_playerdata_pictures
    	proc_playerdata_player

