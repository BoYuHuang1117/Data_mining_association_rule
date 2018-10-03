# Author: BoYu Huang 
# Date: 2018/10/2


dataset = pd.read_csv('data')

# Preprocessing the disorganized data (each transaction was already sorted )
# which was created by IBM
dataset.columns = ['items']

num_trans = []
for patterns in df['items']: 
    num_trans.append(int(patterns.split()[0]))
    
df['Code'] = num_trans

for i in range(len(dataset['items'])):
    dataset['items'][i] = int(dataset['items'][i].split()[2])
    #29024rows - 10 mins

# 把同一個 transaction 存成一個個list，用一個大list包著
dataset_list = []
for i in range(dataset['Code'].nunique()):
    dataset_list.append(list(dataset['items'][dataset['Code'] == i+1]))
    
    
# create C1 in frozen set
C1 = []
for transaction in dataset_list:
    for item in transaction:
        if not [item] in C1:
            C1.append([item])
        
C1.sort()
set_c1 = list(map(frozenset,C1))

# Turning the C(i) into L(i) by Searching the data base 

def check_freq(dataset_list,Ck,min_support):
    # dataset_list: dataset packaged by each transaction
    # Ck: cand_set
    # min_support: minimum support of each set
    
    ssCnt = {}
    for tid in dataset_list:
        for can in Ck:
            if can.issubset(tid):
                if not can in ssCnt: ssCnt[can]=1
                else: ssCnt[can] += 1
    
    
    return 
######

freq_set = df['items'][df['itmes'] > min_support]

for i in range(1,num_items):
    min_support = 500
    cand_set[i+1] = apriori_gen(freq_set[i],i+1)
    for transaction in DB:
        cand_trans[i] = subset(cand_set,transaction)
        cand_trans[i].nunique()
    freq_set[i] = cand_trans[i](cand_trans.nunique() > min_support)
    
def apriori_gen(freq_set,k):
    # freq_set: frequent itemset (data type: set)
    cand_set = []
    len_f = len(freq_set)
    for i in range(len_f):
        for j in range(i+1,len_f):
            f1 = list(freq_set[i])[:k-2]
            f2 = list(freq_set[j])[:k-2]
            f1.sort();f2.sort()
            if f1==f2:
                cand_set.append(freq_set[i] | freq_set[j]) 
    
    return cand_set
    
def subset(cand_set, transaction):
    # cand_set: candidata itemset
    # transaction: total transaction itemset
    
    
    
    return cand_trans
    
def min_conf(m,p):
    # m: number of superset satisfied minimum support 
    # p: number of subset satisfied minimum support 
    confidence = m/p
    return True

def min_sup(s,L):
    # s: number of support transaction
    # L: number of total transaction
    support = s/L
    return True
    
