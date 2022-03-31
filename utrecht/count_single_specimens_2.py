import pandas as pd
import numpy as np

metadata='To upload eu datalake metadata dc002-group4-melanoma.csv'
#metadata='Uploaded Eu datalake Metadata SOW dc002-group1-nevi.csv'
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
raw_df=df
raw_df.fillna('')
for idx in range(len(raw_df)):
        if(idx)>10:
            break
        row = raw_df.iloc[idx]

        # When `folder_parent_name is not empty` and when `folder_name is not empty`, we assume that we found
        # a specimen in the csv

        if row["folder_parent_name"] != "" and row["folder_name"] != "":
            case_id = row["folder_parent_id"]
            print(case_id)
            case_id = int(case_id)
            
            case_name = row["folder_parent_name"]
            current_specimen_row = idx + 1
            #print(row)
            # We start from the specimen row and loop through the data frame until we find the next specimen row
            # This is done to identify multiple WSIs under each subfolder of each case
            print('GOING OVER SPECIMENS!')
            while (current_specimen_row < len(raw_df)) \
                   and (raw_df.iloc[current_specimen_row]["folder_parent_name"] != ""
                   and raw_df.iloc[current_specimen_row]["folder_name"] == ""):
                next_row = raw_df.iloc[current_specimen_row]
                print(next_row)

                if next_row["Slide_Field_Specimen"] != "":
                    specimen_id, specimen_name = next_row["Slide_Field_Specimen"], next_row["folder_parent_name"]

                current_specimen_row += 1

for i in range(df.shape[0]):
    if len(str(df.iloc[i]['folder_name'])) == 40:
        n_cases+=1
        if(found_multispecimen==True):
            n_multi_specimen_cases+=1            
            found_multispecimen=False
        if(specimen_dict[multi_keys[0]]==0 and specimen_dict[multi_keys[1]]==0 and specimen_dict[multi_keys[2]]==0 and specimen_dict[multi_keys[3]]==0 and specimen_dict[multi_keys[4]]==0 and specimen_dict[multi_keys[5]]==0):
        #if(found_multispecimen==False):
            n_single_specimens+=1
        specimen_dict['I']=0
        for key in multi_keys:
            specimen_dict[key]=0
    specimen=df.iloc[i]['Slide_Field_Specimen']
    if(pd.isnull(df.iloc[i]['image_id'])==False):
        if(pd.isnull(specimen)==True):
            empty_wsis+=1
    if(pd.isnull(specimen)==False):
        specimen_dict[specimen]+=1
        if(specimen!='I'):
            found_multispecimen=True
            

print('number of single specimens: ', n_single_specimens)
print('number of cases: ',n_cases)
print('number of multispecimen cases: ',n_multi_specimen_cases)
print('empty wsis: ',empty_wsis)
