# Author: BoYu Huang 
# Date: 2018/10/2
# Finished: 2018/10/14
#The Apriori algorithm principle says that if an itemset is frequent, 
#then all of its subsets are frequent.this means that if {0,1} is frequent, 
#then {0} and {1} have to be frequent.

#The rule turned around says that if an itemset is infrequent, then its supersets are also infrequent.

import pandas as pd 
import time
###### Apriori algorithm in association rule
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
        #29024rows - 10 mins

    # make every transaction in each list which is contained by a big list
    dataset_list = []
    for i in range(dataset['Code'].nunique()):
        dataset_list.append(list(dataset['items'][dataset['Code'] == i+1]))
    
    #D is a dataset in the setform.
    D = list(map(set,dataset_list))
    
    return D
    
def generateC1(dataset_list):
    # create C1 in frozen set
    C1 = []
    for itemsets in dataset_list:
        for item in itemsets:
            if not [item] in C1:
                C1.append([item])
        
    C1.sort()# must do before brute force
    set_c1 = list(map(frozenset,C1))
    
    return set_c1

# Turning the C(i) into L(i) by Searching the data base 

def check_freq(dataset_list,Ck,min_support):
    # dataset_list: dataset packaged by each transaction
    # Ck: cand_set
    # min_support: minimum support of each set (%)
    
    ssCnt = {}
    for tid in dataset_list:
        for can in Ck:
            if can.issubset(tid):
                if not can in ssCnt: ssCnt[can]=1
                else: ssCnt[can] += 1
    numItems = float(len(dataset_list))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= min_support:
            retList.insert(0,key)
        supportData[key] = support
        #example input: suppData[frozenset({4})]
    return retList, supportData

def apriori_gen(Lk,k):
    # Lk: (k-1) frequent itemset (data type: set)
    # k: size of the itemsets
    cand_set = []
    len_f = len(Lk)
    for i in range(len_f):
        for j in range(i+1,len_f):
            f1 = list(Lk[i])[:k-2]
            #list(L1[i])[:0]=[]
            f2 = list(Lk[j])[:k-2]
            f1.sort();f2.sort()
            if f1==f2:
                cand_set.append(Lk[i] | Lk[j]) 
    
    return cand_set
    
dataset_list = loadIBM()

start = time.time()
C1 = generateC1(dataset_list)
L1,support = check_freq(dataset_list,C1,min_support = 0.6)
All_freq_set = [L1]
k = 2

while (len(All_freq_set[k-2]) > 0):
    Ck = apriori_gen(All_freq_set[k-2],k)
    Lk,supportk = check_freq(dataset_list,Ck,min_support = 0.6)
    support.update(supportk)
    All_freq_set.append(Lk)
    
    k += 1
    
end = time.time()

print("Time Taken is:")
print(end-start)
print("All frequent itemsets:")
print(All_freq_set)