import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "demobucketdb", table_name = "raw_playerdata_player", transformation_ctx = "datasource0")

applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("id", "long", "player_id", "long"), ("gender", "string", "gender", "string"), ("name_title", "string", "title", "string"), \
("name_first", "string", "first_name", "string"), ("name_last", "string", "last_name", "string"), ("location_street", "string", "street", "string"), \
("location_city", "string", "city", "string"), ("location_state", "string", "state", "string"), ("location_postcode", "string", "postcode", "string"), \
("email", "string", "email", "string"), ("login_username", "string", "username", "string"), ("login_password", "string", "password", "string"), ("login_salt", "string", "login_salt", "string"), \
("login_md5", "string", "login_md5", "string"), ("login_sha1", "string", "login_sha1", "string"), ("login_sha256", "string", "login_sha256", "string"), ("dob", "string", "date_of_birth", "date"), \
("registered", "string", "registered", "timestamp"), ("phone", "string", "phone", "string"), ("cell", "string", "cell", "string"), ("id_name", "string", "id_name", "string"), \
("id_value", "string", "id_value", "string"), ("picture_large", "string", "picture_large", "string"), ("picture_medium", "string", "picture_medium", "string"), \
("picture_thumbnail", "string", "picture_thumbnail", "string"), ("nat", "string", "nationality", "string")], transformation_ctx = "applymapping1")

resolvechoice2 = ResolveChoice.apply(frame = applymapping1, choice = "make_struct", transformation_ctx = "resolvechoice2")

playersDF = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "playersDF")

playerdata_contactinfoDF = SelectFields.apply(frame = playersDF, paths = ["player_id", "street", "city", "state", "postcode", "phone", "cell", "email"], transformation_ctx = "playerdata_contactinfoDF")
playerdata_playerDF = SelectFields.apply(frame = playersDF, paths = ["player_id", "gender", "title", "first_name", "last_name", "date_of_birth", "registered", "nationality"], transformation_ctx = "playerdata_playerDF")
playerdata_loginDF = SelectFields.apply(frame = playersDF, paths = ["player_id", "username", "password", "login_salt", "login_md5", "login_sha1", "login_sha256", "id_name", "id_value"], transformation_ctx = "playerdata_loginDF")
playerdata_picturesDF = SelectFields.apply(frame = playersDF, paths = ["player_id", "picture_large", "picture_medium", "picture_thumbnail"], transformation_ctx = "playerdata_picturesDF")

datasinkCI = glueContext.write_dynamic_frame.from_options(frame = playerdata_contactinfoDF, connection_type = "s3", connection_options = {"path": "s3://demobucketdb/lz/playerdata/playerdata_contactinfo"}, format = "parquet", transformation_ctx = "datasinkCI")
datasinkPL = glueContext.write_dynamic_frame.from_options(frame = playerdata_playerDF, connection_type = "s3", connection_options = {"path": "s3://demobucketdb/lz/playerdata/playerdata_player"}, format = "parquet", transformation_ctx = "datasinkPL")
datasinkLO = glueContext.write_dynamic_frame.from_options(frame = playerdata_loginDF, connection_type = "s3", connection_options = {"path": "s3://demobucketdb/lz/playerdata/playerdata_login"}, format = "parquet", transformation_ctx = "datasinkLO")
datasinkPI = glueContext.write_dynamic_frame.from_options(frame = playerdata_picturesDF, connection_type = "s3", connection_options = {"path": "s3://demobucketdb/lz/playerdata/playerdata_pictures"}, format = "parquet", transformation_ctx = "datasinkPI")


job.commit()