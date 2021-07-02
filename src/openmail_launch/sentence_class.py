import geopandas as gpd
import pandas as pd
import requests
import re
import json
from shapely import wkt
import numpy as np
import os 
import pickle as pck
from datetime import datetime

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


class get_api:
    def __init__(self,api_key):
        self.api_key = api_key

    def get_api(self):
        url = 'https://api.notion.com/v1/databases/60a5d525378d4421a4a5c42f1e2f2a0e/query'
        header = {
            "Notion-Version": "2021-05-13",
            "Authorization": "Bearer {0}".format(self.api_key),
            "Content-Type": "application/json"
        }
        result_json = postUrl(url, headers = header)
        data = json.loads(result_json.content)
        self.data = data

    def get_meta(self):

        name = []
        birthday = []
        grade = []
        team = []
        email = []
        phone = []
        for result in self.data['results']:
            if (result['properties']['block']['select']['name'] != '명예의전당'):
                # 이름 
                name.append(result['properties']['Name']['title'][0]['text']['content'])
                # 생일
                birthday.append(result['properties']['생년월일']['date']['start'])
                # 직급
                grade.append(result['properties']['직급']['select']['name'])
                # 팀 
                team.append(result['properties']['팀']['select']['name'])	
                # email
                email.append(result['properties']['email']['rich_text'][0]['text']['content'])
                #phone
                phone.append(result['properties']['Phone']['phone_number'])

            else :
                pass

        email_meta = pd.DataFrame({'name':name,'grade':grade,'team':team,'birthday':birthday,'email':email,'phone':phone})

        self.meta = email_meta
        return email_meta



    def __del__(self):
        print('delete attributes')


class sentence(get_api):
    def __init__(self,api_key):
        super().__init__(api_key)
        super().get_api()
        super().get_meta()

    def birthday(self):
        name = []
        birthday = []
        grade = []
        team = []
        notion_url = []
        for result in self.data['results']:
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

        self.birthday_sentence = sentence
        self.birthday_sentence2 = sentence2

        return sentence ,sentence2

    def anniversary(self):
        today = datetime.now().strftime('%Y-%m-%d')

        name = []
        anniversary = []
        grade = []
        n = []
        team = []
        notion_urls = []
        for result in self.data['results']:
            if (result['properties']['block']['select']['name'] != '명예의전당') and (result['properties']['근무일체크']['formula']['boolean'] == True):
                # 이름 
                name.append(result['properties']['Name']['title'][0]['text']['content'])
                # 입사일 
                anniversary.append(result['properties']['입사일']['date']['start'])
                # N
                n.append(str(int(datetime.now().strftime('%Y')) - int(datetime.strptime(result['properties']['입사일']['date']['start'],'%Y-%m-%d').strftime('%Y'))))
                # 직급
                grade.append(result['properties']['직급']['select']['name'])
                # 팀 
                team.append(result['properties']['팀']['select']['name'])
                # notion_url
                notion_urls.append("https://notion.so"+result['id'].replace('-',''))
            else :
                pass


        if len(name) == 1:
            sentence = f'{today} 오늘은 {team[0]}팀의 {name[0]} {grade[0]}님의 입사 {n[0]} 년차 입니다. \n 축하의 메세지를 전해주세요!'
        elif len(name)> 1:
            sentence = f'{today} 오늘은 {team[0]}팀의 {name[0]} {grade[0]}님의 입사 {n[0]} 년차'

            for t,n1,g,n2 in zip(team[1:],name[1:],grade[1:],n[1:]):
                sentence += (f',{t}팀 {n1} {g}님의 입사 {n2} 년차')

            sentence += '입니다. \n 축하의 메세지를 전해주세요!'	
        elif len(name) == 0 :
            return

        sentence2 = ''
        for n,u in zip(name,notion_urls):
            sentence2 += f'{n}님의 노션 : {u} \n'

        self.anniversary_sentence = sentence
        self.anniversary_sentence2 = sentence2

        return sentence ,sentence2        
	
