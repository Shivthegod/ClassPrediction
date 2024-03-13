
import pandas as pd
import numpy as np
import networkx as nx

from itertools import chain, combinations
import time

def powerset(iterable, max=-1):
    
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))

def stateToString(state):
    s = sorted(state)
    return str(s)

def makeStateMachine(dag, time_limit_sec=20, timing_info=False):
    stime = time.time()
    iterations = 0
    timing=[[],[],[],[],0] #holds timing info for [whole iter, avail moves, move set, updateing graph, self loops(only 1 val)]
    newStates = []

    dag2 = nx.DiGraph()
    stateStack = [[]]
    
    edge_attrs = dict()
    
    while len(stateStack) > 0:
        t0 = time.time()
        
        #pick a state from stack
        s = stateStack.pop()
        
        
        #find all in-degree 0 nodes with state removed
        dagCopy = dag.copy()
        dagCopy.remove_nodes_from(s)
        degs = list(dagCopy.in_degree())
        moves = [x[0] for x in degs if x[1]==0]
        # moves = list(filter(lambda x: x!=-1, moves))
        t1 = time.time()
        
        #find power set of possible moves (not including no move)
        # was tuples, so convert to lists
        pSet = [list(x) for x in powerset(moves)]
        t2 = time.time()
        
        #for each move, append to current state, and add to stack
        for p in pSet:
            n = s.copy()
            n.extend(p)
            if(stateToString(n) not in dag2.nodes):
                stateStack.append(n)
            dag2.add_edge(stateToString(s), stateToString(n))
        
        #add to the edge attributes
        edge_attrs[stateToString(s), stateToString(n)] = {"new_classes": p}
        
        t3 = time.time() #timing for whole iteration
        #timing code
        
        timing[0].append(t3-t0) #timing of whole iteration
        timing[1].append(t1-t0) #timing of finding avaialable classes
        timing[2].append(t2-t1) #timing of generating power set
        timing[3].append(t3-t2) #timing of updating graph
        
        
        iterations+=1
        if (time.time()-stime) > time_limit_sec:
            break
    
    t4=time.time()
    
    
    #include self edges
    for n in dag2.nodes:
        dag2.add_edge(n,n)
        #add edge attrs for consistancy
        edge_attrs[n,n] = {"new_classes": []}
    
    #attatch the edge attributes
    nx.set_edge_attributes(dag2, edge_attrs)
    
    t5=time.time()
    
    timing[4] = t5-t4 #timing to add the self loops
    
    if timing_info:
        print(f'{len(dag2.nodes)} states found across {iterations} iterations.')
        print(f'Avg times for:')
        totTime = sum(timing[0])/iterations
        print(f'Iteration: {totTime} sec')
        print(f'Finding available Classes: {sum(timing[1])/iterations} sec ({sum(timing[1])/iterations / totTime *100}%)')
        print(f'Finding possible moves: {sum(timing[2])/iterations} sec ({sum(timing[2])/iterations / totTime *100}%)')
        print(f'Updating the Graph: {sum(timing[3])/iterations} sec ({sum(timing[3])/iterations / totTime *100}%)')
        print("")
        print(f'Time for adding self loops: {timing[4]} sec')
    return dag2
