# Author: BoYu Huang 
# Date: 2018/10/2
# Finished: 2018/10/20

###### FP growth in association rules
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
        #683rows - 15 secs

    # make every transaction in each list which is contained by a big list
    dataset_list = []
    for i in range(dataset['Code'].nunique()):
        dataset_list.append(list(dataset['items'][dataset['Code'] == i+1]))
    
    return dataset_list
    
def generateL1(dataset_list,min_support = 0.4):
    # create L1 in a huge list 
    L1 = []
    min_support = 0.4*len(dataset_list)
    for itemsets in dataset_list:
        for item in itemsets:
            if not item in L1:
                L1.append(item)
    
    # Dictionary 
    dictL1 = {}
    for i in range(len(L1)):
        count = 0
        for transaction in dataset_list:
            if L1[i] in transaction:
                count += 1
        if count >= min_support:
            dictL1[L1[i]] = count
        
    # Sorting the dictonary by value 
    import operator
    # A big list contains multiple tuple
    sorted_dictL1 = sorted(dictL1.items(),key=operator.itemgetter(1),reverse=True)
    
    # convert back to dictionary without losing the order 
    from collections import OrderedDict
    sorted_dictL1 = OrderedDict(sorted_dictL1)
    
    return sorted_dictL1
    
def new_dataset(dataset_list,sorted_dictL1):
    # Utilize keys in sorted_dictL1 to elminate non-frequent item in each transaction
    # And put transaction in sorted_dictL1 order
    freq_item_one = list(sorted_dictL1.keys())
    new_dataset_list = []
    for transaction in dataset_list:
        new_tran = list([element for element in freq_item_one if element in transaction])
        new_dataset_list.append(new_tran)
    
    return new_dataset_list
    
def :
    
    
    return 
    
def FPTree(new_dataset_list,):
    
    
    return 