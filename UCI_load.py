# BoYuHuang
# Date: 2018/10/21

# datasource: https://archive.ics.uci.edu/ml/datasets/Absenteeism+at+work
import pandas as pd
from numpy import median

def loaddUCI():
    dataset = pd.read_csv('Absenteeism_at_work.csv')
    
    ignore_cols = ["Reason for absence", "Month of absence", "Seasons", "Transportation expense","Service time", "Age"]
    ignore_cols.extend(["Social smoker","Pet","Weight","Height","Body mass index","Work load Average/day ", "Hit target", "Son"])
    dataset.drop(columns = ignore_cols, inplace=True)
    
    Dist_median = median(dataset["Distance from Residence to Work"])
    average_time = round(dataset["Absenteeism time in hours"].mean())
    
    L = []
    for i in range(len(dataset)):
        L.append([])
        if dataset["Absenteeism time in hours"][i] > average_time:
            L[i].append(1)
        L[i].append(dataset["Day of the week"][i])
        if dataset["Distance from Residence to Work"][i] > Dist_median:
            L[i].append(7)
        if dataset["Disciplinary failure"][i] == 1:
            L[i].append(8)
        if dataset["Education"][i] == 1:
            L[i].append(9)
        if dataset["Social drinker"][i] == 1:
            L[i].append(10)
            
    return L
    
# For Apriori algorithm
def setform(dataset_list):
    #D is a dataset in the setform.
    D = list(map(set,dataset_list))

# For Fp growth algorithm
def Tofrozenset(dataset):
    Dict = {}
    for tran in dataset:
        Dict[frozenset(tran)] = 0
    for tran in dataset:
        Dict[frozenset(tran)] += 1
    return Dict
    
