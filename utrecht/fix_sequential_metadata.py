import pandas as pd
import numpy as np
import csv

#metadata='To upload eu datalake metadata dc002-group4-melanoma.csv'
#metadata='Uploaded Eu datalake Metadata SOW dc002-group1-nevi.csv'
metadata='/Users/grullon/Documents/utrecht_new_data/metadata_dc002-skin_sequential-ai_labels.csv'
group='group1'
badlist='/Users/grullon/Documents/utrecht_new_data/problematic_cases_wNewGroup1CSV.txt'
newmetadata='/Users/grullon/Documents/utrecht_new_data/fixed_metadata_dc002-skin-sequential-ai_labels.csv'
lims=pd.read_csv('/Users/grullon/Documents/utrecht_new_data/lims_utrecht_full.csv').set_index('scancode')
udps_full='/Users/grullon/Documents/utrecht_new_data/udps_full.csv'
udps=pd.read_csv(udps_full).drop_duplicates(subset=['rapnaam']).set_index('rapnaam')

#metadata="Uploaded Eu datalake Metadata SOW dc002-group3-melanoma_in_situ.csv"
#metadata="To upload eu datalake metadata SOW-DC002.1_skin.csv"
#metadata="Uploaded Metadata dc002-group4-melanoma.csv"
df=pd.read_csv(metadata)
bad_case_list=pd.read_csv(badlist,header=None)[1].values
bad_locs=[]
n_single_specimens = 0
n_cases = 0
n_multi_specimen_cases=0
multi_diagnoses=0
specimen_dict={}
specimen_total_counts=0
empty_wsis=0
specimen_dict['I']=0

found_multispecimen=False
multi_keys=['II','III','IV','V','VI','VII']
case_ids=[]
conclusion_strings=[]

for key in multi_keys:
    specimen_dict[key]=0
df["folder_parent_name"].fillna("", inplace=True)
df["folder_name"].fillna("", inplace=True)
df["Slide_Field_Specimen"].fillna("", inplace=True)
df["image_name"].fillna("", inplace=True)
df["Slide_Field_Staining"].fillna("", inplace=True)
count=0

case_id=''
n_bad_cases=0
for i in range(df.shape[0]):
    scancode=df.iloc[i]['name']
    if(pd.isnull(scancode)==False):
        if ((scancode in lims.index.values) == True):
            stain=lims.loc[scancode]['staining']
            df['Slide_Field_Staining'].iloc[i]=stain
            #print(stain)
            df['Slide_Field_Block'].iloc[i]=lims.loc[scancode]['block']
            df['Slide_Field_Scancode'].iloc[i]=scancode
            df['Slide_Field_Specimen'].iloc[i]=lims.loc[scancode]['specimen']
            df['Slide_Field_Specimen.1'].iloc[i]=lims.loc[scancode]['specimen']
    if len(str(df.iloc[i]['folder_name'])) == 40:
        case_id=df.iloc[i]['folder_name']
        conclusie=udps.loc[case_id]['conclusie']
        df['Case_Field_Conclusie'].iloc[i]=conclusie

df.to_csv(newmetadata,index=False)
