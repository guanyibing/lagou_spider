# -*- coding:utf8 -*-
from __future__ import division
import urllib2
import json
import pandas as pd
from bs4 import BeautifulSoup
import re
import datetime
from multiprocessing import Pool
import math
from time import sleep
def getPageNum(keyword):
    keywordindex=keyword.encode('utf-8')
    keywordindex=keywordindex.replace("'","")
    #获取结果页数
    url='http://www.lagou.com/jobs/positionAjax.json?px=default&first=true&kd='+keywordindex+'&pn=1'
    response=urllib2.urlopen(url)
    data=response.read()
    text=json.loads(data)
    urlcount=int((json.loads(data))['content']['positionResult']['totalCount'])
    pagesize=(json.loads(data))['content']['positionResult']['pageSize']
    pagenum=math.ceil(urlcount/pagesize)
    print u"共有%d页搜素结果"%pagenum
    return int(pagenum),keywordindex
def getUrls(keywordindex,pagenum):
    urlslist=[]
    for i in range(1,pagenum):
        if i==1:
            type=True
        else:
            type=False
        url='http://www.lagou.com/jobs/positionAjax.json?px=default&first='+str(type)+'&kd='+keywordindex+'&pn='+str(i)
        urlslist.append(url)
    return urlslist
def getJob(url):
        rdata=pd.DataFrame()
        #搜索免费代理，选择可用代理
        #proxy={'http':'183.130.85.194:9000'}
        #proxy_handle=urllib2.ProxyHandler(proxy)
        #opener=urllib2.build_opener(proxy_handle)
        #response=opener.open(url)
        response=urllib2.urlopen(url)
        data=response.read()
        #解析json数据
        results=json.loads(data)['content']['positionResult']['result']

        for j in list(range(len(results))):
            results[j]['companyLabelList']='-'.join(results[j]['companyLabelList'])
            if results[j]['businessZones'] !=None:
                results[j]['businessZones']='-'.join(results[j]['businessZones'])
            if j==0:
                rdata=pd.DataFrame(pd.Series(results[j])).T
            else:
                rdata=pd.concat([rdata,pd.DataFrame(pd.Series(results[j])).T],axis=0)#默认axis=0,纵向连接

        rdata.index=range(1,len(results)+1)
        rdata['salarymin']=0
        rdata['salarymax']=0
        rdata['url']=''
        rdata['jd']=''
        rdata['handle_perc']=''
        rdata['handle_day']=''
        for t in range(len(rdata['salary'])):
            rdata.ix[t+1,'salarymin']=re.search(('(.*?)k'),rdata['salary'].iloc[t]).group(1)
            if re.search('-(.*?)k',rdata['salary'].iloc[t])!=None:
                rdata.ix[t+1,'salarymax']=re.search('-(.*?)k',rdata['salary'].iloc[t]).group(1)
            else:
                rdata.ix[t+1,'salarymax']=''
            rdata.ix[t+1,'url'] =  'http://www.lagou.com/jobs/%s.html'% rdata.ix[t+1,'positionId']
            response=urllib2.urlopen(rdata.ix[t+1,'url']).read()
            soup=BeautifulSoup(response,'lxml')
            jobDescribe=soup.find_all('dd',class_='job_bt')[0].strings
            rdata.ix[t+1,'jd']=''.join(jobDescribe)
            rdata.ix[t+1,'handle_perc']=soup.find_all('span',class_='data')[0].string
            rdata.ix[t+1,'handle_day']=soup.find_all('span',class_='data')[1].string.encode('utf8').replace('天','')
        return rdata
if __name__=='__main__':
    time1=datetime.datetime.now()
    keyword=u'python'
    pagenum,keywordindex=getPageNum(keyword)
    urlslist=getUrls(keywordindex,pagenum)
    pool=Pool(2)
    rdata=pool.map(getJob,urlslist)
    pool.close()
    pool.join()

    totaldata=pd.DataFrame()
    for data in rdata:
        totaldata=pd.concat([totaldata,data],axis=0)
    totaldata.index=range(1,len(totaldata)+1)
    totaldata['keyword']=keywordindex
    ew=pd.ExcelWriter('shujuwajue2.xls',encoding='utf-8')
    totaldata.to_excel(ew,sheet_name='lagou')
    ew.save()

    time2=datetime.datetime.now()
    deltatime=time2-time1
    print deltatime#用时0:05:42.060000
