# Semester Courses is Taken (ex. Fall 2022, Spring/Summer 2023)
    # -> Name of Course / Course Code / Name of Professor / Course Type (ie. Mandatory / Elective)
        # -> Assignments #, Weight on Course Grade, Grade Received
        # -> Group Projects #, Weight on Course Grade, Grade Received
        # -> Miscellaneous, Weight on Course Grade, Grade Received
        # -> Midterms #, Weight on Course Grade, Grade Received
        # -> Finals, Weight on Course Grade, Grade Received

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import mysql.connector

gpa_calculator_db = mysql.connector.connect(
    host ="localhost",
    user="root",
    passwd="(-c6w4d4b5i2f3-)",
    database="gpa_calculator_db"
)

mycursor = gpa_calculator_db.cursor()

global standard_font 
standard_font = ("Arial", 10, "bold")

def get_courses():
    sql = "SELECT * FROM courses WHERE semester_taken = 'Spring/Summer 2023'"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    courses = []

    for row in myresult:
        courses.append(row)

    return courses

def get_course_desc(course_id):
    sql = f"SELECT * FROM table_of_contents WHERE course_id = {course_id}"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    course_descs = [] # Must place in a 2d list of dictionaries

    for row in myresult:
        course_descs.append(row)

    return course_descs

def add_more_content():
    if messagebox.askyesno(title="Add More Content", message="Would you like to add more content?"):
        add_content()
    else:
        pass

def add_content():
    def submit_content():
        content_desc = [0, "", "", "", 0.0, 0.0, 0.0]

        content_desc[0] = int(course_id.get())
        content_desc[1] = content_type.get()
        content_desc[2] = content_name.get()
        content_desc[3] = f"Ch {content_coverage.get()}"
        content_desc[4] = float(weight.get())
        content_desc[5] = float(grade.get())
        content_desc[6] = content_desc[4]*(content_desc[5]/100)

        print(content_desc)

        sql = "INSERT INTO table_of_contents (course_id, content_type, content_name, content_coverage, weight, grade, weight_achieved) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        mycursor.execute(sql, content_desc)
        gpa_calculator_db.commit()

        add_content_form_window.destroy()

        add_more_content()

    add_content_form_window = Toplevel()

    add_content_form_window.title("Add Content")
    add_content_form_window.geometry("450x270")

    def add_content_entry(title, grid):
        Label(add_content_frame, text=title, font=standard_font, width=25).grid(row=grid[0], column=grid[1])
        
        content_entry = Entry(add_content_frame, font=("Arial", 10), width=20)
        content_entry.grid(row=grid[0], column=grid[1]+1)

        return content_entry

    def add_content_drop_down(title, grid, width, list, l_width=25):
        Label(add_content_frame, text=title, font=standard_font, width=l_width).grid(row=grid[0], column=grid[1])

        content_drop_down = ttk.Combobox(add_content_frame, value=list, width=width)
           
        content_drop_down.current(0)
        content_drop_down.grid(row=grid[0], column=grid[1]+1)

        return content_drop_down

    a = 0
    b = 0

    nums_list = []

    i = 0
    for i in range(101):
        nums_list.append(i)

    nums_width_dd = 4

    add_content_title = Label(add_content_form_window, text="Add Content", font=standard_font).place(x=190, y=15)

    add_content_frame = Frame(add_content_form_window)

    course_id = add_content_drop_down("Course ID", [a,b], nums_width_dd, nums_list)
    content_type = add_content_drop_down("Content Type", [a+1, b], 20, ["Assignment", "Midterm", "Final"])
    content_name = add_content_entry("Content Name", [a+2, b])
    content_coverage = add_content_entry("Content Coverage | Ch", [a+3,b])
    weight = add_content_entry("Weight", [a+4, b])
    grade = add_content_entry("Grade", [a+5,b])

    add_content_frame.place(x=30, y=60)

    submit_button = Button(add_content_form_window, text="Submit", font=("Arial", 10), width=8, height=1, command=submit_content)
    submit_button.place(x=195, y=220)

def display_grade_breakdown(descs):
    grades_window = Toplevel()

    grades_window.title("Grade Breakdown")
    grades_window.geometry("900x400")

    def create_content_frame(content_desc, x, y):
        def display_content(desc, a, b):
            name = desc[2]
            coverage = desc[3]
            weight = desc[4]
            grade = desc[5]
            weight_achieved = desc[6]

            Label(content_frame, text = name, justify="left").grid(row=a,column=b)
            Label(content_frame, text = coverage).grid(row=a,column=b+1)
            Label(content_frame, text = f"{weight}%").grid(row=a,column=b+2)

            Label(content_frame, text = f"{grade}%").grid(row=a,column=b+3)
            Label(content_frame, text = f"{weight_achieved}%").grid(row=a,column=b+4)

        a = 2
        b = 0
        
        content_frame = Frame(grades_window)

        Label(content_frame, text = "Name", font = standard_font).grid(row=1,column=b)
        Label(content_frame, text = "Coverage", font = standard_font).grid(row=1,column=b+1)
        Label(content_frame, text = "Weight", font = standard_font).grid(row=1,column=b+2)
        Label(content_frame, text = "Grade", font = standard_font).grid(row=1,column=b+3)
        Label(content_frame, text = "Weight Achieved", font = standard_font).grid(row=1,column=b+4)

        for i in range(len(content_desc)):
            if i > 0:
                display_content(content_desc[i], a, b)
            else:
                display_content(content_desc[i], a, b)

            a+=1

        content_frame.place(x=x, y=y)

    x = 10
    y = 60

    create_content_frame(descs, x, y)

    add_content_button = Button(grades_window, text="+", font=standard_font, width=2, height=1, command=add_content).place(x=850,y=15)

class Course:
    def __init__(self, desc, coords):
        self.desc = desc
        self.coords = coords

    def display_course(self):
        course_frame = Frame(window)
        course_frame.config(width=600, height=20)

        desc = get_course_desc(self.desc[0]) #returns course desc list for specific course 

        Label(course_frame, text = f"{self.desc[1]}: {self.desc[2]}", width=50, justify=["left"]).grid(row=0,column=0)
        Label(course_frame, text = f"w/Prof {self.desc[3]}", width=25, justify=["left"]).grid(row=0,column=1)
        Label(course_frame, text = self.desc[4], width=10, justify=["left"]).grid(row=0,column=2)
        Button(course_frame, text = "See More", command = lambda: display_grade_breakdown(desc)).grid(row=0,column=3)

        course_frame.place(x=self.coords[0], y=self.coords[1])

course_descs = get_courses()

window = Tk()

window.title("GPA Calculator")
window.geometry("700x600")

x = 20
y = 100

for i in range(len(course_descs)):
    if i > 0:
        course = Course(course_descs[i], [x,y])
    else:
        course = Course(course_descs[i], [x,y])

    course.display_course()

    y+=40

window.mainloop()
    