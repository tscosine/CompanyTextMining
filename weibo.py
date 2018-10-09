# -*- coding: utf-8 -*-

import urllib.request
import json
import re
import xlwt
'''
马化腾
马云
李彦宏
丁磊
张朝阳
周鸿祎
刘强东
王志东
梁建章
张近东
王兴
沈亚
莫天全
雷军
陈天桥
李瑜
'''
#定义要爬取的微博大V的微博ID
id_dict = {'周鸿祎':'1708942053','刘强东':'1866402485','王志东':'1644471760',
           '梁建章':'3514741113','王兴':'1616192700','雷军':'1749127163',
           '李瑜':'1742912084'}
#设置代理IP
proxy_addr="122.246.48.116:8010"

#定义页面打开函数
def use_proxy(url,proxy_addr):
    req=urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    proxy=urllib.request.ProxyHandler({'http':proxy_addr})
    opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data=urllib.request.urlopen(req).read().decode('utf-8','ignore')
    return data

#获取微博主页的containerid，爬取微博内容时需要此id
def get_containerid(url):
    data=use_proxy(url,proxy_addr)
    content=json.loads(data).get('data')
    for data in content.get('tabsInfo').get('tabs'):
        if(data.get('tab_type')=='weibo'):
            containerid=data.get('containerid')
    return containerid

#获取微博大V账号的用户基本信息，如：微博昵称、微博地址、微博头像、关注人数、粉丝数、性别、等级等
def get_userInfo(id):
    url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
    data=use_proxy(url,proxy_addr)
    content=json.loads(data).get('data')
    profile_image_url=content.get('userInfo').get('profile_image_url')
    description=content.get('userInfo').get('description')
    profile_url=content.get('userInfo').get('profile_url')
    verified=content.get('userInfo').get('verified')
    guanzhu=content.get('userInfo').get('follow_count')
    name=content.get('userInfo').get('screen_name')
    fensi=content.get('userInfo').get('followers_count')
    gender=content.get('userInfo').get('gender')
    urank=content.get('userInfo').get('urank')
    print("微博昵称："+name+"\n"+"微博主页地址："+profile_url+"\n"+"微博头像地址："+profile_image_url+"\n"+"是否认证："+str(verified)+"\n"+"微博说明："+description+"\n"+"关注人数："+str(guanzhu)+"\n"+"粉丝数："+str(fensi)+"\n"+"性别："+gender+"\n"+"微博等级："+str(urank)+"\n")

def text_filter(text):
    black_list = ['红包','吃','足球','世界杯','球鞋','看球','广告','配置','阅读','恭喜','祝','转发','抽','双十一','邮票','答题','出题','泄题','题目','猜','奖金','新书','欢迎',
                  '直播','感谢','主播','公众号','电影','奖品','中奖','回复','视频','预约','春节','福利','百万赢家','节目','开播','节日','节快乐','加油','微博问答​​','网页链接','礼品',
                  '售罄','推送','礼物','谢谢','同学']
    for word in black_list:
        if re.search(word,text):
            return None
    pattern1 = re.compile('\(.*?\)')
    pattern2 = re.compile('【.*?】')
    pattern3 = re.compile('<.*?>')
    pattern5 = re.compile('@\w+')
    while re.search(pattern1,text):
        text = re.sub(pattern1,'',text)
    while re.search(pattern2,text):
        text = re.sub(pattern2,'',text)
    while re.search(pattern3,text):
        text = re.sub(pattern3,'',text)
    while re.search(pattern5,text):
        text = re.sub(pattern5,'',text)
    for i in range(len(text)):
        if text[i:i+2] == '//':
            text = text[:i]
            break
    if text.__len__() < 40:
        return None
    return text



#获取微博内容信息,并保存到文本中，内容包括：每条微博的内容、微博详情页面地址、点赞数、评论数、转发数等
def get_weibo(uname,id,sheet):
    i=1
    count = 0
    sheet_row = 0
    default_year = 2018
    while True:
        url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
        weibo_url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id+'&containerid='+get_containerid(url)+'&page='+str(i)
        try:
            data=use_proxy(weibo_url,proxy_addr)
            content=json.loads(data).get('data')
            cards=content.get('cards')
            if(len(cards)>0):
                for j in range(len(cards)):
                    print("-----正在爬取第"+str(i)+"页，第"+str(j)+"条微博------")
                    card_type=cards[j].get('card_type')
                    if(card_type==9):
                        mblog=cards[j].get('mblog')
                        # attitudes_count=mblog.get('attitudes_count')    #点赞数
                        # comments_count=mblog.get('comments_count')      #评论数
                        # reposts_count=mblog.get('reposts_count')        #转发数
                        # scheme=cards[j].get('scheme')                   #微博地址
                        created_at=mblog.get('created_at')              #创建时间
                        text=mblog.get('text')
                        clean_text = text_filter(text)#微博内容
                        date_pattern = re.compile('(\d+)-(\d+)-(\d+)')
                        year = default_year
                        if re.search(date_pattern,created_at):
                            year = re.search(date_pattern,created_at).group(1)
                        if int(year) < 2013:
                            return
                        if clean_text != None:
                            sheet.write(sheet_row,0,uname)
                            sheet.write(sheet_row,1,year)
                            sheet.write(sheet_row,2,clean_text)
                            sheet_row += 1
                            count += 1
                    print('Total:'+str(count))
                i += 1
            else:
                continue
        except Exception as e:
            print(e)
            return

def get_portals_weibo(id,sheet):
    uname = ['马化腾','马云','李彦宏','丁磊','张朝阳','周鸿祎','刘强东','王志东','梁建章','张近东',
             '王兴','沈亚','莫天全','雷军','陈天桥','李瑜']
    pattern = re.compile('马化腾|马云|李彦宏|丁磊|张朝阳|周鸿祎|刘强东|王志东|梁建章|张近东|王兴|沈亚|莫天全|雷军|陈天桥|李瑜')
    i=1
    count = 0
    sheet_row = 0
    default_year = 2018
    while True:
        url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
        weibo_url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id+'&containerid='+get_containerid(url)+'&page='+str(i)
        try:
            data=use_proxy(weibo_url,proxy_addr)
            content=json.loads(data).get('data')
            cards=content.get('cards')
            if(len(cards)>0):
                for j in range(len(cards)):
                    # print("-----正在爬取第"+str(i)+"页，第"+str(j)+"条微博------")
                    card_type=cards[j].get('card_type')
                    if(card_type==9):
                        mblog=cards[j].get('mblog')
                        created_at=mblog.get('created_at')              #创建时间
                        text=mblog.get('text')
                        clean_text = text_filter(text)#微博内容
                        date_pattern = re.compile('(\d+)-(\d+)-(\d+)')
                        year = default_year
                        if re.search(date_pattern,created_at):
                            year = re.search(date_pattern,created_at).group(1)
                        if int(year) < 2013:
                            return
                        if clean_text != None:
                            if re.search(pattern,clean_text):
                                print(clean_text)
                                sheet.write(sheet_row,0,re.search(pattern,clean_text).group())
                                sheet.write(sheet_row,1,year)
                                sheet.write(sheet_row,2,clean_text)
                                sheet_row += 1
                                count += 1
                    # print('Total:'+str(count))
                i += 1
            else:
                continue
        except Exception as e:
            print(e)
            return

def search_portals_weibo():
    partals_id=['1649173367',#每日经济新闻
                '1956700750',#电商报
                '1974561081' #网易财经
                ]
    for id in partals_id:
        workbook = xlwt.Workbook(encoding='ascii')
        worksheet = workbook.add_sheet('My_Worksheet')
        get_portals_weibo(id,worksheet)
        workbook.save(id+'.xls')
def search_personal_weibo():
    uname = '李瑜'
    uid = id_dict[uname]
    workbook = xlwt.Workbook(encoding = 'ascii')
    worksheet = workbook.add_sheet('My_Worksheet')
    # get_userInfo(uid)
    get_weibo(uname,uid,worksheet)
    workbook.save(uname+'.xls')
if __name__=="__main__":
    # search_personal_weibo()
    search_portals_weibo()
