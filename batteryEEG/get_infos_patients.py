import numpy as np
import pandas as pd
import platform
import mne


def load_from_csv(csv_path):
    
    df = pd.read_csv(csv_path ,sep=",", keep_default_na=False) # was sep=","
    
    return df

'''
    
    all_subjects_LG=[]
    all_subjects_PP=[]
    all_subjects_Rest = []
    id_patient=[]
    #protocol=[]
    #type_EEG=[]
    diagnostic = []
    bad_subs_chans_LG=[]
    bad_subs_chans_PP=[]
    bad_subs_chans_Rest=[]

    print(df)
    
    for i in range(len(df)):
        id_patient.append(df["ID_patient"][i])
        all_subjects_LG.append(df["Name_File_LG"][i])
        all_subjects_PP.append(df["Name_File_PP"][i]) #sub
        all_subjects_Rest.append(df["Name_File_resting"][i]) #sub
        #protocol.append(df["Protocol"][i])
        #diagnostic.append(df["Diagnostic"][i])

        bad_sub_chans_LG = []
        chanstring = df["Bad_Chans_LG"][i]
        chanstring=chanstring.split(",")
        if chanstring != ['']:
            for ii in range (len(chanstring)):
                bad_sub_chans_LG.append(chanstring[ii])
        else:
            bad_sub_chans_LG.append('')
       
        bad_sub_chans_PP = []
        chanstring = df["Bad_Chans_PP"][i]
        chanstring = chanstring.split(",")
        if chanstring != ['']:
            for j in range (len(chanstring)):
                bad_sub_chans_PP.append(chanstring[j])
        else:
            bad_sub_chans_PP.append('')

        bad_sub_chans_Resting = []
        chanstring = df["Bad_Chans_Resting"][i]
        chanstring=chanstring.split(",")
        if chanstring != ['']:
            for k in range (len(chanstring)):
                bad_sub_chans_Resting.append(chanstring[k])
        else:
            bad_sub_chans_Resting.append('')

        
        bad_subs_chans_LG.append(bad_sub_chans_LG)
        bad_subs_chans_PP.append(bad_sub_chans_PP)
        bad_subs_chans_Rest.append(bad_sub_chans_Resting)
        #this dictionnarry comes from preliminary data visual checking using 'get_bad_chan' function
        
'''