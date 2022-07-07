import pandas as pd
import numpy as np
import json

#metadata='To upload eu datalake metadata dc002-group4-melanoma.csv'
#metadata='Uploaded Eu datalake Metadata SOW dc002-group1-nevi.csv'
#metadata="1- Unilabs_Batch Uploads (2).csv"
json1="unilabs_specimen2wsi.json"
json2="unilabs_specimen2wsi_limited_wsi_number.json"

with open(json1,'rb') as f:
    data_all=json.load(f)

with open(json2,'rb') as f:
    data_limited=json.load(f)

for case in data_limited['test']:
    data_limited['specimen_to_wsis'][case] = data_all['specimen_to_wsis'][case]

with open("unilabs_specimen2wsi_mike_test_set.json", "w") as outfile:
    json.dump(data_limited, outfile,indent=4)