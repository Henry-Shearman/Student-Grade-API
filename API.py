import os
import psycopg2
import numpy as np
from flask import Flask, jsonify, request


#Instantiate API
app = Flask(__name__)


# API call to return grade data with options to filter by name or course. NB: will not work with any null entries.
@app.get('/grades_search')
def get_all_grades_test():
    
    query_name = request.args.get('name', default='%')
    query_course = request.args.get('course', default='%')

    query = f"""SELECT Name
                      ,CourseName
                      ,Grade
                      ,AcademicGrade

                  FROM Class.FactGrades g 
                  JOIN Class.DimStudent s ON g.StudentNo = s.StudentNo
                  JOIN Class.DimCourse c ON g.CourseKey = c.CourseKey

                  WHERE Name LIKE '{query_name}'
                    AND CourseName LIKE '{query_course}';"""  

    conn = psycopg2.connect(host="localhost"
                           ,database=os.getenv('DB_NAME')
                           ,user=os.getenv('DB_USERNAME')
                           ,password=os.getenv('DB_PASSWORD'))

    cursor = conn.cursor()
    cursor.execute(query)
    course_grade_pair_list = cursor.fetchall()
    conn.commit()
    conn.close()

    course_grade_pair_dict = {"search_results":list(map(lambda x: {"student_name":x[0]
                                                                  ,"course_name":x[1]
                                                                  ,"grade":x[2]
                                                                  ,"academic_grade":x[3]}, course_grade_pair_list))}
    
    return jsonify(course_grade_pair_dict)    


#Returns summary statisics for grade group with given grade search parameters.
@app.get('/summary_stats')
def get_summary_statistics():

    query_name = request.args.get('name', default='%')
    query_course = request.args.get('course', default='%')

    query = f"""SELECT Grade

                  FROM Class.FactGrades g
                  JOIN Class.DimStudent s ON g.StudentNo = s.StudentNo
                  JOIN Class.DimCourse c ON g.CourseKey = c.CourseKey

                  WHERE Name LIKE '{query_name}'
                    AND CourseName LIKE '{query_course}';"""

    conn = psycopg2.connect(host="localhost"
                           ,database=os.getenv('DB_NAME')
                           ,user=os.getenv('DB_USERNAME')
                           ,password=os.getenv('DB_PASSWORD'))

    cursor = conn.cursor()
    cursor.execute(query)
    grade_list = cursor.fetchall()
    conn.commit()
    conn.close()

    mean = round(np.mean(grade_list), 1)
    std_dv = round(np.std(grade_list, mean=mean) ,1)
    summary_stats_dict = {"summary_stats":{"mean":mean, "standard_deviation":std_dv}}


    return jsonify(summary_stats_dict)


#Curves grades using a flat scale curve.
@app.put('/flat_scale_curve')
def curve_grades_with_flat_scale():

    query = "SELECT Grade FROM Class.FactGrades;"

    conn = psycopg2.connect(host="localhost"
                           ,database=os.getenv('DB_NAME')
                           ,user=os.getenv('DB_USERNAME')
                           ,password=os.getenv('DB_PASSWORD'))

    cursor = conn.cursor()
    cursor.execute(query)
    grade_list = cursor.fetchall()
    max_grade = np.max(grade_list)
    grade_adjust_value = 100 - max_grade

    update_string = f"UPDATE Class.FactGrades SET Grade = Grade + {grade_adjust_value};"
    cursor.execute(update_string)

    conn.commit()
    conn.close()

    return jsonify({"message":"grades updated successfully", "number_of_updated_grades":len(grade_list)})


def main():

    app.run(debug=True)
    

if __name__ == '__main__':

    main()

