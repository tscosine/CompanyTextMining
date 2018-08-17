# -*- coding: utf-8 -*-

import urllib.request
import json
import re
import cparser as cp

#定义要爬取的微博大V的微博ID
id='1259110474'

id_dict = {'周鸿祎':'1708942053'}
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
def get_weibo(id,file):
    i=1
    count = 0
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
                        attitudes_count=mblog.get('attitudes_count')    #点赞数
                        comments_count=mblog.get('comments_count')      #评论数
                        created_at=mblog.get('created_at')              #创建时间
                        reposts_count=mblog.get('reposts_count')        #转发数
                        scheme=cards[j].get('scheme')                   #微博地址
                        text=mblog.get('text')
                        clean_text = text_filter(text)#微博内容
                        if re.match('(\d+)-(\d+)-(\d+)',created_at):
                            if int(re.match('(\d+)-(\d+)-(\d+)',created_at).group(1)) < 2013:
                                break
                        if clean_text != None:
                            with open(file, 'a', encoding='utf-8') as fh:
                                fh.write('发布时间：'+str(created_at)+'\n')
                                fh.write('微博内容:'+clean_text+'\n')
                                fh.write('-----------------------\n')
                                count += 1
                i+=1
            else:
                break
        except Exception as e:
            print(e)
            pass
    print('存储'+str(count)+'条数据')

if __name__=="__main__":
    id = id_dict['周鸿祎']
    file=id+".txt"
    f = open(file,'w')
    get_userInfo(id)
    get_weibo(id,file)