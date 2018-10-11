# Author: BoYu Huang 
# Date: 2018/10/8

###### Brute force 
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

# make every transaction in each list which is contained by a bug list
dataset_list = []
for i in range(dataset['Code'].nunique()):
    dataset_list.append(list(dataset['items'][dataset['Code'] == i+1]))
    
    
# create C1 in a huge list containing multiple sub-lists with single element inside
C1 = []
for transaction in dataset_list:
    for item in transaction:
        if not [item] in C1:
            C1.append([item])
        
C1.sort()# must do before brute force
# make every element encapsulated by list
for i in range(len(C1)):
    C1[i] = list([C1[i]])

All_set = []
#C1 = [[1],[2],[3],[4]]
All_set.append(C1)

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
                
                #print(All_set)
            del list_current

# check whether minimum support requirement is satisfied

#min_support = 2
freq_set = []
for set_group in All_set:
    for each_set in set_group:
        count = 0
        for tran_set in dataset_list:
            if [element for element in each_set if element in tran_set] == each_set:
                count = count + 1
                #print(count)
        if count > min_support:
            print(each_set) 
            freq_set.append(each_set)
            #del each_set

