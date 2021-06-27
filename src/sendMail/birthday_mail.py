import geopandas as gpd
import pandas as pd
import requests
import re
import json
from shapely import wkt
import numpy as np
import os 
import pickle as pck


def postUrl(url, headers, param = None, retries=10):
	resp = None

	try:
		resp = requests.post(url, params = param, headers = headers)
		resp.raise_for_status()
	except requests.exceptions.HTTPError as e:
		if 500 <= resp.status_code < 600 and retries > 0:
			print('Retries : {0}'.format(retries))
			return postUrl(url, param, retries - 1)
		else:
			print(resp.status_code)
			print(resp.reason)
			print(resp.request.headers)
	return resp


def send_birthday_mail(api_key):
	url = 'https://api.notion.com/v1/databases/60a5d525378d4421a4a5c42f1e2f2a0e/query'
	header = {
		"Notion-Version": "2021-05-13",
		"Authorization": "Bearer {0}".format(api_key),
		"Content-Type": "application/json"
	}
	result_json = postUrl(url, headers = header)
	data = json.loads(result_json.content)

	name = []
	birthday = []
	grade = []
	team = []
	notion_url = []
	
	for result in data['results']:
		if (result['properties']['block']['select']['name'] != '명예의전당') and (result['properties']['생일check']['formula']['boolean'] == True):
			# 이름 
			name.append(result['properties']['Name']['title'][0]['text']['content'])
			# 생일
			birthday.append(result['properties']['생년월일']['date']['start'])
			# 직급
			grade.append(result['properties']['직급']['select']['name'])
			# 팀 
			team.append(result['properties']['팀']['select']['name'])	
			# notion_url
			notion_url.append("https://notion.so/"+result['id'].replace('-',''))
		else :
			pass


	if len(name) == 1:
		sentence = f'{birthday[0]}일 오늘은 {team[0]}팀의 {name[0]} {grade[0]}님 의 생일입니다. \n 축하의 메세지를 전해주세요!'
		
	elif len(name)> 1:
		sentence = f'{birthday[0]}일 오늘은 {team[0]}팀의 {name[0]} {grade[0]}님'
		for t,n,g,u in zip(team[1:],name[1:],grade[1:],notion_url[1:]):
			sentence = sentence + (f',{t}팀 {n} {g}님')
		sentence = sentence + '의 생일입니다. \n 축하의 메세지를 전해주세요!'	
	if len(name) == 0 :
		return
	
	sentence2 = ''
	for n,u in zip(name,notion_url):
		sentence2 += f'{n}님의 노션 : {u} \n'


	return sentence ,sentence2


if __name__ == "__main__":
	with open("openmate_key_df.p", 'rb') as f:
		key_df = pck.load(f)
	
	send_birthday_mail(key_df.yourmap_notion_api_key[0])
