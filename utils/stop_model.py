import pandas as pd

from utils.base_model import CognitiveTask

class stopModel(CognitiveTask):
    def __init__(self, participant_id, exp_id, task_data):
        super().__init__(participant_id, exp_id, task_data)
        
    def calculate_by_condition(self, condition_column):
        
        test_data = self.task_data.query('trial_id == "test_trial"')
        conditions = test_data[condition_column].unique()
        
        overall_omission_rate = super().calculate_omissions(test_data, condition_column)
        
        results = {
            "subject": self.participant_id,
            f'{self.exp_id}_go_rt': self.get_go_rt(test_data, condition_column),
            f'{self.exp_id}_stop_failure_rt': self.get_stop_failure(test_data, condition_column),
            f'{self.exp_id}_stop_success': self.get_stop_success(test_data),
            f'{self.exp_id}_max_ssd': self.get_max_ssd(test_data),
            f'{self.exp_id}_min_ssd': self.get_min_ssd(test_data),
            f'{self.exp_id}_mean_ssd': self.get_mean_ssd(test_data),
            #f'{self.exp_id}_max_ssd_count': self.get_max_ssd_count(test_data),
            #f'{self.exp_id}_min_ssd_count': self.get_min_ssd_count(test_data),
            f'{self.exp_id}_go_acc': self.get_go_acc(test_data),
            f'{self.exp_id}_stop_fail_acc': self.get_stop_fail_acc(test_data)
        }
            
        df = pd.DataFrame([results]).set_index("subject")
        df[f"{self.exp_id}_omission_rate"] = overall_omission_rate
        return df
    
    def get_go_rt(self, data, condition_column):
        go_rt = data[data[condition_column] == 'go'].rt.mean()
        return go_rt
    
    def get_stop_failure(self, data, condition_column):
        stop_data = data[data[condition_column] == 'stop']
        stop_fails = stop_data[stop_data['stop_acc'] == 0]
        stop_failure_rt = stop_fails.rt.mean()
        return stop_failure_rt

    def get_stop_success(self, data):
        return data.stop_acc.mean()
        
    def get_max_ssd(self, data):
        """This function grabs the max SSD for subject"""
        max_ssd = data.query("SS_trial_type == 'stop'").SSD.max()
        return max_ssd
    
    def get_min_ssd(self, data):
        min_ssd = data.query("SS_trial_type == 'stop'").SSD.min()
        return min_ssd
    
    def get_mean_ssd(self, data):
        mean_ssd = data.query("SS_trial_type == 'stop'").SSD.mean()        
        return mean_ssd
            
    def get_max_ssd_count(self, data):
        """This function grabs the max SSD fo subject"""
        max_ssd_count = data.query("SS_trial_type == 'stop' and SSD == 1000").SSD.count()
        return max_ssd_count
    
    def get_min_ssd_count(self, data):
        min_ssd_count = data.query("SS_trial_type == 'stop' and SSD == 0").SSD.count()            
        return min_ssd_count

    def get_go_acc(self, data):
        go_acc = data.query("SS_trial_type == 'go'").go_acc.mean()
        return go_acc
    
    def get_stop_fail_acc(self, data):
        return data.stop_acc.mean()
