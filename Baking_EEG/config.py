


###################################################
###### File names organisation and prefixes ######

# folder to store the data for preprocessing
data_preproc_path = 'data_preproc/'
stimDict_path = 'data_stimdict/'
data_con_path = 'data_connectivity/'
result_con_path = 'connectivity/'
data_epochs_path = 'data_epochs/'
result_con_path_BRU = 'connectivity/'

##folders to store the data for PP analysis
all_folders_PP = {
    #'data_Subject_Dir' : 'data_EEG/',
    #'data_preproc_path' : 'data_preproc/',
    #'stimDict_path' : 'PP/data_stimdict/',
    'data_epochs_path' : 'PP/data_epochs/',
    'data_evoked_path' : 'PP/data_evoked/',
    'plot_topo_path' : 'PP/plots/Topomap/',
    'plot_erp_path' : 'PP/plots/ERP/',
    'plot_stats_path' : 'PP/plots/stats/',
    'data_stats_path' : 'PP/stats/',
    'text_stats_path' : 'PP/stats/',
    'cleaning_path' : 'PP/plots/cleaning/',
    'data_grandaverage_path' : 'PP/data_grandaverage/',
    'plot_grandaverage_path' : 'PP/plots/grandaverage/',
    'plot_GFP_path' : 'PP/plots/GFP/',
    'data_evoked_group_path' : 'PP/data_evoked_group/',
    'plot_evoked_group_path' : 'PP/evoked_group/'
}

all_folders_LG = {key: value.replace('PP', 'LG') for key, value in all_folders_PP.items()}
all_folders_Resting = {key: value.replace('PP', 'Resting') for key, value in all_folders_PP.items()}


##Prefixes - how to name the data after each step
prefix_stimDict = '_event_id.npy'
prefix_processed = '_preproc.fif'
prefix_epochs_PPAP = '_PP-epo.fif'
prefix_epochs_BRU = '-epo10s_new.fif'
prefix_ICA = '_preproc_ICA.fif'
prefix_noICA = '_preproc_noICA.fif'
prefix_epo_conn = '_epo_conn.fif'
#prefix_autoreject = '_ar.fif'
#prefix_ave = '-erp.fif'
#prefix_grandaverage = 'GrandAverage'
#prefix_evoked_group = '_evoked_group.fif'

###################################################
##################################################
######### Configuration for preprocessing ########

# EGI system : chan coordinates are loaded with name 'EEG 001', 'EEG 002',...
# so MNE 1.0.0 doesn't found them in the digmontage
# this list is use to set same names
EGI_chan_names = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10',
                'E11', 'E12', 'E13', 'E14', 'E15', 'E16', 'E17', 'E18', 'E19', 'E20',
                'E21', 'E22', 'E23', 'E24', 'E25', 'E26', 'E27', 'E28', 'E29', 'E30',
                'E31', 'E32', 'E33', 'E34', 'E35', 'E36', 'E37', 'E38', 'E39', 'E40',
                'E41', 'E42', 'E43', 'E44', 'E45', 'E46', 'E47', 'E48', 'E49', 'E50',
                'E51', 'E52', 'E53', 'E54', 'E55', 'E56', 'E57', 'E58', 'E59', 'E60',
                'E61', 'E62', 'E63', 'E64', 'E65', 'E66', 'E67', 'E68', 'E69', 'E70',
                'E71', 'E72', 'E73', 'E74', 'E75', 'E76', 'E77', 'E78', 'E79', 'E80',
                'E81', 'E82', 'E83', 'E84', 'E85', 'E86', 'E87', 'E88', 'E89', 'E90',
                'E91', 'E92', 'E93', 'E94', 'E95', 'E96', 'E97', 'E98', 'E99', 'E100',
                'E101', 'E102', 'E103', 'E104', 'E105', 'E106', 'E107', 'E108', 'E109', 'E110',
                'E111', 'E112', 'E113', 'E114', 'E115', 'E116', 'E117', 'E118', 'E119', 'E120',
                'E121', 'E122', 'E123', 'E124', 'E125', 'E126', 'E127', 'E128', 'VREF'] #E129

EGI_chan_names_BRU = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10',
                'E11', 'E12', 'E13', 'E14', 'E15', 'E16', 'E17', 'E18', 'E19', 'E20',
                'E21', 'E22', 'E23', 'E24', 'E25', 'E26', 'E27', 'E28', 'E29', 'E30',
                'E31', 'E32', 'E33', 'E34', 'E35', 'E36', 'E37', 'E38', 'E39', 'E40',
                'E41', 'E42', 'E43', 'E44', 'E45', 'E46', 'E47', 'E49', 'E50',
                'E51', 'E52', 'E53', 'E54', 'E55', 'E56', 'E57', 'E58', 'E59', 'E60',
                'E61', 'E62', 'E63', 'E64', 'E65', 'E66', 'E67', 'E68', 'E69', 'E70',
                'E71', 'E72', 'E73', 'E74', 'E75', 'E76', 'E77', 'E78', 'E79', 'E80',
                'E81', 'E82', 'E83', 'E84', 'E85', 'E86', 'E87', 'E88', 'E89', 'E90',
                'E91', 'E92', 'E93', 'E94', 'E95', 'E96', 'E97', 'E98', 'E99', 'E100',
                'E101', 'E102', 'E103', 'E104', 'E105', 'E106', 'E107', 'E108', 'E109', 'E110',
                'E111', 'E112', 'E113', 'E114', 'E115', 'E116', 'E117', 'E118', 'E120',
                'E121', 'E122', 'E123', 'E124', 'E129', 'ECG']

EGI_misc_dict = {'E8':'misc','E25':'misc','E17':'misc','E126':'misc','E127':'misc'}
EGI_misc_dict_BRU = {'E125':'misc','E126':'misc','E127':'misc','E128':'misc', 'E119':'misc', 'E48':'misc', 'ECG':'misc'}

#VEOG = veog1 - veog
occular_EGI = {'veog1':'E25', 'veog2':'E127', 'veogr1':'E8', 'veogr2':'E126', 'heog1':'E32', 'heog2':'E1'}
#occular_Gtec = ?? {'veog1':'E25', 'veog2':'E127', 'veogr1':'E8', 'veogr2':'E126', 'heog1':'E32', 'heog2':'E1'}

GTec_mapping = {'EEG 001':'FP1', 'EEG 002':'FP2', 'EEG 003':'AF7', 'EEG 004':'AF8', 'EEG 005':'F3',
                'EEG 006':'Fz', 'EEG 007':'F4', 'EEG 008':'FT7', 'EEG 009':'FT8', 'EEG 010':'FC5', 
                'EEG 011':'C3', 'EEG 012':'C4', 'EEG 013':'FC6', 'EEG 014':'C5', 'EEG 015':'C1',
                'EEG 016':'Cz', 'EEG 017':'C2', 'EEG 018':'C6', 'EEG 019':'CP3', 'EEG 020':'CP4',
                'EEG 021':'CP1', 'EEG 022':'CP2', 'EEG 023':'P7', 'EEG 024':'P3', 'EEG 025':'Pz',
                'EEG 026':'P4', 'EEG 027':'P8', 'EEG 028':'PO7', 'EEG 029':'PO3', 'EEG 030':'PO4',
                'EEG 031':'PO8', 'EEG 032':'Oz'}

###MAPPING FOR BRU###

mapping_type_che = {'D255': 'misc', 'DIN4': 'misc', 'DI75': 'misc', 'DI77': 'misc', 'DI79': 'misc',
  'DI65': 'misc', 'DI67': 'misc', 'DI69': 'misc', 'DI66': 'misc', 'DI68': 'misc',
  'DI70': 'misc', 'STI 014': 'stim', 'ECG': 'ecg', 'EMG': 'emg'}

mapping_type_tai = {
  'DI65': 'misc', 'DI67': 'misc', 'DI69': 'misc', 'DI66': 'misc', 'DI68': 'misc',
  'DI70': 'misc', 'STI 014': 'stim', 'ECG': 'ecg', 'EMG': 'emg'}

mapping_type = {'DI75': 'misc', 'DI77': 'misc', 'DI79': 'misc',
  'DI65': 'misc', 'DI67': 'misc', 'DI69': 'misc', 'DI66': 'misc', 'DI68': 'misc',
  'DI70': 'misc', 'STI 014': 'stim', 'ECG': 'ecg', 'EMG': 'emg'}

highpass = 0.1 ## TODOLX was 0.5 for Fabrice
highcut = 45 # TODOLX was 25 for Fabrice

highpass_BRU = 1
highcut_BRU = 30

# DownSampling to
sfreq = 250

###################################################
######### Configuration for cleaning (ICA) ########

minBlinksICA = 100  #300 for protocol PP Lizette
eog_threshold = 3
# For ICA
n_components = 0.95 #15 was ok #0.99 from Fabrice  # (instead of 0.95) if float, select n_components by explained variance of PCA
method = 'fastica'  # for comparison with EEGLAB try "extended-infomax" here
decim = 2  # we need sufficient statistics, not all time points -> saves time
random_state = 23
ica_reject = None

######## For ICA - BRU #########
# For blink detection (could be a dict if different params by subjects)
eeg_for_eog = ['E25'] # No EOG for Bruno so we take some EEG
blink_detect_th =0.00005  #seuil pour détection des blinks

minBlinksICA = 150
eog_threshold = 3

n_components = 0.95  # if float, select n_components by explained variance of PCA
method = 'fastica'  # for comparison with EEGLAB try "extended-infomax" here
decim = 2  # we need sufficient statistics, not all time points -> saves time
random_state = 23
ica_reject = None
erp_reject = {'eeg': 100e-6, 'eog': 200e-6}

###################################################
##############  Configuration for ERP  ############

#erp_reject = {'eeg': 100e-6, 'eog': 200e-6}

#for epoching [Fabrice PP / Word]
erp_window_tmin = -0.2
erp_window_tmax = 1
erp_baseline = (None, 0) # from first instance to t=0
erp_detrend = None # Either 0 or 1, the order of the detrending. 0 is a constant (DC) detrend, 1 is a linear detrend.
erp_topo = True

# Specific PP
events_id_PP = { 'PP/10': 110,'PP/20': 120,'PP/30': 130, 'AP/11': 111, 'AP/12': 112, 'AP/13': 113, 'AP/14': 114, 'AP/15': 115, 'AP/16': 116,
'AP/21': 121, 'AP/22': 122, 'AP/23': 123, 'AP/24': 124, 'AP/25': 125, 'AP/26': 126,
'AP/31': 131, 'AP/32': 132, 'AP/33': 133, 'AP/34': 134, 'AP/35': 135, 'AP/36': 136 } #'AP/22': 108, 'AP/12': 4 pour TpJC5 qui a 2 triggers en trop (22 et 23 devenus 4 et 108)

epochs_reject_PP = dict(eeg= 150e-6, eog=150e-6)

# Specific Words
events_id_Words = {'TW/C/1': 2,'TW/C/2': 3,'TW/C/3': 4,'TW/C/4': 5, 'TW/C/5': 6, 'TW/C/6': 7, 'TW/C/7': 8, 'TW/C/8': 9, 'TW/C/9': 10, 'TW/C/10': 11, 'TW/C/11': 12, 'TW/C/12': 13, 'TW/C/13': 14, 'TW/C/14': 15, 'TW/C/15': 16, 'TW/C/16': 17, 'TW/C/17': 18, 'TW/C/18': 19, 'TW/C/19': 20, 'TW/C/20': 21, 'TW/C/21': 22, 'TW/C/22': 23, 'TW/C/23': 24,'TW/C/24': 25, 'TW/C/25': 26, 'TW/C/26': 27, 'TW/C/27': 28, 'TW/C/28': 29, 'TW/C/29': 30, 'TW/C/30': 31, 'TW/C/31': 32, 'TW/C/32': 33, 'TW/C/33': 34, 'TW/C/34': 35,'TW/C/35': 36, 'TW/C/36': 37, 'TW/C/37': 38, 'TW/C/38': 39, 'TW/C/39': 40, 'TW/C/40': 41, 'TW/C/41': 42, 'TW/C/42': 43, 'TW/C/43': 44, 'TW/C/44': 45, 'TW/C/45': 46, 'TW/C/46': 47, 'TW/C/47': 48, 'TW/C/48': 49, 'TW/C/49': 50, 'TW/C/50': 51, 'TW/C/51': 52, 'TW/C/52': 53, 'TW/C/53': 54, 'TW/C/54': 55, 'TW/C/55': 56, 'TW/C/56': 57, 'TW/C/57': 58, 'TW/C/58': 59, 'TW/C/59': 60, 'TW/C/60': 61, 'TW/C/61': 62, 'TW/C/62': 63, 'TW/C/63': 64, 'TW/C/64': 65, 'TW/C/65': 66, 'TW/C/66': 67, 'TW/C/67': 68, 'TW/C/68': 69, 'TW/C/69': 70, 'TW/C/70': 71, 'TW/C/71': 72, 'TW/C/72': 73, 'TW/C/73': 74, 'TW/C/74': 75, 'TW/C/75': 76, 'TW/C/76': 77, 'TW/C/77': 78, 'TW/C/78': 79, 'TW/C/79': 80, 'TW/C/80': 81,
'TW/I/1': 101, 'TW/I/2': 102,'TW/I/3': 103,'TW/I/4': 104, 'TW/I/5': 105, 'TW/I/6': 106, 'TW/I/7': 107, 'TW/I/8': 108, 'TW/I/9': 109, 'TW/I/10': 110, 'TW/I/11': 111, 'TW/I/12': 112, 'TW/I/13': 113, 'TW/I/14': 114, 'TW/I/15': 115, 'TW/I/16': 116, 'TW/I/17': 117, 'TW/I/18': 118, 'TW/I/19': 119, 'TW/I/20': 120, 'TW/I/21': 121, 'TW/I/22': 122, 'TW/I/23': 123, 'TW/I/24': 124, 'TW/I/25': 125, 'TW/I/26': 126, 'TW/I/27': 127, 'TW/I/28': 128, 'TW/I/29': 129, 'TW/I/30': 130, 'TW/I/31': 131, 'TW/I/32': 132, 'TW/I/33': 133, 'TW/I/34': 134, 'TW/I/35': 135, 'TW/I/36': 136, 'TW/I/37': 137, 'TW/I/38': 138, 'TW/I/39': 139, 'TW/I/40': 140, 'TW/I/41': 141, 'TW/I/42': 142, 'TW/I/43': 143, 'TW/I/44': 144, 'TW/I/45': 145, 'TW/I/46': 146, 'TW/I/47': 147, 'TW/I/48': 148, 'TW/I/49': 149, 'TW/I/50': 150, 'TW/I/51': 151, 'TW/I/52': 152, 'TW/I/53': 153, 'TW/I/54': 154, 'TW/I/55': 155, 'TW/I/56': 156, 'TW/I/57': 157, 'TW/I/58': 158, 'TW/I/59': 159, 'TW/I/60': 160, 'TW/I/61': 161, 'TW/I/62': 162, 'TW/I/63': 163, 'TW/I/64': 164, 'TW/I/65': 165, 'TW/I/66': 166, 'TW/I/67': 167, 'TW/I/68': 168, 'TW/I/69': 169, 'TW/I/70': 170, 'TW/I/71': 171, 'TW/I/72': 172, 'TW/I/73': 173, 'TW/I/74': 174, 'TW/I/75': 175, 'TW/I/76': 176, 'TW/I/77': 177, 'TW/I/78': 178, 'TW/I/79': 179, 'TW/I/80': 180,
'TPW': 201, 'PPW': 200, 'PC': 1, 'PI': 100}



epochs_reject_Words = None #dict(eeg= 150e-6, eog=150e-6)

####EPOCHING BRU####

goodttrigs = [65, 66, 67, 68, 69, 70]
nb_trig2add = 5             #59
size_win = 10 # en secondes  #1

#for epoching
# Initial rejection setting
epochs_reject=dict(eeg= 300e-6)
erp_window_tmin = 0
erp_window_tmax = size_win
erp_baseline = None # from first instance to t=0
erp_detrend = None # Either 0 or 1, the order of the detrending. 0 is a constant (DC) detrend, 1 is a linear detrend.
erp_topo = True

events_id_BRU = {'Music': 65, 'Noise':66, 'Rest after Music':67, 'Rest after noise':68,
                 'Interact music': 69, 'Interact noise':70}

###################################################
#########  Configuration for connectivity  ########

# Connectivity epoching
epochs_reject_con = dict(eeg=1000e-6)      # unit: V (EEG channels)
#epochs_reject_con = None

# Connectivity parameters for computation                  
con_freq_bands = {"delta": [0.5, 4.0],
                "theta": [4.0, 8.0],
                "alpha": [8.0, 13.0],
                "beta": [13.0, 30.0],
                "sigma": [30.0, 40.0],}
#fmin = 4
#fmax = 8
con_tmin = 0.0  # exclude the baseline period
con_method = 'wpli2_debiased'

con_vmin = 0
con_vmax = 1

con_event_ids_BRU = ['Music', 'Noise', 'Rest after Music', 'Rest after noise', 'Interact music', 'Interact noise']
con_event_ids = ['303']   

con_all_ROI_chan = {
    'ROI_Frontal' : ['E22', 'E15', 'E9', 'E18', 'E16', 'E10', 'E19', 'E11', 'E4', 'E12', 'E5'], #E17, E21, E14
    'ROI_Frontal_droit' : ['E2', 'E3', 'E123', 'E124', 'E122', 'E118', 'E117', 'E116'],  #121 E8, E1
    'ROI_Frontal_gauche' : ['E26', 'E23', 'E27', 'E24', 'E33', 'E34', 'E28', 'E20'], #E38
    'ROI_Central' :  ['E6', 'E13', 'E112', 'E30', 'E7', 'E106', 'E105', 'E31', 'E37', 'E80', 'E87', 'E79', 'E54', 'E55'], #Remis CZ (nommé 'VREF', position 128) E128
    'ROI_Temporal_droit' : ['E110', 'E111', 'E115', 'E109', 'E104', 'E103', 'E108', 'E93', 'E98', 'E102'], #E114
    'ROI_Temporal_gauche' :  ['E39', 'E35', 'E29', 'E40', 'E41', 'E36', 'E45', 'E46', 'E47', 'E42'], #E44
    'ROI_Parietal' : ['E61', 'E62', 'E78', 'E67', 'E72', 'E77', 'E71', 'E76', 'E70', 'E75', 'E83'], #E74, E82
    'ROI_Occipito_temporal_droit' : ['E50', 'E51', 'E52', 'E53', 'E58', 'E59', 'E60', 'E65', 'E66'], #E57, E64, E69
    'ROI_Occipito_temporal_gauche' : ['E86', 'E92', 'E97', 'E101', 'E85', 'E91', 'E96', 'E84', 'E90'] #E100, E95, E89
}

con_all_ROI_chan_BRU = {
    'lFP': ['E32', 'E25', 'E26', 'E22', 'E21', 'E17'],
    'rFP': ['E15', 'E14', 'E9', 'E8', 'E1', 'E2'],
    'lF': ['E38', 'E39', 'E33', 'E34', 'E35', 'E27', 'E28', 'E29', 'E23', 'E24', 'E20', 'E13', 'E18', 'E19', 'E12',
           'E16'],
    'rF': ['E11', 'E10', 'E4', 'E5', 'E112', 'E118', 'E3', 'E124', 'E123', 'E117', 'E111', 'E110', 'E116', 'E122',
           'E121', 'E115'],
    'Ce': ['E40', 'E41', 'E36', 'E30', 'E37', 'E31', 'E7', 'E6', 'E106', 'E55', 'E80', 'E105', 'E87', 'E104',
           'E103', 'E109'],
    'lT': ['E43', 'E44', 'E49', 'E45', 'E50', 'E56', 'E57', 'E58', 'E63', 'E64'],
    'rT': ['E120', 'E114', 'E113', 'E108', 'E101', 'E100', 'E107', 'E96', 'E99', 'E95'],
    'lP': ['E46', 'E51', 'E47', 'E42', 'E52', 'E59', 'E60', 'E53', 'E54', 'E61', 'E67', 'E71', 'E66', 'E62'],
    'rP': ['E72', 'E76', 'E77', 'E78', 'E79', 'E84', 'E85', 'E86', 'E93', 'E92', 'E91', 'E98', 'E97', 'E102'],
    'Oc': ['E68', 'E65', 'E69', 'E73', 'E70', 'E74', 'E75', 'E81', 'E82', 'E83', 'E90', 'E89', 'E88', 'E94']
}

EGI_con_chan =  [x for x in EGI_chan_names if x not in EGI_misc_dict.keys()] # All chan - those declared as misc
EGI_con_chan_BRU =  [x for x in EGI_chan_names_BRU if x not in EGI_misc_dict_BRU.keys()] # All chan - those declared as misc
