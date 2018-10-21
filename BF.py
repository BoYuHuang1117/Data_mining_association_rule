# Author: BoYu Huang 
# Date: 2018/10/8

import pandas as pd 
import time

###### Brute force 
def loadIBM(filename='data.ntrans_0.1.nitems_0.01'):
    # Preprocessing the disorganized data (each transaction was already sorted )
    # which was created by IBM
    
    dataset = pd.read_csv(filename)
    dataset.columns = ['items']

    num_trans = []
    for patterns in dataset['items']:
        num_trans.append(int(patterns.split()[0]))
    
    dataset['Code'] = num_trans

    for i in range(len(dataset['items'])):
        dataset['items'][i] = int(dataset['items'][i].split()[2])

    # make every transaction in each list which is contained by a big list
    dataset_list = []
    for i in range(dataset['Code'].nunique()):
        dataset_list.append(list(dataset['items'][dataset['Code'] == i+1]))
    
    return dataset_list

def generateC1(dataset_list):
    # create C1 in a huge list containing multiple sub-lists with single element inside
    C1 = []
    for itemsets in dataset_list:
        for item in itemsets:
            if not [item] in C1:
                C1.append([item])
        
    C1.sort()# must do before brute force
    
    return C1
#C1 = [[1],[2],[3],[4]...]

# make every element encapsulated by list
#for i in range(len(C1)):
#    C1[i] = list([C1[i]])

def createALL(All_set,C1):
# create all possible frequent itemset
    for i in range(len(C1)-1):
        All_set.append([])
        #print("i=",i)
        for l_current in All_set[i]:
            for item in C1:
                # only single element needs to transfer to list
                if type(l_current) is int:
                    list_current = list([l_current])
                else:
                    list_current = l_current.copy()
                    
                if item[-1] > list_current[-1]:
                    list_current.append(item[-1])
                    All_set[i+1].append(list_current)
                    
                del list_current
    return All_set

def check_freq(dataset_list, All_set,min_support = 0.6):
    # check whether minimum support requirement is satisfied
    # min_support = 0.6
    freq_set = []
    numItems = float(len(dataset_list))
    for set_group in All_set:
        for each_set in set_group:
            count = 0
            for tran_set in dataset_list:
                if [element for element in each_set if element in tran_set] == each_set:
                    count = count + 1
            if count/numItems >= min_support:
                freq_set.append(each_set)

    return freq_set
    
    
dataset_list = loadIBM()

start = time.time()
C1 = generateC1(dataset_list)
All_set = []
All_set.append(C1)
All_set = createALL(All_set,C1)
freq_set = check_freq(dataset_list,All_set)
end = time.time()

print("Time Taken is:")
print(end-start)
print("All frequent itemsets:")
print(freq_set)