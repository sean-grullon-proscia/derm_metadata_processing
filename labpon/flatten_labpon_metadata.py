import pandas as pd
import numpy as np

metadata='LabPON_raw_metadata.csv'
diagnosis_metadata='labpon_unique_diagnoses_mb.csv'

diag=pd.read_csv(diagnosis_metadata)
diag['diagnosis']=diag['diagnosis'].apply(lambda x: x.strip())
diag=diag.set_index('diagnosis')
df=pd.read_csv(metadata)
df=df.fillna('')
specimen=[]
wsi=[]
dermai=[]
case_id=df['Casenaam'].iloc[0]
diagnosis=df['Conclusion (EN)'].iloc[0]

for idx in range(len(df)):
        
        row = df.iloc[idx]
        #print('idx ',idx, ' coupe ' ,row['Coupe'])
        #print('idx ',idx, ' caseid ' ,case_id)

        specimen.append(row['Coupe'].split('-')[0])
        wsi.append(row['Coupe'].split('-')[1])

        if row["Casenaam"] == "":
            df['Casenaam'].iloc[idx]=case_id
        else:
            case_id=row['Casenaam']
        if row["Conclusion (EN)"] == "":
            df['Conclusion (EN)'].iloc[idx]=diagnosis
        else:
            diagnosis=row['Conclusion (EN)']
        dai_label=diag.loc[diagnosis.strip()]['dermai_label']
        if(type(dai_label) is str):
            dermai.append(dai_label.rstrip().strip())
        else:
            dermai.append(dai_label.values[0].rstrip().strip())
df['specimen']=specimen
df['wsi']=wsi
df['dermai_label']=dermai
df.to_csv('LabPON_flattened_metadata.csv',index=False)