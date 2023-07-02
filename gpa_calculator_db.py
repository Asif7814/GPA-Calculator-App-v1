import mysql.connector

gpa_calculator_db = mysql.connector.connect(
    host ="localhost",
    user="root",
    passwd="(-c6w4d4b5i2f3-)",
    database="gpa_calculator_db"
)

mycursor = gpa_calculator_db.cursor()

def add_course_info(course_info):
    sql = "INSERT INTO courses (course_code, course_name, course_prof, gpa, course_type, semester_taken) VALUES (%s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, course_info)
    gpa_calculator_db.commit()

def update_course_info(course_id, course_code):
    sql = f"UPDATE courses SET course_id = '{course_id}' WHERE course_code = '{course_code}'"
    mycursor.execute(sql)
    gpa_calculator_db.commit()

def alter_courses_tb():
    sql = "ALTER TABLE courses MODIFY COLUMN gpa DECIMAL(3,1)"
    mycursor.execute(sql)

def add_table_of_content_info(toc_info):
    sql = "INSERT INTO table_of_contents (course_id, content_type, content_name, content_coverage, weight, grade, weight_achieved) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, toc_info)
    gpa_calculator_db.commit()

def update_table_of_content_info(content, percent, course_id, content_name):
    sql = f"UPDATE table_of_contents SET {content} = {percent} WHERE (course_id = {course_id} AND content_name = '{content_name}')"
    mycursor.execute(sql)
    gpa_calculator_db.commit()

def alter_table_of_contents_tb():
    sql = "ALTER TABLE table_of_contents CHANGE content_id course_id INT"
    mycursor.execute(sql)

def delete_entry_from_table_of_contents(content_name):
    sql = f"DELETE FROM table_of_contents WHERE content_name = '{content_name}'"
    mycursor.execute(sql)
    gpa_calculator_db.commit()

#TEMPORARY USE UNTIL GUI FORM IS MADE 
#update_table_of_content_info("grade", 80, 6, "5: Techniques of Differentiation & Applications of Derivatives")
#update_table_of_content_info("weight_achieved", "weight*(grade/100)", 6, "5: Techniques of Differentiation & Applications of Derivatives")