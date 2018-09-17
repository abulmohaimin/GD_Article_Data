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

#AURORA DB credentials

host="mohaimin-mysql.cvw8wwctyadr.us-east-1.rds.amazonaws.com"
port=3306
dbname="mydb"
user="mydb1"
password="mydb12345"

def get_zip_file(url):
	web_data = requests.get(url).text
	if re.search(r'(?mis)(http.*?\.zip)',web_data):
		zip_urls = re.findall(r'(?mis)(http.*?\.zip)',web_data)
		for zip_url in zip_urls:
			print zip_url
			r = requests.get(zip_url, stream=True)
			z = zipfile.ZipFile(StringIO.StringIO(r.content))
			z.extractall()
		extract_information_from_csv()
			

def extract_information_from_csv():
	urls_extracted = []
	for csv_file in glob.glob('*[csv|CSV]'):
		input_file = csv.DictReader(open(csv_file))
		for rows in input_file:
			for row in rows:
				if re.search(r'(?mis)(http[\w\/\:\.\=\-\?\&]*)',str(row)):
					urls = re.findall(r'(?mis)(http[\w\/\:\.\=\-\?\&]*)',str(row))
					for url in urls:
						if url in urls_extracted:
							
							pass
						else:
							
							urls_extracted.append(url)
		
		os.remove(csv_file)
		

	if len(urls_extracted) >= 1:
		extract_article_content(urls_extracted)

def extract_article_content(urls_extracted):

	connection = pymysql.connect(host, user=user,port=port,
						   passwd=password, db=dbname)
	for url in urls_extracted:
		print url
		g = Goose()
		article = g.extract(url=url)
		article_title = re.sub(r'(?mis)[\[\]\!\@\#\$\%\&\*\`\~\^\-\_\"\{\}\:\;\<\>\'\/\\\|\(\)\n\r]*','',article.title).encode('utf-8')
		
		if len(article_title) == 0:
			article_title = " "
		article_content_1 = re.sub(r'(?mis)[\[\]\!\@\#\$\%\&\*\`\~\^\-\_\"\{\}\:\;\<\>\/\'\\\|\(\)\n\r]*','',article.cleaned_text).encode('utf-8')
		if len(article_content_1) == 0:
			article_content_1 = " "

		cursor = connection.cursor()
		sql = "INSERT INTO article_data(url,title,article_content,added_dt) VALUES ('{0}','{1}','{2}','{3}')".format(url,article_title,article_content_1,datetime.today().strftime("%Y-%m-%d"))
		#try:
		cursor.execute(sql)
			# Commit your changes in the database
		connection.commit()
		#except:
		#	print "yes"
		#	connection.rollback()
		
	connection.close()

def list_database():
	connection = pymysql.connect(host, user=user,port=port,
						   passwd=password, db=dbname)
	cursor = connection.cursor()
	#cursor.execute("DROP TABLE article_data")
	
	#sql = """CREATE TABLE article_data (url text,title text,article_content text,added_dt text )"""

	#cursor.execute(sql)
	sql = "select * from article_data"

	cursor.execute(sql)
   
	results = cursor.fetchall()
	co = 1
	for result in results:
		print result
		time.sleep(3)
		co = co + 1
		print co


#get_zip_file("http://data.gdeltproject.org/gdeltv2/lastupdate.txt")
#extract_information_from_csv()
#extract_article_content("http://www.southeastsun.com/daleville/image_e52875a6-b433-11e7-bbbf-6bd09628743c.html")
list_database()
