from sendmail_class import SendEmail
from sentence_class import Sentence
from datetime import datetime 

if __name__ == '__main__':
    # 발송 메일 설정 

    # gmail은 추가 설정해줘야 하기 때문에 구현이 어려울 것으로 판단!
    SenderMailServer = 'smtp.office365.com' 
    SenderEmail = '' 
    SenderPW = ''
    SMail = SendEmail(SenderMailServer, SenderEmail, SenderPW) # 수신 메일 설정 
    
    TargetEmail = ''
    
    # 메일 내용 설정 
    Subject = 'HTML service!' 
    Message = \
    '''
    <div>
        <a href="https://plotly.com/~niceguy1575/32/?share_key=R0pz3e7CrJBD4pSKM2azV6" target="_blank" title="yourmap_ver_openmate_0612" style="display: block; text-align: center;"><img src="https://plotly.com/~niceguy1575/32.png?share_key=R0pz3e7CrJBD4pSKM2azV6" alt="yourmap_ver_openmate_0612" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plotly.com/404.png';" /></a>
        <script data-plotly="niceguy1575:32" sharekey-plotly="R0pz3e7CrJBD4pSKM2azV6" src="https://plotly.com/embed.js" async></script>
        </div>
    ''' 
    SMail.MailSender(Message, Subject, SenderEmail, TargetEmail)