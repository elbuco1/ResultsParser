import json 
import csv 
import numpy as np
import pandas as pd 
import os 
import helpers.helpers as helpers

class ResultsParser():
    def __init__(self,parameters_path):
        self.parameters = json.load(open(parameters_path))
        self.models_path = self.parameters["models_path"]+"{}/losses.json"
        self.outputs_path = self.parameters["outputs_path"]+"{}.csv"

        self.losses_dict = self.parameters["losses_dict"]
        self.models_dict = self.parameters["models_dict"]
        self.models_list = self.parameters["models_list"]
        self.scenes_list = self.parameters["scenes_list"]
        self.losses_list = self.parameters["losses_list"]
        self.decimals = self.parameters["decimals"]
        self.metrics_to_percentage = self.parameters["metrics_to_percentage"]

    def temp(self):
        
            df = self.__parse()
            print(df)
    def __parse(self):            
        for loss in self.losses_list:

            df = pd.DataFrame(
                np.zeros( ( len(self.scenes_list), len(self.models_list) ) ),
                index=self.scenes_list,columns = self.models_list
                )
            for scene in self.scenes_list:
                for model in self.models_list:
                    model_metrics = json.load(open(self.models_path.format(model)))


                    # if "unjoint" in loss or "disjoint" in loss:
                    if loss in self.metrics_to_percentage:
                        df.loc[scene,model] = helpers.truncate(float(model_metrics[scene][loss]),4)*100
                    else:
                        df.loc[scene,model] = helpers.truncate(float(model_metrics[scene][loss]),4)
            print(df)
        return None

    


