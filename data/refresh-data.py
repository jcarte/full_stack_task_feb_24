import json
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup


def extract_all_links(html):
    """intake html string, returns array of all url links found inside."""
    soup = BeautifulSoup(html, 'html.parser').find_all('a')
    links = [link.get('href') for link in soup]
    return links

def getEnforcementTrackerDF(path):
    """
        Prepares the EF data and returns a pandas dataframe.
        Output Cols: 
            eTid
            dateOfDecision
            fineEUR
            controllerProcessor
            sector
            summary
            country
            directURL
            sources
    """

    etFile = open(path)
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
    return etDf


def getGDPRHubDF(path):
    """
        Prepares the GH data and returns a pandas dataframe.
        Output Cols:
            summary
            country
            directURL
            ghId
            fineAmount
            fineCurrency
    """
    ghFile = open(GDPR_HUB_LOCAL_PATH, encoding="utf-8")
    ghData = json.load(ghFile)
    ghDf = pd.json_normalize(ghData, record_path="rows") #json has single property "rows" where array sits in

    ghDf['content.fine.amount'] = pd.to_numeric(ghDf['content.fine.amount'], errors='coerce')#convert fines to numeric and filter for only rows with fines (as task is only fine information)
    ghDf = ghDf[ghDf['content.fine.amount'] > 0] 

    ghDf['content.jurisdiction'] = ghDf['content.jurisdiction'].apply(lambda x: x.upper()) #uppercase to match other ef data

    ghDf['content.sources'] = ghDf['content.sources'].apply(lambda x: [] if x is np.NaN else x)#clean up array if any blanks
    ghDf['sources'] = ghDf['content.sources'].apply(lambda x: [y['url'] for y in x])#just take the url for each source
    
    ghDf['content.parties'] = ghDf['content.parties'].apply(lambda x: [] if x is np.NaN else x)#clean up array if any blanks
    ghDf['partiesCompanyName'] = ghDf['content.parties'].apply(lambda x: [y['name'] for y in x])#just take the name for each party

    ghDf = ghDf[['content.text.summary','content.jurisdiction','wiki.url','wiki.page_id','content.fine.amount','content.fine.currency']]#only select column we need

    #rename cols so inline with other dataframe
    ghDf = ghDf.rename(columns={
        'content.text.summary': 'summary',
        'content.jurisdiction': 'country',
        'wiki.url': 'directURL',
        'content.fine.amount': 'fineAmount',
        'content.fine.currency': 'fineCurrency',
        'wiki.page_id': 'ghId'
        })

    return ghDf






#pd.show_versions()
pd.set_option('display.max_columns', 25)
pd.set_option('display.width', 170)
pd.set_option('display.max_colwidth', 100)

print("Starting")

ENFORCEMENT_TRACKER_LOCAL_PATH = 'enforementtracker_sample_download.json'
GDPR_HUB_LOCAL_PATH = 'gdprhub_sample_download.json'

etDf = getEnforcementTrackerDF(ENFORCEMENT_TRACKER_LOCAL_PATH)
ghDf = getGDPRHubDF(GDPR_HUB_LOCAL_PATH)

#print (etDf)
#print (ghDf)

print("Finished")


