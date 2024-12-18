import mne
import numpy as np
import matplotlib.pyplot as plt
import os
from EEG_Analysis import utils


## logging info ###
import logging
from datetime import datetime

logname = './logs/' + datetime.now().strftime('log_%Y-%m-%d.log')
logging.basicConfig(filename=logname,level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)



def preprocess_mff(patient_info, cfg, save=False, verbose=True, plot=True):
    """
    Preprocess EEG data from EGI format.
    This function performs the following steps:
        - Import data
        - Correct channels (define stim channel and channel type, match names to montage, create Cz, HEOG/VEOG, re-reference, interpolate)
        - Apply filters (notch filter at 50Hz and band-pass filter from 0.1-45Hz)
        - Save preprocessed data of interest (from 1st trigger -3s to last trigger +3s) in FIF format with '_preproc' extension
    Parameters:
    -----------
    patient_info : object
        Object containing patient information and file paths.
    save : bool, optional
        If True, save the preprocessed data (default is False).
    verbose : bool, optional
        If True, print information during processing (default is True).
    plot : bool, optional
        If True, plot data at various stages (default is True).
    define_bad_chan : bool, optional
        If True, allow manual definition of bad channels (default is True).
    Returns:
    --------
    data : instance of mne.io.Raw
        The preprocessed EEG data.
    Notes:
    ------
    - The function uses MNE-Python for EEG data processing.
    - The function assumes specific channel names and types for HEOG and VEOG creation.
    - The function interpolates bad channels to calculate the average reference.
    - The function saves the preprocessed data in FIF format and also saves a dictionary of event names.
    Example:
    --------
    >>> patient_info = PatientInfo()
    >>> preprocessed_data = preprocess_mff(patient_info, save=True, verbose=True, plot=False)
    """

    #################### Load data ####################
    
    print('###### Load data and set montage ######')
    if patient_info['ID_patient'] == 'TT02':
        data = mne.io.read_raw_egi(patient_info['data_fname'], eog=None, misc=None, include=None, preload=True, verbose=None)
    else:
        data = mne.io.read_raw_egi(patient_info['data_fname'], eog=None, misc=None, exclude=None, include=None, preload=True, verbose=None)

    sfreq = data.info['sfreq']
    event_id = data.event_id
    print(event_id)

    # set montage 
    coordinatesfile = patient_info['data_fname'] + '/coordinates.xml'
    montage = mne.channels.read_dig_egi(coordinatesfile)
    print('montage loaded ch_names : ', montage.ch_names)
    montage.ch_names = cfg.EGI_chan_names
    print('montage new ch_names : ', montage.ch_names)
    
    data.set_montage(montage)#, raise_if_subset=False) for old MNE 0.19


    if verbose:
        print('montage : ', montage)
        print(data.info)
    if plot:
        data.plot_sensors(kind='3d')

    ############# Set data general info ##############
    
    #data.info['proj_name'] = cfg.proj_name
    data.info['subject_info'] = {'his_id' : patient_info['ID_patient']}

    ################ Channels operations ##############
    # set stim chan type
    mapping_type = {'STI 014': 'stim'}
    data.set_channel_types(mapping_type)

    logger.info('Raw data info ch_names: ,%s', data.info['ch_names'])
    logger.info('Raw data info channels: ,%s', len(data.info['ch_names']))
    logger.info('Raw data info highpass: ,%s', data.info['highpass'])
    logger.info('Raw data info lowpass: ,%s', data.info['lowpass'])
    logger.info('Raw data info sfreq: ,%s', data.info['sfreq'])

    if plot:
        data.plot(show_options=True, block=True, title='Raw EEG data') # scaling set to eeg=20e-6, eog=150e-6

    #################### Filters ####################
    
    print('###### Filter data and downsample ######')
    # notch filter around 50hz
    picks_eeg = mne.pick_types(data.info, eeg=True)
    data.notch_filter(np.arange(50, 200, 50), picks=picks_eeg, filter_length='auto', phase='zero-double')
    # band pass filter around 1-25Hz
    data.filter(cfg.highpass, cfg.highcut, method='fir', phase='zero-double', fir_design='firwin2')

    if plot:
        picks_psd_plot = mne.pick_types(data.info, eeg=True, selection=['E15','E11', 'E55', 'E62','E75', 'E108', 'E45', 'E122', 'E33'])
        fig, ax = plt.subplots(1)
        data.plot_psd(ax = ax, area_mode='range', tmax=10.0, picks = picks_psd_plot, average=False, show=False)
        ax.set_title('FFT after filtering for patient ' + patient_info['ID_patient'])
        plt.show()

       # Downsample data
    data = data.resample(cfg.sfreq)
      
    #################### Set bad chans ####################
    
    print('###### Set bad chans ######')
    ## Manual check
    if len(patient_info['bad_sub_chan'])==0:
        print('No bad channels for subject')
    else:
        data.info['bads'] = patient_info['bad_sub_chan']

    ## Manual check to set bad channels and update excel file + patient_info
    datacheck = data.copy()
    events = mne.find_events(datacheck, stim_channel='STI 014')
    evoked = mne.Epochs(datacheck, events=events, picks='eeg', tmin=-0.2, tmax=1.2).average()
    evoked.plot(titles='Global average triggers, any new bad sensors? (the actual bads are not showned) Note them and indicate in next EEG plot')
    data.plot(show_options=True, title='Indicate bad sensors manually by a clic on the channel (apears in grey). Greyy one are already defined as bads.', block=True)
    utils.update_excel_bad_chan(patient_info, data.info['bads'])
    patient_info['bad_sub_chan'] = data.info['bads']

    data.set_channel_types({'E8':'misc','E25':'misc','E17':'misc','E126':'misc','E127':'misc'})

    data.info['bads'].extend(['VREF']) # was 'E129'+ ['Cz']
    
  
    logger.info('Bad channels : ,%s', data.info['bads'])
    print('Bad channels : %s for patient %s', data.info['bads'], patient_info['ID_patient'])


    #################### Interpollation ####################
    
    print('###### Interpolate bad chans ######') # used only to calculate average ref (for now)
    data.interpolate_bads(reset_bads=False)
    ### Pay ATTENTION! All bad channels are interpolated, this we did to be able to interpolate the Cz channel with only good ones, and is necessary for source reconstruction.
    ### PAY ATTENTION : keep using (for pick_types, epochs etc.) " exclude=[] " otherwise the bads get deleted!
    print(data.info['bads'])
    data.info['bads'].remove('VREF')
    print(data.info['bads'])
    if plot:
        data.plot_sensors(kind='3d', ch_type ='eeg', title='Sensory positions, Red ones are indicated as bads ')

  
    # ########### Create HEOG and VEOG chans ###########
    
    print('###### Create oculars ######')
    chan1 = data.copy().pick_channels(['E25']).get_data()
    chan2 = data.copy().pick_channels(['E127']).get_data()
    VEOGL = chan1 - chan2
    infoVEOGL = mne.create_info(['VEOGL'], sfreq, ['eog'])
    raw_VEOGL = mne.io.RawArray(VEOGL, infoVEOGL)

    chan1 = data.copy().pick_channels(['E8']).get_data()
    chan2 = data.copy().pick_channels(['E126']).get_data()
    VEOGR = chan1 - chan2
    infoVEOGR = mne.create_info(['VEOGR'], sfreq, ['eog'])
    raw_VEOGR = mne.io.RawArray(VEOGR, infoVEOGR)

    chan1 = data.copy().pick_channels(['E32']).get_data()
    chan2 = data.copy().pick_channels(['E1']).get_data()
    HEOG = chan1 - chan2
    infoHEOG = mne.create_info(['HEOG'], sfreq, ['eog'])
    raw_HEOG = mne.io.RawArray(HEOG, infoHEOG)

    data.add_channels([raw_VEOGL, raw_VEOGR], force_update_info=True)  #TODO Only VEOG added for now
    

    #################### Re-Referencing ####################
    
    print('###### Re-reference ######')
    data.set_eeg_reference(ref_channels='average', projection=False) # Set EEG average reference

    #################### save preprocessed data of interest ####################
    
    print('###### Save preprocessed data ######')
    
    #Export only data of interest : from first trig -3s to last trig + 3s  
    # TODO why last trig +3s??
    # TODO difference betwen proto ??
    events = mne.find_events(data, stim_channel='STI 014')
    event_names = np.zeros((events.shape[0],), dtype='S10') # new array one column of zero's with max lenght of 10 caracters

    for x in range(events.shape[0]): # loop over rows
        value = events[x, 2] # take each 3th column
        new_value = [k for k,v in event_id.items() if v==value][0]
        event_names[x] = new_value
        good_events = events[(event_names!=b'Rest') & (event_names!=b'Code') & (event_names!=b'star') & (event_names!=b'rest'), :] # all events where names is not 'rest'

    if verbose:
        print(data.info)
        print(data.ch_names)
        print("sfreq : ", sfreq)

    if patient_info['ID_patient'] == 'CB31':  #Generalize ??
        i_start = 860
    elif patient_info['ID_patient'] == 'GU32':
        i_start = 780 #Patient GU32 extra headphone check resulted in triggers before start of protocol!
    else:
        i_start = int(good_events[0][0]/data.info['sfreq']-3)
        i_stop =  int(good_events[-1][0]/data.info['sfreq']+3)
    
    
    if save:
        data_name = patient_info['data_save_dir'] + cfg.all_folders_PP['data_preproc_path']
        data_name = data_name + patient_info['ID_patient'] + '_' + patient_info['protocol'] + cfg.prefix_processed
        print("Saving data : " + data_name)
        data.save(data_name, tmin=i_start, tmax=i_stop, overwrite=True)
        logger.info("Saved preprocessed data " + data_name)
        ######For EGI subjects, save stimulation name dictionary #######
        nameStimDict =  patient_info['data_save_dir'] + cfg.all_folders_PP['stimDict_path'] 
        nameStimDict = nameStimDict + patient_info['ID_patient'] + '_' + patient_info['protocol'] + cfg.prefix_stimDict ## For the stimuli dictionary (names of stimuli given automatically vs ones we gave the stimuli)
        np.save(nameStimDict, event_id)
        logger.info("Saved stimdict data " + nameStimDict)


    if plot and patient_info['protocol'] != 'Resting':
        scalings=dict(eeg=20e-6, eog=100e-6, misc=20e-6)
        events = mne.find_events(data, stim_channel='STI 014')
        eventplot = mne.viz.plot_events(events, data.info['sfreq'], show=True)
        plt.show() 

    return data




#def preprocess_mircomed(cfg, data_fname, sub_name, bad_sub_chan=[], save=False, verbose=True, plot=True):
    '''
    This function preprocess the data :
        - import data
        - channels correction (define stim chan and chan type, names to match the montage,
                              Cz creation, HEOG/VEOG, re-ref, interpolation,..)
        - apply filter on data (notch 50H and 0.1-40Hz Higth pass)
        - save preproc data of interest (from 1st trig-3s to last trig+3s)
        in fif format, with '_preproc' extention.

    If 'verbose' set to True, print informations.
    If 'plot' set to True, plot data.
    If 'save' set to True, save the data.
    '''

    #################### Load data ####################
    data = trc.raw_from_neo(data_fname)
    sfreq = data.info['sfreq']
    #event_id = data.event_id
    print(sfreq)
    #print(event_id)
    print(data.info)
    #data.plot(title =data_fname, block=True)

    # set montage

    ten_twenty_montage = mne.channels.make_standard_montage('standard_1020')

    data.set_montage(ten_twenty_montage)

    if verbose:
        print(data.info)
        print('montage : ', ten_twenty_montage)
        #data.plot_sensors(kind='3d', block=True)

    ############# Set data general info ##############
    data.info['proj_name'] = cfg.proj_name
    data.info['subject_info'] = {'his_id' : sub_name}


    if verbose:
        print(data.info)
    logger.info('Raw data info channels: ,%s', len(data.info['ch_names']))
    logger.info('Raw data info highpass: ,%s', data.info['highpass'])
    logger.info('Raw data info lowpass: ,%s', data.info['lowpass'])
    logger.info('Raw data info sfreq: ,%s', data.info['sfreq'])

    if plot:
        data.plot(show_options=True, block=True) # scaling set to eeg=20e-6, eog=150e-6

    #################### Filters ####################
    # notch filter around 50hz
    picks_eeg = mne.pick_types(data.info, eeg=True)
    data.notch_filter(np.arange(50, 100, 50), picks=picks_eeg, filter_length='auto', phase='zero-double')
    # band pass filter around 1-25Hz
    data.filter(cfg.highpass, cfg.highcut, method='fir', phase='zero-double', fir_design='firwin2')

    if plot:
        picks_psd_plot = mne.pick_types(data.info, eeg=True)
        data.plot_psd(area_mode='range', tmax=10.0, picks = picks_psd_plot, average=False)


    #################### Set bad chans ####################
    print(data.info)
    print("bad_sub_chan", bad_sub_chan)
    if len(bad_sub_chan)==0:
        print('no bad channels for subject')
    else:
        data.info['bads'] = bad_sub_chan
    print(data.info)

    ## Manual check

    datacheck = data.copy()
    events = mne.find_events(datacheck, stim_channel='STI 014')
    evoked = mne.Epochs(datacheck, events=events, tmin=-0.2, tmax=1.2)
    evoked = evoked.average()
    evoked.plot(titles='Global average triggers, any sensorys bad?' + sub_name)
    data.plot(show_options=True, title='Indicate bad sensors manually', block=True)
    print(data.info)

    if plot:
        data.plot_sensors(kind='3d', ch_type ='eeg', title='Sensory positions, Red ones & Cz are indicated as bads '+ sub_name)

    logger.info('Bad channels : ,%s', data.info['bads'])


    #################### Interpollation ####################
    print ('Bad channels are interpolated') # used only to calculate average ref (for now)
    data.interpolate_bads(reset_bads=False)
    ### Pay ATTENTION! All bad channels are interpolated, this we did to be able to interpolate the Cz channel with only good ones, and is necessary for source reconstruction.
    #PAY ATTENTION : keep using (for pick_types, epochs etc.) " exclude=[] " otherwise the bads get deleted!
    if plot:
        data.plot(show_options=True, block=True) # scaling set to eeg=20e-6, eog=150e-6
        data.plot_sensors(kind='3d', ch_type ='eeg', title='Sensory positions, Red ones are indicated as bads ')

    #################### Re-Referencing ####################
    data.set_eeg_reference(ref_channels='average', projection=False) # Set EEG average reference

    #################### save preprocessed data of interest ####################
    if save:
        #Export only data of interest : from first trig -3s to last trig + 3s
        print("ici : ", data.info['subject_info']['his_id'])
        print("ici type : ",  type(data.info['subject_info']))

        data_name = cfg.data_preproc_path + data.info['subject_info']['his_id'] + prefix_processed
        print("Saving data : " + data_name)
        data.save(data_name, overwrite=True)
        logger.info("Saved preprocessed data " + data_name)


    if plot:
        scalings=dict( eeg=20e-6, eog=100e-6, misc=20e-6)
        data.plot(show_options=True, scalings=dict(eeg=20e-6, eog=100e-6),block=True)
        eventplot = mne.viz.plot_events(events, data.info['sfreq'])

    return data
