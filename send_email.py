# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime
import threading

# 创建一个全局锁对象
lock = threading.Lock()

# 邮件配置
sender = '1572189162@qq.com'
password = 'zwtskcdwrqoajfci'
subject = '自动化邮件测试'
content = '这是一封自动发送的测试邮件。'

# 获取当前日期
current_date = datetime.datetime.now().strftime('%Y_%m_%d')

def send_emails():
    # 读取邮箱地址并清空文件内容
    with lock:
        with open('emails.txt', 'r+') as file:
            emails = file.read().splitlines()
            if not emails:
                print('没有要发送的邮件地址，结束本次运行。')
                return
            file.truncate(0)  # 清空文件内容

    # 发送邮件并记录结果
    for email in emails:
        try:
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = sender
            msg['To'] = email

            smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
            smtp.login(sender, password)
            failed_recipients = smtp.sendmail(sender, email, msg.as_string())
            smtp.quit()

            if not failed_recipients:
                # 记录成功
                with open(f'{current_date}.txt', 'a') as file:
                    file.write(f'{email}: 成功发送\n')
            else:
                # 记录失败
                with open(f'{current_date}.txt', 'a') as file:
                    file.write(f'{email}: 发送失败 - 失败的收件人: {failed_recipients}\n')

        except Exception as e:
            # 记录失败
            with open(f'{current_date}.txt', 'a') as file:
                file.write(f'{email}: 发送失败 - {str(e)}\n')

    print('邮件发送完成，请查看结果文件。')

if __name__ == "__main__":
    send_emails()
