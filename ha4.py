
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# # 1

# In[50]:


import urllib
import requests


# In[51]:


url = 'https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'


# In[52]:


r = requests.get(url)


# In[53]:


r


# Загрузим файлы в переменные:

# In[2]:


data = pd.read_csv('survey_results_public.csv', index_col = 'Respondent')
schema = pd.read_csv('survey_results_schema.csv', index_col = 'Column')


# In[4]:


data.iloc[:,:1].head()


# In[5]:


data.shape[0]


# In[6]:


schema.shape[0]


# В опросе на 154 вопроса приняло участие 51392 респондента

# # 2

# Топ стран по количеству участников:

# In[7]:


((data.groupby(['Country']).size())).sort_values(ascending = False)[0:10]


# Доли участников по странам:

# In[8]:


((data.groupby(['Country']).size())/data.shape[0]).sort_values(ascending = False)[0:10]


# # 3
# 

# # 4

# Мы с вами освоили Git в качестве системы управления версиями. Покажите, какими системами управления версиями (колонка VersionControl) пользуются участники опроса (упорядочите их по количеству ответов).
# 

# In[9]:


((data.groupby(['VersionControl']).size())).sort_values(ascending = False)[0:10]


# # 5

# Теперь посмотрим какие языки программирования популярны. В колонке HaveWorkedLanguage перечислены языки, которыми респондент недавно пользовался. Проблема в том, что можно было отмечать несколько вариантов ответа (они разделены точкой с запятой):

# In[10]:


data['HaveWorkedLanguage'].head()


# In[11]:


language = []
for i in data['HaveWorkedLanguage']:
    if not pd.isnull(i):
        for j in i.split(';'):
            #if j.strip() not in languages:
            language.append(j.strip())
languages = set(language)


# Пожалуйста, создайте новую переменную, в которой будет содержаться список всех языков, встречавшихся среди ответов.

# In[43]:


languages


# # 6

# Теперь сосчитайте, сколько респондентов пользуются каждым из указанных языков. Покажите 10 наиболее популярных. Есть ли среди них Python?

# In[13]:


d = {x:language.count(x) for x in languages}
print(d)    


# In[14]:


lang = pd.DataFrame.from_dict(d, orient='index')
lang = lang.rename(columns = {'index':'language'})
lang = lang.rename(columns = {0:'count'})
lang.sort_values(by = ['count'], ascending = False)[:10]


# # 7

# Добавим колонки по числу языков с бинарными признаками:

# In[15]:


for i in languages:
    data[i] = data['HaveWorkedLanguage'].apply(lambda x: int(str(x).find(i)>=0))


# In[39]:


data.groupby('Country').count()

