import re
def emailre(teststr):
    email=re.compile(r'[A-Za-z0-9\-\.]+@[A-Z0-9a-z\-\.]+')
    emailset=set()  #列表
    for em in email.findall(teststr):
        emailset.add(em)
    for eml in sorted(emailset):
        print(eml)
emailtest='''招商证券投资银行部股权团队近期招聘项目实习生，工作地点：佛山，主要参与某IPO项目承做相关工作。

硬性要求：
1 立志于从事投行工作，对投行业务有热情；
2 本科大三及以上或研究生（不限专业，会计、法律、财务、金融类专业优先），每周可保证工作日至少四天以上（最好全周）全天现场工作，可尽快入职并至少工作三个月；
3 工作认真、细致严谨、积极主动、责任心强，能承受较大工作压力，具有良好的沟通协调能力、团队合作精神及保密意识。

项目组氛围融洽，能够深入锻炼投行工作能力，积累项目执行经验。正规公司HR程序。

如有意向，欢迎发送简历至mrl7@qq.com，简历命名格式为“姓名-学校-专业-年级-一周可实习天数”，谢谢！

需要帮推的，私我一下就好。'''
emailre(emailtest)
#或
strtest='''【天弘基金】互联网金融业务部实习生（北京，能尽快到岗优先）

简历发送到： kangjy@thfund.com.cn
【岗位职责】
1. 参与基金直播的幕后支持工作
2. 参与线上基金社区的内容和活动运营策划
3. 运营数据的整理和分析、竞品分析、用户调研；
4. 营销方案的策划和撰写；

【职位要求】
1. 负责行业信息的搜集、竞品分析对比、数据整理分析等；
2. 文字表达能力强，有方案策划和文案撰写经验；有微信、微博等社交媒体运营经验者优先；
3. 负责互联网金融相关产品运营方案策划、文案输出、页面逻辑设计等
4. 双休制，实习期需满3个月方可提供实习证明， 2023年及以后毕业优先
5. 认真细心、服从安排、吃苦耐劳，能够熟练使用办公软件；
6. 本信息长期有效，欢迎自荐或推荐。

【福利待遇】
1、与余额宝创始人团队共事，接触国内顶尖金融电商思维；团队超nice！
2、薪酬150元/日；
3、每日水果、下午茶、咖啡。'''
emailre(strtest)