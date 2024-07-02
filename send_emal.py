import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email = '1572189162@qq.com'
password = '1019GUOYIFU'

smtp = smtplib.SMTP('smtp.qq.com', 465)
smtp.ehlo()
smtp.starttls()
smtp.login(email, password)
print('登录成功')
msg = MIMEMultipart()
msg['From'] = email
msg['Subject'] = 'woyao tian ni'
msg.attach(MIMEText('Wo yao tian ni', 'plain'))

recipients = ['344169186@qq.comm']
msg['To'] = ', '.join(recipients)

smtp.sendmail(email, recipients, msg.as_string())

smtp.quit()


print('邮件发送成功')