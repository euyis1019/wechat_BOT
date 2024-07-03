# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime
import threading
import os

# 创建一个全局锁对象
lock = threading.Lock()

# 默认邮件内容
default_content = '''您好，我们是领先的大学生求职服务领导品牌 求职蛙，我们专注于国内外名校的同学求职服务。为同学提供“求职辅导+机会推荐匹配"的一站式求职解决方案。
如果您需要实习生，我们有非常多的实习生社群和应届生资源，可以提供高质量并且背景对口的候选人，以及想要和您进行深入的合作包括但不仅限于（求职辅导/简历修改/讲座宣讲/实习和全职内推）我们会给予您高于市场价的求职费用
我的VX号是 careerfrog01    \n您也可以直接通过此邮件回复'''

# 获取当前日期
current_date = datetime.datetime.now().strftime('%Y_%m_%d')

# 读取配置文件
def read_config():
    config = {}
    with open('config.properties', 'r', encoding='utf-8') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config

# 读取邮件内容文件
def read_email_content():
    if os.path.exists('email_content.txt'):
        with open('email_content.txt', 'r', encoding='utf-8') as file:
            print('读取邮件内容文件成功')
            return file.read()
    else:
        print('邮件内容文件不存在，使用默认邮件内容')
        return default_content

# 发送邮件
def send_emails():
    config = read_config()
    sender = config.get('email', '1572189162@qq.com')
    password = config.get('password', 'zwtskcdwrqoajfci')
    content = read_email_content()

    # 读取邮箱地址并清空文件内容
    with lock:
        with open('emails.txt', 'r+') as file:
            emails = file.read().splitlines()
            # if not emails:
            #     print('没有要发送的邮件地址，结束本次运行。')
            #     return
            file.truncate(0)  # 清空文件内容

    # 发送邮件并记录结果
    for email in emails:
        try:
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['Subject'] = Header('求职蛙', 'utf-8')
            msg['From'] = sender
            msg['To'] = email

            smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
            smtp.login(sender, password)
            failed_recipients = smtp.sendmail(sender, email, msg.as_string())
            smtp.quit()

            if not failed_recipients:
                # 记录成功
                with open(f'{current_date}.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{email}: 成功发送\n')
            else:
                # 记录失败
                with open(f'{current_date}.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{email}: 发送失败 - 失败的收件人: {failed_recipients}\n')

        except Exception as e:
            # 记录失败
            with open(f'{current_date}.txt', 'a', encoding='utf-8') as file:
                file.write(f'{email}: 发送失败 - {str(e)}\n')

    print('邮件发送完成，请查看结果文件。')

if __name__ == "__main__":
    send_emails()
