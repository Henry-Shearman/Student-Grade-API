# API ENDPOINTS<br />
## GET /grades\_search
### Description: returns student grade data filtered by name and course.
### Parameters

|Parameter|Type  |Required|Description                    |
|:--------|:-----|:-------|:------------------------------|
|name     |String|No      |Filters results by student name|
|course   |String|No      |Filters results by course name |

### Example Call
```sh
curl -X GET "http://${SERVER_NAME}:${PORT}/grades_search?name=Susan&course=math"
```
#### Output
```
{
  "search_results": [
    {
      "academic_grade": "C",
      "course_name": "Mathematics",
      "grade": 68,
      "student_name": "Susan Frese",
      "student_number": 10012
    }
  ]
}
```


## GET /summary\_stats
### Description: returns grade summary statistics filtered by name and course.
### Parameters

|Parameter|Type  |Required|Description                    |
|:--------|:-----|:-------|:------------------------------|
|name     |String|No      |Filters results by student name|
|course   |String|No      |Filters results by course name |

### Example Call
```sh
curl -X GET "http://${SERVER_NAME}:${PORT}/summary_stats?course=Mathematics"
```
#### Output
```
{
  "summary_stats": {
    "N_courses": 1,
    "N_grades": 13,
    "N_students": 13,
    "grade_standard_deviation": 16.3,
    "max_grade": 100,
    "mean_grade": 71.2,
    "min_grade": 41
  }
}
```



## PUT /flat\_scale\_curve
### Description: scales grades using a flat scale curve.
### Parameters
None
### Request Body
None
### Example Call
```sh
curl -X PUT "http://${SERVER_NAME}:${PORT}/flat_scale_curve"
```
#### Output
```
{
  "message": "grades updated successfully",
  "number_of_updated_grades": 91
}
```


## POST /insert\_student\_data
### Description: upserts student data
### Parameters
None
### Request Body
```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "description": "insert or update student records",
  "type": "object",
  "properties": {
    "new_student_grades": {
      "type": "array",
      "uniqueItems": true,
      "minItems": 1,
      "items": {
        "required": [
          "student_number",
          "student_name",
          "student_gender",
          "student_course",
          "student_grade"
        ],
        "properties": {
          "student_number": {
            "type": "number"
          },
          "student_name": {
            "type": "string",
            "minLength": 1
          },
          "student_gender": {
            "type": "string",
            "minLength": 1
          },
          "student_course": {
            "type": "string",
            "minLength": 1
          },
          "student_grade": {
            "type": "number"
          }
        }
      }
    }
  },
  "required": [
    "new_student_grades"
  ]
}
```
### Example Call
```sh
curl -X POST "http://${SERVER_NAME}:${PORT}/insert_student_data" -H "Content-Type: application/json" -d '{"new_student_grades":[{"student_number":20000, "student_name":"Henry Shearman", "student_gender":"male", "student_course":"Music", "student_grade":20}, {"student_number":20000, "student_name":"Henry Shearman", "student_gender":"male", "student_course":"Computer Science", "student_grade":88}]}'
```
#### Output
```
{
  "message": "users updated successfully",
  "number_of_updated_users": 2
}
```
