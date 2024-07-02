import re

# 待匹配的文本
text = """
招商证券投资银行部股权团队近期招聘项目实习生，工作地点：佛山，主要参与某IPO项目承做相关工作。

硬性要求：
1 立志于从事投行工作，对投行业务有热情；
2 本科大三及以上或研究生（不限专业，会计、法律、财务、金融类专业优先），每周可保证工作日至少四天以上（最好全周）全天现场工作，可尽快入职并至少工作三个月；
3 工作认真、细致严谨、积极主动、责任心强，能承受较大工作压力，具有良好的沟通协调能力、团队合作精神及保密意识。

项目组氛围融洽，能够深入锻炼投行工作能力，积累项目执行经验。正规公司HR程序。

如有意向，欢迎发送简历至mrl7@qq.com，简历命名格式为“姓名-学校-专业-年级-一周可实习天数”，谢谢！

需要帮推的，私我一下就好。
"""

# 正则表达式，用于匹配邮箱
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]\b'
# 使用 re.findall 查找所有匹配的邮箱
emails = re.findall(EMAIL_REGEX, text)

# 打印找到的邮箱
print("找到的邮箱地址：", emails)