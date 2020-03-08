# programmatically create a subset schema from a JSON schema in Spark/PySpark
# example parsing the Twitter schema

new_schema = StructType()
col_info = {"id":"id", "entities.hashtags": "hashtags", "entities.urls": "urls", "user":"user"}
for col, col_name in col_info.items():
    col_schema = df.select(col).schema
    print(col)
    print(col_schema)
    for field in col_schema.fields:
      field = StructField(col_name, field.dataType, True)
    new_schema.add(field)
new_schema