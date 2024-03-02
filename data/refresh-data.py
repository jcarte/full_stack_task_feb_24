import json
import pandas as pd

#pd.show_versions()
pd.set_option('display.max_columns', 25)
pd.set_option('display.width', 200)

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


print(etDf)

# # print(etData)

# ghFile = open(GDPR_HUB_LOCAL_PATH, encoding="utf-8")
# ghData = json.load(ghFile)
# # print(ghData)

print("Finished")

