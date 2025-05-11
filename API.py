import os
import psycopg2
import numpy as np
from flask import Flask, jsonify, request


#Instantiate API
app = Flask(__name__)


#Returns a database connection instance from environment variables
def get_database_connection():

    conn_instance = psycopg2.connect(host=os.getenv('DB_HOSTNAME')
                                    ,database=os.getenv('DB_NAME')
                                    ,user=os.getenv('DB_USERNAME')
                                    ,password=os.getenv('DB_PASSWORD'))

    return conn_instance


#API call to return grade data with options to filter by name or course. NB: will not work with any null entries.
@app.get('/grades_search')
def get_all_grades_test():
    
    query_name = request.args.get('name', default='%')
    query_name = f'{query_name}%'.lower() if query_name != '%' else '%'

    query_course = request.args.get('course', default='%')
    query_course = f'{query_course}%'.lower() if query_course != '%' else '%'

    query = f"""SELECT s.StudentNo
                      ,Name
                      ,CourseName
                      ,Grade
                      ,AcademicGrade

                  FROM Class.FactGrades g 
                  JOIN Class.DimStudent s ON g.StudentNo = s.StudentNo
                  JOIN Class.DimCourse c ON g.CourseKey = c.CourseKey

                  WHERE LOWER(Name) LIKE '{query_name}'
                    AND LOWER(CourseName) LIKE '{query_course}';"""  

    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    course_grade_pair_list = cursor.fetchall() 
    conn.close()

    course_grade_pair_dict = {"search_results":list(map(lambda x: {"student_number":x[0]
                                                                  ,"student_name":x[1]
                                                                  ,"course_name":x[2]
                                                                  ,"grade":x[3]
                                                                  ,"academic_grade":x[4]}, course_grade_pair_list))}
    
    return jsonify(course_grade_pair_dict)    


#Returns summary statisics for grade group with given grade search parameters.
@app.get('/summary_stats')
def get_summary_statistics():

    query_name = request.args.get('name', default='%')
    query_name = f'{query_name}%'.lower() if query_name != '%' else '%'

    query_course = request.args.get('course', default='%')
    query_course = f'{query_course}%'.lower() if query_course != '%' else '%'
    
    query = f"""SELECT g.CourseKey
                      ,g.StudentNo  
                      ,Grade

                  FROM Class.FactGrades g
                  JOIN Class.DimStudent s ON g.StudentNo = s.StudentNo
                  JOIN Class.DimCourse c ON g.CourseKey = c.CourseKey

                  WHERE LOWER(Name) LIKE '{query_name}'
                    AND LOWER(CourseName) LIKE '{query_course}';"""

    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    results_list = list(zip(*cursor.fetchall())) 
    conn.close()
    
    #Summary Statistics
    no_of_courses = len(set(results_list[0]))
    no_of_students = len(set(results_list[1]))
    grade_list = results_list[2]
    no_of_grades = len(grade_list)
    mean = round(np.mean(grade_list), 1)
    std_dv = round(np.std(grade_list, mean=mean) ,1)
    summary_stats_dict = {"summary_stats":{"N_courses":no_of_courses
                                          ,"N_students":no_of_students
                                          ,"N_grades":no_of_grades
                                          ,"min_grade":int(np.min(grade_list))
                                          ,"max_grade":int(np.max(grade_list))
                                          ,"mean_grade":mean
                                          ,"grade_standard_deviation":std_dv}}

    return jsonify(summary_stats_dict)


#Curves grades using a flat scale curve.
@app.put('/flat_scale_curve')
def curve_grades_with_flat_scale():

    query = "SELECT Grade FROM Class.FactGrades;"

    conn = get_database_connection()
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


#Upserts user data from json in request body
@app.post('/insert_student_data')
def upsert_users():
 
    data = request.get_json(silent=True)

    if data is None:

        data = request.form
        data_entries = [data]

    else:

        data_entries = data["new_student_grades"]

    #Format data into SQL values tuple string for batch processing
    sql_values = ",".join([f"{tuple(entry.values())}" for entry in data_entries])

    query = f"""INSERT INTO Class.StudentDataLanding VALUES {sql_values};"""

    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

    return jsonify({"message":"users updated successfully", "number_of_updated_users":len(data_entries)})


def main():

    app.run(debug=True)
    

if __name__ == '__main__':

    main()
