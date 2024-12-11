


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
    'data_evoked_group_path' : 'PP_TpAP/data_evoked_group/',
    'plot_evoked_group_path' : 'PP_TpAP/plots/evoked_group/'
}

##Prefixes - how to name the data after each step
prefix_stimDict = '_event_id.npy'
prefix_processed = '_preproc.fif'
prefix_epochs_PPAP = '_PP-epo.fif'
prefix_ICA = '_preproc_ICA.fif'
prefix_noICA = '_preproc_noICA.fif'
prefix_autoreject = '_ar.fif'
prefix_ave = '-erp.fif'
prefix_grandaverage = 'GrandAverage'
prefix_evoked_group = '_evoked_group.fif'

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

###################################################
######### Configuration for cleaning (ICA) ########

minBlinksICA = 100  #300 for protocol PP Lizette
eog_threshold = 3
# For ICA
n_components = 20 #0.99 from Fabrice  # (instead of 0.95) if float, select n_components by explained variance of PCA
method = 'fastica'  # for comparison with EEGLAB try "extended-infomax" here
decim = 2  # we need sufficient statistics, not all time points -> saves time
random_state = 23
ica_reject = None


###################################################
##############  Configuration for ERP  ############

#erp_reject = {'eeg': 100e-6, 'eog': 200e-6}