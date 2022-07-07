import pandas as pd
import numpy as np

#metadata='To upload eu datalake metadata dc002-group4-melanoma.csv'
#metadata='Uploaded Eu datalake Metadata SOW dc002-group1-nevi.csv'
#metadata="1- Unilabs_Batch Uploads (2).csv"
metadata="unilabs_raw_metadata_dermai_results_sollie.csv"

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
dermai_plabels=[]
dermai_preds=[]

for i in range(df.shape[0]):
    if str(df.iloc[i]['folder_name'])[0] == 'M':
        #print(i)
        #print(df.iloc[i]['folder_name'])
        diagnosis = df.iloc[i]['folder_name']
        snomed_code=diagnosis.split(' ')[0]
        dermai_label=diag_df['dermai_class'].loc[snomed_code].upper()
        
    filename=df.iloc[i]['image_name']
    #if str(df.iloc[i]['folder_parent_name'])[0] == 'M':
     #       dermai_labels.append(dermai_label)
    if(pd.isnull(filename)==False):
        partition=df.iloc[i]['Slide_Field_train_valid_test']
        if(pd.isnull(partition)==False):
            if(partition=='test'):
                case_ids.append(df.iloc[i]['folder_parent_name'])
                filenames.append(filename)
                dermai_labels.append(dermai_label)
                diagnoses.append(diagnosis)
                specimen_label.append('I')
                dermai_plabels.append(df.iloc[i]['Slide_Field_P_label'])
                dermai_preds.append(df.iloc[i]['Slide_Field_P_score'])


final_df=pd.DataFrame({'case_id':case_ids,'image_name':filenames,'diagnosis':diagnoses,'ground_truth_dermai_label':dermai_labels,'specimen':specimen_label,'predicted_dermai_label':dermai_plabels,'predicted_dermai_label_score':dermai_preds})
final_df.to_csv('unilabs_flattened_metadata_sollie_review_dermai_preds.csv',index=False)
#final_df=pd.DataFrame({'dermai_label':dermai_labels})
#print(final_df['dermai_label'].value_counts())