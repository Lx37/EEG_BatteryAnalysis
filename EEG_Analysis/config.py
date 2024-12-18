


###################################################
###### File names organisation and prefixes ######

# folder to store the data for preprocessing
#data_preproc_path = 'data_preproc/'

##folders to store the data for PP analysis
all_folders_PP = {
    #'data_Subject_Dir' : 'data_EEG/',
    'data_preproc_path' : 'data_preproc/',
    'stimDict_path' : 'PP/data_stimdict/',
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

##Prefixes - how to name the data after each step
prefix_stimDict = '_event_id.npy'
prefix_processed = '_preproc.fif'
prefix_epochs_PPAP = '_PP-epo.fif'
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

highpass = 0.1 ## TODOLX was 0.5 for Fabrice
highcut = 45 # TODOLX was 25 for Fabrice

# DownSampling to
sfreq = 250

###################################################
######### Configuration for cleaning (ICA) ########

minBlinksICA = 100  #300 for protocol PP Lizette
eog_threshold = 3
# For ICA
n_components = 0.95 #20 #0.99 from Fabrice  # (instead of 0.95) if float, select n_components by explained variance of PCA
method = 'fastica'  # for comparison with EEGLAB try "extended-infomax" here
decim = 2  # we need sufficient statistics, not all time points -> saves time
random_state = 23
ica_reject = None


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


###################################################
#########  Configuration for connectivity  ########

epochs_reject_con = None 
                    #dict(eeg=200e-6,      # unit: V (EEG channels)
                    #eog=250e-6      # unit: V (EOG channels)
                    #)