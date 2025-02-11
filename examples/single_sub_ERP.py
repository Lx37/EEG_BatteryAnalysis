from getpass import getuser
import sys
import os
import mne
import numpy as np

user = getuser()  # Username of the user running the script
print('User is:', user)

if user == 'tkz':
    sys.path.append('/home/tkz/Projets/0_FPerrin_FFerre_2024_Baking_EEG_CAP/Baking_EEG')
if user == 'adminlocal':    
    sys.path.append('C:\\Users\\adminlocal\\Desktop\\ConnectDoc\\EEG_2025_CAP_FPerrin_Vera\\Baking_EEG')

from Baking_EEG import config as cfg
from Baking_EEG import utils
from Baking_EEG import _1_preprocess as prepro
from Baking_EEG import _2_cleaning as cleaning
from Baking_EEG import _3_epoch as epoch

######################################
############ Your part ! #############
######################################
# Indicate the protocol and subject you're working on + data directory and excel file with patients info
protocol = 'Resting'  # 'PP' or 'LG' or 'Resting' (TODO: 'Words' or 'Arythmetic')
sujet = 'AD94'

# Set the parameters for the preprocessing : save data or not, verbose or not, plot or not (True or False)
save = True
verbose = True
plot = True

if user == 'tkz':
    raw_data_dir = '/home/tkz/Projets/data/data_EEG_battery_2019-/'
    xls_patients_info = '/home/tkz/Projets/0_FPerrin_FFerre_2024_Baking_EEG_CAP/ConnectDoc_patients_df.csv'
    data_save_dir = '/home/tkz/Projets/0_FPerrin_FFerre_2024_Baking_EEG_CAP/Baking_EEG_data/'
elif user == 'adminlocal':
    raw_data_dir = 'C:\\Users\\adminlocal\\Desktop\\ConnectDoc\\Data\\data_EEG_battery_2019-\\'
    xls_patients_info = 'C:\\Users\\adminlocal\\Desktop\\ConnectDoc\\EEG_2025_CAP_FPerrin_Vera\\ConnectDoc_patients_df.csv'
    data_save_dir = 'C:\\Users\\adminlocal\\Desktop\\ConnectDoc\\EEG_2025_CAP_FPerrin_Vera\\Analysis_Baking_EEG_Vera\\'
elif user == 'tom':
    raw_data_dir = '/Users/tom/Desktop/ENSC/2A/PII/Tom/raw_eeg_data/'  
    xls_patients_info = '/Users/tom/Desktop/ENSC/2A/PII/Tom/raw_eeg_data/ConnectDoc_patients_df.csv'  
    data_save_dir = '/Users/tom/Desktop/ENSC/2A/PII/Tom/Baking_EEG_data/' 


############################################################################

## Start of the script

print('MNE VERSION : ', mne.__version__)

# create the patient_info object (with names, config, protocol, file name, bad channels, etc.)
patient_info = utils.create_patient_info(sujet, xls_patients_info, protocol, raw_data_dir, data_save_dir)
print('patient_info : ', patient_info)

data = []
epochs = []
epochs_TtP = []

# create the arborescence for required analysis
utils.create_arbo(protocol, patient_info, cfg)

''''''
print("################## Preprocessing data " + sujet + " ##################")

data = prepro.preprocess(patient_info, cfg, save, verbose, plot)

print("################## End of Preprocess ##################")

'''

'''

# Patch for data that have not been cutted around events [from Riham Analysis]
data_name = patient_info['data_save_dir'] + cfg.data_preproc_path
data_name = data_name + patient_info['ID_patient'] + '_' + patient_info['protocol'] + cfg.prefix_processed

data = mne.io.read_raw_fif(data_name, preload=True)

print('DATA : ')
print(data.info)

utils.cut_preprocessed_sig(data, patient_info, cfg)
'''

#'''

print("################## Cleaning data " + sujet + " ##################")

 

data_name = patient_info['data_save_dir'] + cfg.data_preproc_path
data_name = data_name + patient_info['ID_patient'] + '_' + patient_info['protocol'] + cfg.prefix_processed

data = mne.io.read_raw_fif(data_name, preload=True)
data = cleaning.correct_blink_ICA(data, patient_info, cfg, save=save, verbose=verbose, plot=plot) # to test, work, adjust threshold,..
#'''

'''
print("################## Epoching data " + sujet + " ##################")

data_name = patient_info['data_save_dir'] + cfg.data_preproc_path
data_name = data_name + patient_info['ID_patient'] + '_' + patient_info['protocol'] + cfg.prefix_processed #prefix_ICA  # cfg.prefix_processed

data = mne.io.read_raw_fif(data_name, preload=True)
data = epoch.get_ERP_epochs(data, patient_info, cfg, save=True, verbose=True, plot=True)

'''