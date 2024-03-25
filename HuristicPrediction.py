import pandas as pd
import numpy as np
import sklearn as sk

'''
TODO: Vectorize class enrollments 
    - Read in classes from output.txt
    - Based on term and previous terms create a vector that is the classes enrolled in 
    - Can reuse vector for both since it will just be zeros for previous years 

TODO: Create way to find percent similarity between people per year
TODO: Create buckets based on similarity
TODO: Based on similar buckets find pattern in enrollments in classes by year 
TODO: Create prediction of current buckets for this semester 
'''
def read_in_catalogs(files):
    classes = set()
    for file in files:
        with open(file,'r') as f:
            for line in f:
                line = line.split(' ')
                line = [i.replace('\n','') if '\n' in i else i for i in line]
                classes.update(line)

    return {key:value for key,value in enumerate(list(classes))}

def vectorize_term(classes,term,df):
    print(term)
    year = int(term.split()[-1])
    x = df[((df['Semester Admitted'] >= year-4) & (df['Semester Admitted'] <=year))]
    print(x.values[1][2:])
    y = x[['Semester Admitted','Major']]
    print(y)
    # df2 = df[]
    
    # columns = [i for i in df.columns[3:] if int(i.rsplit(' ')[-1]) < term]
    
    # print(columns)

if __name__ == '__main__':
    df = pd.read_excel("output.xlsx")
    files = ['prereqs2021.txt','prereqsnewcat.txt']
    classes = read_in_catalogs(files)


    vectorize_term(classes,'Summer 2023',df)
