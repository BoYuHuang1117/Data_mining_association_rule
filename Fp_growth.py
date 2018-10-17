# Author: BoYu Huang 
# Date: 2018/10/2
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
        #683rows - 15 secs

    # make every transaction in each list which is contained by a big list
    dataset_list = []
    for i in range(dataset['Code'].nunique()):
        dataset_list.append(list(dataset['items'][dataset['Code'] == i+1]))
    
    return dataset_list
    
def generateL1(dataset_list,min_support):
    # create L1 in a huge list 
    L1 = []
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
    
    # To convert initial transaction into frozenset
    #retDict = {}
    #for trans in new_dataset_list:
        #retDict[frozenset(trans)] = 1
    return new_dataset_list
    
class Treenode:
    def __init__(self,name,num,parentNode):
        self.item = name
        self.count = num
        self.nodeLink = None   # junp to next node with the same item 
        self.parent = parentNode
        self.children = {}
        
    def up(self):
        """ 
        count will increase by one, once it is found in each transaction 
        """
        
        self.count += 1
    def show(self):
        """ 
        This function will show the entire tree 
        """
        
        print(self.item, self.count)
        for child in self.children.values():
            child.show()
            
            
def create_FPTree(dataset_list, min_support):
    """
    create FPTree and HeaderTable
    """
    # dataset_list: data in list or ? (frozenset) 
    
    HeaderTable = generateL1(dataset_list, min_support)
    order_dataset = new_dataset(dataset_list, HeaderTable)
    sorted_dictL1 = set(HeaderTable.keys())
    
    if len(sorted_dictL1) == 0:
        return None, None
    
    for k in HeaderTable:
        HeaderTable[k] = [HeaderTable[k], None]
    
    retTree = Treenode('Null Set',1,None)
    for dataset in order_dataset:
        #dataset is the ordered itemsets in each transactions
        updateTree(dataset, retTree, HeaderTable)
    
    return retTree, HeaderTable
    
def updateTree(itemset, FPTree, HeaderTable):
    # itemset: ordered_itemset in certain transaction
    if itemset[0] in FPTree.children:
        FPTree.children[itemset[0]].up()
    else:
        FPTree.children[itemset[0]] = Treenode(itemset[0], 1, FPTree)

        if HeaderTable[itemset[0]][1] == None:
            HeaderTable[itemset[0]][1] = FPTree.children[itemset[0]]
        else:
            update_NodeLink(HeaderTable[itemset[0]][1], FPTree.children[itemset[0]])
    
    if len(itemset) > 1:
        updateTree(itemset[1::],FPTree.children[itemset[0]],HeaderTable)
    
def update_NodeLink(Test_Node, Target_Node):
    # To update the link between nodes contain same item in FP Tree
    
    while (Test_Node.nodeLink != None):
        Test_Node = Test_Node.nodeLink

    Test_Node.nodeLink = Target_Node
    
def uptransverse(Node, prefixpath):
    """
    This function is to find the whole parent node of certain node
    """
    while (Node.parent !=None):
        prefixpath.append(Node.item)
        uptransverse(Node.parent,prefixpath)
    
def prefix_path(basepatt, Treenode):
    # basepatt: frequent one item
    # Use nodelink to traceback each same-item node in the tree
    cond_patt_base = {}
    
    while Treenode != None:
        # Until the same item reach its last appearance in the tree
        prefixpath = []
        uptransverse(Treenode, prefixpath)
        if len(prefixpath) > 1:
            cond_patt_base[forzenset(prefixPath[1:])] = Treenode.count
        Treenode = Treenode.nodeLink
    
    return cond_patt_base
    
    
def Mining (FPTree, HeaderTable, min_support, prefix, frequent_itemset):
    L1 = list(HeaderTable.keys())
    for basePat in L1:
        new_frequentset = prefix.copy()
        new_frequentset.add(basePat)
        # add frequent itemset to final list of frequent itemsets
        frequent_itemset.append(new_frequentset)
        
        # get all conditional pattern bases for item or itemsets
        Conditional_pattern_bases = prefix_path(basePat, HeaderTable[basePat][1])
        # call FP Tree construction to make conditional FP Tree
        Conditional_FPTree, Conditional_header = create_FPTree(Conditional_pattern_bases,min_support)

        if Conditional_header != None:
            Mine_Tree(Conditional_FPTree, Conditional_header, min_support, new_frequentset, frequent_itemset)
    
    
dataset_list = loadIBM()
min_support = float(0.6*len(dataset_list))

start = time.time()

FPtree, HeaderTable = create_FPTree(dataset_list, min_support)

frequent_itemset = []
Mining(FPtree,HeaderTable, min_support, set([]), frequent_itemset)
end = time.time()

print("Time Taken is:")
print(end-start)
print("All frequent itemsets:")
print(frequent_itemset)