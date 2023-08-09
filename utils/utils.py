import pandas as pd
import numpy as np
import json
import ast
import os

def organize_data(json_file, data_dir, ses, output_flag = False):
    # reading in data json for now
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    data_dict = {}
    
    for task in data.keys():
        sub_id = data[task][0]['subject']

        dict_obj = ast.literal_eval(data[task][0]['data'])
        trial_data = json.loads(dict_obj['trialdata'])
        single_sub_df = pd.DataFrame(trial_data) 
        
        if output_flag:
            
            # checks/makes ses directory
            if not os.path.exists(file_path+ '/' + sub_id + '/' + 'ses-01'):
                os.makedirs(file_path+ '/' + sub_id + '/' + 'ses-01')
            else:
                # add a check for session or something?
                print('working on it')
            single_sub_df.to_csv(f'{file_path}/{sub_id}/{ses}/{sub_id}_{task}.csv', sep=',')
            
        if not data_dict:
            data_dict[sub_id] = {task: single_sub_df}
        else:
            data_dict[sub_id][task] = single_sub_df
        
    
    return data_dict
        
