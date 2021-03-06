import os
from glob import glob
import pandas as pd

def load_table(dirname, names=None, ext='csv', sep=','):
    # load a csv, assuming there is only one csv in the directory
    if ext.startswith('.'):
        ext = ext[1:]
    g = glob(os.path.join(dirname, '*.{}'.format(ext)))
    if len(g) != 1:
        raise RuntimeError
    fname = g[0]
    return pd.read_csv(fname, sep=sep, header=None, names=names)

def load_spark_session(appName="sparkApp", mem='80g', showConsoleProgress=False, additional_conf=[], logLevel=None):
    from dotenv import load_dotenv
    load_dotenv('.env')

    import findspark
    findspark.init()

    import pyspark
    conf = pyspark.SparkConf().setAll([
        ('spark.executor.memory', mem), 
        ('spark.driver.memory', mem),
        ('spark.ui.showConsoleProgress', showConsoleProgress),
        ('spark.driver.maxResultSize', '0'),
        ('spark.reducer.maxSizeInFlight', '5g'),
    ])
    for k,v in additional_conf:
        conf.set(k, v)

    sc = pyspark.SparkContext(appName=appName, conf=conf)
    if logLevel:
        sc.setLogLevel(logLevel)
    spark = pyspark.sql.SparkSession(sc)
    return spark
