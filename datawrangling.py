from ast import List
import pandas as pd
import numpy as np

def class_extraction():
    cat_map = {}
    with open("prereqs2021.txt", 'r') as p:
        cat_21 = set()
        for line in p:
            vals = line.split(' ')
            for i in vals:
                i = i.replace('\n','')
                cat_21.add(i)
        cat_map['2021'] = list(cat_21)
        
    with open("prereqsnewcat.txt", 'r') as p:
        cat_prev = set()
        for line in p:
            vals = line.split(' ')
            for i in vals:
                i = i.replace('\n','')
                cat_prev.add(i)
        cat_map['before'] = list(cat_prev)
    return cat_map

def list_2_string(l_input: list):
    output = "["
    for i in range(len(l_input)):
        if l_input[i] == '\'\'':
            output += l_input[i]
        else:
            l_input[i] = l_input[i].replace(' ','\', \'')
            output += "\'" + l_input[i] + "\'"
        if i != len(l_input)-1:
            output += ', '
    output += ']'
    return output

            
def dataWrangling(data : pd.DataFrame,start : str,end : str):
    
    #Get the columns that will be used for this segement we are looking at
    count_flag = False
    column_list = []
    for i in data.columns:
        if i == start:
            count_flag = True
        if count_flag:
            column_list.append(i)
        if i == end:
            count_flag = False

    #Extract only the data from this segment 
    cut_table = data[column_list]
    timesteplookup = {col:i for i,col in enumerate(column_list)}
    #Get only students that change there values 
    cut_table = cut_table.dropna(subset=column_list,how='all')

    #Get all the indexes of the students 
    students = cut_table.index.values
    #Create the data structure
    output = pd.Series(data=[pd.Series() for i in range(cut_table.shape[0])])

    #Go through each student and create the Series
    for i in range(len(students)):
        student_row = data.iloc[students[i]]
        previous_classes = student_row['Spring 2008':start].values
        previous_classes= previous_classes[~pd.isnull(previous_classes)]
        curr_state = previous_classes.tolist()
        temp = []
        for q in curr_state:
            if ' ' in q:
                temp.extend(q.split(' '))
            else:
                temp.append(q)
        curr_state = [s.split(' ') for s in curr_state]
        curr_state = [x for xs in curr_state for x in xs]
        cut_table_student_row = cut_table.loc[students[i]].values
        student_path = []
        if len(curr_state) ==0:
            curr_state = ['\'\'']
            student_path.append(curr_state)
        else:
            student_path.append(list_2_string(curr_state))
        for x in cut_table_student_row[1:]:
            z = list(curr_state)
            if type(x) != type(0.0):
            
                z.append(x)
            else:
                z.append('\'\'')
            student_path.append(list_2_string(z))
            curr_state = z
        output[i] = pd.Series(student_path)
        
    return output,timesteplookup


if __name__ == "__main__":
    df = pd.read_excel("output.xlsx")
    data,dict = dataWrangling(df,"Fall 2017","Spring 2018")
    for d in data:
        print (d)
    print(dict)
    print(class_extraction())
