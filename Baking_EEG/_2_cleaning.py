import mne
import numpy as np
import matplotlib.pyplot as plt
import os

from mne.preprocessing import ICA
from autoreject import get_rejection_threshold
from autoreject import (AutoReject, set_matplotlib_defaults)

## logging info ###
import logging
from datetime import datetime

#logname = '/home/lizette/Projets/GIT_LAB/coma_stuff/logs/' + datetime.now().strftime('log_%Y-%m-%d.log')
logname = './logs/' + datetime.now().strftime('log_%Y-%m-%d.log')
logging.basicConfig(filename=logname,level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)


def correct_blink_ICA(data, patient_info, cfg, save=False, verbose=True, plot=True):
    '''
    This function tries to removes blink artefacts from preprocessed data.
    Indeed, data needs to be clean and cut to relevant to improve the removal.
    the method used is based on ICA projection where we remove the blink composante.
    All the difficulty is to get the purest blink composant !
    This is a first working version - feel free to improve it !
    '''

    picks_eog = mne.pick_types(data.info, eog=True)
    datacopy = data.copy()
    datacopy.filter(1, 10, n_jobs=1, l_trans_bandwidth='auto', h_trans_bandwidth='auto',
    			 picks=picks_eog, filter_length='auto', phase='zero-double')

    eog_id = 0
    eog_events = mne.preprocessing.find_eog_events(datacopy, eog_id, ch_name='VEOGL',verbose = 'DEBUG')
    average_eog = mne.preprocessing.create_eog_epochs(datacopy).average()
    n_blinks = len(eog_events)

    if verbose:
        print('Nb blink found : ', n_blinks)

    if plot:
        data.plot(events=eog_events, title='Show EOG artifacts detection')
        average_eog.plot_joint()

    logger.info('Nb blink found : ,%s', n_blinks)

    ################ ICA correction ##################
    if n_blinks >cfg.minBlinksICA:
        logger.info('Too many blinks ICA performed')
        ica = ICA(n_components=cfg.n_components,method=cfg.method, random_state=cfg.random_state)#, fit_params=dict(extended=True)
        #ica = ICA(n_components=None,method=cfg.method, random_state=cfg.random_state)#, fit_params=dict(extended=True)
        #print(ica)

        picks = mne.pick_types(datacopy.info, meg=False, eeg=True, eog=False, stim=False, exclude='bads')


        ###Autorejection (global)###
        #ICA solutions can be affected by high amplitude artifacts, therefore we recommend to determine
        # a reasonable rejection threshold on which data segments to ignore in the ICA. autoreject (global)
        # can be used exactly for this purpose
        #In case you want to fit your ICA on the raw data, you will need an intermediate step, because autoreject only works on epoched data.
        # ICA is ignoring the time domain of the data, so we can simply turn the raw data into equally spaced “fixed length” epochs using ::func::mne.make_fixed_length_events:
        #tstep = 1.0
        ##autorejectEvents = mne.make_fixed_length_events(datacopy, duration=tstep)
        #autorejectEpochs = mne.Epochs(datacopy, autorejectEvents, tmin=0.0, tmax=tstep,baseline=(0, 0))
        #AutorejectGlobal = get_rejection_threshold(autorejectEpochs)
        #print(' AutorejectGlobal : ' , AutorejectGlobal)

        ica.fit(datacopy, picks=picks)#, reject=AutorejectGlobal, tstep=tstep) #decim=cfg.decim,
        if verbose:
            print(ica)
        if plot:
            ica.plot_components()
        logger.info('ICA info = ,%s', ica)

        #eog_epochs =  mne.preprocessing.create_eog_epochs(datacopy, reject=AutorejectGlobal)
        eog_inds, scores = ica.find_bads_eog(datacopy, threshold=3) #ch_name='VEOGL' ??

        if verbose:
            print("eog_inds : ", eog_inds)
            print("scores : ", scores)
        logger.info("eog_inds : ,%s", eog_inds)

        if not eog_inds:
            print("No eog_inds, need to choose manually")
            ica.plot_sources(datacopy, block=True)
            #eog_inds = ica.exclude
            #print("eog_inds chosen manually: ", eog_inds)
        elif eog_inds:
            #ica.plot_components()
            if plot:
                ica.plot_scores(scores, exclude=eog_inds)
                ica.plot_sources(average_eog)#, exclude=eog_inds)
                title = 'Sources related to %s artifacts (red)'
                ica.plot_properties(datacopy, picks=eog_inds, psd_args={'fmax': 35.},
                                image_args={'sigma': 1.})


        ica.exclude.extend(eog_inds)
        if plot:
            data.plot(events=eog_events)
            ica.plot_sources(datacopy, block=True)
            ica.plot_overlay(average_eog, exclude=eog_inds, show=False)
        ica.apply(data, exclude=eog_inds)
        if plot:
            data.plot(events=eog_events, block=True)
        if save:
            data_name = patient_info['data_save_dir'] + cfg.all_folders_PP['data_preproc_path']
            data_name = data_name + patient_info['ID_patient'] + '_' + patient_info['protocol'] + cfg.prefix_ICA

            #data_name = cfg.data_preproc_path + data.info['subject_info']['his_id'] + cfg.prefix_processed.strip('.fif') + cfg.prefix_ICA
            data.save(data_name, overwrite=True)
            logger.info('saved ICA data', data_name)
            return data
        logger.info('components excluded = %s', eog_inds)
    if save:
        data_name = patient_info['data_save_dir'] + cfg.all_folders_PP['data_preproc_path']
        data_name = data_name + patient_info['ID_patient'] + '_' + patient_info['protocol'] + cfg.prefix_noICA

        #data_name = cfg.data_preproc_path + data.info['subject_info']['his_id'] + cfg.prefix_processed.strip('.fif') + cfg.prefix_noICA
        data.save(data_name, overwrite=True)
        logger.info('saved ICA data', data_name)

    return data

def correct_blink_ICA2(data, patient_info, cfg, save=False, verbose=True, plot=True):
    
    eog_chan = 'VEOGL'
    
    eog_epoch = mne.preprocessing.create_eog_epochs(data, ch_name=eog_chan)
    eog_evoked = eog_epoch.average()
    eog_evoked.apply_baseline(baseline=(None, -0.2))
    n_blinks = eog_evoked.nave
    
    if verbose:
        print(f"Number of blink found: {n_blinks}")

    if plot:
        data.plot(events=eog_epoch.events, title='Show EOG artifacts detection')
        eog_evoked.plot_joint(title='Show averaged EOG artifacts')

    logger.info('Nb blink found : ,%s', n_blinks)
    
    
    ################ ICA correction ##################
    if n_blinks >cfg.minBlinksICA:
    
        filt_raw = data.copy().filter(l_freq=1.0, h_freq=None)
    
        ica = ICA(n_components=15, max_iter="auto", random_state=97)
        ica.fit(filt_raw)
    
        explained_var_ratio = ica.get_explained_variance_ratio(filt_raw)
        for channel_type, ratio in explained_var_ratio.items():
            print(f"Fraction of {channel_type} variance explained by all components: {ratio}")

        ica.plot_components()
    
        # blinks
        #ica.plot_overlay(data, exclude=[0,6], picks="eeg")
        ica.plot_overlay(data, exclude=np.array([0,6]), picks="eeg", title='Plot Overlay')
        ica.plot_properties(data, picks=slice(0,15,1))
    
        # find which ICs match the EOG pattern
        eog_comp_indices, eog_scores = ica.find_bads_eog(data, ch_name=eog_chan)
        ica.exclude = eog_comp_indices
        
        print('ICA eog_comp_indices : ', eog_comp_indices)
        print('ica.exclude : ', ica.exclude)

        # barplot of ICA component "EOG match" scores
        ica.plot_scores(eog_scores)

        # plot diagnostics
        ica.plot_properties(data, picks=eog_comp_indices)

        # plot ICs applied to raw data, with EOG matches highlighted
        ica.plot_sources(data, show_scrollbars=False)

        # plot ICs applied to the averaged EOG epochs, with EOG matches highlighted
        ica.plot_sources(eog_evoked)
        
        print('ICA eog_comp_indices : ', eog_comp_indices)
        print('ica.exclude : ', ica.exclude)
        
        if plot:
            data.plot(events=eog_epoch.events, title="EEG signal before ICA correction")
        
        #Apply ICA
        #ica.exclude.extend(eog_comp_indices)
        ica.apply(data)#, exclude=eog_comp_indices)
        logger.info('components excluded = %s',  ica.exclude)
        
        if plot:
            data.plot(events=eog_epoch.events, block=True, title="EEG signal after ICA correction")
        
        if save:
            data_name = patient_info['data_save_dir'] + cfg.all_folders_PP['data_preproc_path']
            data_name = data_name + patient_info['ID_patient'] + '_' + patient_info['protocol'] + cfg.prefix_ICA

            #data_name = cfg.data_preproc_path + data.info['subject_info']['his_id'] + cfg.prefix_processed.strip('.fif') + cfg.prefix_ICA
            data.save(data_name, overwrite=True)
            logger.info('saved ICA data', data_name)
            return data
        
    if save:
        data_name = patient_info['data_save_dir'] + cfg.all_folders_PP['data_preproc_path']
        data_name = data_name + patient_info['ID_patient'] + '_' + patient_info['protocol'] + cfg.prefix_noICA

        #data_name = cfg.data_preproc_path + data.info['subject_info']['his_id'] + cfg.prefix_processed.strip('.fif') + cfg.prefix_noICA
        data.save(data_name, overwrite=True)
        logger.info('saved ICA data', data_name)

    return data
    

def correct_blink_ICA3(data, patient_info, cfg, save=False, verbose=True, plot=True):
    
    eog_evoked = mne.preprocessing.create_eog_epochs(data, ch_name='VEOGL').average()
    print(f"Number of epochs used to calculate evoked: {eog_evoked.nave}")
    eog_evoked.apply_baseline(baseline=(None, -0.2))
    eog_evoked.plot_joint()
    
    filt_raw = data.copy().filter(l_freq=1.0, h_freq=None)
    
    ica = ICA(n_components=15, max_iter="auto", random_state=97)
    ica.fit(filt_raw)
    
    ica.exclude = []
    # find which ICs match the EOG pattern
    eog_indices, eog_scores = ica.find_bads_eog(data)
    ica.exclude = eog_indices

    # barplot of ICA component "EOG match" scores
    ica.plot_scores(eog_scores)

    # plot diagnostics
    ica.plot_properties(data, picks=eog_indices)

    # plot ICs applied to raw data, with EOG matches highlighted
    ica.plot_sources(data, show_scrollbars=False)

    # plot ICs applied to the averaged EOG epochs, with EOG matches highlighted
    ica.plot_sources(eog_evoked)

def autorejection_epochs(cfg, epochs,fif_fname, protocol, save=False, verbose=True, plot=True):

    n_interpolates = np.array([1, 4, 32])
    consensus_percs = np.linspace(0, 1.0, 11)
    picks = mne.pick_types(epochs.info, meg=False, eeg=True, stim=False,eog=False, exclude=[])

    ar = AutoReject(n_interpolate=n_interpolates, consensus=consensus_percs, picks=picks,
                thresh_method='random_search', random_state=42)
    epochs_clean, reject_log = ar.fit_transform(epochs, return_log=True)


    if plot:
        reject_log.plot_epochs(epochs)
        ar.get_reject_log(epochs).plot()
        epochs_clean.plot(title='Epochs after cleaning')
        epochs_clean.plot_drop_log()

    old = epochs.average()
    png_name = cfg.cleaning_path +  fif_fname.split('/')[-1].strip('.fif') + '_old.png'

    old.plot(spatial_colors=True, show=False, titles='Old data').savefig(png_name)

    new = epochs_clean.average()
    png_name = cfg.cleaning_path +  fif_fname.split('/')[-1].strip('.fif') + '_new.png'
    new.plot(spatial_colors=True, show=False, titles='Cleaned data').savefig(png_name)
    png_name = cfg.cleaning_path +  fif_fname.split('/')[-1].strip('.fif') + '_difference.png'
    difference = mne.combine_evoked([old, - new], weights='equal').plot_joint(show=False, title='Difference raw & cleaned').savefig(png_name)

    if plot:
        plt.show()

    print('Nb epochs uncleaned, %s',len(epochs))
    print('Nb epochs cleaned, %s',len(epochs_clean))
    print('Nb epochs deleted, %s',(len(epochs)-len(epochs_clean)))


    #logger.info('The instances of _AutoReject for each channel type. %s', ar.local_reject)
    #logger.info('Percentage dropped epochs, %s', epochs_clean.drop_log_stats)
    logger.info('Nb epochs uncleaned, %s',len(epochs))
    logger.info('Nb epochs cleaned, %s',len(epochs_clean))
    logger.info('Nb epochs deleted, %s',(len(epochs)-len(epochs_clean)))

    if save:
        data_name = fif_fname.strip('.fif') + cfg.prefix_autoreject
        epochs_clean.save(data_name, overwrite=True)
        logger.info('saved cleaned data', data_name)

    return epochs


def ICA_0Artifact (epochs, n_components, all_conditions):
    epochs["PP"].average().plot(spatial_colors=True)
    epochsfilt = epochs.copy()
    #epochsfilt.plot_psd(fmin=0.5,fmax=40,tmin=-0.03, tmax=0.03)
    #epochsfilt.plot_psd(tmin=-0.03, tmax=0.03)

    print (epochsfilt)

    epochsfilt.filter(5., 30., n_jobs=2, fir_design='firwin')
    ################ ICA correction ##################
    method = 'fastica'  # for comparison with EEGLAB try "extended-infomax" here
    decim = 3  # we need sufficient statistics, not all time points -> saves time
    random_state = 23


    ica = ICA(n_components=n_components, method=method, random_state=random_state)
    picks = mne.pick_types(epochsfilt.info, meg=False, eeg=True, eog=False, stim=False, exclude='bads')
    reject = {'eeg': 100e-6}
    ica.fit(epochsfilt, picks=picks, decim=3, reject=reject)
    print(ica)
    ica.plot_components()

    oaverage_filt = epochsfilt.average()
    oaverage_filt.plot(titles = 'Average ERP (all conditions)')

    ica.plot_sources(oaverage_filt)
    ica.plot_sources(epochsfilt, show=True, block=True)
    ica.plot_properties(epochsfilt, picks=(ica.exclude), psd_args={'fmax': 35.})
    ica.plot_overlay(oaverage_filt, exclude=(ica.exclude), show=False)


    ica.apply(epochs, exclude=(ica.exclude))
    oaverage = epochs.average()
    oaverage.plot(titles = 'Average ERP (all conditions) after 0-artifact ICA')
    epochs["PP"].average().plot(spatial_colors=True)

    return epochs

    ## for eyes you use find_bads_eog which uses pearson correlation to find scores matching components.
    ## TRY!! Not sure how to adapt the scripts in MNE to work for us.
    #o_inds, scores = ica.find_bads_eog(oaverage)
    #print(o_inds)
    #print(scores)
    #ica.plot_scores(scores, exclude=o_inds)
    #ica.plot_sources(eog_average, exclude=o_inds)
