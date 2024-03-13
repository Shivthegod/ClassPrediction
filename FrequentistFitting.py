import networkx as nx
import random as rand
import pandas as pd
import numpy as np
import StateMachine as sm

def pretty_print(G: nx.digraph, labels=True, layout=nx.planar_layout):
    pos = layout(G)
    nx.draw(G, pos, with_labels=labels)
    e_labels = nx.get_edge_attributes(G, "beta")
    for e in e_labels:
        e_labels[e] = format(e_labels[e], ".2f")
    nx.draw_networkx_edge_labels(G, pos, edge_labels = e_labels)
    
def addRandomBetaTerms(G: nx.digraph, self_factor=1/10):
    #for each node, with out-degree k, generate k random weights
    betas = dict()
    
    for n in G.nodes:
        neighbors = list(nx.neighbors(G,n))
        k = len(neighbors)
        beta = [rand.random() for x in range(k)] #generates a set of k random numbers
        
        #reduce the self loop
        if n in neighbors:
            beta[neighbors.index(n)]*=self_factor
    
        beta = [x/sum(beta) for x in beta] #normalize the vector to constrain the sum (not totally uniform, but good enough)
        for i, nei in enumerate(neighbors):
            betas[n, nei] = {"beta":beta[i]}
    
    nx.set_edge_attributes(G, betas)
    
def extract_beta(G: nx.digraph):
    beta = dict()
    e_weights = nx.get_edge_attributes(G, "beta")
    for n in G.nodes:
        k = list(nx.neighbors(G, n))
        w = [e_weights[n,x] for x in k]
        beta[n] = {"neighbors": k, "betas": w}
    return beta

def generate_random_data(G: nx.digraph, n: int):
    
    
    #find start and end of the graph
    g = G.copy()
    for x in g.nodes:
        if (x,x) in g.edges:
            g.remove_edge(x,x)
    topo = list(nx.topological_sort(g))
    start = topo[0]
    end = topo[len(topo)-1]
    print(f'Detected path {start} -> {end}')
    
    # create the data structure
    data = pd.Series(data=[pd.Series() for i in range(n)])
    
    #make a random path
    beta = extract_beta(G)
    for i in range(len(data)):
        n = start
        arr = [n]
        while not n == end:
            n = rand.choices(beta[n]["neighbors"], weights=beta[n]['betas'])[0]
            arr.append(n)
        data[i]=pd.Series(arr)
    return data


def residuals(betaActual, betaExpected, returnDict=True):
    residDict = dict()
    
    for a in betaActual.keys():
        residDict[a] = {'neighbors': betaActual[a]['neighbors'], 'betas': []}
        
        for b in betaActual[a]['neighbors']:
            vA = betaActual[a]['betas'][betaActual[a]['neighbors'].index(b)]
            vE = betaExpected[a]['betas'][betaExpected[a]['neighbors'].index(b)]
            residDict[a]['betas'].append(vA - vE)
        
    if returnDict:
        return residDict
    
    residArr = []
    for x in residDict.keys():
        residArr.extend(residDict[x]['betas'])
    
    return residArr

def rmse(betaActual, betaExpected):
    resid =residuals(betaActual, betaExpected, returnDict=False)
    resid = [x**2 for x in resid]
    s = sum(resid) / len(resid)
    r = np.sqrt(s)
    return r

def parse_array(s):
    if s == '[]':
        return []
    r = s[2:-2]
    r = r.split("\', \'")
    return r
    
def parse_data(data):
    parsed = pd.Series(data=[pd.Series() for i in range(len(data))])
    for i in range(len(data)):
        arr = []
        for j in range(len(data[i])):
            arr.append(parse_array(data[i][j]))
        parsed[i] = pd.Series(data=arr)
    
    return parsed

def make_empty_beta(G):
    beta = dict()
    for n in G.nodes:
        neighbors = list(nx.neighbors(G,n))
        k = len(neighbors)
        betas = [0]*k
        beta[n]={'neighbors': neighbors, 'betas': betas}
    return beta

def fit_frequentist(G, data):
    # create beta structure for G
    beta = make_empty_beta(G)
    
    # parse out the data
    data = parse_data(data)
    
    #count up the amount of transitions
    for d in data:
        # each d is a Series of states
        #for each step, add 1 to each 
        for i in range(len(d)-1):
            curState = sm.stateToString(d[i])
            nextState = sm.stateToString(d[i+1])
            
            beta[curState]['betas'][beta[curState]['neighbors'].index(nextState)] += 1
    
    # find frequentist estimators
    beta_attr = dict()
    # NOTE: im using an altered Agresti-Coull estimator, made for any number of categories
    # it makes the assumption that with no data, there is an equal chance
    # Not an exact p = x/n estimator, but in the limit is equivalent
    # not sure if the statistical benefit extends to more categories, but heres hoping
    for n in beta.keys():
        counts = beta[n]['betas']
        s = sum(counts) + 2*len(counts)
        betaEst = [(c+2)/s for c in counts]
    
        #apply betaEstimators to the attr
        for i, ni in enumerate(beta[n]['neighbors']):
            beta_attr[n,ni] = {'beta': betaEst[i]}
    nx.set_edge_attributes(G,beta_attr)
    
    