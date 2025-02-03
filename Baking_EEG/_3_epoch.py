import mne
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


## logging info ###
import logging
from datetime import datetime


logname = './logs/'+ datetime.now().strftime('log_%Y-%m-%d.log')
logging.basicConfig(filename=logname,level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)


# From Fabrice code
def get_ERP_epochs(data, patient_info, cfg, save=True, verbose=True, plot=True):

    # if patient_info['protocol'] == 'WORDS':
    #     import config_WORDS as cfg

    # if protocol == 'PP':
    #     import config_PP as cfg

    SubName = patient_info['ID_patient']

    ########### Renaming of EGI-loaded triggers  ###########
    
    if patient_info['EEG_system'] == 'EGI':
        
        StimNpy = patient_info['data_save_dir'] + cfg.stimDict_path + SubName + '_' + patient_info['protocol'] + cfg.prefix_stimDict
        print(StimNpy)
        translate_dict = np.load(StimNpy, allow_pickle=True).item()

        events = mne.find_events(data, stim_channel='STI 014')
        print('Events BEFORE first changes : ', events)
        print('translate_dict : ', translate_dict)
        #eventplot = mne.viz.plot_events(events, data.info['sfreq'])

        new_dict = {}
        new_events = events.copy()
        for key, value in translate_dict.items():
            if key != 'Rest' and key != 'Code' and key != 'rest' and key != 'star' and key != 'IEND':
                new_key = ''.join(x for x in key if x.isdigit())
                #new_key = int(new_key) # retire or ...
            else:
                new_key = key
            new_dict[new_key] = value
        print('new_dict : ', new_dict)

        for (x,y), value in np.ndenumerate(events):
            if y==2:
                new_value = [k for k,v in new_dict.items() if v==value][0] #corect here because one key is associated to one value. better to use inverse dict ?
                if new_value != 'IEND' and new_value  != 'rest' and new_value != 'Code' and new_value != 'Rest' and new_value != 'star':
                    new_events[x,y] = new_value

        if verbose:
            print('Events AFTER changes : ', new_events)
        if plot:
            eventplot = mne.viz.plot_events(new_events, data.info['sfreq'])


    ########### Segmetation and rejection ###########
    tmin, tmax = cfg.erp_window_tmin, cfg.erp_window_tmax
    baseline = cfg.erp_baseline
    detrend = cfg.erp_detrend # Either 0 or 1, the order of the detrending. 0 is a constant (DC) detrend, 1 is a linear detrend.

    if patient_info['protocol'] == 'PP':
        events_id = cfg.events_id_PP
        epochs_reject = cfg.epochs_reject_PP
        
    elif patient_info['protocol'] == 'WORDS':
        events_id = cfg.events_id_WORDS
        epochs_reject = cfg.epochs_reject_WORDS
    
    
    #TODO other protocols
    


    picks_eeg_eog = mne.pick_types(data.info, eeg=True, eog=True, exclude=[]) #eeg and eog chan for rejection
    #picks_eeg_eog = mne.pick_types(data.info, eeg=True, eog=True, selection =['Cz', 'E55', 'E62', 'E106', 'E7', 'E80', 'E31', 'E79', 'E54', 'E61', 'E78']) #FOR PATIENT TpTP
    epochs = mne.Epochs(data, events=new_events, event_id=events_id, tmin=tmin, tmax=tmax,
                        baseline=baseline, detrend=detrend, picks=picks_eeg_eog, on_missing='warn',
                        reject=epochs_reject, preload=True)
    if verbose:
        print('epochs : ', epochs.info)
        print('Number of events :', new_events.size/3)
        #print('Number of redefined events :', events_redef_equal.size)
        print('Number of epochs :', len(epochs))


    if plot:
        epochs.plot_drop_log(subject=SubName)
        epochs.plot(title=SubName, show=True, block=True, scalings=dict(eeg=50e-6, eog=100e-6))  # Here it's possible to click on event to reject
        #epochs["TW/Congurent"].average().plot()
        #epochs["TW/Incongruent"].average().plot()
        #epochs["TPW"].average().plot()


    logger.info('Number of events : ,%s', events.size)
    logger.info('Number of events : ,%s', events.size)
    #gger.info('Number of redefined events :,%s', events_redef_equal.size)
    logger.info('Number of epochs :,%s', len(epochs))
    
    if save:
        if patient_info['protocol'] == 'PP':
            epochs_name = patient_info['data_save_dir'] + cfg.all_folders_PP['data_epochs_path']
        elif patient_info['protocol'] == 'LG':
            epochs_name = patient_info['data_save_dir'] + cfg.all_folders_LG['data_epochs_path']
        elif patient_info['protocol'] == 'Resting':
            epochs_name = patient_info['data_save_dir'] + cfg.all_folders_Resting['data_epochs_path']
        epochs_name = epochs_name + patient_info['ID_patient'] + '_' + patient_info['protocol'] + cfg.prefix_epo_conn
        print("Saving data : " + epochs_name)
        
        #epochs_name = cfg.data_epochs_path + data.info['subject_info']['his_id'] + '_' + proto + cfg.prefix_epoched
        #print("Saving data : " + epochs_name)
        epochs.save(epochs_name, overwrite=True)

    return epochs



# From Riham epoching code -> connectivity epochs
def get_epochs_connectivity(data, sub, proto, data_save_dir, cfg, save=True, verbose=True, plot=True):
    
    #SubName = patient_info['ID_patient']
    #proto = patient_info['protocol']

    assert data.info['sfreq'] == cfg.sfreq, 'Pbl Fréquences d"echantillonnage !!'

    # Define new trigs: 60 event of 10s = 10 min, from first trig or first 1min
    event_id = 303
    nb_event = 60
    size_epoch_s = 10

    if proto == 'PP' or proto == 'LG':
        data_events = mne.find_events(data, stim_channel='STI 014')
        onset_init = data_events[0][0]
    elif proto == 'Resting':  # pas de trig dans ce proto
        onset_init = cfg.sfreq*60
    else:
        print('Error on the protocol name - can"t find it')
        return
    onsets = np.arange(start=onset_init, stop=onset_init+(nb_event*cfg.sfreq*size_epoch_s), step=cfg.sfreq*size_epoch_s, dtype='int64') 
    events = np.vstack((onsets, np.ones(nb_event, int), event_id * np.ones(nb_event, int))).T   # event : (times, durations, codes)

    print('New Events: ', events)
    print(data)
    #eventplot = mne.viz.plot_events(events, data.info['sfreq'])
    #plt.show()


    ########### Segmetation and rejection ###########
   
    tmin, tmax = 0, size_epoch_s

    picks_eeg = mne.pick_types(data.info, eeg=True, exclude=[]) #eeg and eog chan for rejection
    epochs = mne.Epochs(data, events=events, event_id=event_id, tmin=tmin, tmax=tmax, #new_events
                        baseline = (None, None), picks=picks_eeg, reject=cfg.epochs_reject_con, preload=True,
                        detrend=1, reject_by_annotation=False)
    if verbose:
        print('epochs : ', epochs.info)
        #print('Number of events :', new_events.size)
        print('Number of epochs :', len(epochs))

    if plot:
        #epochs.plot_drop_log(subject=SubName)
        epochs.plot(title= sub + " " + proto + ' - Click to manually reject event if needed', show=True, block=True, scalings=dict(eeg=200e-6, eog=100e-6))  # Here it's possible to click on event to reject

    logger.info('Number of events : ,%s', events.size)
    logger.info('Number of events : ,%s', events.size)
    logger.info('Number of epochs :,%s', len(epochs))
    
    if save:
        epochs_name = data_save_dir + cfg.data_con_path
        epochs_name = epochs_name + sub + '_' + proto + cfg.prefix_epo_conn
        print("Saving data : " + epochs_name)
        
        #epochs_name = cfg.data_epochs_path + data.info['subject_info']['his_id'] + '_' + proto + cfg.prefix_epoched
        #print("Saving data : " + epochs_name)
        epochs.save(epochs_name, overwrite=True)

    return epochs
    
