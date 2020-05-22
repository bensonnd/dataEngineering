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


playerdata_contactinfoDF = glueContext.create_dynamic_frame.from_catalog(database = "demobucketdb",
                                                            table_name = "lz_playerdata_contactinfo",
                                                            redshift_tmp_dir = args["TempDir"],
                                                            transformation_ctx = "playerdata_contactinfoDF")

playerdata_playerDF = glueContext.create_dynamic_frame.from_catalog(database = "demobucketdb",
                                                            table_name = "lz_playerdata_player",
                                                            redshift_tmp_dir = args["TempDir"],
                                                            transformation_ctx = "playerdata_playerDF")

playerdata_loginDF = glueContext.create_dynamic_frame.from_catalog(database = "demobucketdb",
                                                            table_name = "lz_playerdata_login",
                                                            redshift_tmp_dir = args["TempDir"],
                                                            transformation_ctx = "playerdata_loginDF")

playerdata_picturesDF = glueContext.create_dynamic_frame.from_catalog(database = "demobucketdb",
                                                            table_name = "lz_playerdata_pictures",
                                                            redshift_tmp_dir = args["TempDir"],
                                                            transformation_ctx = "playerdata_picturesDF")


datasinkCI = glueContext.write_dynamic_frame.from_options(frame=playerdata_contactinfoDF,
                                                               connection_type="s3", connection_options={
                                                               "path": "s3://demobucketdb/proc/playerdata/playerdata_contactinfo"}, format="parquet",
                                                               transformation_ctx="datasinkCI")

datasinkPL = glueContext.write_dynamic_frame.from_options(frame=playerdata_playerDF,
                                                               connection_type="s3", connection_options={
                                                               "path": "s3://demobucketdb/proc/playerdata/playerdata_player"}, format="parquet",
                                                               transformation_ctx="datasinkPL")

datasinkLO = glueContext.write_dynamic_frame.from_options(frame=playerdata_loginDF,
                                                               connection_type="s3", connection_options={
                                                               "path": "s3://demobucketdb/proc/playerdata/playerdata_login"}, format="parquet",
                                                               transformation_ctx="datasinkLO")

datasinkPI = glueContext.write_dynamic_frame.from_options(frame=playerdata_picturesDF,
                                                               connection_type="s3", connection_options={
                                                               "path": "s3://demobucketdb/proc/playerdata/playerdata_pictures"}, format="parquet",
                                                               transformation_ctx="datasinkPI")

job.commit()