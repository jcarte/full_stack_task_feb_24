import json

print("Starting")

ENFORCEMENT_TRACKER_LOCAL_PATH = '.\enforementtracker_sample_download.json'
GDPR_HUB_LOCAL_PATH = '.\gdprhub_sample_download.json'

etFile = open(ENFORCEMENT_TRACKER_LOCAL_PATH)
etData = json.load(etFile)
# print(etData)

ghFile = open(GDPR_HUB_LOCAL_PATH, encoding="utf-8")
ghData = json.load(ghFile)
# print(ghData)

print("Finished")

