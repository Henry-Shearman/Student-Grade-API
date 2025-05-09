----Drop any existing tables----
DROP TABLE IF EXISTS Class.StudentDataLanding;
DROP TABLE IF EXISTS Class.FactGrades;
DROP TABLE IF EXISTS Class.DimStudents;
DROP TABLE IF EXISTS Class.DimCourse;


----Create tables for "Class" schema
CREATE TABLE Class.StudentDataLanding(StudentNo INT
	                             ,Name VARCHAR(50)                                                           
				     ,Gender VARCHAR(10)
                                     ,CourseName VARCHAR(50)
				     ,Grade SMALLINT
			             ,CreatedDate TIMESTAMP DEFAULT current_timestamp);

CREATE TABLE Class.DimStudent(StudentKey INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY
	                     ,StudentNo INT UNIQUE NOT NULL
	                     ,Name VARCHAR(50)
		             ,Gender VARCHAR(10));

CREATE TABLE Class.DimCourse(CourseKey INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY
                            ,CourseName VARCHAR(50) UNIQUE NOT NULL);
	
CREATE TABLE Class.FactGrades(GradeKey INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY
                             ,StudentNo SMALLINT REFERENCES Class.DimStudent(StudentNo) ON UPDATE CASCADE 
			                                                                ON DELETE CASCADE
			     ,CourseKey SMALLINT REFERENCES Class.DimCourse(CourseKey) ON UPDATE CASCADE 
			                                                               ON DELETE CASCADE
			     ,Grade SMALLINT
		             ,AcademicGrade VARCHAR(2)
		             ,UpdatedDate TIMESTAMP);


----Create indexes---------------------------
CREATE INDEX idx_name ON Class.DimStudent(LOWER(Name)); --index for case-insensitive API search queries
CREATE INDEX idx_course_name ON Class.DimCourse(LOWER(CourseName)); --index for case-insensitive API search queries
CREATE INDEX idx_grades_std_no ON Class.FactGrades(StudentNo); --index for foreign key
CREATE INDEX idx_grades_course_key ON Class.FactGrades(CourseKey); --index for foreign key


----Create triggers and trigger functions----
CREATE OR REPLACE FUNCTION Class.update_student_data() RETURNS TRIGGER AS
    $$
    BEGIN

	MERGE INTO Class.DimStudent s
	USING (SELECT DISTINCT StudentNo 
		              ,Name
			      ,Gender
	           FROM Class.StudentDataLanding) AS lnd ON s.StudentNo = lnd.StudentNo
	WHEN NOT MATCHED THEN
	    INSERT (StudentNo, Name, Gender) 
	    VALUES (lnd.StudentNo, lnd.Name, lnd.Gender);
        
	MERGE INTO Class.DimCourse c
        USING (SELECT DISTINCT CourseName 
	           FROM Class.StudentDataLanding) AS lnd ON c.CourseName = lnd.CourseName
        WHEN NOT MATCHED THEN
	    INSERT (CourseName)
	    VALUES (lnd.CourseName);

	WITH cte_grade_keys AS (SELECT s.StudentNo
                     		      ,c.CourseKey
                                      ,lnd.Grade
                                      ,lnd.CreatedDate
				      ,ROW_NUMBER() OVER(PARTITION BY s.StudentNo
					                             ,c.CourseKey 
							     ORDER BY CreatedDate DESC) AS RowNumber
				    FROM Class.StudentDataLanding lnd		
                                    JOIN Class.DimStudent s ON lnd.StudentNo = s.StudentNo
                                    JOIN Class.DimCourse c ON lnd.CourseName = c.CourseName)

	MERGE INTO Class.FactGrades g
        USING cte_grade_keys AS g_keys ON g.StudentNo = g_keys.StudentNo
	                              AND g.CourseKey = g_keys.CourseKey
	WHEN MATCHED AND RowNumber = 1 THEN        
            UPDATE SET Grade = g_keys.Grade
        WHEN NOT MATCHED AND RowNumber = 1 THEN
	    INSERT (StudentNo, CourseKey, Grade, AcademicGrade, UpdatedDate) 
	    VALUES (g_keys.StudentNo
		   ,g_keys.CourseKey
		   ,g_keys.Grade
		   ,CASE WHEN Grade >= 85 THEN 'HD'
                         WHEN Grade >= 75 THEN 'D'
                         WHEN Grade >= 65 THEN 'C'
                         WHEN Grade >= 50 THEN 'P'
                         ELSE 'FF'
                    END
	           ,g_keys.CreatedDate);

      DELETE FROM Class.StudentDataLanding;
      RETURN NULL;

    END;
    $$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER data_update
    AFTER INSERT ON Class.StudentDataLanding
    EXECUTE FUNCTION Class.update_student_data();	


CREATE OR REPLACE FUNCTION Class.update_academic_grades() RETURNS TRIGGER AS 
    $$
    BEGIN
     
       UPDATE Class.FactGrades 
           SET AcademicGrade = CASE WHEN NEW.Grade >= 85 THEN 'HD'
                                    WHEN NEW.Grade >= 75 THEN 'D'
                                    WHEN NEW.Grade >= 65 THEN 'C'
                                    WHEN NEW.Grade >= 50 THEN 'P'
                                    ELSE 'FF'
			       END
	      ,UpdatedDate = current_timestamp

	   WHERE GradeKey = NEW.GradeKey;
	
       RETURN NEW;

    END;
    $$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER academic_grade_update
    AFTER UPDATE ON Class.FactGrades
    FOR EACH ROW
    WHEN (OLD.Grade != NEW.Grade)	
    EXECUTE FUNCTION Class.update_academic_grades();	
    


----Populate tables with dummy data----
COPY Class.StudentDataLanding 
    FROM '/tmp/StudentDummyData.csv'
    DELIMITER ','
    CSV HEADER;
