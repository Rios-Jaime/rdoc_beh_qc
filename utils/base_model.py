import pandas as pd
import numpy as np

class CognitiveTask:
    def __init__(self, participant_id, exp_id, task_data):
        self.participant_id = participant_id
        self.exp_id = exp_id
        self.task_data = pd.DataFrame(task_data)

    def _metrics_for_data(self, data, acc_column):
        acc = data[acc_column].mean()
        avg_rt = data['rt'].mean()
        return {'acc': acc, 'avg_rt': avg_rt}

    def calculate_by_condition(self, condition_column='condition', acc_column='correct_trial', test_query='trial_id == "test_trial"'):
        test_data = self.task_data.query(test_query)
        conditions = test_data[condition_column].unique()
        
        overall_omission_rate = self.calculate_omissions(test_data, condition_column)
        
        results = {}
        for condition in conditions:
            condition_data = test_data[test_data[condition_column] == condition]
            results[condition] = self._metrics_for_data(condition_data, acc_column)
            
        
        df = self._results_to_dataframe(results)
        df[f"{self.exp_id}_omission_rate"] = overall_omission_rate
        return df

    def calculate_omissions(self, data, condition_column=None):
        if self.exp_id == 'go_nogo':
            omission_rate = data.query(f'{condition_column} == "go"')['rt'].isna().mean()
        elif self.exp_id == 'stop_signal':
            omission_rate = data.query(f'{condition_column} == "go"')['rt'].isna().mean()
        else:
            omission_rate = data['rt'].isna().mean()
        return omission_rate

    def calculate_factorial_condition(self, first_order_conditions, second_order_conditions, acc_column='correct_trial', test_query='trial_id == "test_trial"'):
        if second_order_conditions is None:
            second_order_conditions = [None]

        test_data = self.task_data.query(test_query)
        
        conditions_1 = test_data[first_order_conditions].unique()
        conditions_2 = test_data[second_order_conditions].unique()
        
        overall_omission_rate = self.calculate_omissions(test_data)
        
        results = {}        
        for condition1 in conditions_1:
            for condition2 in conditions_2:
                condition_data = test_data[test_data[first_order_conditions] == condition1]
                if condition2:
                    condition_data = condition_data[condition_data[second_order_conditions] == condition2]
                results[f"{condition1}_{condition2}"] = self._metrics_for_data(condition_data, acc_column)

        df = self._results_to_dataframe(results)
        df[f"{self.exp_id}_omission_rate"] = overall_omission_rate
        return df

    def _results_to_dataframe(self, results):
        data = []
        for condition, metrics in results.items():
            row = {
                "subject": self.participant_id,
                f"{self.exp_id}_{condition}_acc": metrics["acc"],
                f"{self.exp_id}_{condition}_rt": metrics["avg_rt"]
            }
            data.append(row)
        df = pd.DataFrame(data).set_index("subject")
        combined_df = df.groupby('subject').first().reset_index()
        return combined_df
