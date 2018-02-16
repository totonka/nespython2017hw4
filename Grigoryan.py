#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 23:11:06 2018

@author: macbookpro
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 15:38:50 2018

@author: macbookpro
"""
#%%
#(1)
import numpy as np
import pandas as pd
import requests
#df = pd.DataFrame.from_csv('Users/macbookpro/Documents/NES/Data analysis/HW/4/survey/survey_results_public.csv')
answers=pd.read_csv('survey_results_public.csv', sep = ',')
questions = pd.read_csv('survey_results_schema.csv', sep =',')

url = 'https://drive.google.com/uc?export= download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
req = requests.get(url)


#Сколько вопросов было в опросе?
questions.iloc[:,:2]
len(questions.Question)
#154

#Сколько разработчиков приняло участие в нем?
answers.Respondent.count()
#51392
#%%
#(2)
answers2=answers.groupby('Country').Country.count()
answers2=answers2.sort_values('index', ascending = False)
answers2.iloc[:10] # 10 стран с наибольшим числом респондентов

answers2 = pd.Series.to_frame(answers2) 
summ = sum(answers2.Country)

y=answers2.Country/summ #доля в общем количестве
y.iloc[:10]

# США лидирует с явным отрывом. 


#%% 
#(3)


#%%
#(4)
answers4=answers.groupby('VersionControl').VersionControl.count()
answers4=answers4.sort_values('index', ascending = False)
print(answers4)
#%%
#(5)
answers['HaveWorkedLanguage'].head()

raw_answers5=answers['HaveWorkedLanguage'].str.split(';', expand=True)

#answers5=[]
#for i in range(len(answers)):
    #искать уникальные значения. Если встеритлось что-то новое,
    #то закинуть в answers5. Если есть хотя бы одно совпадение, то не включать.


#answers5.iloc[:,0]
answers5=raw_answers5.dropna()
#raw_answers5.replace(None, 0)
languages=np.unique(answers5)
languages=list(languages)
print(languages)


# надо переделать так как выбрасывает строки с None

#%%
#6

dict={}
for i in raw_answers5:
    count = raw_answers5.count()
    dict[i]=count[i]
    


#%%
#7

#%%
#8

armenia=answers[answers.Country=='Armenia']
gender_share=len(armenia[armenia.Gender=='Male'])/len(armenia[armenia.Gender == 'Female'])
print(gender_share)





















