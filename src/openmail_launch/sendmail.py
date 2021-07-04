import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SendEmail:

    def __init__(self, senderEmailServer, senderEmail, senderPW):
        try: 
            # 587 -> outlook port number
            self.smtp = smtplib.SMTP(senderEmailServer, 587)
            self.smtp.ehlo() # say Hello
            self.smtp.starttls() # TLS 사용시 필요
            self.smtp.login(senderEmail, senderPW) 
        except Exception as e:
            print(e)
            self.smtp = smtplib.SMTP(senderEmailServer, 587)
            self.smtp.ehlo() # say Hello
            # self.smtp.starttls() # TLS 사용시 필요
            self.smtp.login(senderEmail, senderPW) 
            
    def MailSender(self, message, subject, senderEmail, targetEmail):
        
        # send with message
        #msg = MIMEText(message) 

        # send with HTML
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = senderEmail
        msg['To'] = ', '.join(targetEmail)
        
        # attach HTML
        msg.attach( MIMEText(message, 'html') )

        self.smtp.sendmail(senderEmail, targetEmail, msg.as_string()) 
        self.QuitSMTP()
        
    def QuitSMTP(self):
        self.smtp.quit()
