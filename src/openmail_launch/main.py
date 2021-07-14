from sendmail import SendEmail
from sentence import Sentence
from datetime import datetime 
import pandas as pd
import pickle as pck
import os

if __name__ == '__main__':

    today = datetime.today()
    today_str = str(today.strftime("%Y-%m-%d"))

    os.system( 'echo "==========================================" >> ../../log/openmail_consulting_log.txt' )
    os.system( 'echo "' + today_str + ' logging." >> ../../log/openmail_consulting_log.txt' )
    os.system( 'echo "==========================================" >> ../../log/openmail_consulting_log.txt' )


    print("1. load setup data")
    os.system( 'echo "1. load setup data" >> ../../log/openmail_consulting_log.txt' )

    # 1. 암호 data 호출
    with open("../../data/openmate_key_df_rev.p", 'rb') as f:
        key_df = pck.load(f)

    print("1. make contents")
    sent = Sentence(key_df.yourmap_notion_api_key[0])
	
    # 2. make all contents
    meta = sent.meta

    # 2-1. 생일 축하 메시지
    msg_birthday1, msg_birthday2 = sent.birthday()

    # 2-2. N주년 축하 메시지
    msg_anniv1, msg_anniv2 = sent.anniversary()

    # 2-3. 주간보고 알림
    msg_weekly = sent.weeklyReport()

    # 2-4. 패밀리데이 알림
    msg_family = sent.familyday()

    # 2-5. 신규입사자 알림
    msg_newbie = sent.newbie()

    # gmail은 추가 설정해줘야 하기 때문에 구현이 어려울 것으로 판단!
    SenderMailServer = 'smtp.office365.com' 
    SenderEmail = key_df.email_id[0]
    SenderPW = key_df.email_pw[0]
    SMail = SendEmail(SenderMailServer, SenderEmail, SenderPW) # 수신 메일 설정 
    
    TargetEmail = meta.email.to_list()

    # 메일 내용 설정 
    print("2. make mail message")
    os.system( 'echo "2. make mail message" >> ../../log/openmail_consulting_log.txt' )

    Subject = "📧 " + today_str + " 오픈메이트 알림"
    Message = \
    """<html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <h2> 오늘의 생일자는? 🥰 </h2>
                <p> 
                """ + \
                    msg_birthday1 + """<br>""" + \
                    msg_birthday2 + """<br>
                </p>
                <h2> 오늘의 N년차 근무자는? 👩 </h2>
                <p> 
                """ + \
                    msg_anniv1 + """<br>""" + \
                    msg_anniv2 + """<br>
                </p>
                <h2> Notification 👀 </h2>
                <p> 
                """ + \
                    msg_weekly + """<br>""" + \
                    msg_family + """<br>""" + \
                    msg_newbie + """<br>
                </p>
            </body>
        </html>
    """

    msg_len = len(msg_birthday1) + len(msg_anniv1) + len(msg_weekly) + len(msg_family) + len(msg_newbie)

    print("3. send e-mail")
    os.system( 'echo "3. send e-mail" >> ../../log/openmail_consulting_log.txt' )

    if msg_len > 0:
        SMail.MailSender(Message, Subject, SenderEmail, TargetEmail)
    else:
        print("no need to send e-mail")
        os.system( 'echo "no need to send e-mail" >> ../../log/openmail_consulting_log.txt' )

    print("4. dump yesterday data")
    os.system( 'echo "4. dump yesterday data" >> ../../log/openmail_consulting_log.txt' )
    with open ("../../data/team_list_yesterday.p", 'wb') as f2:
        pck.dump(meta, f2)
