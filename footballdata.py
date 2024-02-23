from pyspark.sql import SparkSession
spark=SparkSession.builder.appName('project1').getOrCreate()
#load data from hdfs
# uefa=spark.read.options(header=True,inferSchema=True).csv('hdfs://localhost:9000/sparkproject1/UEFAChampionsLeague2004-2021.csv')
# uefa.show()
# # to print column names
# for i in uefa.columns:
#     print(i)
# #
# # # to print no.of columns
# print('no.of columns are:',len(uefa.columns))
# #
# # # to print no.of rows
# print('no.of rows are:',uefa.count())

# Analysis 1: draw a graph of away team and home team goal scoring in each year of quaterfinal,semifinal and final (plot it as 2 graph).
#
# from pyspark.sql import functions as f
# newuefa=uefa.withColumn("date",f.from_unixtime(f.unix_timestamp(uefa.date),"yyyy-MM-dd"))
# newuefa.show()
# newuefa.printSchema()
#
# from pyspark.sql.functions import udf
# from pyspark.sql.functions import split
# #
# def yeargenerator(x):
#     if x!='':
#         li=x.split('-')
#         return li[0]
# #
# myfn=udf(yeargenerator)
# out=newuefa.withColumn('year',myfn(newuefa['date']))
# out.show()
# # #
# flt_out=out.filter((out['round']=='round : quarterfinals')|
#                    (out['round']=='round : semifinals')|
#                    (out['round']=='round : final'))
# new=flt_out.select('homescore','awayscore','round','year')
# new.show(n=50)
# # #
# def myremove(value):
#     return value[0]
# #
# newfn=udf(myremove)
# one=new.withColumn('home_score',newfn(new['homescore']))
# one.show()
# result=one.withColumn('away_score',newfn(one['awayscore']))
# result.show(n=50)
# final=result.drop('homescore','awayscore')
# final.show(n=50)
# final.printSchema()
# #
# # #convert string to i integers for home_score and away_score:
# from pyspark.sql.types import IntegerType
# newdf=final.withColumn('hmscore',final['home_score'].cast(IntegerType()))
# finaldf=newdf.withColumn('awscore',newdf['away_score'].cast(IntegerType()))
# finaldf=finaldf.drop('home_score','away_score')
# finaldf.show()
# finaldf.printSchema()
# #
# # # #grouping year wise:
# grp=finaldf.groupBy('year').agg(f.sum(finaldf['hmscore']).alias('totalhomegoals'),
#                                 f.sum(finaldf['awscore']).alias('totalawaygoals'))
# grp=finaldf.groupBy('year').agg(f.sum('hmscore').alias('totalhomegoals'),
#                                 f.sum('awscore').alias('totalawaygoals'))
# grp.show()
# grp=grp.orderBy('year')
# # graphical representation:
# import pandas as pd
# df=grp.toPandas()
# #
# import matplotlib.pyplot as plt
# plt.plot(df['year'],df['totalhomegoals'])
# plt.plot(df['year'],df['totalawaygoals'])
# plt.show()
# # # #
#

# ANALYSIS 2#
# teams that most appeared in quarterfinal and final #

uefa = spark.read.options(header=True,inferSchema=True).csv('hdfs://localhost:9000/sparkproject1/UEFAChampionsLeague2004-2021.csv')
# uefa.show()
# uefa = spark.read.csv("/home/sreelakshmi/project_data/UEFAChampionsLeague2004-2021.csv",header=True,inferSchema=True)
uefa.show()
newuefa=uefa.filter((uefa['round']=='round : quarterfinals')|
                   (uefa['round']=='round : semifinals')|
                   (uefa['round']=='round : final'))
newuefa.show()
qf = uefa.filter(uefa['round']=='round : quarterfinals')
qf.show()
sf = uefa.filter(uefa['round']=='round : semifinals')
fi = uefa.filter(uefa['round']=='round : final')

qf_data = qf.select('homeTeam','date','homeScore','sl_no')
sf = sf.select('sl_no','homeTeam','round','date')
fi = fi.select('sl_no','homeTeam','round','date')
qf_data.show()
sf.show()
fi.show()

import pyspark.sql.functions as f
li=[qf,sf,fi]
for i in li:
    out1=i.groupBy('homeTeam').agg(f.count('sl_no').alias('no_of_participation'))
    out2=out1.orderBy('no_of_participation',ascending=False)
    out2.show()
    maxvlue=out2.select(f.max(out2.no_of_participation))
    print(maxvlue.collect()[0])
    print('..............')























