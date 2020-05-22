import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


game_dataDF = glueContext.create_dynamic_frame.from_catalog(database = "demobucketdb", table_name = "lz_gamedata_games", redshift_tmp_dir = args["TempDir"], transformation_ctx = "game_dataDF")


game_data_games = glueContext.write_dynamic_frame.from_options(frame=game_dataDF,
                                                               connection_type="s3", connection_options={
                                                               "path": "s3://demobucketdb/proc/gamedata/gamedata_games"}, format="parquet",
                                                               transformation_ctx="game_data_games")
job.commit()