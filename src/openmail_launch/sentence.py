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
from datetime import timedelta

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
                try:
                    # 미리 변수 할당을 함으로써 오류 있는지를 확인
                    # 이후 list에 append
                    name_sample = result['properties']['Name']['title'][0]['text']['content']
                    birth_sample = result['properties']['생년월일']['date']['start']
                    grade_sample = result['properties']['직급']['select']['name']
                    team_sample = result['properties']['팀']['select']['name']
                    email_sample = result['properties']['email']['rich_text'][0]['text']['content']
                    phone_sample = result['properties']['Phone']['phone_number']
                    # 이름 
                    name.append(name_sample)
                    # 생일
                    birthday.append(birth_sample)
                    # 직급
                    grade.append(grade_sample)
                    # 팀 
                    team.append(team_sample)
                    # email
                    email.append(email_sample)
                    #phone
                    phone.append(phone_sample)
                except:
                    pass
            else :
                pass

        email_meta = pd.DataFrame({'name':name,'grade':grade,'team':team,'birthday':birthday,'email':email,'phone':phone})

        self.meta = email_meta
        return email_meta

    def __del__(self):
        print('delete attributes')


class Sentence(get_api):
    def __init__(self,api_key):
        super().__init__(api_key)
        super().get_api()
        super().get_meta()

    def birthday(self):
        today = datetime.now().strftime('%Y-%m-%d')
        name = []
        birthday = []
        grade = []
        team = []
        notion_url = []
        for result in self.data['results']:
            if (result['properties']['block']['select']['name'] != '명예의전당') and (result['properties']['생일check']['formula']['boolean'] == True): # 근무일&생일check는 기본 공란이기 때문에 예외처리할 필요가 없음.
                try:
                    name_sample = result['properties']['Name']['title'][0]['text']['content']
                    birth_sample = result['properties']['Name']['title'][0]['text']['content']
                    grade_sample = result['properties']['Name']['title'][0]['text']['content']
                    team_sample = result['properties']['Name']['title'][0]['text']['content']
                    notion_sample = "https://notion.so/"+result['id'].replace('-','')

                    # 이름 
                    name.append(name_sample)
                    # 생일
                    birthday.append(birth_sample)
                    # 직급
                    grade.append(grade_sample)
                    # 팀 
                    team.append(team_sample)    
                    # notion_url
                    notion_url.append(notion_sample)
                except:
                    pass
            else :
                pass

        sentence = ""
        if len(name) == 1:
            sentence = f'{today}일 오늘은 {team[0]}팀의 {name[0]} {grade[0]}님 의 생일입니다. 🥰🥰 \n 축하의 메세지를 전해주세요!'

        elif len(name)> 1:
            sentence = f'{today}일 오늘은 {team[0]}팀의 {name[0]} {grade[0]}님'
            for t,n,g,u in zip(team[1:],name[1:],grade[1:],notion_url[1:]):
                sentence = sentence + (f',{t}팀 {n} {g}님')
            sentence = sentence + '의 생일입니다. 🥰🥰 \n 축하의 메세지를 전해주세요!'	
        else:
            sentence = ""

        sentence2 = ''
        for n,u in zip(name,notion_url):
            sentence2 += f'{n}님의 노션 : <a href = "{u}"> click this! </a> <br>'
            #sentence2 += f'{n}님의 노션 : {u} \n'

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
            if (result['properties']['block']['select']['name'] != '명예의전당') and (result['properties']['근무일체크']['formula']['boolean'] == True): # 근무일&생일check는 기본 공란이기 때문에 예외처리할 필요가 없음.
                try:
                    name_sample = result['properties']['Name']['title'][0]['text']['content']
                    anniv_sample = result['properties']['입사일']['date']['start']
                    n_sample = str(int(datetime.now().strftime('%Y')) - int(datetime.strptime(result['properties']['입사일']['date']['start'],'%Y-%m-%d').strftime('%Y')))
                    grade_sample = result['properties']['직급']['select']['name']
                    team_sample = result['properties']['팀']['select']['name']
                    notion_sample = "https://notion.so/"+result['id'].replace('-','')

                    # 이름 
                    name.append(name_sample)
                    # 입사일
                    anniversary.append(anniv_sample)
                    # N
                    n.append(n_sample)
                    # 직급
                    grade.append(grade_sample)
                    # 팀 
                    team.append(team_sample)    
                    # notion_url
                    notion_urls.append(notion_sample)
                except:
                    pass
            else :
                pass

        sentence = ""
        if len(name) == 1:
            sentence = f'{today} 오늘은 {team[0]}팀의 {name[0]} {grade[0]}님의 입사 {n[0]} 년차 입니다. 🤭🤭 \n 축하의 메세지를 전해주세요!'
        elif len(name)> 1:
            sentence = f'{today} 오늘은 {team[0]}팀의 {name[0]} {grade[0]}님의 입사 {n[0]} 년차'

            for t,n1,g,n2 in zip(team[1:],name[1:],grade[1:],n[1:]):
                sentence += (f',{t}팀 {n1} {g}님의 입사 {n2} 년차')

            sentence += '입니다. 🤭🤭 \n 축하의 메세지를 전해주세요!'
        else:
            sentence = ""

        sentence2 = ''
        for n,u in zip(name,notion_urls):
            sentence2 += f'{n}님의 노션 : <a href = "{u}"> click this! </a> <br>'
            #sentence2 += f'{n}님의 노션 : {u} <br>'

        self.anniversary_sentence = sentence
        self.anniversary_sentence2 = sentence2

        return sentence, sentence2        
	
    def weeklyReport(self):
	
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
            sentence = '오늘은 목요일! 😆😆 다들 잊지 않고 주간보고를 작성해주세요~ 💁‍♀️ {url}'.format(url = weekly_report_page)
        else:
            sentence = ""

        self.weeklyReport_sentence = sentence

        return sentence

    def familyday(self):
        
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

        self.familyday_sentence = sentence

        return sentence

    def newbie(self):
        meta_today = self.meta

        with open("../../data/team_list_yesterday.p", 'rb') as f:
            meta_yesterday = pck.load(f)
        
        # 어제와의 메타정보 비교
        meta_compare = pd.merge(meta_today, meta_yesterday, on = ['name','grade'], how = 'left', suffixes=['_today','_yesterday'])
        
        new_nms = meta_compare.loc[meta_compare.birthday_yesterday.isnull()].name
        new_grade = meta_compare.loc[meta_compare.birthday_yesterday.isnull()].grade

        if len(new_nms) > 0:
            sentence_list = ['반갑게 인사해주세요! 오픈메이트에 ' + nm + ' ' +  grd + '님께서 입사하셨습니다~ 모두 환영해주세요! 👋🏻👋🏻 <br> ' for nm, grd in zip(new_nms, new_grade)]
            sentence = '\n'.join(sentence_list)
        else:
            sentence = ""
            
        self.newbie_sentence = sentence
        return sentence