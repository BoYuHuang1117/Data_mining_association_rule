###### Brute force 
All_set = []
C1 = [[1],[2],[3],[4]]
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
min_support = 2

for set_group in All_set:
    for each_set in set_group:
        count = 0
        for tran_set in data_list:
            if [element for element in each_set if element in tran_set] == each_set:
                count = count + 1
                print(count)
        if count > min_support:
            print(each_set) 
            #del each_set
