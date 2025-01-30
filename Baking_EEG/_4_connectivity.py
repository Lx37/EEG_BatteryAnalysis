#https://mne.tools/1.4/auto_tutorials/time-freq/10_spectrum_class.html
import numpy as np
import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
from mne_connectivity import spectral_connectivity_epochs
from mne_connectivity.viz import plot_sensors_connectivity
import os
#import netCDF4 as nc
import xarray as xr
from mne_connectivity.viz import plot_connectivity_circle
import mne

#import config as cfg

## logging info ###
import logging
from datetime import datetime

import os
os.environ["QT_API"] = "pyside6"




def connectivity_overSubs(subs, data_save_dir, selected_chans, proto, cfg, save=True, plot=True, show_plot=True):
        
    event_ids = cfg.con_event_ids
    freq_bands = cfg.con_freq_bands
    tmin = cfg.con_tmin
    
    # We will keep all data in multidim array to hack plot_sensors_connectivity (see below)
    if selected_chans != 'All':
        n_chans = len(selected_chans)
        df_chan = pd.DataFrame(np.nan, index=selected_chans, columns=selected_chans)
    else:
        fif_fname = f'{data_save_dir}{cfg.data_con_path}{subs[0]}_{proto}{cfg.prefix_epo_conn}'  #pas top clean, on suppose que tous les sujets ont les memes canaux
        print('################fif_fname : ', fif_fname)
        #TODO set VREF as good ?
        epochs = mne.read_epochs(fif_fname, proj=False, verbose=True, preload=True)#.pick_types(eeg=True) 
        chans_names = epochs.ch_names
        n_chans = len(chans_names) 
        print('nb chan : ', n_chans)
        print('###################chans_names : ', chans_names)
        assert chans_names == cfg.EGI_con_chan, "All chan for this sub are not consistent" #check channel consistency over subjects   
        df_chan = pd.DataFrame(np.nan, index=chans_names, columns=chans_names)

    #Get real chan index
    All_ROI = cfg.con_all_ROI_chan
    for kk in All_ROI.keys():
        print('key :', kk)
        index_list = []
        for cc in cfg.con_all_ROI_chan[kk]:
            index = chans_names.index(cc)
            index_list.append(index)
        All_ROI[kk] = index_list

    print('******************All_ROI : ', All_ROI)
         
    n_events = len(event_ids)
    n_subs = len(subs)
    n_bands = len(freq_bands)
    all_conn_aray = np.zeros((n_chans, n_chans, n_events, n_subs))
   
    #n_ROI = len( All_ROI.keys())
    #all_conn_ROI_aray = np.zeros((n_ROI, n_ROI, n_events, n_subs))
    #df_ROI_2 = pd.DataFrame(np.nan, index = All_ROI.keys(), columns = All_ROI.keys())
    
    
    # loop over frequencies
    for i_key, k in enumerate(freq_bands.keys()):
        fmin = freq_bands[k][0]
        fmax = freq_bands[k][1]
    
        for i_sub, sub in enumerate(subs):
            fif_fname = f'{data_save_dir}{cfg.data_con_path}{sub}_{proto}{cfg.prefix_epo_conn}'
            print('fif_fname : ', fif_fname)
            epochs = mne.read_epochs(fif_fname, proj=False, verbose=True, preload=True)
        
            print('event_ids : ', event_ids)
            # loop over conditions
            for i_event, event_id in enumerate(event_ids):

                # Get epochs selection (sub chans, eventID) if necessary
                if selected_chans != 'All':
                    selected_epochs = epochs[event_id].pick_channels(selected_chans, ordered=True)
                    chans_names = selected_chans
                else:
                    selected_epochs = epochs[event_id]#.pick_types(eeg=True)
                    chans_names = selected_epochs.ch_names
                    
                print('Chan names : ', chans_names)

                # Connectivity computation
                con_data = spectral_connectivity_epochs(selected_epochs, method=cfg.con_method, mode='multitaper',
                        sfreq=epochs.info['sfreq'], fmin=fmin, fmax=fmax, faverage=True, tmin=tmin, mt_adaptive=False, n_jobs=1)

                con_matrix = con_data.get_data(output="dense")[:, :, 0].copy()
                Result_ROI_sub, df_ROI_sub = get_ROI(con_matrix, All_ROI)

                # Saving data
                if save:
                    if not os.path.exists(f'{data_save_dir}{cfg.result_con_path}/{sub}/'):
                        os.makedirs(f'{data_save_dir}{cfg.result_con_path}/{sub}/')
                    #Saving connectivity chan values for each sub/freq/proto
                    df_chan_sub = pd.DataFrame(np.nan, index=chans_names, columns=chans_names)
                    df_chan_sub.loc[:, :] = con_matrix
                    df_con_sub_name =  f'{data_save_dir}{cfg.result_con_path}/{sub}/{sub}_{proto}_{cfg.con_method}_{k}_conData.xlsx'
                    df_chan_sub.to_excel(df_con_sub_name)
                    
                    #Saving connectivity ROI velues for each sub/freq/proto
                    df_Roi_sub_name =  f'{data_save_dir}{cfg.result_con_path}/{sub}/{sub}_{proto}_{cfg.con_method}_{k}_ROI.xlsx'
                    df_ROI_sub.to_excel(df_Roi_sub_name)
                    
                #plot conn ROI for each subjet
                ROI_sub_fig, ROI_sub_ax = plot_connectivity_circle(df_ROI_sub.to_numpy(), All_ROI.keys(), title=f'{sub} {proto} Connectivity {k} band', vmin=cfg.con_vmin, vmax=cfg.con_vmax)
                fname_sub_fig =  f'{data_save_dir}{cfg.result_con_path}/{sub}/{sub}_{proto}_{cfg.con_method}_{k}_conData_ROI.png'
                ROI_sub_fig.savefig(fname_sub_fig, facecolor='black') 
                
               
                all_conn_aray[:, :, i_event, i_sub] = con_data.get_data(output='dense')[:, :, 0].copy()
                #all_conn_ROI_aray[:, :, i_event, i_sub] = df_ROI_sub.to_numpy()
        
        if save:
            all_conn_aray_name = f'{data_save_dir}{cfg.result_con_path}/{proto}_{cfg.con_method}_{k}_allSubConArray.npy'
            np.save(all_conn_aray_name, all_conn_aray)
        
        
        if len(event_ids) == 1 : #TODO traiter le cas si plusieurs event_id
            all_con_matrix = np.average(all_conn_aray, axis = 3).reshape(all_conn_aray.shape[0],all_conn_aray.shape[1])
            # ROI of averaged con data
            Result_ROI, df_ROI = get_ROI(all_con_matrix, All_ROI)
            df_ROI_name = f'{data_save_dir}{cfg.result_con_path}/{proto}_{cfg.con_method}_{k}_allSub_ROI.xlsx'
            df_ROI.to_excel(df_ROI_name)
            
            #averaged ROI of each con data  - it's the same as ROI of averaged data
            #avAll_ROI =  np.average(all_conn_ROI_aray, axis = 3).reshape(all_conn_ROI_aray.shape[0], all_conn_ROI_aray.shape[1])
            #df_ROI_2.loc[:, :] = avAll_ROI
            #df_ROI2_name = f'{cfg.data_conn_path}/{proto}_{cfg.con_method}_{k}_allSub_ROI2.xlsx'
            #df_ROI_2.to_excel(df_ROI2_name)
            
            df_chan.loc[:, :] = all_con_matrix
            df_chan_name = f'{data_save_dir}{cfg.result_con_path}/{proto}_{cfg.con_method}_{k}_allSub_Chan.xlsx'
            df_chan.to_excel(df_chan_name)
            
            print(df_ROI.to_numpy().shape)
            ROI_fig, ROI_ax = plot_connectivity_circle(df_ROI.to_numpy(), All_ROI.keys(), title=f'{proto} AllSub Connectivity {k} band', vmin=cfg.con_vmin, vmax=cfg.con_vmax)
            fname_fig = f'{data_save_dir}{cfg.result_con_path}/{proto}_{cfg.con_method}_{k}_allSub_ROI.png'
            ROI_fig.savefig(fname_fig, facecolor='black') 
        
        # Hack the sensor connectivity plot to show averaged conn data (over subj)
        hack_con_data_av = np.average(all_conn_aray, axis = 3)
        #for ii in range(n_events):
            #plot_sensors_connectivity(epochs.info, hack_con_data_av[:,:,ii], picks=chans_names)
            #plot_connectivity_circle(hack_con_data_av[:,:,ii], chans_names)
        #plt.show(block=True)
        
    return all_conn_aray 
        
                
def connectivity_1sub(data_name, patient_info, cfg, save=True, verbose=True, plot=True): #(fif_fname, cfg.con_method, plot=True):

    #load epochs
    epochs = mne.read_epochs(data_name, proj=False, verbose=True, preload=True).pick_types(eeg=True) 
    #epochs = epochs[event_id].pick_channels(selected_chans, ordered=True)
    
    # define connectivity params
    fmin, fmax = 4.0, 9.0
    sfreq = epochs.info["sfreq"]  # the sampling frequency
    tmin = 0.0  # exclude the baseline period

    # Connectivity computation
    con_data = spectral_connectivity_epochs(epochs, method=cfg.con_cfg.con_method, mode='multitaper',
                sfreq=sfreq, fmin=fmin, fmax=fmax, faverage=True, tmin=tmin, mt_adaptive=False, n_jobs=1)
    
    print('epochs.info: ', epochs.info)
    
    if plot:
        #plot_sensors_connectivity(epochs.info, con_data.get_data(output="dense")[:, :, 0])
        # use shrotcut to see connections https://defkey.com/pyvista-0-42-shortcuts
        # v puis w
        
        con_epochs_matrix = con_data.get_data(output="dense")[:, :, 0]
        fig = plt.figure()
        im = plt.imshow(con_epochs_matrix)
        fig.colorbar(im, label="Connectivity")
        plt.ylabel("Channels")
        plt.xlabel("Channels")
        plt.show()

    return con_data


def get_ROI(con_matrix, All_ROI):  #need con_matrix as con_matrix = con_data.get_data(output="dense")[:, :, 0]
    
    new_np_con_data= np.add(con_matrix, con_matrix.transpose())  # get symetrical matrix to access data reversively from chan index
    
    Result_ROI = {}
    df_ROI = pd.DataFrame(np.nan, index= All_ROI.keys(), columns= All_ROI.keys())

    for Current_Roi_1 in All_ROI.keys():   # loop on ROI to get one ROI and the others
        Other_Roi = list(All_ROI.keys()).copy()
        Other_Roi.remove(Current_Roi_1)
        
        for Current_Roi_2 in Other_Roi: #loop on each other ROI
            
            Av_Con_Roi = []
            for ii, chan in enumerate(All_ROI[Current_Roi_1]):
                Current_Con_Roi = new_np_con_data[chan, All_ROI[Current_Roi_2]] # Get connectivity of one chan with all from other ROI
                Av_Con_Roi.append(Current_Con_Roi.tolist()) 
            
            flat_Av_Con_Roi = [item for sublist in Av_Con_Roi for item in sublist]   #flatten the data
            ROI2_name = Current_Roi_1 + ' / ' + Current_Roi_2
            Result_ROI[ROI2_name] = np.array(flat_Av_Con_Roi).mean()  #mean added to dict
            df_ROI.loc[[Current_Roi_1],Current_Roi_2] = np.array(flat_Av_Con_Roi).mean() #mean added to dataframe
            
    return Result_ROI, df_ROI   # return result as dict or dataframe <3

def print_infos(con_data):
    #Some prints to get how it's organized :
    
    #print('###con data : ', con_data.get_data())
    #print('###con data : ', con_data.get_data(output='dense')[:, :, 0])
    
    #print('###con data : ', con_data.attrs)  #attrs stores all informations about computation
    
    ## node_names = channels names here
    ## instance of classe 'mne_connectivity.base.SpectralConnectivity'
    ## shape : (n_connections, n_freqs) with n_connections = n_chan*n_chan [in case of indices=None : all to all]
    ## but inside, (only n_chan²-n_chan)/2 values (other are 0 because redundant and null for a chan with itself
    # ex : 7 channels, shape 49, 21 values interestings (for 21 coupling) 6+5+4+3+2+1


    print('dense : ', con_data.get_data(output='dense')[:, :, 0]) # (n_chan, nchan, 1)
    print('dense shape : ', con_data.get_data(output='dense')[:, :, 0].shape) # (n_chan, nchan, 1)
    #print('compact : ', con_data.get_data(output='compact')) #(n_chan, nchan)
    #print('raveled : ', con_data.get_data(output='raveled')) #(n_chan, nchan)
    print('coords : ', con_data.coords)
    #print('companion : ', con_data.companion) #gives an error..
    print('dims : ', con_data.dims)
    print('indices : ', con_data.indices)
    print('names : ', con_data.names)
    print('shape : ', con_data.shape)  # -> shape (n_chan², 1)
    
    print('coords : ', con_data.coords.node_in)
    plot_sensors_connectivity(selected_epochs.info, con_data.get_data(output='dense')[:, :, 0])
    plot_connectivity_circle(con_data.get_data(output='dense')[:, :, 0], chans_names)
    con_data.plot_circle()
    plt.show()

