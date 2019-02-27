# !/usr/bin/env Python3

# -*- encoding:utf-8 *-*

'''
from urllib import request
import re  # 使用正则表达式


def getResponse(url):
    # url请求对象 Request是一个类
    url_request = request.Request(url)
    # print("Request对象的方法是：",url_request.get_method())

    # 上下文使用的对象，包含一系列方法
    # url_response = request.urlopen(url) #打开一个url或者一个Request对象
    url_response = request.urlopen(url_request)

       geturl()：返回 full_url地址 
         info(): 返回页面的元(Html的meta标签)信息 
         <meta>：可提供有关页面的元信息（meta-information），比如针对搜索引擎和更新频度的描述和关键词。 
      getcode(): 返回响应的HTTP状态代码  
      100-199 用于指定客户端应相应的某些动作。 
      200-299 用于表示请求成功。      ------>  200 
      300-399 用于已经移动的文件并且常被包含在定位头信息中指定新的地址信息。 
      400-499 用于指出客户端的错误。  ------>  404 
      500-599 用于支持服务器错误。  
         read(): 读取网页内容，注意解码方式(避免中文和utf-8之间转化出现乱码) 


    return url_response  # 返回这个对象


def getJpg(data):
    jpglist = re.findall(r'src="http.+?.jpg"', data)
    return jpglist


def downLoad(jpgUrl, n):
    # request.urlretrieve(jpg_link, path)
    try:
        request.urlretrieve(jpgUrl, '%s.jpg' % n)
    except Exception as e:
        print(e)
    finally:
        print('图片%s下载操作完成' % n)


http_response = getResponse("https://www.google.com.hk/search?newwindow=1&safe=strict&hl=zh-CN&biw=1536&bih=762&tbm=isch&sa=1&ei=9_fjW5zIHYGchwPmz5joDw&q=side+face&oq=side+face&gs_l=img.3..0l4.14738.21515.0.22284.24.13.10.1.1.0.179.1397.0j12.12.0....0...1c.1j4.64.img..3.20.1133...0i24k1j0i12k1.0.tHkI6f6ldPo")  # 拿到http请求后的上下文对象(HTTPResponse object)
#print(http_response.read().decode('utf-8'))
data = http_response.read().decode('utf-8',"ignore")
# print(data)
global n
n = 1
L = getJpg(data)
for jpginfo in L:
    print(jpginfo)
    s = re.findall(r'http.+?.jpg', jpginfo)
    downLoad(s[0], n)
    n = n + 1
'''
from bs4 import BeautifulSoup
import requests
import re,json
import pandas as pd
import time

#京东小米官方网站爬取小米6X的评论
#动态网页爬取

def getHtml(url,data): #只输入URL的主体部分，后面的参数用下面的字典附加上
    try:
        r=requests.get(url,params=data)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        print('爬取失败')

def getComment(html):#获得一页的评论
    commentList=[]
    i = json.dumps(html)  # 将页面内容编码成json数据，（无论什么格式的数据编码后都变成了字符串类型str）
    j = json.loads(i)  # 解码，将json数据解码为Python对象
    # print(type(j))
    comment = re.findall(r'{"productAttr":.*}', j)  # 对网页内容筛选找到我们想要的数据，得到值为字典的字符串即'{a:1,b:2}'
    #print(comment)
    comm_dict = json.loads(comment[0])  # 将json对象obj解码为对应的字典dict
    # print(type(comm_dict))
    commentSummary = comm_dict['comments']  # 得到包含评论的字典组成的列表
    for comment in commentSummary:  # 遍历每个包含评论的字典，获得评论和打分
        c_content = ''.join(comment['content'].split())  # 获得评论,由于有的评论有换行，这里用split（）去空格，换行，并用join（）连接起来形成一整段评论，便于存储
        score = comment['score']  # 用户打分
        # print(score)
        # print(c_content)
        commentList.append([score,c_content])
    return commentList

'''获得多页评论'''
def conments(url,num):#url主体和爬取网页的数量
    data = {'callback': 'fetchJSON_comment98vv6708',  # 调整页数page
            'productId': '4771320',
            'score': 0,
            'sortType': 5,
            'page': 0,
            'pageSize': 10,
            'isShadowSku': 0,
            'rid': 0,
            'fold': 1
            }
    comments=[]
    for i in range(num+1):
        try:#防止网页提取失败，使爬取终断，直接跳过失败页，继续爬取
            data['page']=i
            html = getHtml(url, data)
            comment = getComment(html)
        except:
            continue
        comments+=comment
        print('页数',i)
        time.sleep(3)#由于网站反爬虫，所以每爬一页停3秒
        # if i/20==0:
        #     time.sleep(5)
    return comments

if __name__ =='__main__':
    time_start = time.time()
    url = 'https://sclub.jd.com/comment/productPageComments.action?'
    comm=conments(url,100)
    print('共计%d条评论'%(len(comm)))#打印出总共多少条评论
    name=['score','comment']
    file=pd.DataFrame(columns=name,data=comm)
    file.to_csv('comment_fin.txt',index=False)
    time_end = time.time()
    print('耗时%s秒' % (time_end - time_start))