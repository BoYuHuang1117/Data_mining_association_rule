# Author: BoYu Huang 
# Date: 2018/10/10
# Finished: 2018/10/21

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
        #683rows - 15 secs

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
    for tran in dataSet:
        retDict[frozenset(tran)] = 1
    return retDict
    

# create the tree with initial node as null 
# dataset: {[tran1]:count1,[tran2]:count2,....}
def createTree(dataset, min_support):
    
    HeaderTable = {}
    for transaction in dataset:
        for item in transaction:
            HeaderTable[item] = HeaderTable.get(item,0) + dataset[transaction]
    for item in HeaderTable:
        if HeaderTable[item] < min_support:
            del HeaderTable(item)
    
    order_Header = [v[0] for v in sorted(HeaderTable.item(),key = lambda p: p[1], reverse=True)]
    
    if len(order_Header) == 0:
        return None,None
    
    for item in HeaderTable:
        HeaderTable[item] = [HeaderTable[item],None] 
    
    tree = Treenode('Null',1,None) # Actually a node
    for transaction, count in dataset.trans():
        order_set = [element for element in order_Header if element in transaction ]
        if len(order_set) > 0:
            update_tree(order_set, tree, HeaderTable, count)
            
    return tree, HeaderTable

# stretch down the branch (by each transaction/ branch)
def update_tree(order_set, treenode, HeaderTable, count):
    
    if item not in treenode.children:
        treenode.children[item] = Treenode(item, count, treenode)
        if (HeaderTable[item][1] == None): # if current header is the rightmost node
            HeaderTable[item][1] = treenode.children[item]
        else:
            update_link(HeaderTable[item][1], treenode.children[item])
    else:
        treenode.children[item].up_count(count)
        
    # move to the end of this branch (transaction)
    
    
# different nodes contain same item must connect to each other through nextnode property in class Treenode
def update_link(current_node, next_node):
    
    # if current node is not the rightmost node, move to it 
    while current_node.nextnode != None:
        current_node = current_node.nextnode
        
    current_node.nextnode = next_node
    
# trace back from certain node to inital null node
def uptransverse():
    
    
    
# find all the prefix of certain node which construct a subtree throughout the mining
def find_subtree_patt():
    
    
    
    return cond_pattern_base
    
    
# 
def mining(prenode, tree, HeaderTable, min_support,frequent_set):
    
    
    

dataset = loadIBM()
min_support = float(0.6*len(dataset))
dataset = Tofrozenset(dataset)

start = time.time()

Fptree, HeaderTable = createTree(dataset, min_support)

frequent_set = []
mining(set([]), Fptree, HeaderTable, min_support, frequent_set)

end = time.time()

