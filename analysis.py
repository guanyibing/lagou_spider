# -*-coding:utf-8 -*-
from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import pygal
import jieba
from wordcloud import WordCloud
import os

data=pd.read_excel('E:\pachong9\lagou.xls')
jcity=data['city'].value_counts()
jjcity=data.city.value_counts()

i=0
for j  in  jcity.cumsum():
    if (j/jcity.sum())<=0.9:
        i+=1
    else:
        break
city=jcity[:i+1]

pie_chart=pygal.Pie()
pie_chart.title=u'数据挖掘城市分布'
for ind,num in city.iteritems():
    pie_chart.add("%s:%s"%(ind,num),num)
pie_chart.render_to_file(os.path.dirname(__file__)+'/company1.svg')
bar_chart=pygal.HorizontalBar()
bar_chart.title=u'数据挖掘城市分布'
for ind2,num2 in city.iteritems():
    bar_chart.add(ind2,num2)
bar_chart.render_to_file(os.path.dirname(__file__)+'/company2.svg')

city_experience=pd.crosstab(data['city'],data['workYear'],margins=True).sort_values(by='All',ascending=False)[:10]
city_experience=city_experience.drop('All',axis=1).drop('All',axis=0).drop(u'1年以下',axis=1)
bar_chart1=pygal.Bar()
bar_chart1.title=u'前十个地区对工作经验要求情况'
bar_chart1.x_labels=city_experience.index
city_experience=city_experience.T
for i in range(len(city_experience.index)):
    bar_chart1.add(city_experience.index[i],city_experience.values[i])
bar_chart1.render_to_file(os.path.dirname(__file__)+'/city_experience.svg')

salary_workyear=pd.crosstab(data['workYear'],data['salary'],margins=True).sort_values(by='All',ascending=False).drop('All',axis=0).drop('All',axis=1)
bar_chart2=pygal.StackedBar()
bar_chart2.title=u'薪资待遇受工作经验影响情况'
bar_chart2.x_labels=salary_workyear.index
salary_workyear=salary_workyear.T
for i in range(len(salary_workyear.index)):
    bar_chart2.add(salary_workyear.index[i],salary_workyear.values[i])
bar_chart2.render_to_file(os.path.dirname(__file__)+'/salary_workyear.svg')

salary_stage=pd.crosstab(data['financeStage'],data['salary'],margins=True).sort_values(by='All',ascending=False).drop('All',axis=1)
bar_chart3=pygal.Bar()
bar_chart3.width=1200
bar_chart3.title=u'公司型态与薪资分布'
bar_chart3.x_labels=salary_stage.drop('All',axis=0).index
salary_stage=salary_stage.T.sort_values(by='All',ascending=False).drop('All',axis=1)[0:6]
for i in range(len(salary_stage.index)):
    bar_chart3.add(salary_stage.index[i],salary_stage.values[i])
bar_chart3.render_to_file(os.path.dirname(__file__)+'/salary_stage.svg')

#关键字云图
otherwords=['']
text=''.join(data['jd'])
text=text.split('\n')
# list(data['jd'].values)页可以得到目标文本列表
wordlist=[]
for i in text:
    try:
        j=jieba.cut(i)

        for word in j:
            if len(word)>=2 and not word in otherwords :
                wordlist.append(word.lower().encode('utf-8'))
    except:print 'something wrong'

dic_wordlist={}
for word in wordlist:
    if word in dic_wordlist:
        d=dic_wordlist.get(word)
        dic_wordlist[word]=d+1
    else:
        dic_wordlist[word]=1

dic_wordlist=sorted(dic_wordlist.items(),key=lambda x:x[1],reverse=True)
#wordcloud=WordCloud(max_font_size=50,width=400,height=400,margin=5,background_color='black',max_words=100).fit_words(dic_wordlist)

t=' '.join(wordlist)
print t
wordcloud=WordCloud(max_font_size=70,width=800,height=800,margin=5,background_color='black').generate(t)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()










