import pandas as pd
from random import choice, randint
from itertools import product
from names import get_full_name

no_students = int(input('Enter number of dummy students: '))
student_tuples = [(i+10000, choice(['male', 'female'])) for i in range(no_students)] 
student_tuples = list(map(lambda x: (x[0], get_full_name(x[1]) , x[1]), student_tuples))

course_choice = ['English', 'Mathematics', 'History', 'Geography','Science', 'PDHPE', 'Music']
student_courses = product(student_tuples, course_choice)

grades = list(zip(*[(student, course, randint(30, 90)) for student, course in student_courses]))
grades = list(zip(*grades[0])) + grades[1:]

df = pd.DataFrame({'StudentNo':grades[0], 'Name':grades[1], 'Gender':grades[2], 'CourseName':grades[3], 'Grade':grades[4]})
df.to_csv('StudentDummyData.csv', index=False)
