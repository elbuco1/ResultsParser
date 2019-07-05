import json 
import csv 
import os 
import numpy as np

def truncate(number,n_decimal):
    number_td = int(number * 10**n_decimal)/10**n_decimal
    return number_td
def main():
    dirs = [d for d in os.listdir(".") if os.path.isdir(d)]
    print(dirs) 
    results_path = "./results.csv"
    if os.path.exists(results_path):
        os.remove(results_path)
    with open(results_path,"w") as r:
        writer = csv.writer(r)
        for model in dirs:
            losses_dic = {}
            writer.writerow([model])
            with open(model+"/losses.json") as f:
                losses = json.load(f)
                i = 0

                if not i:
                    row = ["",""]
                    for loss in losses[list(losses.keys())[0]]:
                        # if "unjoint" in loss or "disjoint" in loss:
                            
                        row.append(loss)
                        losses_dic[loss] = []
                    writer.writerow(row)    
                
                for scene in losses:
                    row = [""]
                    row.append(scene)

                    for loss in losses[scene]:
                        # if "unjoint" in loss or "disjoint" in loss:
                        if "social" in loss or "spatial" in loss:
                            row.append(truncate(float(losses[scene][loss]),4)*100)
                            losses_dic[loss].append(truncate(float(losses[scene][loss]),4)*100)
                        else:
                            row.append(truncate(float(losses[scene][loss]),4))
                            losses_dic[loss].append(truncate(float(losses[scene][loss]),4))

                    writer.writerow(row) 

                row_mean = ["","mean"]
                row_std = ["","std"]

                for key in losses_dic:
                    row_mean.append(np.mean(losses_dic[key]))
                    row_std.append(np.std(losses_dic[key]))

                
                writer.writerow([])
                writer.writerow(row_mean)
                writer.writerow(row_std)
                writer.writerow([])


if __name__ == "__main__":
    main()
