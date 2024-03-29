import PreReqs
import StateMachine as sm
import FrequentistFitting as ffit
import random
import networkx as nx
from collections import defaultdict

#get the model
dag = PreReqs.getPrereqGraph()
G = sm.makeStateMachine(dag)

# print(G.edges)

#this is to generate random data with assumed Beta values
ffit.addRandomBetaTerms(G)
data = ffit.generate_random_data(G, 1000)

#fit the model to the data
ffit.fit_frequentist(G, data)

#Predict registration numbers
def predict_students_registered(current_state, state_machine_graph):
    predicted_students = defaultdict(int)

    #Loop through each edge in the state machine
    for source, target, data in state_machine_graph.edges(data=True):
        beta = data.get('beta', 0)
        new_classes = data.get('new_classes', [])

        #Update new classes based on the source node beta ignoring self edges
        # (source != '[]') &
        if (source != target):
            for class_ in new_classes:
                change = current_state.get(source, 0) * beta
                predicted_students[class_] += change

    return predicted_students

#For testing with a random current state
def generate_random_numbers(graph):
    random_numbers = {}
    for node in graph.nodes():
        random_numbers[node] = random.randint(1, 10)  # Generate a random number of students for each state
    return random_numbers

#generate random current state
current_state = generate_random_numbers(G)

predicted_students = predict_students_registered(current_state, G)
print(predicted_students)