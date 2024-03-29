import PreReqs
import StateMachine as sm
import FrequentistFitting as ffit
import random

#get the model
dag = PreReqs.getPrereqGraph()
G = sm.makeStateMachine(dag)

#this is to generate random data with assumed Beta values
ffit.addRandomBetaTerms(G)
data = ffit.generate_random_data(G, 1000)

#fit the model to the data
ffit.fit_frequentist(G, data)

#Predict registration numbers
def predict_students_registered(current_state, state_machine_graph):
    predicted_students = {'CSCI101': 0, 'CSCI128': 0, 'CSCI200': 0, 'CSCI210': 0, 'CSCI220': 0, 'CSCI261': 0, 'CSCI262': 0, 'CSCI274': 0, 'CSCI306': 0, 'CSCI341': 0, 'CSCI358': 0, 'CSCI370': 0, 'CSCI400': 0, 'CSCI403': 0, 'CSCI406': 0, 'CSCI442': 0, 'MATH111': 0, 'MATH112': 0, 'MATH213': 0, 'MATH332': 0, 'MATH334': 0}

    #Loop through each edge in the state machine
    for source, target, data in state_machine_graph.edges(data=True):
        beta = data.get('beta', 0)
        new_classes = data.get('new_classes', [])

        #Update new classes based on the source node beta ignoring self edges
        if (source != '[]') & (source != target):
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