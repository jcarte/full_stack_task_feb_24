import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime


def extract_all_links(html):
    """intake html string, returns array of all url links found inside."""
    soup = BeautifulSoup(html, 'html.parser').find_all('a')
    links = [link.get('href') for link in soup]
    return links


"""
    Prepares the EF data and returns a pandas dataframe.
    Output Cols: 
        ETid
        ETdateOfDecision
        ETfineEUR
        ETcontrollerProcessor
        ETsector
        ETsummary
        ETcountry
        ETdirectURL
        ETsources
"""
def getEnforcementTrackerDF(path):


    etFile = open(path)
    etData = json.load(etFile)

    etDf = pd.json_normalize(etData, record_path="data") #json has single property "data" where array sits in
    etDf = etDf.drop(columns=[0])#remove first col as its just blank col for buttons on FE

    #give each col a name
    eCol = etDf.columns
    etDf = etDf.rename(columns={
        eCol[0]: 'ETid',
        eCol[1]: 'ETcountryHTML',
        eCol[2]: 'ETauthority',
        eCol[3]: 'ETdateOfDecision',
        eCol[4]: 'ETfineEUR',
        eCol[5]: 'ETcontrollerProcessor',
        eCol[6]: 'ETsector',
        eCol[7]: 'ETquotedArticles',
        eCol[8]: 'ETtype',
        eCol[9]: 'ETsummary',
        eCol[10]: 'ETsourceHTML',
        eCol[11]: 'ETdirectURLHTML'
        })


    etDf['ETcountry'] = etDf['ETcountryHTML'].apply(lambda x: x[(x.rindex('<br />')+6):]) #Just take the country name out of the html, if not found will return all of it except first 6 but its always populated
    etDf['ETdirectURL'] = etDf['ETid'].apply(lambda x: 'https://www.enforcementtracker.com/' + x) #reconstruct direct url from id
    etDf['ETfineEUR'] = etDf['ETfineEUR'].str.replace(',','').apply(pd.to_numeric, errors='coerce') #convert fine amount to number, if non numeric, turn to NAN
    etDf['ETsources'] = pd.array(etDf['ETsourceHTML'].apply(lambda x: extract_all_links(x))) #extract just the links from the html

    #Simplies date to a day format, removes unknowns, months and years for simplicity - I ran out of time for this, I'd do a wide compare on year, month when merging later
    timeFormat = '%Y-%m-%d'
    etDf['ETdateOfDecision'] =  etDf['ETdateOfDecision'].apply(lambda x: datetime.strptime(x, timeFormat) if (len(x)==10 and x[4] =='-' and x[7] == '-') else np.NaN)

    etDf = etDf.drop(columns=['ETcountryHTML','ETauthority','ETquotedArticles','ETtype','ETdirectURLHTML','ETsourceHTML']) #remove unused cols
    return etDf


"""
    Prepares the GH data and returns a pandas dataframe.
    Output Cols:
        GHsummary
        GHcountry
        GHdirectURL
        GHid
        GHfineAmount
        GHfineCurrency
        GHsources
        GHpartiesCompanyName
        GHdate
"""
def getGDPRHubDF(path):

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

    #convert dates to datetime object - will NAT any "unknowns" but also removes just years and months which can't use to cast wide compare later - I ran out of time to do this properly but would later join based on same year/month
    timeFormat = '%Y-%m-%d 00:00:00 UTC'
    ghDf['date'] = ghDf.apply(lambda x: (np.NaN if x['content.date_published'] is np.NaN else datetime.strptime(x['content.date_published'], timeFormat)) if x['content.date_decided'] is np.NaN else datetime.strptime(x['content.date_decided'], timeFormat), axis=1)

    ghDf = ghDf[[
        'content.text.summary',
        'content.date_decided', 
        'content.jurisdiction',
        'wiki.url','wiki.page_id',
        'content.fine.amount',
        'content.fine.currency',
        'sources',
        'partiesCompanyName',
        'date'
        ]]#only select column we need

    #rename cols so inline with other dataframe
    ghDf = ghDf.rename(columns={
        'content.text.summary': 'GHsummary',
        'content.jurisdiction': 'GHcountry',
        'wiki.url': 'GHdirectURL',
        'wiki.page_id': 'GHid',
        'content.fine.amount': 'GHfineAmount',
        'content.fine.currency': 'GHfineCurrency',
        'sources': 'GHsources',
        'partiesCompanyName': 'GHpartiesCompanyName',
        'date': 'GHdate'
        })

    return ghDf




#setup pandas
pd.set_option('display.max_columns', 25)
pd.set_option('display.width', 180)
pd.set_option('display.max_colwidth', 25)

print("Starting")

ENFORCEMENT_TRACKER_LOCAL_PATH = 'enforementtracker_sample_download.json'
GDPR_HUB_LOCAL_PATH = 'gdprhub_sample_download.json'

etDf = getEnforcementTrackerDF(ENFORCEMENT_TRACKER_LOCAL_PATH)
ghDf = getGDPRHubDF(GDPR_HUB_LOCAL_PATH)

#Cut datasets just down to the info needed to join
etDf2 = etDf[['ETid','ETsources']] #, 'ETfineEUR', 'ETdateOfDecision', 'ETcountry' ]]
ghDf2 = ghDf[['GHid','GHsources']] #, 'GHfineAmount', 'GHfineCurrency', 'GHdate', 'GHcountry']]

intersectionDf = etDf2.merge(ghDf2, how = 'cross') # cross join on just the cols needed to join and the ids to outer join back

intersectionDf['sourceMatch'] = intersectionDf.apply(lambda x: any([item in x['GHsources'] for item in x['ETsources']]) , axis=1) #are any of the sources in both lists?
# intersectionDf['fineMatch'] = intersectionDf.apply(lambda x: (x['GHfineCurrency'] == 'EUR') and (x['GHfineAmount'] == x['ETfineEUR']) , axis=1) #do they have the same fine amount?
# intersectionDf['dateMatch'] = intersectionDf.apply(lambda x: x['ETdateOfDecision'] == x['GHdate'] , axis=1) #are they on the same day? Would do a month/year comparison if had more time
# intersectionDf['countryMatch'] = intersectionDf.apply(lambda x: x['ETcountry'] == x['GHcountry'] , axis=1) #are they in the same country?

#intersectionDf = intersectionDf[intersectionDf['sourceMatch'] | ( intersectionDf['fineMatch'] & intersectionDf['dateMatch'] & intersectionDf['countryMatch']  )] #Cut down
intersectionDf = intersectionDf[intersectionDf['sourceMatch']]

combinedDf = pd.merge(intersectionDf, etDf, on='ETid', how='outer')
combinedDf = pd.merge(combinedDf, ghDf, on='GHid', how='outer')

#replace nan with '' in string cols
combinedDf[['GHsummary','ETsummary', 'ETsector', 'GHdirectURL', 'ETdirectURL']] = combinedDf[['GHsummary','ETsummary', 'ETsector', 'GHdirectURL', 'ETdirectURL']].fillna('')

#replace nan with [] in list cols
combinedDf['ETsources_x'] = [ [] if x is np.NaN else x for x in combinedDf['ETsources_x'] ]
combinedDf['GHsources_x'] = [ [] if x is np.NaN else x for x in combinedDf['GHsources_x'] ]
combinedDf['GHpartiesCompanyName'] = [ [] if x is np.NaN else x for x in combinedDf['GHpartiesCompanyName'] ]

combinedDf['sources'] = combinedDf.apply(lambda x: list(set(x['ETsources_x']) | set(x['GHsources_x'])),axis=1)
combinedDf['summary'] = combinedDf.apply(lambda x: x['GHsummary'] + x['ETsummary'],axis=1)

combinedDf['fine_currency'] = combinedDf['GHfineCurrency'].fillna('EUR')
combinedDf['fine_amount'] = combinedDf['ETfineEUR'].fillna(combinedDf['GHfineAmount'])

combinedDf = combinedDf.rename(columns={
    'GHdirectURL': 'gh_direct_url',
    'ETdirectURL': 'et_direct_url',
    'ETsector': 'sector',
    'GHpartiesCompanyName': 'companies',
    'GHid': 'gh_id',
    'ETid': 'et_id'
    })

combinedDf = combinedDf[[
    'gh_direct_url',
    'et_direct_url',
    'sources',
    'companies',
    'summary',
    'fine_amount',
    'fine_currency',
    'sector',
    'gh_id',
    'et_id'
    ]] #cut down to just the cols to output

print(combinedDf)

combinedDf.to_json('combined.json', orient='records')
# etDf.to_json('etDf.json', orient='records')#, lines=True)
# ghDf.to_json('ghDf.json', orient='records')#, lines=True)


#print(intersectionDf)

#print (etDf)
#print (ghDf)

#print(df)


print("Finished")


