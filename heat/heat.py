import pyspark
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, SparkSession
import datetime
import urllib.request
import json
import os
import csv

sc = SparkContext(conf=SparkConf().setAppName("StreamApp").setMaster("local"))
def caculate_heat(online, dic):
	gifts = 0
	for g in dic:
		gifts = gifts + g[1]

	return online * gifts / 10000

def process(online):
	log_txt = sc.textFile("gift_1.txt")
	temp_var = log_txt.map(lambda k: k.split("|   |")).map(lambda k: [k[1]] + [1])
	result = temp_var.reduceByKey(lambda x,y:x+y).collect()

	return caculate_heat(online, result)

timer= datetime.datetime.now()
start_time = datetime.datetime.now()
Data = []
f = open("file.csv", 'a', newline='')
csv_write = csv.writer(f, dialect='excel')
csv_write.writerow(["date", "jz"])
cnt = 0


while True:
	if cnt == 10:
		os.remove("file.csv")
		f = open("file.csv", 'a', newline='')
		csv_write = csv.writer(f, dialect='excel')
		csv_write.writerow(["date", "jz"])
		cnt = 0

	if datetime.datetime.now() - start_time >= datetime.timedelta(seconds=5):
		f = open("file.csv", 'a', newline='')
		csv_write = csv.writer(f, dialect='excel')
		csv_write.writerow([str(timer).split(" ")[1].split(".")[0], int(process(sum(Data) / len(Data)))])
		Data = []
		start_time = datetime.datetime.now()
		cnt = cnt + 1
	else:
		if datetime.datetime.now() - timer >= datetime.timedelta(seconds=1):
			url = "http://open.douyucdn.cn/api/RoomApi/room/288016"
			req = urllib.request.Request(url)
			resp = urllib.request.urlopen(req)
			data = json.loads(resp.read().decode('utf-8'))
			Data.append(data["data"]["online"])
			timer = datetime.datetime.now() 
