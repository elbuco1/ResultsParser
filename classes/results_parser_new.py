import json 
import csv 
import numpy as np
import pandas as pd 
import os 
import helpers.helpers as helpers

class ResultsParser():
    def __init__(self,parameters_path):
        self.parameters = json.load(open(parameters_path))
        self.losses = self.parameters["models_path"]+"{}/losses.json"
        self.dynamic_losses = self.parameters["models_path"]+"{}/dynamic_losses.json"

        self.outputs_path = self.parameters["outputs_path"]+"{}.txt"

        self.losses_dict = self.parameters["losses_dict"]
        self.models_dict = self.parameters["models_dict"]
        self.models_list = self.parameters["models_list"]
        self.scenes_list = self.parameters["scenes_list"]
        self.losses_list = self.parameters["losses_list"]
        self.decimals = self.parameters["decimals"]
        self.metrics_to_percentage = self.parameters["metrics_to_percentage"]
        self.table_name = self.parameters["table_name"]
        self.dynamic_list = self.parameters["dynamic_losses"]

    def json_to_latex(self):
        df = self.__parse()
        # df = self.__parse()
        new_columns = [ self. models_dict[c] for c in df.columns]
        new_columns = [ "\\textit{"+ c + "}" for c in new_columns]

        new_index = [ self. losses_dict[c] for c in df.index]
        new_index = [ "\\textit{"+ c + "}" for c in new_index]

        df.columns = new_columns        
        df.index = new_index

        
        latex_table = df.to_latex(escape=False, column_format = self.__get_header() )

        latex_table = latex_table.replace("\\toprule","\\hline",1)
        latex_table = latex_table.replace("\\midrule","\\hline",1)
        latex_table = latex_table.replace("\\bottomrule","\\hline",1)
        
        

        if os.path.exists(self.outputs_path.format(self.table_name)):
            os.remove(self.outputs_path.format(self.table_name))
        with open(self.outputs_path.format(self.table_name), "w") as output_file:
            output_file.write(latex_table)
            print(latex_table)
        
        
            
    # def __parse(self):  
    #     dataframes = []          
    #     for loss in self.losses_list:

    #         df = pd.DataFrame(
    #             np.zeros( ( len(self.scenes_list), len(self.models_list) ) ),
    #             index=self.scenes_list,columns = self.models_list
    #             )

    #         for scene in self.scenes_list:
    #             for model in self.models_list:
    #                 model_metrics = json.load(open(self.models_path.format(model)))

    #                 if loss in self.metrics_to_percentage:
    #                     df.loc[scene,model] = helpers.truncate(float(model_metrics[scene][loss])*100,self.decimals)
    #                 else:
    #                     df.loc[scene,model] = helpers.truncate(float(model_metrics[scene][loss]),self.decimals)
            
    #         mean_df = np.array(df.mean(axis=0).values)
    #         mean_df = np.array([helpers.truncate(v,self.decimals) for v in mean_df]).reshape(1,-1)
    #         mean_df = pd.DataFrame(mean_df,columns = self.models_list, index = ["Moyenne"])
    #         df = df.append(mean_df)
    #         df = self.__bold_minimum_values(df)
    #         dataframes.append(df)
            
    #     df_result = self.__merge_dataframes(dataframes)  
    #     return df_result

    def __parse(self):  

        df = pd.DataFrame(
            np.zeros( ( len(self.losses_list), len(self.models_list) ) ),
            index=self.losses_list,columns = self.models_list
            )
        for model in self.models_list:
            for loss in self.losses_list:
                if loss in self.dynamic_list:
                    model_metrics = json.load(open(self.dynamic_losses.format(model)))
                    df.loc[loss,model] = helpers.truncate(float(model_metrics[loss]["global"]),self.decimals)


                else:
                    model_metrics = json.load(open(self.losses.format(model)))

                    if loss in self.metrics_to_percentage:
                        df.loc[loss,model] = helpers.truncate(float(model_metrics["global"][loss])*100,self.decimals)
                    else:
                        df.loc[loss,model] = helpers.truncate(float(model_metrics["global"][loss]),self.decimals)
        
        df = self.__bold_minimum_values(df)
        return df

        # dataframes = []          
        # for loss in self.losses_list:

        #     df = pd.DataFrame(
        #         np.zeros( ( len(self.scenes_list), len(self.models_list) ) ),
        #         index=self.scenes_list,columns = self.models_list
        #         )

        #     for scene in self.scenes_list:
        #         for model in self.models_list:
        #             model_metrics = json.load(open(self.models_path.format(model)))

        #             if loss in self.metrics_to_percentage:
        #                 df.loc[scene,model] = helpers.truncate(float(model_metrics[scene][loss])*100,self.decimals)
        #             else:
        #                 df.loc[scene,model] = helpers.truncate(float(model_metrics[scene][loss]),self.decimals)
            
        #     mean_df = np.array(df.mean(axis=0).values)
        #     mean_df = np.array([helpers.truncate(v,self.decimals) for v in mean_df]).reshape(1,-1)
        #     mean_df = pd.DataFrame(mean_df,columns = self.models_list, index = ["Moyenne"])
        #     df = df.append(mean_df)
        #     df = self.__bold_minimum_values(df)
        #     dataframes.append(df)
            
        # df_result = self.__merge_dataframes(dataframes)  
        # return df_result


    def __bold_minimum_values(self,df):
        maxs = df.idxmin(axis = 1)        
        for max_,id_ in zip(maxs, df.index):
            df.loc[id_,max_] = "\\textbf{"+ str(df.loc[id_,max_]) + "}"
        return df
       
    def __merge_dataframes(self,dataframes):

        merged = pd.DataFrame(
                np.zeros( ( len(self.scenes_list) + 1, len(self.models_list)  ) ),
                index=self.scenes_list + ["Moyenne"],columns = self.models_list
                )

        for row in merged.index:
            for column in list(merged.columns):
                losses_values = []
                for df in dataframes:
                    losses_values.append( df.loc[row,column])
                losses_values = self.merge_values(losses_values)
                merged.loc[row,column] = losses_values
        return merged
    def __get_header(self):
        header = "|l||"
        for i in range(len(self.models_list)):
            header += "c|"
        return header


    def merge_values(self,values):
        out_str = ""
        for i,value in enumerate(values):
            value = str(value)
            out_str += value
            if i < len(values) - 1:
                out_str += "/"
        return out_str