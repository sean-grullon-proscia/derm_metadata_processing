import pandas as pd
import numpy as np
import csv

#metadata='To upload eu datalake metadata dc002-group4-melanoma.csv'
#metadata='Uploaded Eu datalake Metadata SOW dc002-group1-nevi.csv'
#metadata='/Users/grullon/Documents/utrecht_new_data/metadata_dc002-skin_sequential-ai_labels.csv'
#metadata='/Users/grullon/Documents/utrecht_new_data/metadata_dc002-group2-dysplastic_ai_labels.csv'
metadata='/Users/grullon/Documents/utrecht_new_data/deid_failed_utrecht_SG-specimen_labels.csv'

group='group1'
#badlist='/Users/grullon/Documents/utrecht_new_data/problematic_cases_wNewGroup1CSV_FlipSpecimenStainorder.txt'
badlist='/Users/grullon/Documents/utrecht_new_data/problematic_cases_wNewGroup1CSV.txt'
udps_full='/Users/grullon/Documents/utrecht_new_data/udps_full.csv'
badmetadata='/Users/grullon/Documents/utrecht_new_data/NEW_FILTERED_metadata_dc002-group2-dysplastic_ai_labels.csv'
#metadata="Uploaded Eu datalake Metadata SOW dc002-group3-melanoma_in_situ.csv"
#metadata="To upload eu datalake metadata SOW-DC002.1_skin.csv"
#metadata="Uploaded Metadata dc002-group4-melanoma.csv"
df=pd.read_csv(metadata)
udps=pd.read_csv(udps_full).drop_duplicates(subset=['rapnaam']).set_index('rapnaam')
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
#df["Slide_Field_Staining"].fillna("", inplace=True)
count=0

case_id=''
n_bad_cases=0
n_bad_diagnoses=0
for i in range(df.shape[0]):
    if len(str(df.iloc[i]['folder_name'])) == 40:
        n_cases+=1
        case_id=df.iloc[i]['folder_name']
        print(case_id)
        """
        case_field_conclusie=df.iloc[i]['Case_Field_Conclusie']
        conclusie=udps.loc[case_id]['conclusie']
        #print("CONCLUSIE ",conclusie)
        #print("CASE CONCLUSIE ",case_field_conclusie)
        #print(i)

        if(conclusie!=case_field_conclusie):
            print('Uh Oh! Diagnosis mismatch for case ',case_id)
            n_bad_diagnoses+=1
        if case_id in bad_case_list:
            n_bad_cases+=1
    #if case_id in bad_case_list:
    if(df.iloc[i]['folder_parent_name'] in bad_case_list):
        #df.iloc[i].to_csv(badmetadata,mode='a',header=False)
        #writer.writerow(df.iloc[0].fillna('').values)
        bad_locs.append(i)
        bad_locs.append(i+1)
        """
#df.iloc[bad_locs].to_csv(badmetadata,index=False)
print('number of cases ',n_cases)
print('number of bad cases', n_bad_cases)
print('Number of missing diagnoses',n_bad_diagnoses)
print('Group counts',pd.read_csv(badlist,header=None).groupby(0).count())
