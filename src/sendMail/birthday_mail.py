import geopandas as gpd
import pandas as pd
import requests
import re
import json
from shapely import wkt
import numpy as np
import os 
import pickle as pck
from datetime import timedelta
from datetime import datetime
import time


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

def sentence_weekly_report():
	
	# 0: 월 ~ 6: 일
	# 3: 목요일
	today = datetime.today()
	weekday = today.weekday()
	hour = today.hour
	minute = today.hour

	############
	# notion api를 이용한 weekly report page 자동 생성 (09:00에 생성)
	############

	weekly_report_page = ""

	# 주간보고는 해당 주차 목요일 오전 발송
	if weekday == 3 and hour == 10 and minute == 0:
		sentence = '오늘은 목요일! 주간보고를 작성해주세요~ {url}'.format(url = weekly_report_page)
	else:
		sentence = ""

	return sentence

def sentence_family_day():
	
	today = datetime.today()
	weekday = today.weekday()

	firstday = today.replace(day=1)

	if firstday.weekday() == 6: # 6: 일 => 3주차 잘 인식함
		origin = firstday
		add_value = 0
	elif firstday.weekday() < 3: # 0 ~ 2: 월~수 => 3주차 잘 인식
		origin = firstday - timedelta(days=firstday.weekday() + 1)
		add_value = 0
	else: # 수,목,금 => 2주차로 인식됨, 1을 더해준다.
		origin = firstday + timedelta(days=6-firstday.weekday())
		add_value = 1

	family_weekday = (today - origin).days // 7 + 1 + add_value
	family_weekday

	# 패밀리데이는 해당 주차 목, 금요일에 발송
	if family_weekday == 3 and weekday in [3,4]: 

		# make day name
		if weekday == 3:
			day_name = "목요일"
		else:
			day_name = "금요일"

		# make sentence
		if day_name == "목요일":
			sentence = '오늘은 ' + family_weekday + '주차 ' + day_name + '입니다! \n' +  '내일은 패밀리 데이가 있는 날이니, 염두에 두시고 즐거운 하루 보내시길 바랍니다~ 😆😆 \n\n' + '🙌  해당 요일에 외부 프로젝트 및 기타 업무를 하시는 분들께서는 대신 반차로 적립됩니다. '
		else:
			sentence = '오늘은 ' + family_weekday + '주차 ' + day_name + '입니다! \n' +  '오늘은 패밀리 데이가 있는 날이니, 오전에 업무 정리 잘 하시고 오후에 퇴근 하세요~ 😆😆 \n\n' + '🙌  해당 요일에 외부 프로젝트 및 기타 업무를 하시는 분들께서는 대신 반차로 적립됩니다. '
	else:
		sentence = ""
		
	return sentence

if __name__ == "__main__":
	#with open("openmate_key_df.p", 'rb') as f:
	#	key_df = pck.load(f)
	
	#msg_congr, msg_congr_detal = send_birthday_mail(key_df.yourmap_notion_api_key[0])
	msg_week = sentence_weekly_report()
	msg_family = sentence_family_day()

	print(msg_week)
	print(msg_family)

