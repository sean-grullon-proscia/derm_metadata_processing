import pandas as pd
import numpy as np

#metadata='To upload eu datalake metadata dc002-group4-melanoma.csv'
#metadata='Uploaded Eu datalake Metadata SOW dc002-group1-nevi.csv'
metadata="Uploaded Eu datalake Metadata SOW dc002-group3-melanoma_in_situ.csv"
#metadata="To upload eu datalake metadata SOW-DC002.1_skin.csv"
#metadata="Uploaded Metadata dc002-group4-melanoma.csv"
df=pd.read_csv(metadata)
n_single_specimens = 0
n_cases = 0
n_multi_specimen_cases=0
multi_diagnoses=0
specimen_dict={}
specimen_total_counts=0

specimen_dict['I']=0

found_multispecimen=False
multi_keys=['II','III','IV','V','VI','VII']
case_ids=[]
conclusion_strings=[]

for key in multi_keys:
    specimen_dict[key]=0

for i in range(df.shape[0]):
    if len(str(df.iloc[i]['folder_name'])) == 40:
        n_cases+=1
        if(found_multispecimen==True):
            n_multi_specimen_cases+=1
            specimen_total_counts+=1
            for key in multi_keys:
                if(specimen_dict[key]>0):
                    specimen_total_counts+=1
            found_multispecimen=False
        if(specimen_dict[multi_keys[0]]==0 and specimen_dict[multi_keys[1]]==0 and specimen_dict[multi_keys[2]]==0 and specimen_dict[multi_keys[3]]==0 and specimen_dict[multi_keys[4]]==0 and specimen_dict[multi_keys[5]]==0):
        #if(found_multispecimen==False):
            n_single_specimens+=1
            specimen_dict['I']=0
            for key in multi_keys:
                specimen_dict[key]=0
        else:
            #n_multi_specimen_cases+=1
            if(type(conclusion_string)==str):
                if(len(conclusion_string.split('II')) > 1):
                    
                    multi_diagnoses+=1
                else:
                    case_ids.append(case_id)
                    conclusion_strings.append(conclusion_string)
            specimen_dict['I']=0
            for key in multi_keys:
                specimen_dict[key]=0
        case_id=df.iloc[i]['folder_name']
        conclusion_string=df.iloc[i]['Case_Field_Conclusie']

    specimen=df.iloc[i]['Slide_Field_Specimen']
    if(pd.isnull(specimen)==False):
        if(specimen!='I'):
            found_multispecimen=True
            
        specimen_dict[specimen]+=1

print('number of single specimens: ', n_single_specimens)
print('number of cases: ',n_cases)
print('number of multispecimen cases: ',n_multi_specimen_cases)
print('number of multi specimen diagnoses strings',multi_diagnoses)
print('total number of specimens' , specimen_total_counts)
final_df=pd.DataFrame({'case_id':case_ids,'case_field_conclusie':conclusion_strings})
final_df.to_csv('multi_specimen_single_diagnoses_group3_2.csv',index=False)

# if (specimen_dict['I'] == 0):
               # print('problem!')