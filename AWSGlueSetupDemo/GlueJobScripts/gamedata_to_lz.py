import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import row_number, monotonically_increasing_id
from pyspark.sql import Window
from pyspark.sql.functions import col
from pyspark.sql import functions as f
from pyspark.sql.types import *
from pyspark.sql.functions import sum as _sum


def cum_sum(df, sum_col, order_col, cum_sum_col_nm='cum_sum'):
    '''Find cumulative sum of a column.
    Parameters
    -----------
    sum_col : String
        Column to perform cumulative sum.
    order_col : List
        Column/columns to sort for cumulative sum.
    cum_sum_col_nm : String
        The name of the resulting cum_sum column.

    Return
    -------
    df : DataFrame
        Dataframe with additional "cum_sum_col_nm".

    '''
    df = df.withColumn('tmp', f.lit('tmp'))

    windowval = (Window.partitionBy('tmp')
                 .orderBy(order_col)
                 .rangeBetween(Window.unboundedPreceding, 0))

    df = df.withColumn('cum_sum', _sum(sum_col).over(windowval).alias('cumsum').cast(StringType()))
    df = df.drop('tmp')
    return df


def forward_fill(df, order_col, fill_col, fill_col_name=None):
    '''Forward fill a column by a column/set of columns (order_col).
    Parameters:
    ------------
    df: Dataframe
    order_col: String or List of string
    fill_col: String (Only work for a column for this version.)

    Return:
    ---------
    df: Dataframe
        Return df with the filled_cols.
    '''

    # "value" and "constant" are tmp columns created ton enable forward fill.
    df = df.withColumn('value', f.when(col(fill_col).isNull(), 0).otherwise(1))
    df = cum_sum(df, 'value', order_col).drop('value')
    df = df.withColumn(fill_col,
                       f.when(col(fill_col).isNull(), 'constant').otherwise(col(fill_col)))

    win = (Window.partitionBy('cum_sum')
           .orderBy(order_col))

    if not fill_col_name:
        fill_col_name = f'ffill_{fill_col}'

    df = df.withColumn(fill_col_name, f.collect_list(fill_col).over(win)[0])
    df = df.drop('cum_sum')
    df = df.withColumn(fill_col_name, f.when(col(fill_col_name) == 'constant', None).otherwise(col(fill_col_name)))
    df = df.withColumn(fill_col, f.when(col(fill_col) == 'constant', None).otherwise(col(fill_col)))
    return df


## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource0 = glueContext.create_dynamic_frame.from_catalog(database="demobucketdb",
                                                            table_name="raw_gamedata_games",
                                                            transformation_ctx="datasource0")

applymapping1 = ApplyMapping.apply(frame=datasource0, mappings=[("game_id", "string", "game_id", "string"),
                                                                ("player_id", "long", "player_id", "long"),
                                                                ("move_number", "long", "move_number", "long"),
                                                                ("column", "long", "column", "long"),
                                                                ("result", "string", "result", "string")],
                                   transformation_ctx="applymapping1")

resolvechoice2 = ResolveChoice.apply(frame=applymapping1, choice="make_struct", transformation_ctx="resolvechoice2")

dropnullfields3 = DropNullFields.apply(frame=resolvechoice2, transformation_ctx="dropnullfields3")

game_dataDF = dropnullfields3.toDF()

game_dataDF = (game_dataDF
               .withColumn("player_id", game_dataDF["player_id"].cast(IntegerType()))
               .withColumn("move_number", game_dataDF["move_number"].cast(IntegerType()))
               .withColumn("column", game_dataDF["column"].cast(IntegerType()))
               )

# ------------------------------------
# build data frame to clean up game_id

# fix the game id by selecting move_number == 1 and indexing
game_data_gameidnew = (game_dataDF.select('game_id', 'move_number')
                       .filter(game_dataDF.move_number == 1))

# index to correct for wrong game_id data type
newIDdf = game_data_gameidnew.withColumn("index", row_number().over(Window.orderBy(monotonically_increasing_id())) - 1)

# join updated IDs back to original DF, remove redundant columns and rename appropriately
game_dataDF = (game_dataDF.join(newIDdf, game_dataDF.game_id == newIDdf.game_id)
               .select(col('index').alias('game_id'), game_dataDF.player_id, game_dataDF.move_number,
                       game_dataDF.column, game_dataDF.result))

# ------------------------------------
# build data frame to identify winners, and both players if there is a draw
# Will eventually only return dataframe with each player and the result of the match for each player, win, lose, or draw
order_cols = ["game_id", f.desc("move_number")]

# fill in the result column for all moves - returns DF with col ffill_result
game_dataDF = forward_fill(game_dataDF, order_cols, 'result', fill_col_name=None)

# create dataframe to identify players who won, and both players in a draw using flag
game_data_res_wdDF = game_dataDF.withColumn('game_end', (f.when(col('result') != '', 'flag') \
                                                         .otherwise(''))) \
    .drop('result') \
    .withColumnRenamed('ffill_result', 'result')

game_data_res_wdDF = game_data_res_wdDF.withColumn('game_end', (f.when(col('result') == 'draw', 'flag') \
                                                                .otherwise(game_data_res_wdDF.game_end))) \
    .drop('move_number', 'column')

game_data_res_wdDF = game_data_res_wdDF.distinct() \
    .filter(game_data_res_wdDF.game_end == 'flag') \
    .drop('game_end')  # dropping flag

game_data_res_wdDF = (game_data_res_wdDF
                      .withColumnRenamed('game_id', 'game_id2')
                      .withColumnRenamed('player_id', 'player_id2')
                      .withColumnRenamed('result', 'result2'))

# left outer join back to game_dataDF with cleaned up IDs, identify those who lost, remove redundant columns and rename appropriately
game_dataDF = (game_dataDF.join(game_data_res_wdDF,
                                (game_dataDF.game_id == game_data_res_wdDF.game_id2) &
                                (game_dataDF.player_id == game_data_res_wdDF.player_id2), 'left_outer')
               .select(game_dataDF.game_id, game_dataDF.player_id, game_dataDF.move_number, game_dataDF.column,
                       game_data_res_wdDF.result2))

game_dataDF = (game_dataDF
               .withColumnRenamed('result2', 'result'))

game_dataDF = game_dataDF.withColumn('result',
                                     f.when(col('result').isNull(), 'lose').otherwise(col('result')))

game_dataDF = game_dataDF.dropDuplicates()

game_data_dynamicDF = DynamicFrame.fromDF(game_dataDF, glueContext, "game_data_dynamicDF")

game_data_results_update_game_id = ResolveChoice.apply(frame=game_data_dynamicDF, specs=[('game_id', 'cast:long')],
                                                       transformation_ctx="game_data_results_update_game_id")

game_data_games = glueContext.write_dynamic_frame.from_options(frame=game_data_results_update_game_id,
                                                               connection_type="s3", connection_options={
        "path": "s3://demobucketdb/lz/gamedata/gamedata_games"}, format="parquet",
                                                               transformation_ctx="game_data_games")
job.commit()