import networkx as nx


def getPrereqGraph(file = 'prereqs2021.txt'):
    G = nx.DiGraph()

    with open(file) as fp:
        lines = fp.readlines()

    classes = set()
    for line in lines:
        split = line.split(" ")
        classes.add(split[0].replace("\n", ""))
        classes.add(split[1].replace("\n", ""))

    G.add_nodes_from(classes)

    for line in lines:
        split = line.split(" ")
        G.add_edge(split[0].replace("\n", ""), split[1].replace("\n", ""))
    
    return G