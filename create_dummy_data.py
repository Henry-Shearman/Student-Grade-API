import pandas as pd
from datetime import datetime
from random import choice, randint
from itertools import product
from names import get_full_name

#Generate student gendered tuples with student number
no_students = int(input('Enter number of dummy students: '))
student_tuples = [(i+10000, choice(['male', 'female'])) for i in range(no_students)] 
student_tuples = list(map(lambda x: (x[0], get_full_name(x[1]) , x[1]), student_tuples))

#Create Cartesian product set of student tuples and course grades
course_choice = ['English', 'Mathematics', 'History', 'Geography','Science', 'PDHPE', 'Music']
student_courses = product(student_tuples, course_choice)

#Generate random grade data and unzip into list
grades = list(zip(*[(student, course, randint(30, 90), datetime.now()) for student, course in student_courses]))
grades = list(zip(*grades[0])) + grades[1:]

#Format data into dataframe columns and export to csv
df = pd.DataFrame({'StudentNo':grades[0]
                  ,'Name':grades[1]
                  ,'Gender':grades[2]
                  ,'CourseName':grades[3]
                  ,'Grade':grades[4]
                  ,'CreatedDate':grades[5]})

#Export to csv
df.to_csv('StudentDummyData.csv', index=False)
