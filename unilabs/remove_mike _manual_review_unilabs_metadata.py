import pandas as pd
import numpy as np
import json


mike_metadata = "unilabs_mike_bonham_testset_only.csv"
filenames_to_exclude = []
filenames=[]
specimen_to_wsi={}
case_ids=[]
df = pd.read_csv(mike_metadata)
json1="unilabs_specimen2wsi_mike_test_set.json"

with open(json1,'rb') as f:
    data_all=json.load(f)

for i in range(df.shape[0]):
    filename=df.iloc[i]['image_name']
    exclude = df.iloc[i]['Slide_Field_exclude_from_case']
    if(pd.isnull(filename)==False):
        case = df.iloc[i]['folder_parent_name'].split(' ')[-1]+'-I'
        if case not in case_ids:
           case_ids.append(case)
           specimen_to_wsi[case] = []
        if exclude:
            filenames_to_exclude.append(filename.split('.')[0])
        else:
            specimen_to_wsi[case].append(filename.split('.')[0])
n_removed = 0 
n_bad = 0

# TEMP!!!!!
    #for wsi in filenames_to_exclude:
     #   if wsi in data_all['specimen_to_wsis'][case]:
            #data_all['specimen_to_wsis'][case].remove(wsi)
            #n_removed += 1
data_all['test'] = case_ids
for case in case_ids:
    data_all['specimen_to_wsis'].pop(case,None)
    data_all['specimen_to_wsis'][case] = specimen_to_wsi[case]
all_cases = list(data_all['specimen_to_wsis'].keys())
for case in all_cases:
    if case not in data_all['test']:
        if case not in data_all['train']:
            if case not in data_all['valid']:
                data_all['specimen_to_wsis'].pop(case,None)
                n_removed += 1
print(len(data_all['test']))
with open("unilabs_specimen2wsi_mike_test_set_2.json", "w") as outfile:
    json.dump(data_all, outfile,indent=4)