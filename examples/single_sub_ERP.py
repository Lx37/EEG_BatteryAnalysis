import sys
sys.path.append('/home/tkz/Projets/FPerrin_FFerre_2024_BatteryAnalyseEEG_CAP/BatteryAnalyseEEG')
import os
import mne
from getpass import getuser

#from batteryEEG import get_infos_patients
from batteryEEG import preprocessFAB as preprocess
from batteryEEG import utils
from batteryEEG import config as cfg

######################################
############ Your part ! #############
######################################
# Indicate the protocol and subject you're working on + data directory and excel file with patients info
protocol = 'PP' # 'PP' or 'LG' or 'Words' or 'Arythmetic' or 'Resting'
sujet = 'AD94'
# Set the parameters for the preprocessing : save data or not, verbose or not, plot or not (True or False)
save = True
verbose = True
plot = False #True

user = getuser()  # Username of the user running the scripts

if user == 'tkz':
    # where the data are stored
    raw_data_dir = '/home/tkz/Projets/data/data_EEG_battery_2019-/'
    # excel file with all patients info
    xls_patients_info = '/home/tkz/Projets/FPerrin_FFerre_2024_BatteryAnalyseEEG_CAP/ConnectDoc_patients_df.csv'
    # path to save the analyzed data
    data_save_dir = '/home/tkz/Projets/FPerrin_FFerre_2024_BatteryAnalyseEEG_CAP/Battery_Analysis/'


######################################
######################################

## Start of the script

print('MNE VERSION : ', mne.__version__)

# create the patient_info object (with names, config, protocol, file name, bad channels, etc.)
patient_info = utils.create_patient_info(sujet, xls_patients_info, protocol, raw_data_dir, data_save_dir)

data = []
epochs = []
epochs_TtP = []

# create the arborescence for required analysis
utils.create_arbo(protocol, patient_info, cfg)

print("################## Preprocessing data " + sujet + " ##################")

if patient_info['data_fname'].endswith('.mff'): # EGI .mff raw data format
    data = preprocess.preprocess_mff(patient_info, cfg, save, verbose, plot)
#else:
#   mircromed #TODO : update script for micromed
#   data = preprocess.preprocess_mircomed(cfg, data_fname, sujet, bad_sub_chan, save, verbose, plot)