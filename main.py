import itchat
import re
from itchat.content import TEXT
import os
# 正则表达式，用于匹配邮箱
EMAIL_REGEX = r'[A-Za-z0-9\-\.\_]+@[A-Z0-9a-z\-\.\_]+'

# 要保存邮箱的文件路径
EMAIL_SAVE_FILE = 'emails.txt'

# 检查文件是否存在，如果不存在则创建
if not os.path.exists(EMAIL_SAVE_FILE):
    with open(EMAIL_SAVE_FILE, 'w', encoding='utf-8') as f:
        pass  # 创建文件后不需要写入任何内容

def save_emails_to_file(emails):
    """将邮箱列表保存到文件中"""
    with open(EMAIL_SAVE_FILE, 'a', encoding='utf-8') as f:
        for email in emails:
            f.write(email + '\n')

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    # 使用正则表达式查找消息中的邮箱
    emails = re.findall(EMAIL_REGEX, msg['Text'])
    if emails:  # 如果找到邮箱
        save_emails_to_file(emails)  # 保存邮箱到文件
        print(f"Emails found and saved: {emails}")

    if msg.isAt:
        msg.user.send(u'@%s I received: %s' % (msg.actualNickName, msg.text))

def chatrooms():
    return itchat.get_chatrooms(update=True)

itchat.auto_login(hotReload=True)
itchat.run()