import requests
import zipfile
import os
import numpy as np
import pandas as pd
import os


import re
import re
import urllib.request
from bs4 import BeautifulSoup


pd.set_option('float_format', '{:6.6f}'.format)
np.set_printoptions(precision=3, suppress=True)
pd.options.display.max_rows = 999
pd.options.display.max_columns = 999


url = 'https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
dirname = '../data/'
path = dirname + 'file.zip'

os.makedirs(dirname, exist_ok=True)
if not os.path.isfile(path):
    response = requests.get(url)
    with open(path, "wb") as file:
        file.write(response.content)


zf = zipfile.ZipFile(path)
files = zf.namelist()

print(files)


survey_results = pd.read_csv( zf.open(files[5]))


survey_results.head()


survey_schema =pd.read_csv( zf.open(files[6]))


survey_schema.head()


# Сколько вопросов было в опросе? Сколько разработчиков приняло участие в нем?




len(survey_results)


len(survey_schema)

#2. Сосчитайте число участников опроса по странам (колонка Country). Выведите 10 стран
#с наибольшим числом респондентов. Покажите число респондентов и их долю в общем
#количестве. Прокомментируйте результаты.

survey_results_respondents=    pd.DataFrame(survey_results.Country.value_counts()[0:10])


survey_results_respondents.columns=['Number']


survey_results_respondents['Ratio'] = survey_results.Country.value_counts()[0:10]/len(survey_results.Country)


print(survey_results_respondents)


sum(survey_results_respondents.Ratio)

#3. Что если число участников определяется просто населением стран, в которых они живут?
#Сосчитайте и выедите 10 стран для которых отношение числа респондентов к населению
#страны наибольшее? Для определенности население стран мира возьмите на страничке
#https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population. Для
#простоты при объединении наборов данных ограничьтесь странами, число участников в
#которых не меньше ста. Прокомментируйте результаты.



url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser') #class object creation




tables = soup.find("table", { "class" : "wikitable sortable" })
T = []
line = []

for row in tables.findAll("tr"):
    cells = row.findAll("td")
    line = []
    for i in range(len(cells)):
        line.append(cells[i].text)
    T.append(line)
    
T = pd.DataFrame(T)
#удалим ненужные строки и столбцы
T = T.loc[1: , ]
del T[0]
del T[3]
del T[4]
del T[5]



T = T.reset_index(drop = True)


T.columns = ['Country', 'Population']


#удалить Notes 1 -23
for c in (T.index) :
    if  T.loc[c].Country.find('Note') > 0   :
        new = ( re.sub("[\(\[].*?[\)\]]", "", str(T.loc[c].Country))  )
        T.loc[c].Country = new



T.Population = T.Population.apply( lambda row: re.sub( ',', "",row ) )



T.Population = T.Population.astype(float)



T.Country = T.Country.apply( lambda row: row[1:]  )




T = T.set_index('Country', drop = True)


T.head()



T.index.rename(None, inplace=True)



Country_value_counts   = pd.DataFrame(survey_results.Country.value_counts())



Country_value_counts.columns = ['Responces']




Country_value_counts.head( ) 


Country_value_counts.loc['United States']



ratio_table = Country_value_counts.join( T )


ratio_table.head()



ratio_table['Ratio'] =ratio_table.Responces / ratio_table.Population



answer3 = ratio_table[ratio_table.Responces >100].sort_values(by='Ratio', ascending= False) [0:10]


print( answer3)



#4. Мы с вами освоили Git в качестве системы управления версиями. Покажите, какими
#системами управления версиями (колонка VersionControl) пользуются участники опроса
#(упорядочите их по количеству ответов).


survey_results.VersionControl.value_counts()

#5. Теперь посмотрим какие языки программирования популярны. В колонке HaveWorkedLanguage
#перечислены языки, которыми респондент недавно пользовался. Проблема в том, что мож-
#но было отмечать несколько вариантов ответа (они разделены точкой с запятой):


survey_results.HaveWorkedLanguage[1]



s = survey_results.HaveWorkedLanguage[1]


languages = set([])




def get_uniq_words ( row):
    if pd.isnull(row):
        return( set())
    else:
        return (set(re.split(';',    row.replace('; ', ';')) ))



get_uniq_words(survey_results.HaveWorkedLanguage[12])



survey_results.apply(  lambda row:  languages.update(   get_uniq_words ( row.HaveWorkedLanguage   )      
                                        ) , axis = 1)


print(list(languages))


#теперь для каждого языка


languages =list(languages)



def coun_word_in_df ( word , string):
    if pd.isnull(string):
        return( 0 )
    else:
        return ( (word in get_uniq_words(string))*1 )


sum(survey_results.HaveWorkedLanguage.apply( lambda row: coun_word_in_df ( languages[4] , row)   ))



def language_count ( lang):
    s = sum(survey_results.HaveWorkedLanguage.apply( lambda row: coun_word_in_df ( lang , row)   ))
    return s



d = { 'counts': [0]*len(languages) , 'languages': languages}
df = pd.DataFrame(data=d)


df = df.set_index('languages', drop=True)


language_count( df.index[0] )




for i in df.index:
    df.loc[i , 'counts' ] =  (language_count( i))



df

#6. Теперь сосчитайте, сколько респондентов пользуются каждым из указанных языков.
#Покажите 10 наиболее популярных. Есть ли среди них Python?
# In[115]:


answer6= df.sort_values(by = 'counts', ascending=False)[0:10]



print( answer6)

#7. Интересно, какие языки программирования популярны в разных странах? Для каждой
#страны, представленной в опросе найдите наиболее популярный язык программирования.
#Выведите его для 10 стран с наибольшим числом респондентов. (Для этого я бы реко-
#мендовал добавить в набор данных колонки бинарных переменных, соответствующими
#каждому языку программирования, и равные единице если язык перечислен в колонке
#HaveWorkedLanguage.)


for i in languages:
    survey_results[i] = survey_results.HaveWorkedLanguage.apply( lambda row: coun_word_in_df ( i , row)   )



c_index = survey_results.Country.value_counts()[0:10].index


survey_results.groupby('Country').sum().loc[c_index , languages]


survey_results.groupby('Country').sum().loc[c_index , languages]



m = survey_results.groupby('Country').sum().loc[c_index , languages]


answer7 = survey_results.groupby('Country').sum().loc[c_index , languages].idxmax(axis=1)



answer7 = pd.DataFrame(answer7)
answer7.columns = ['Language']


answer7



survey_results.groupby('Country')



answer7


p =survey_results.groupby('Country').sum().loc[survey_results.Country.value_counts().index, languages].idxmax(axis=1)




p[p!='JavaScript'][0:10]




p[p!='JavaScript'].index[0]


# 8. Придумайте интересный для вас вопрос, относящийся к исследуемому набору данных,
# и ответьте на него. Оригинальность вопроса поощряется.




survey_results.head()


survey_results.Salary


Salary_table =   survey_results.groupby('Country').count().Salary




Salary_table = pd.DataFrame(Salary_table)
Salary_table.columns = ['Counts']



Salary_table['Mean_Salary'] =     survey_results.groupby('Country').mean().Salary



Salary_table['Std_Salary'] =     survey_results.groupby('Country').std().Salary



Salary_table['Median_Salary'] =     survey_results.groupby('Country').median().Salary




Salary_table_100 =    Salary_table[Salary_table.Counts > 100].sort_values( by ='Mean_Salary', ascending = False )



pd.set_option('float_format', '{:6.0f}'.format)


print( Salary_table_100)







