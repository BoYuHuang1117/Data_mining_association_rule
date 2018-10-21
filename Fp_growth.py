# Author: BoYu Huang 
# Date: 2018/10/10
# Finished: 2018/10/20

import pandas as pd 
import time

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

    # make every transaction in each list which is contained by a big list
    dataset_list = []
    for i in range(dataset['Code'].nunique()):
        dataset_list.append(list(dataset['items'][dataset['Code'] == i+1]))
    
    return dataset_list
    
class Treenode:
    def __init__(self,name,num,parentNode):
        self.item = name
        self.count = num
        self.nextnode = None   # junp to next node with the same item 
        self.parent = parentNode
        self.children = {}
        
    def up_count(self,num):
        """ 
        count will increase by one, once it is found in each transaction 
        """
        self.count += num
        
def Tofrozenset(dataset):
    Dict = {}
    for tran in dataset:
        Dict[frozenset(tran)] = 0
    for tran in dataset:
        Dict[frozenset(tran)] += 1
    return Dict
    

# create the tree with initial node as null 
# dataset: {[tran1]:count1,[tran2]:count2,....}
def createTree(dataset, min_support):
    
    HeaderTable = {}
    for transaction in dataset:
        for item in transaction:
            HeaderTable[item] = HeaderTable.get(item,0) + dataset[transaction]
    for item in list(HeaderTable):
        if HeaderTable[item] < min_support:
            del HeaderTable[item]
        if item == 'Null':
            del HeaderTable['Null']
    
    order_Header = [v[0] for v in sorted(HeaderTable.items(),key = lambda p: p[1], reverse=True)]
    
    if len(order_Header) == 0:
        return None,None
    
    for item in HeaderTable:
        HeaderTable[item] = [HeaderTable[item],None] 
    
    tree = Treenode('Null',1,None) # Actually a node
    for transaction, count in dataset.items():
        order_set = [element for element in order_Header if element in transaction ]
        if len(order_set) > 0:
            update_tree(order_set, tree, HeaderTable, count)
            
    return tree, HeaderTable

# stretch down the branch (by each transaction/ branch)
def update_tree(order_set, treenode, HeaderTable, count):
    
    if order_set[0] not in treenode.children:
        treenode.children[order_set[0]] = Treenode(order_set[0], count, treenode)
        if (HeaderTable[order_set[0]][1] == None): # if current header is the rightmost node
            HeaderTable[order_set[0]][1] = treenode.children[order_set[0]]
        else:
            update_link(HeaderTable[order_set[0]][1], treenode.children[order_set[0]])
    else:
        treenode.children[order_set[0]].up_count(count)
        
    # move to the end of this branch (transaction)
    if len(order_set) > 1:
        update_tree(order_set[1:], treenode.children[order_set[0]], HeaderTable, count)
    
# different nodes contain same item must connect to each other through nextnode property in class Treenode
def update_link(current_node, next_node):
    
    # if current node is not the rightmost node, move to it 
    while current_node.nextnode != None:
        current_node = current_node.nextnode
        
    current_node.nextnode = next_node
    
# trace back from certain node to inital null node
def uptransverse(node, one_branch):
    one_branch.append(node.item)
    
    while node.parent != None:
        one_branch.append(node.parent.item)
        node = node.parent
    
# find all the prefix of certain node which construct a subtree throughout the mining
def find_subtree_patt(one_item, current_node):
    # current_node: it moves from leftmost to rightmost 
    # And using uptransverse to find each entire branch on each same-item node
    cond_pattern_bases = {}
    
    while current_node != None:
        one_branch = []
        uptransverse(current_node, one_branch)
        if len(one_branch) > 1: # this branch bigger than only 'Null'
            cond_pattern_bases[frozenset(one_branch[1:])] = current_node.count
        current_node = current_node.nextnode
    return cond_pattern_bases
    
# mining should implement from end node to the top 
# because there must be only one node on top of certain node 
# but there may be multiple nodes under certain node 
def mining(prenodes, tree, HeaderTable, min_support,frequent_set):
    if HeaderTable != None:
        one_itemset = [v[0] for v in sorted(HeaderTable.items(),key = lambda p: p[1][0])]
        for one_item in one_itemset:
            new_freq_set = prenodes.copy()
            new_freq_set.add(one_item)
        
            # add new frequent set into final frequent
            frequent_set.append(new_freq_set)
            # find all conditional pattern bases 
            cond_pattern_bases = find_subtree_patt(one_item, HeaderTable[one_item][1])
            # create subtree according to conditional pattern bases
            cond_tree, cond_header = createTree(cond_pattern_bases, min_support)
            
            if cond_header != None:
                mining(new_freq_set, cond_tree, cond_header, min_support, frequent_set)

dataset = loadIBM()
min_support = float(0.6*len(dataset))
dataset = Tofrozenset(dataset)

start = time.time()

Fptree, HeaderTable = createTree(dataset, min_support)

frequent_set = []
mining(set([]), Fptree, HeaderTable, min_support, frequent_set)

end = time.time()

print("Time Taken is:")
print(end-start)
print("All frequent itemsets:")
print(frequent_set)