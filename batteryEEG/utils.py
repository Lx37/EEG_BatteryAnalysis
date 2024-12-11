import numpy as np
import pandas as pd
import platform
import mne
import os



def load_from_csv(csv_path):
    df = pd.read_csv(csv_path ,sep=",", keep_default_na=False) # was sep=","
    return df


def create_patient_info(sujet, xls_patients_info, protocol, raw_data_dir, data_save_dir):
        
    print('###### Creating Patient Info ######')
    #load all patients info from the excel file and get specific patient info
    all_patients_info = load_from_csv(xls_patients_info)
    ID_patient = sujet
    Name_File_PP = all_patients_info[all_patients_info['ID_patient'] == sujet]['Name_File_PP'].values[0]
    data_fname = raw_data_dir + sujet + '/EEG/' + Name_File_PP 
    Bad_Chans_PP =  all_patients_info[all_patients_info['ID_patient'] == sujet]['Bad_Chans_PP'].values[0]
    # Bad chan should be marqued as E23,E125 in the correspondig excel file (no space!)
    # We need to convert it to a list of strings
    bad_sub_chan = []
    if len(Bad_Chans_PP)==0:
        bad_sub_chan = Bad_Chans_PP
    else:
        chanstring = Bad_Chans_PP.split(",")
        for i in range (len(chanstring)):
            bad_sub_chan.append(chanstring[i])
    
    #print('bad_sub_chan : ', bad_sub_chan)
  
#    if protocol == 'PP': #TODO : other protocols : LG' / 'Words' / 'Arythmetic'
#        from batteryEEG import config  as cfg

  
    #create patient_info dictionary
    patient_info = {
        'xls_patients_info': xls_patients_info, 
        'ID_patient': ID_patient, 
        'protocol': protocol, 
        'raw_data_dir': raw_data_dir, 
        'data_save_dir': data_save_dir,
        'data_fname': data_fname, 
        'bad_sub_chan': bad_sub_chan, 
        }

    return patient_info


def create_arbo(protocol, patient_info, cfg):
    """
    Create the arborescence for the required analysis
    """
    # Create the folders for the preprocessing
    if protocol == 'PP':
        print('###### Creating the PP arborescence folders ######')
        for key in cfg.all_folders_PP:
            folder = patient_info['data_save_dir'] + cfg.all_folders_PP[key]
            #print('folder : ', folder)
            if not os.path.exists(folder):
                #print('Creating folder : ', folder)
                os.makedirs(folder)
    else:
        print('Protocol not recognized')
        return


def update_excel_bad_chan(patient_info, bad_chans):
    """
    Update the excel file with the bad channels given for the subject
    """
    df = pd.read_csv(patient_info['xls_patients_info'])
    
    print("df['ID_patient'] : ", df['ID_patient'])
    print("patient_info.ID_patient : ", patient_info['ID_patient'])
    print('bad_chans : ', bad_chans)
    print('[str(i) for i in bad_chans] : ', ''.join(str(i) + ',' for i in bad_chans)[:-1])
    
    # Convert bad_chans to a single string with a comma separator (no space!)
    bad_chans_str = ','.join(str(i) for i in bad_chans)
    
    # Update the DataFrame
    df.loc[df['ID_patient'] == patient_info['ID_patient'], 'Bad_Chans_PP'] = bad_chans_str
    
    print('df : ', df[df['ID_patient'] == patient_info['ID_patient']]['Bad_Chans_PP'])
    
    # Save the updated DataFrame back to the CSV file
    df.to_csv(patient_info['xls_patients_info'], index=False)
    print('csv saved')
   
    return df

