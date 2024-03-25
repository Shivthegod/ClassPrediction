import networkx as nx
import PreReqs
import StateMachine as sm
import FrequentistFitting as ffit

#get the model
dag = PreReqs.getPrereqGraph()
G = sm.makeStateMachine(dag)

#this is to generate random data with assumed Beta values
ffit.addRandomBetaTerms(G)
data = ffit.generate_random_data(G, 1000)

#fit the model to the data
ffit.fit_frequentist(G, data)

def predict_students_registered(current_state, state_machine_graph):
    predicted_students = {class_: current_state.get(class_, 0) for class_ in current_state}

    #Loop through each edge in the state machine
    for u, v, data in state_machine_graph.edges(data=True):
        beta = data.get('beta', 0)
        new_classes = data.get('new_classes', [])

        #Update new classes based on the source node beta
        for class_ in new_classes:
            predicted_students[class_] += current_state.get(u, 0) * beta
            predicted_students[u] -= current_state.get(u, 0) * beta


    return predicted_students

current_state = {'CSCI101': 50, 'CSCI128': 100, 'CSCI200': 100, 'CSCI210': 100, 'CSCI220': 100, 'CSCI261': 100, 'CSCI262': 100, 'CSCI274': 100, 'CSCI306': 100, 'CSCI341': 100, 'CSCI358': 100, 'CSCI370': 100, 'CSCI400': 100, 'CSCI406': 100, 'CSCI442': 100, 'MATH111': 100, 'MATH112': 100, 'MATH213': 100, 'MATH332': 100, 'MATH334': 100}
predicted_students = predict_students_registered(current_state, G)
print(predicted_students)