#!/user/bin/env python
# Author: Duy Nguyen
# Solution to question 2,  homework 3
# Felsenstein's Algorithm
# You should be able to run the program as of the following commands
# python computeLikelihood tree.txt score.txt assign.txt


import sys
import io
import getopt
import operator

def read_score(filename):
    "Read score matrix from score.txt"
    # Initialize 2D list with dim = 4*4
    score = [[0 for x in range(4)] for y in range(4)]
    row = 0
    with open(filename, 'r') as file:
        file.readline() # omit the first line
        for line in file:
            vals = line.strip().split()
            score[row] = [float(vals[1]), float(vals[2]), float(vals[3]), float(vals[4])]
            row += 1
    return score

def read_tree(filename):
    "Read child/parent from tree.txt"
    # Initialize the dictionary to store child/parent relations
    relations = {}
    child = 0
    parent = 0
    with open(filename, 'r') as file:
        for line in file:
            #import pdb; pdb.set_trace()
            vals = line.strip().split()
            child = int(vals[0].strip('S'))
            parent = int(vals[1].strip('S'))
            relations[child] = parent
    return relations

def read_assign(filename):
    "Read assignments at leaf nodes from assign.txt"
    # Initialize the dictionary for assignments: NO space format s1=a
    assign = {}
    leaf = 0
    character = ''
    with open(filename, 'r') as file:
        for line in file:
            vals = line.strip().split()
    for i in range(len(vals)):
        leaf = int(vals[i][1])
        character = vals[i][3]
        assign[leaf] = character
    return assign

def nodeNum_Eval(relations):
    "Evaluate number of nodes for the given tree"
    foo = list(set(relations.keys() + relations.values()))
    return len(foo)

def inverseDict(Dict):
    "Inverse a dictionary, also for case of non-unique map. This is used for computing childrens of a given internal node"
    invDict = {}
    for k, v in Dict.iteritems():
        # This creates a list to store nodes of inverse map
        invDict[v] = invDict.get(v, [])
        invDict[v].append(k)
    return invDict

def addList(L1, L2):
    return [x + y for x, y in zip(L1, L2)]

def multList(L1, L2):
    return [x*y for x, y in zip(L1, L2)]

def mapEval(relations):
    "Create the mapping from node_unique (map key) to {1,..., nodeNum} (map value)"
    node_unique = list(set(relations.keys() + relations.values()))        
    mapping = {}
    index = 1
    for x in node_unique:
        mapping[x] = index
        index += 1 
    return mapping

def relabel(relations, mapping):
    "Relabel nodes in var relations to avoid the non-consecutive labeling case."
    relations_new = {}
    for k, v in relations.iteritems():
        relations_new[mapping[k]] = mapping[v]
    return relations_new

def relabel_assign(assign, mapping):
    "Relabel leaf nodes in var assign"
    assign_new = {}
    for k, v in assign.iteritems():
        assign_new.update({mapping[k]:v})
    return assign_new

def dictToTree(inv_relations, root):
    """convert inv_relations to Tree representation whose format is used in class BinTree
    inv_relations = {1:[2,5], 2:[3,4]} must start with root
    treeRep = [(1,2,5), (2,3,4)]
    """
    treeRep = []
    ii = 0
    ## root case
    children = inv_relations[root]
    if len(children) == 2:
        child1,child2 = children[0], children[1]
    else:
        child1,child2 = children[0], None
    treeRep.insert(ii, (root, child1, child2))
    ii +=1
    # Delete the key = root    
    inv_relations.pop(root, None)

    for i in range(len(inv_relations)):
        parent = inv_relations.items()[i][0]
        children = inv_relations.items()[i][1]
        if len(children) == 2:
            child1,child2 = children[0], children[1]
        else:
            child1,child2 = children[0], None
        treeRep.insert(ii, (parent, child1, child2))
        ii += 1
    return treeRep


class BinTree:
  """Node in a binary tree
##       1
##     2     3
##   4   5  6  7
##  8
  treeRep = [(1,2,3),(2,4,5),(3,6,7),(4,8,None)]
  tree= BinTree.createTree(treeRep)
  tree.printBfsLevels()
>>>
1 

2 3 

4 5 6 7 

  """
  def __init__(self,val,leftChild=None,rightChild=None,root=None):
    self.val=val
    self.leftChild=leftChild
    self.rightChild=rightChild
    self.root=root
    if not leftChild and not rightChild:
      self.isExternal=True

  def getChildren(self,node):
    children=[]
    if node.isExternal:
      return []
    if node.leftChild:
      children.append(node.leftChild)
    if node.rightChild:
      children.append(node.rightChild)
    return children

  @staticmethod
  def createTree(tupleList):
    "Creates a Binary tree Object from a given Tuple List"
    Nodes={}
    root=None
    for item in treeRep:
      if not root:
        root=BinTree(item[0])
        root.isExternal=False
        Nodes[item[0]]=root
        root.root=root
        root.leftChild=BinTree(item[1],root=root)
        Nodes[item[1]]=root.leftChild
        root.rightChild=BinTree(item[2],root=root)
        Nodes[item[2]]=root.rightChild
      else:
        CurrentParent=Nodes[item[0]]
        CurrentParent.isExternal=False
        CurrentParent.leftChild=BinTree(item[1],root=root)
        Nodes[item[1]]=CurrentParent.leftChild
        CurrentParent.rightChild=BinTree(item[2],root=root)
        Nodes[item[2]]=CurrentParent.rightChild
    root.nodeDict=Nodes
    return root

  def printBfsLevels(self, levels=None):
      """  
      order nodes in tree from top to bottom and save it in variable store
      treeRep = [(1,2,5),(2,3,4)]
      tree = BinTree.createTree(treeRep)
      tree.printBfsLevels()
      
"""
      global store
      global index
      if levels==None:
          levels=[self]
      nextLevel=[]
      for node in levels:
          store.insert(index, node.val)
          index += 1
      for node in levels:
          nextLevel.extend(node.getChildren(node))
      if nextLevel:
          node.printBfsLevels(nextLevel)

def sort_IntNodes(store, leaves):
    "Sort intNodes from Bottom level to top level"
    intNodes = store
    for x in leaves:
        intNodes.remove(x)
    return intNodes[::-1]

def likelihoodEval():
    pass

def findRoot(inv_relations, nodeNum):
    "find root of the given tree"
    ii = 0
    root = -1
    childSet_unlist = []
    childSet = inv_relations.values()
    parentSet = inv_relations.keys()
    for i in range(len(childSet)):
        if len(childSet[i])==2:
            x1, x2 = childSet[i][0], childSet[i][1]
            childSet_unlist.insert(ii, x1)
            ii += 1
            childSet_unlist.insert(ii, x2)
            ii += 1
        else:
            childSet_unlist.insert(ii, childSet[i][0])
            ii += 1
    root = list(set(range(1,nodeNum+1)) - set(childSet_unlist) )[0]
    return root

def costEval(score, relations, assign, store, root):
    "Evaluate the cost/likelihood matrix by the weighted parsimony algorithm"
    ### Initialize, relabeling, and find root of tree
    leaves = []
    relations_new = {}
    assign_new = {}
    mapping = {}
    nodeLevel = []
    # Evaluate number of nodes
    nodeNum = nodeNum_Eval(relations)
    # Create the mapping for relabeling
    mapping = mapEval(relations)
    # Relabel nodes in relations
    relations_new = relabel(relations, mapping)
    # Relabel leaves in assign
    assign_new = relabel_assign(assign, mapping)
    # root of tree
    root = list( set(range(1,nodeNum+1)) - set(relations_new.keys()))[0]
    
    ### Initialize the Cost Matrix. Ordering as score matrix:  Col1 = 'a', Col2 = 'c', Col3 = 'g', Col4 = 't'
    index = {'a':1, 'c':2, 'g':3, 't':4}
    Cost = [[0 for x in range(4)] for y in range(nodeNum)]
    # Initialize the Cost(leaf)
    for x in assign_new:
        leaves.append(x)
        Cost[x-1] = [0, 0, 0, 0]
        Cost[x-1][index[assign_new[x]]-1] = 1
    ### Evaluate Cost matrix for internal nodes
    intNodes = sort_IntNodes(store, leaves)
    inv_relations = inverseDict(relations_new)
    # start i from bottom of intNodes
    for i in intNodes:
        child1, child2 = inv_relations[i][0], inv_relations[i][1]
        for j in range(4):
            #import pdb; pdb.set_trace()
            sum1 = sum( multList(score[j], Cost[child1 - 1]))
            sum2 = sum( multList(score[j], Cost[child2 - 1]))
            Cost[i-1][j] = sum1 * sum2
            # # for debugging
            # print "+++ parent node=%s, child1=%s, child2=%s" % (i, child1, child2)
            # print("+++ score[j] = ", score[j])
            # print("+++ Cost[child1 - 1] = ", Cost[child1-1])
            # print("+++ Cost[child2 - 1] = ", Cost[child2-1])
            # #
            #Cost[i-1][j] = min1 + min2
    #print(Cost)
    prob = 0.25 * sum(Cost[root-1])
    # print "Cost of the tree = %s" % prob 
    return prob

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hg:d", ["help", "grammar="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    
    File_tree = args[0]
    File_score = args[1]
    File_assign = args[2]
    return [File_tree, File_score, File_assign]



if __name__ == '__main__':
    Files = main(sys.argv[1:])
    File_tree = Files[0]
    File_score = Files[1]
    File_assign = Files[2]
    ### Error Handlings
    ### Main ###
    # store = level of nodes in tree from top to bottom
    store = []
    # index = keep track of index in variable store
    index = 0
    # Initialize root
    root = 0
    score = read_score(File_score)
    relations = read_tree(File_tree)
    assign = read_assign(File_assign)
    # compute inv_relations
    mapping = mapEval(relations)
    relations_new = relabel(relations, mapping)
    inv_relations = inverseDict(relations_new)
    nodeNum = nodeNum_Eval(relations)
    root = findRoot(inv_relations, nodeNum)
    # Compute level of tree's nodes and save it in variable store
    treeRep = dictToTree(inv_relations, root)
    tree = BinTree.createTree(treeRep)
    tree.printBfsLevels()
    root = store[0]
    # Main Function: Compute Cost matrix
    final_prob = 0
    final_prob = costEval(score, relations, assign, store, root)
    print "The likelihood of the sequence is %s" % final_prob
