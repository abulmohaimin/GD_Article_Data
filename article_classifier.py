import os
import re
import glob
import codecs
import csv
import time
# -*- coding: utf-8 -*-
import sys
import json
import requests,zipfile,StringIO
import datetime
from goose import Goose
import pymysql
from datetime import date,datetime,timedelta
import nltk
# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

host="mohaimin-mysql.cvw8wwctyadr.us-east-1.rds.amazonaws.com"
port=3306
dbname="article"
user="mohaimin"
password="mohaimin"

def get_db_contents():
	article_classfication = dict()
	connection = pymysql.connect(host, user=user,port=port,
						   passwd=password, db=dbname)
	cursor = connection.cursor()
	today_date = str(datetime.today().strftime("%Y-%m-%d"))
	sql = "select * from article_data where added_dt='{0}'".format(today_date)
	file_write = open('article_classifications_'+str(today_date)+'.json','a')
	cursor.execute(sql)
   
	results = cursor.fetchall()
	co = 1
	for result in results:
		

		tokenized_doc = nltk.word_tokenize(result[2].encode('utf-8'))

 



		tagged_sentences = nltk.pos_tag(tokenized_doc)

		ne_chunked_sents = nltk.ne_chunk(tagged_sentences)

 



		named_entities = []

		for tagged_tree in ne_chunked_sents:

			if hasattr(tagged_tree, 'label'):

				entity_name = ' '.join(c[0] for c in tagged_tree.leaves()) #

				entity_type = tagged_tree.label()

				named_entities.append((entity_name, entity_type))
		article_classfication["url"] = result[0]
		article_classfication["title"] = result[1]
		article_classfication["article_content"] = result[2]
		article_classfication["classications_from_named_entity_recognition"] = named_entities
		file_write.write(json.dumps(article_classfication)+"\n")
		

	connection.close()
get_db_contents()
