import numpy as np 
import pdb
import csv
import matplotlib.pyplot as plt
import os

#fnames_prospective=['Combined Sequential and Curated - Sequential.csv']
#fnames_prospective=['unilabs_raw_metadata_dermai_results.csv']
fnames_prospective=['unilabs_raw_metadata_dermai_results_sollie.csv']

if len(fnames_prospective)!=1:
	error('script assumes one prospective file')
fnames_curated=['Combined Sequential and Curated - Curated.csv']
fnames = fnames_prospective 
output_file = 'unilabs_sim_results_sollie.csv'
pie_output_file = 'unilabs_data_for_pie_charts_sollie.csv'
raw_data_output_file = 'unilabs_sim_test_set_calibration_results_sollie.csv'
if os.path.isfile(output_file):
	os.remove(output_file)
if os.path.isfile(pie_output_file):
	os.remove(pie_output_file)
if os.path.isfile(raw_data_output_file):
	os.remove(raw_data_output_file)

datamap={}
for fle in fnames:
	with open(fle,'r') as f:
		reader=csv.reader(f)
		columns = zip(*reader)
	dmap={d[0]:d[1:] for d in columns}
	if fle in fnames_prospective:
		datamap_prospective = dmap
	for key in dmap.keys():
		if key in datamap.keys():
			datamap[key]+=(dmap[key])
		else:
			datamap[key]=dmap[key]

#weed out blank rows:
contains_data = [ind for (ind,i) in enumerate(datamap['Slide_Field_P_label']) if i!='']
test_inds = [ind for (ind,i) in enumerate(datamap['Slide_Field_train_valid_test']) if i=='test']
non_duplicate_spec,ind_non_duplicate = np.unique(datamap['Slide_Field_specimen_id'],return_index=True)
inds_of_results = [i for i in contains_data if i in ind_non_duplicate if i in test_inds]
#Find unique prospective specimens with results:
non_duplicate_prospective_spec,ind_non_duplicate_prosp = np.unique(datamap_prospective['Slide_Field_specimen_id'],return_index=True)
contains_data_prosp = [ind for (ind,i) in enumerate(datamap_prospective['Slide_Field_P_label']) if i!='']
test_inds_prosp = [ind for (ind,i) in enumerate(datamap_prospective['Slide_Field_train_valid_test']) if i=='test']
inds_of_prosp_results = [i for i in contains_data_prosp if i in ind_non_duplicate_prosp if i in test_inds_prosp]
prosp_zip = zip(non_duplicate_prospective_spec,ind_non_duplicate_prosp)
prospective_specs = [spec for spec,ind in prosp_zip if ind in inds_of_prosp_results]

#narrow everything to useable data and compute what we need:
result_dict={}
with open(raw_data_output_file,'a') as f:
	f.writelines('Case Name,Specimen ID,Example Image Name,DermAI classification,Ground Truth AI Label,Original Diagnosis (English translation),Dataset\n')
for i in inds_of_results:
	spec_id = datamap['Slide_Field_specimen_id'][i]
	#result_dict['specimens'].append(spec_id)
	result_dict[spec_id]={}
	result_dict[spec_id]['classification']=datamap['Slide_Field_P_label'][i]
	result_dict[spec_id]['ground truth']=datamap['Slide_Field_Ground_Truth'][i]
	result_dict[spec_id]['case']=datamap['folder_parent_name'][i]
	result_dict[spec_id]['image']=datamap['image_name'][i]
	result_dict[spec_id]['diagnosis']=datamap['Slide_Field_Path_Report_Diagnosis_1'][i].replace(',','-')
	if spec_id in prospective_specs:
		result_dict[spec_id]['prospective']=True
		result_dict[spec_id]['dataset']='Sequential DC002.1'
	else:
		result_dict[spec_id]['prospective']=False
		result_dict[spec_id]['dataset']='Curated Melanocytic DC002.2'
	with open(raw_data_output_file,'a') as f:
		f.writelines(result_dict[spec_id]['case']+','+spec_id+','+result_dict[spec_id]['image']+','+result_dict[spec_id]['classification']+','+result_dict[spec_id]['ground truth']+','+result_dict[spec_id]['diagnosis']+','+result_dict[spec_id]['dataset'] +'\n')

# setting up and initializing...
classes=['melanoma','OTHER','BCC','SCC','LOW_RISK','UNCERTAIN']
dermpath_classes = ['MELANOCYTIC_SUSPECT','HIGH_RISK','OTHER','UNCERTAIN','INTERMEDIATE_RISK']
genpath_classes = ['BCC','SCC','LOW_RISK']
ground_truth_classes=['BCC','SCC','LOW_RISK','INTERMEDIATE_RISK','HIGH_RISK','OTHER']
TP={}
TN={}
FN={}
FP={}
dermpath={}
genpath={}
pred_positives={}
for cl in classes +['dermpath','genpath']:
	TP[cl]=0.
	TN[cl]=0.
	FN[cl]=0.
	FP[cl]=0.
	dermpath[cl]=0.
	genpath[cl]=0.
	pred_positives[cl]=[]
pred_positives['MELANOCYTIC_SUSPECT']=[]
pred_positives['HIGH_RISK']=[]

ground_truth=[]
#compute ground truth distribution for prospective only:
for spec in result_dict.keys():
	if result_dict[spec]['prospective']==True:
		ground_truth.append(result_dict[spec]['ground truth'])
total_specimens = float(len(prospective_specs))
ground_truth_perc={}
print('Ground Truth Class Percentages:')
for cl in ground_truth_classes:
	counts=ground_truth.count(cl)
	ground_truth_perc[cl]=counts/total_specimens
	print(cl,':',ground_truth_perc[cl])



# pan through results and compute metrics for prospective set
for spec in prospective_specs:
	
	if result_dict[spec]['ground truth']=='HIGH_RISK' or result_dict[spec]['ground truth']=='INTERMEDIATE_RISK':
		#if melanoma...
		if result_dict[spec]['classification']=='HIGH_RISK' or result_dict[spec]['classification']=='MELANOCYTIC_SUSPECT':
			# if predicted melanoma
			TP['melanoma']+=1
			dermpath['melanoma']+=1
			pred_positives[result_dict[spec]['classification']].append(result_dict[spec]['ground truth'])
			pred_positives['melanoma'].append(result_dict[spec]['ground truth'])
		else:
			#predicted not melanoma
			FN['melanoma']+=1

	else:
		#not melanoma
		if result_dict[spec]['classification']=='MELANOCYTIC_SUSPECT' or result_dict[spec]['classification']=='HIGH_RISK':
			#predicted melanoma
			FP['melanoma']+=1
			pred_positives[result_dict[spec]['classification']].append(result_dict[spec]['ground truth'])
			pred_positives['melanoma'].append(result_dict[spec]['ground truth'])
		else:
			TN['melanoma']+=1
	for cl in classes[1:]:
		if result_dict[spec]['ground truth']==cl:
			#is class
			if result_dict[spec]['classification']==cl:
				#predicted class
				TP[cl]+=1
				pred_positives[result_dict[spec]['classification']].append(result_dict[spec]['ground truth'])
			else:
				#predicted not class
				FN[cl]+=1
		else:
			# is not class
			if result_dict[spec]['classification']!=cl:
				#not predicted class
				TN[cl]+=1
			elif result_dict[spec]['classification']==cl:
				#predicted class
				FP[cl]+=1
				pred_positives[result_dict[spec]['classification']].append(result_dict[spec]['ground truth'])
	if result_dict[spec]['classification'] in dermpath_classes:
		#went to dermpath
		pred_positives['dermpath'].append(result_dict[spec]['ground truth'])
		if result_dict[spec]['ground truth'] in dermpath_classes:
			#should've gone to dermpath
			TP['dermpath']+=1
			TN['genpath']+=1
		else:
			#should've gone to genpath
			FP['dermpath']+=1
			FN['genpath']+=1
	else:
		# went to genpath
		pred_positives['genpath'].append(result_dict[spec]['ground truth'])
		if result_dict[spec]['ground truth'] in genpath_classes:
			#should've gone to genpath
			TP['genpath']+=1
			TN['dermpath']+=1
		else:
			#should've gone to dermpath
			FP['genpath']+=1
			FN['dermpath']+=1



#compute sensitivity and specificity, PPV and NPV and prospective classification %:
sensitivity={}
specificity={}
PPV={}
NPV={}
with open(output_file,'a') as f:
	f.writelines('PROSPECTIVE\n')
	f.writelines(',sensitivity, specificity, PPV, NPV\n')
for cl in classes+['dermpath','genpath']:
	print('~~~~~~~~~~~~~PROSPECTIVE~~~~~~~~~~~~~~~~~',)
	print(cl)
	print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~',)
	print('percentage of data with this classification:',(TP[cl]+FP[cl])/len(prospective_specs))
	if cl!='UNCERTAIN':
		sensitivity[cl]=TP[cl]/(TP[cl]+FN[cl])
		specificity[cl]=TN[cl]/(TN[cl]+FP[cl])
		PPV[cl]=TP[cl]/(TP[cl]+FP[cl])
		NPV[cl]=TN[cl]/(TN[cl]+FN[cl])
		print('PPV:', PPV[cl])
		print('NPV:', NPV[cl])
		print('Sensitivity:',sensitivity[cl])
		print('specificity:',specificity[cl])
		with open(output_file,'a') as f:
			f.writelines(cl +',' + str(sensitivity[cl]) +',' + str(specificity[cl]) +',' + str(PPV[cl]) +',' + str(NPV[cl]) +'\n')

	else:
		print('count:',FP[cl])
		#print('percentage:',FP[cl]/len(result_dict.keys()))


with open(pie_output_file,'a') as f:
	f.writelines('stats for each PREDICTED class\n')

#pie chart each predicted class 
for cl in dermpath_classes[:-1]+genpath_classes+['dermpath','genpath']:
	size_class=float(len(pred_positives[cl]))
	percs=[]
	gt_classes = []
	with open(pie_output_file,'a') as f:
		f.writelines('-'+cl+'-\n')
	for i in np.unique(pred_positives[cl]):
		ct=pred_positives[cl].count(i)
		percs.append(ct/size_class)
		gt_classes.append(i)
		with open(pie_output_file,'a') as f:
			f.writelines(i+','+str(ct)+'\n')
	figure = plt.figure()
	plt.pie(percs,labels=gt_classes,autopct=lambda p: '{:.0f}%'.format(p))
	plt.title(cl)
	plt.show()

with open(output_file,'a') as f:
	f.writelines('% predicted melanoma,'+ str((TP['melanoma']+FP['melanoma'])/len(prospective_specs))+'\n')


#############################################
# pan through results and compute metrics for ALL data 
TP={}
TN={}
FN={}
FP={}
dermpath={}
genpath={}
pred_positives={}
for cl in classes +['dermpath','genpath']:
	TP[cl]=0.
	TN[cl]=0.
	FN[cl]=0.
	FP[cl]=0.
	dermpath[cl]=0.
	genpath[cl]=0.
	pred_positives[cl]=[]
pred_positives['MELANOCYTIC_SUSPECT']=[]
pred_positives['HIGH_RISK']=[]
for spec in result_dict.keys():
	
	if result_dict[spec]['ground truth']=='HIGH_RISK' or result_dict[spec]['ground truth']=='INTERMEDIATE_RISK':
		#if melanoma...
		if result_dict[spec]['classification']=='HIGH_RISK' or result_dict[spec]['classification']=='MELANOCYTIC_SUSPECT':
			# if predicted melanoma
			TP['melanoma']+=1
			dermpath['melanoma']+=1
			pred_positives[result_dict[spec]['classification']].append(result_dict[spec]['ground truth'])
			pred_positives['melanoma'].append(result_dict[spec]['ground truth'])
		else:
			#predicted not melanoma
			FN['melanoma']+=1
	else:
		#not melanoma
		if result_dict[spec]['classification']=='MELANOCYTIC_SUSPECT' or result_dict[spec]['classification']=='HIGH_RISK':
			#predicted melanoma
			FP['melanoma']+=1
			pred_positives[result_dict[spec]['classification']].append(result_dict[spec]['ground truth'])
			pred_positives['melanoma'].append(result_dict[spec]['ground truth'])
		else:
			TN['melanoma']+=1
	for cl in classes[1:]:
		if result_dict[spec]['ground truth']==cl:
			#is class
			if result_dict[spec]['classification']==cl:
				#predicted class
				TP[cl]+=1
				pred_positives[result_dict[spec]['classification']].append(result_dict[spec]['ground truth'])
			else:
				#predicted not class
				FN[cl]+=1
		else:
			# is not class
			if result_dict[spec]['classification']!=cl:
				#not predicted class
				TN[cl]+=1
			elif result_dict[spec]['classification']==cl:
				#predicted class
				FP[cl]+=1
				pred_positives[result_dict[spec]['classification']].append(result_dict[spec]['ground truth'])
	if result_dict[spec]['classification'] in dermpath_classes:
		#went to dermpath
		pred_positives['dermpath'].append(result_dict[spec]['ground truth'])
		if result_dict[spec]['ground truth'] in dermpath_classes:
			#should've gone to dermpath
			TP['dermpath']+=1
			TN['genpath']+=1
		else:
			#should've gone to genpath
			FP['dermpath']+=1
			FN['genpath']+=1
	else:
		# went to genpath
		pred_positives['genpath'].append(result_dict[spec]['ground truth'])
		if result_dict[spec]['ground truth'] in genpath_classes:
			#should've gone to genpath
			TP['genpath']+=1
			TN['dermpath']+=1
		else:
			#should've gone to dermpath
			FP['genpath']+=1
			FN['dermpath']+=1



#compute sensitivity and specificity, PPV and NPV and prospective classification %:
sensitivity={}
specificity={}
PPV={}
NPV={}
with open(output_file,'a') as f:
	f.writelines('ALL DATA\n')
	f.writelines(',sensitivity, specificity, PPV, NPV\n')
for cl in classes+['dermpath','genpath']:
	print('~~~~~~~~~~~~~~ALL DATA~~~~~~~~~~~~~~~~~~',)
	print(cl)
	print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~',)
	print('percentage of data with this classification:',(TP[cl]+FP[cl])/len(result_dict.keys()))
	if cl!='UNCERTAIN':
		sensitivity[cl]=TP[cl]/(TP[cl]+FN[cl])
		specificity[cl]=TN[cl]/(TN[cl]+FP[cl])
		PPV[cl]=TP[cl]/(TP[cl]+FP[cl])
		NPV[cl]=TN[cl]/(TN[cl]+FN[cl])
		print('PPV:', PPV[cl])
		print('NPV:', NPV[cl])
		print('Sensitivity:',sensitivity[cl])
		print('specificity:',specificity[cl])
		with open(output_file,'a') as f:
			f.writelines(cl +',' + str(sensitivity[cl]) +',' + str(specificity[cl]) +',' + str(PPV[cl]) +',' + str(NPV[cl]) +'\n')
	else:
		print('count:',FP[cl])
		#print('percentage:',FP[cl]/len(result_dict.keys()))


#compute ground truth distribution for ALL:
ground_truth_ALL=[]
for spec in result_dict.keys():
	ground_truth_ALL.append(result_dict[spec]['ground truth'])
total_specimens_ALL = float(len(result_dict.keys()))
ground_truth_perc_ALL={}
print('Ground Truth Class Percentages:')
for cl in ground_truth_classes:
	counts=ground_truth_ALL.count(cl)
	ground_truth_perc_ALL[cl]=counts/total_specimens_ALL
	print(cl,':',ground_truth_perc_ALL[cl])

###########################################
with open(output_file,'a') as f:
	f.writelines('--------------------------\n')
	f.writelines('Percentage of each class that goes to genpath vs dermpath\n')
	f.writelines('ground truth class, dermatopathologist, general pathologist\n')
with open(pie_output_file,'a') as f:
	f.writelines('counts for each GROUND TRUTH class\n')
#pie chart each ground truth class 
for cl in dermpath_classes[1:]+genpath_classes:
	if cl!='UNCERTAIN':
		with open(pie_output_file,'a') as f:
			f.writelines('-'+cl+'-\n')
		size_class=float(ground_truth_ALL.count(cl))
		preds = [result_dict[spec]['classification'] for spec in result_dict.keys() if result_dict[spec]['ground truth']==cl]
		percs=[]
		predicted_classes = []
		ct_dermpath=0.
		ct_genpath=0.
		for i in np.unique(preds):
			ct=preds.count(i)
			with open(pie_output_file,'a') as f:
				f.writelines(i+','+str(ct)+'\n')
			percs.append(ct/size_class)
			if i in dermpath_classes:
				ct_dermpath+=ct
			elif i in genpath_classes:
				ct_genpath+=ct
			predicted_classes.append(i)
		percs_derm_gen=[ct_dermpath/size_class,ct_genpath/size_class]
		figure = plt.figure()
		plt.pie(percs,labels=predicted_classes,autopct=lambda p: '{:.0f}%'.format(p))
		plt.title('Ground truth class = '+cl)
		with open(output_file,'a') as f:
			f.writelines(cl+','+str(percs_derm_gen[0])+','+str(percs_derm_gen[1])+'\n')
		figure = plt.figure()
		with open(pie_output_file,'a') as f:
			f.writelines('dermpath,'+str(ct_dermpath)+'\n')
			f.writelines('genpath,'+str(ct_genpath)+'\n')
		plt.pie(percs_derm_gen,labels=['dermatopathologist','general pathologist'],autopct=lambda p: '{:.0f}%'.format(p))
		plt.title('Ground truth class = '+cl)
		plt.show()



