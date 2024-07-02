import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

if __name__ == "__main__":
    from_name = "eric"  # 发件人姓名
    from_addr = "1572189162@qq.com"
    from_pwd = "zwtskcdwrqoajfci"
    to_addr = ["344169186@qq.com", "1572189162@qq.com"]

    my_title = "i WANT U..."  # 修正了缩进
    my_msg = "Hello World"

    # MIMEText三个主要参数
    # 1. 邮件内容
    # 2. MIME子类型，plain表示text类型
    # 3. 邮件编码格式，使用"utf-8"避免乱码
    msg = MIMEText(my_msg, 'plain', 'utf-8')
    msg['From'] = formataddr([from_name, from_addr])
    # 邮件的标题
    msg['Subject'] = my_title

    # SMTP服务器地址，QQ邮箱的SMTP地址是"smtp.qq.com"
    smtp_srv = "smtp.qq.com"

    try:
        # 使用加密过的SMTP_SSL来实例化
        srv = smtplib.SMTP_SSL(smtp_srv.encode(), 465)

        # 使用授权码登录QQ邮箱
        srv.login(from_addr, from_pwd)

        # 使用sendmail方法来发送邮件
        srv.sendmail(from_addr, to_addr, msg.as_string())
        print('发送成功')
    except Exception as e:
        print('发送失败：', e)
    finally:
        # 无论发送成功还是失败都要退出你的QQ邮箱
        srv.quit()