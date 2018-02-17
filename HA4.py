
# coding: utf-8

# In[132]:

#HA4
import pandas as pd
import re
import requests
import zipfile
import os


# In[133]:

path = '../data/'
os.makedirs(path, exist_ok=True)
link = 'https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
filepath = path +'data.zip'
if not os.path.isfile(filepath):
    response = requests.get(link)
    with open(filepath, "wb") as file:
        file.write(response.content)
zf = zipfile.ZipFile(filepath)
print(zf.namelist())
data=pd.read_csv(zf.open('survey_results_public.csv'),sep=',', index_col=list(range(1)), na_values=['.'],header=0)
schema=pd.read_csv(zf.open('survey_results_schema.csv'),sep=',', index_col=list(range(1)), na_values=['.'],header=0)


# In[134]:

#1
print(data.iloc[:,:1].head())


# In[135]:

print(schema.head())


# In[136]:

#2
data['Country'].head()
data['Country'].value_counts().head(10)


# In[137]:

data['Country'].value_counts().head(10)/data['Country'].value_counts().sum()


# In[138]:

#3
import urllib.request
from bs4 import BeautifulSoup
url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
data1=urllib.request.urlopen(url).read()
soup = BeautifulSoup(data1, 'html.parser')
output=[]
list2=[]
header=[]
for tr in soup.find_all('tr'):
    list1=[]
    for td in tr.find_all('td'):
        text=td.text
        if text[0].isdigit():
            text=text.replace(',','') 
        if not text[0].isdigit():
            text=text.split('[')
            text=text[0]
            text=text.split('(')
            text=text[0]
            text=text.strip()
            if text=='Russia':
                text='Russian Federation'
            if text=='Slovakia':
                text='Slovak Republic'
        list1.append(text)
    for th in tr.find_all('th'):
        text=th.text
        list1.append(text)
    list2.append(list1)
task2=pd.DataFrame(list2).iloc[1:-13,1:3]
task2.columns=list(task2.iloc[0,:])
task2=task2.iloc[1:,:]
task2=task2.set_index(task2.columns[0])
task22 = data.groupby(['Country'])['Professional'].agg([pd.Series.count])
task22.sort_values(by='count', ascending=False, inplace=True)
task22.columns=['Country']
result2=task22[task22['Country']>100].merge(task2,how='inner',left_index=True,right_index=True)
result2['Ratio']=result2['Country'].astype(float)/result2['Population'].astype(float)
result2['Country']=result2['Country'].astype(float)
result2['Population']=result2['Population'].astype(float)
print(result2.sort_values(by='Ratio',ascending=False).head(10))


# In[139]:

#4
data['VersionControl'].value_counts()


# In[140]:

list1=set()
for i in data['HaveWorkedLanguage'].fillna('Unknown'):
    if i=='Unknown':
        continue
    else:
        a=set(i.split('; '))
        list1=list1|a
Languages=list(list1)
print(Languages,end=' ')


# In[141]:

#6
task6=data
for i in list(list1):
    task6[i]=0
k=0
for i in task6['HaveWorkedLanguage'].fillna('Unknown'):
    k=k+1
    if i=='Unknown':
        continue
    else:
        a=i.split('; ')
        for l in a:
            task6.ix[k,l]=1
task6[list(list1)].sum().sort_values(ascending=False).head(10)


# In[142]:

#7
task7 = task6.groupby(['Country'])[list(list1)].agg([pd.Series.sum])
task7.columns=[list(list1)]
task7=pd.DataFrame(task7.idxmax(axis=1))
task7.columns=['Popular']
task77 = data.groupby(['Country'])['Professional'].agg([pd.Series.count])
task77.columns=['Total']
result = pd.merge(task77,task7, left_index=True, right_index=True)
result.sort_values(by='Total', ascending=False, inplace=True)
print(result.head(10))


# In[143]:

#7.1
print(result[result['Popular']!='JavaScript'].head(5))


# In[144]:

#8
task8=pd.get_dummies(data, columns=['Overpaid'])
lis89=list(task8.columns[:-5])
lis90=['Greatly overpaid', 'Greatly underpaid',
       'Neither underpaid nor overpaid', 'Somewhat overpaid',
       'Somewhat underpaid']
task8.columns=lis89+lis90
task88 = task8.groupby(['Country'])[task8.columns[-5:]].agg([pd.Series.sum])
task88.columns=task8.columns[-5:]
task88=pd.DataFrame(task88.idxmax(axis=1))
task88.columns=['Overpaid']
task22 = data.groupby(['Country'])['Professional'].agg([pd.Series.count])
task22.columns=['Country']
result8=task22[task22['Country']>50].merge(task88,how='inner',left_index=True,right_index=True)
result8.sort_values(by='Country', ascending=False, inplace=True)
print(result8.head(10))


# In[145]:

#8.1
print(result8[(result8['Overpaid']=='Greatly underpaid')].head(5))


# In[ ]:



