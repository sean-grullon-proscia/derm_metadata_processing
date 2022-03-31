import pandas as pd
import numpy as np

#metadata='To upload eu datalake metadata dc002-group4-melanoma.csv'
#metadata='Uploaded Eu datalake Metadata SOW dc002-group1-nevi.csv'
metadata="1- Unilabs_Batch Uploads (2).csv"
diagnosis_metadata='Unilabs_diagnosis_metadata.csv'
#metadata="To upload eu datalake metadata SOW-DC002.1_skin.csv"
#metadata="Uploaded Metadata dc002-group4-melanoma.csv"
df=pd.read_csv(metadata)
diag_df=pd.read_csv(diagnosis_metadata).set_index('Snomed_Code')

filenames = []
dermai_labels = []
case_ids = []
diagnoses = [] 
specimen_label = []
wsi = []


for i in range(df.shape[0]):
    if str(df.iloc[i]['folder_name'])[0] == 'M':
        diagnosis = df.iloc[i]['folder_name']
        snomed_code=diagnosis.split(' ')[0]
        dermai_label=diag_df['dermai_class'].loc[snomed_code].upper()
        
    filename=df.iloc[i]['image_name']
    #if str(df.iloc[i]['folder_parent_name'])[0] == 'M':
     #       dermai_labels.append(dermai_label)
    if(pd.isnull(filename)==False):
        
        case_ids.append(df.iloc[i]['folder_parent_name'])
        filenames.append(filename)
        dermai_labels.append(dermai_label)
        diagnoses.append(diagnosis)
        specimen_label.append('I')
        wsi.append('')

final_df=pd.DataFrame({'case_id':case_ids,'image_name':filenames,'diagnosis':diagnoses,'dermai_label':dermai_labels,'specimen':specimen_label,'wsi':wsi})
final_df.to_csv('unilabs_flattened_metadata.csv',index=False)
#final_df=pd.DataFrame({'dermai_label':dermai_labels})
print(final_df['dermai_label'].value_counts())