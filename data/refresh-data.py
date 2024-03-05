import json
import pandas as pd

from bs4 import BeautifulSoup

#intake html string, output array of all url links found inside
def extract_all_links(html):
    soup = BeautifulSoup(html, 'html.parser').find_all('a')
    links = [link.get('href') for link in soup]
    return links


#pd.show_versions()
pd.set_option('display.max_columns', 25)
pd.set_option('display.width', 170)
pd.set_option('display.max_colwidth', 100)

print("Starting")

ENFORCEMENT_TRACKER_LOCAL_PATH = 'enforementtracker_sample_download.json'
GDPR_HUB_LOCAL_PATH = 'gdprhub_sample_download.json'



etFile = open(ENFORCEMENT_TRACKER_LOCAL_PATH)
etData = json.load(etFile)

etDf = pd.json_normalize(etData, record_path="data") #json has single property "data" where array sits in
etDf = etDf.drop(columns=[0])#remove first col as its just blank col for buttons on FE

#give each col a name
eCol = etDf.columns
etDf = etDf.rename(columns={
    eCol[0]: 'eTid',
    eCol[1]: 'countryHTML',
    eCol[2]: 'authority',
    eCol[3]: 'dateOfDecision',
    eCol[4]: 'fineEUR',
    eCol[5]: 'controllerProcessor',
    eCol[6]: 'sector',
    eCol[7]: 'quotedArticles',
    eCol[8]: 'type',
    eCol[9]: 'summary',
    eCol[10]: 'sourceHTML',
    eCol[11]: 'directURLHTML'
    })


etDf['country'] = etDf['countryHTML'].apply(lambda x: x[(x.rindex('<br />')+6):]) #Just take the country name out of the html, if not found will return all of it except first 6 but its always populated
etDf['directURL'] = etDf['eTid'].apply(lambda x: 'https://www.enforcementtracker.com/' + x) #reconstruct direct url from id
etDf.loc[etDf['dateOfDecision'] == "Unknown", 'dateOfDecision'] = '' #Remove all unknown dates
etDf['fineEUR'] = etDf['fineEUR'].str.replace(',','').apply(pd.to_numeric, errors='coerce') #convert fine amount to number, if non numeric, turn to NAN
etDf['sources'] = pd.array(etDf['sourceHTML'].apply(lambda x: extract_all_links(x))) #extract just the links from the html


etDf = etDf.drop(columns=['countryHTML','authority','quotedArticles','type','directURLHTML','sourceHTML']) #remove unused cols


print(etDf)
#etDf.to_json('temp.json', orient='records')


# ghFile = open(GDPR_HUB_LOCAL_PATH, encoding="utf-8")
# ghData = json.load(ghFile)
# ghDf = pd.json_normalize(ghData, record_path="rows") #json has single property "rows" where array sits in
# print(ghDf)

print("Finished")

