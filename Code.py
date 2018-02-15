import pandas as pd
from bs4 import BeautifulSoup
import requests
import zipfile
import io
import re
import numpy as np


pd.set_option('float_format', '{:.6f}'.format)

survey = "https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM"
data = "survey_results_public.csv"
schema = "survey_results_schema.csv"
populations = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"

survey = requests.get(survey)
#download zip in memory
zp = zipfile.ZipFile(io.BytesIO(survey.content))

data = pd.read_csv(zp.open(data), index_col = 0)
schema = pd.read_csv(zp.open(schema))
#1

print(data.iloc[:, :1].head())
print(schema.head())
#I used index_col only to match output in assignment, it's uncomfortable for me to use
#therefore, reseting it
data = data.reset_index()
respondents = data["Respondent"].size
questions = schema["Question"].size
print("Number of respondents:", respondents)
print("Number of questions:", questions)
print()

#2
countries = (data[["Respondent", "Country"]]
       .groupby("Country").size()
       .sort_values(ascending = False))
print(countries.head(10))
print()
print(countries.head(10)/respondents)
print()

#3
populations = requests.get(populations)
soup = BeautifulSoup(populations.text, "html.parser")
populations  = soup.find('table', attrs = {'class' : 'wikitable sortable'})

table = []
headers = []

rows = populations.find_all('tr')
for th in populations.find_all('th'):
    headers.append(th.getText().strip().replace('\n',''))
for tr in populations.find_all('tr'):
    row = []
    for td in tr.find_all('td'):
        #deleting text between square brackets, on wiki there are notes for some countries in []
        td = re.sub(r'\[.*?\]', '', td.text)
        row.append(' '.join(td.split()))
    table.append(row)

populations = pd.DataFrame(table, columns = headers)
#from wiki downloaded table leaving only country and population
populations = populations.iloc[1:, 1:3]
populations.columns = ['Country', 'Population']
#change population from string to int
populations["Population"] = populations["Population"].str.replace(',', '').apply(int)
countries100 = countries[countries > 100]
#getting numeric index
countries100 = countries100.reset_index()
countries100.columns = ['Country', 'Developers']
#merging 2 datasets on 'Country' column
merged = pd.merge(countries100, populations, on = 'Country')
merged['Ratio'] = merged['Developers'].apply(int)/merged['Population']
#Adjust data to similar output in home assignment pdf
merged = merged.set_index('Country')
merged.columns = ['Country' , 'Population', 'Ratio']
del merged.index.name
print(merged.sort_values('Ratio', ascending = False).head(10))
print()
#4
versionControl = (data[["Respondent", "VersionControl"]]
       .groupby("VersionControl").size()
       .sort_values(ascending = False))
print(versionControl)
print()
#5
#removing white spaces in language string
dummyLanguages = data["HaveWorkedLanguage"].str.replace(r'\s', '')
#splitting language string into columns, with corresponding binary variables
dummyLanguages = dummyLanguages.str.get_dummies(sep = ';')
#all languages can be retrivied as array of columns after splitting
languages = list(dummyLanguages.columns)
print(languages)
print()
#6
print(dummyLanguages[dummyLanguages == 1]
      .count()
      .sort_values(ascending = False)
      .head(10))
print()
#7
#Counting how many users for each language in countries
dummyLanguages["Country"] = data["Country"]
countryPopular = (dummyLanguages
                  .groupby("Country")
                  .sum())
#Finding maximum value for language in row
countryPopular["Total"] = countryPopular.max(axis = 1)
#and corresponding column for that value
countryPopular["Popular"] = countryPopular.idxmax(axis = 1)
print(countryPopular[["Total", "Popular"]]
      .sort_values("Total", ascending = False)
      .head(10))
print()
print(countryPopular[["Total", "Popular"]]
      .loc[countryPopular["Popular"] != "JavaScript"]
      .sort_values("Total", ascending = False)
      .head(5))
print()
#let's find countries with highest copy paste rate, and countries which provide
#above average salary to copy pasters
cp = data[["Country", "StackOverflowCopiedCode", "Salary"]]
#get countries with at least 100 people in survey for more meaningful results
cp = cp[cp["Country"].isin(list(countries100["Country"]))]
#get list of unique answers on question about code copying, and select where person
#copied code at least once a day or once a week
indicators = list(cp.groupby("StackOverflowCopiedCode").max().index)[:2]
cp = cp[cp["StackOverflowCopiedCode"].isin(indicators)]
#group by country and calculating how many people copied code once a day or week, and their
#average salaries
cp = (cp.groupby('Country')
      .agg({'StackOverflowCopiedCode' : np.size, 'Salary' : np.mean}))
#reseting indices for proper division
cp = cp.reset_index()
countries100 = countries100.sort_values("Country").reset_index(drop = True)
cp["copypaste rate"] = (cp["StackOverflowCopiedCode"]/
                                countries100["Developers"])
#shows countries with highest level of copy paste in their code
print(cp.sort_values("copypaste rate", ascending = False).head(10))
print()
#countries where copypasters can earn salary higher than average in survey
print(cp[cp["Salary"] >= data["Salary"].mean()].head(10))
print()
#in which countries copy pasters earn salary higher than country average?
countryAvg = (data[['Country', 'Salary']]
              .groupby('Country', as_index = False)
              .mean())
countryAvg.columns = ['Country', 'Average Salary']
cp = pd.merge(cp, countryAvg, on = 'Country')
print(cp[cp["Salary"] > cp["Average Salary"]]
      [["Country","Salary","Average Salary"]]
      .head(10))



