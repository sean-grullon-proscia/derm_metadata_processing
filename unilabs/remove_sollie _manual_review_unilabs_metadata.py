import pandas as pd
import numpy as np
import json

from enum import Enum, IntEnum

def dict_merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


class SPECIMEN_LEVEL_JSON_FIELDS(Enum):
    TRAIN = "train"
    VALID = "valid"
    TEST = "test"

    S3_PATH = "s3_path"

    SPECIMEN_TO_WSI_MAP = "specimen_to_wsis"

    IMAGE_ID = "image_id"
    IMAGE_NAME = "image_name"
    PEN_INK = "pen_ink"
    RAW_DIAGNOSIS = "raw_diagnosis"
    SPECIMEN_ID = "specimen_id"
    CASE_ID = "case_id"
    PROSTATE_V1_LABEL = "prostate_v1_label"  # this has been tested using the ProstateAI diagnostic labelling routines
    GLEASON_INFO = "gleason_info"
    TRAIN_VALID_TEST = "train_valid_test"
    BAD_SCAN = "bad_scan"

    # these have been tested using the DermAI diagnostic labelling routines
    CATCHMENT_LABEL = "catchment_label"
    SPECIFIC_LABEL = "specific_label"
    SUPER_LABEL = "super_label"
    SUBCLASS_LABEL = "subclass_label"
    FLAT_LABEL = "flat_label"

def add_custom_labels(metadata_json: dict) -> None:
    """
    Add custom labels in-place for training HI vs REST, CLAM4 and REST models (i.e. merging HIGH_RISK &
    INTERMEDIATE_RISK specimens into HI and all others into REST for HI vs REST classifier)
    Parameters:
    ----------
        metadata_json: [dict] key -> "flat_label"
                              value -> Specimen to flat label mapping (flat label is one of
                                        HIGH_RISK, INTERMEDIATE_RISK, LOW_RISK, BCC, SCC, OTH)
    """

    def change_label(spec2label, list_of_labels_to_replace, replace_label_string):
        return_spec2label = {}
        for each_spec, current_label in spec2label.items():
            if current_label in list_of_labels_to_replace:
                modified_label = replace_label_string
            else:
                modified_label = current_label
            return_spec2label[each_spec] = modified_label
        return return_spec2label

    specimen2flat_labels = metadata_json[SPECIMEN_LEVEL_JSON_FIELDS.FLAT_LABEL.value]

    # For training HI vs REST classifier
    custom_HI_vs_REST_ = change_label(
        specimen2flat_labels,
        list_of_labels_to_replace=["OTH", "LOW_RISK", "BCC", "SCC"],
        replace_label_string="REST",
    )
    metadata_json["custom_HI_vs_REST"] = change_label(
        custom_HI_vs_REST_,
        list_of_labels_to_replace=["HIGH_RISK", "INTERMEDIATE_RISK"],
        replace_label_string="HIGH_AND_INTERMEDIATE_RISK",
    )

    # For training H vs I CLAM4 model
    metadata_json["custom_LR_OTH_BCC_SCC"] = change_label(
        specimen2flat_labels,
        list_of_labels_to_replace=["OTH", "LOW_RISK", "BCC", "SCC"],
        replace_label_string="LR_OTH_BCC_SCC",
    )

    # For training REST classifier
    metadata_json["custom_OTH_H_I"] = change_label(
        specimen2flat_labels,
        list_of_labels_to_replace=["OTH", "HIGH_RISK", "INTERMEDIATE_RISK"],
        replace_label_string="OTH-H-I",
    )


sollie_metadata = "DC001 Review - 07.05.2022.csv"
diagnosis_metadata='Unilabs_diagnosis_metadata.csv'

filenames_to_include = []
filenames_to_exclude = []
dermai_labels=[]
filenames=[]
specimen_to_wsi={}
case_ids=[]
df = pd.read_csv(sollie_metadata)
diag_df=pd.read_csv(diagnosis_metadata).set_index('Snomed_Code')

json1="unilabs_specimen2wsi_mike_exclude.json"

with open(json1,'rb') as f:
    data_all=json.load(f)

for i in range(df.shape[0]):
    if 'completed' in str(df.iloc[i]['folder_name']):
        #print(i)
        #print(df.iloc[i]['folder_name'])
        diagnosis = df.iloc[i]['folder_name']
        snomed_code=diagnosis.split(' ')[1]
        dermai_label=diag_df['dermai_class'].loc[snomed_code].upper()
        #print(dermai_label)

    filename=df.iloc[i]['image_name']
    include = df.iloc[i]['Slide_Field_To_Include']
    if(pd.isnull(filename)==False):
        case = df.iloc[i]['folder_parent_name'].split(' ')[-1]+'-I'
        if case not in case_ids:
           case_ids.append(case)
           dermai_labels.append(dermai_label)
           specimen_to_wsi[case] = []
        if include:
            filenames_to_include.append(filename.split('.')[0])
            specimen_to_wsi[case].append(filename.split('.')[0])
        else:
            filenames_to_exclude.append(filename.split('.')[0])

#print(len(filenames_to_include))
#print(len(filenames_to_exclude))
print(len(case_ids))
print(len(dermai_labels))

sollie_metadata = {
    'specimen_to_wsis':specimen_to_wsi,
    'flat_label':{case_ids[i]: dermai_labels[i] for i in range(len(case_ids))},
    'train':[],
    'valid':[],
    "test":case_ids,
}

add_custom_labels(sollie_metadata)

#data_to_write=dict_merge(data_all,sollie_metadata)
print(len(sollie_metadata['custom_LR_OTH_BCC_SCC']))
sollie_metadata['specimen_to_wsis']=dict_merge(data_all['specimen_to_wsis'],sollie_metadata['specimen_to_wsis'])
sollie_metadata['flat_label']=dict_merge(data_all['flat_label'],sollie_metadata['flat_label'])
sollie_metadata['train']=data_all['train']
sollie_metadata['valid']=data_all['valid']
sollie_metadata['test']=data_all['test']+sollie_metadata['test']
sollie_metadata['custom_HI_vs_REST']=dict_merge(data_all['custom_HI_vs_REST'],sollie_metadata['custom_HI_vs_REST'])
sollie_metadata['custom_LR_OTH_BCC_SCC']=dict_merge(data_all['custom_LR_OTH_BCC_SCC'],sollie_metadata['custom_LR_OTH_BCC_SCC'])
sollie_metadata['custom_OTH_H_I']=dict_merge(data_all['custom_OTH_H_I'],sollie_metadata['custom_OTH_H_I'])


with open("unilabs_specimen2wsi_mike_sollie_exclude.json", "w") as outfile:
    json.dump(sollie_metadata, outfile,indent=4)

"""
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
#with open("unilabs_specimen2wsi_mike_test_set_2.json", "w") as outfile:
 #   json.dump(data_all, outfile,indent=4)"""
