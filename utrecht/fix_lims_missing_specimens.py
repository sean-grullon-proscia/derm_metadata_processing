import pandas as pd
import numpy as np
import csv

#metadata='To upload eu datalake metadata dc002-group4-melanoma.csv'
#metadata='Uploaded Eu datalake Metadata SOW dc002-group1-nevi.csv'
metadata='/Users/grullon/Documents/utrecht_new_data/utrecht_deidentification_failed-MB with specimen ID.csv'
group='group1'
newmetadata='/Users/grullon/Documents/utrecht_new_data/lims_utrecht_full_imputed.csv'
lims=pd.read_csv('/Users/grullon/Documents/utrecht_new_data/lims_utrecht_full.csv',usecols=[1,2,3,4,5])
udps_full='/Users/grullon/Documents/utrecht_new_data/udps_full.csv'
udps=pd.read_csv(udps_full).drop_duplicates(subset=['rapnaam']).set_index('rapnaam')

#metadata="Uploaded Eu datalake Metadata SOW dc002-group3-melanoma_in_situ.csv"
#metadata="To upload eu datalake metadata SOW-DC002.1_skin.csv"
#metadata="Uploaded Metadata dc002-group4-melanoma.csv"
df=pd.read_csv(metadata)

n_single_specimens = 0
n_cases = 0
n_multi_specimen_cases=0
multi_diagnoses=0
specimen_dict={}
specimen_total_counts=0
empty_wsis=0
specimen_dict['I']=0

case_ids=[]
conclusion_strings=[]

imputed=dict()
imputed['scancode']=[]
imputed['PA']=[]
imputed['specimen']=[]
imputed['block']=[]
imputed['staining']=[]


case_id=''
for i in range(df.shape[0]):
    if len(str(df.iloc[i]['folder_name'])) == 40:
        n_cases+=1
        case_id=df.iloc[i]['folder_name']
    
    scancode=df.iloc[i]['name']
    imputed_specimen=df.iloc[i]['Specimen ID-MB']
    stain=df.iloc[i]['Stain']
    if(pd.isnull(scancode)==False):
        if(pd.isnull(stain)==False):
            imputed['scancode'].append(scancode)
            imputed['PA'].append(case_id)
            imputed['block'].append(1.0)
            imputed['staining'].append(stain)
            if(pd.isnull(imputed_specimen)==False):
                imputed['specimen'].append(imputed_specimen)
            else:
                imputed['specimen'].append('I')

print(pd.DataFrame(imputed).shape)       
imputed_df=pd.concat([lims,pd.DataFrame(imputed)])

imputed_df.to_csv(newmetadata,index=False)
