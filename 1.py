from tabulate import tabulate
import sqlite3

# Connect to the database or create if not exists
conn = sqlite3.connect('student_database_1.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    roll_no TEXT,
    is_international INTEGER,
    is_on_campus INTEGER,
    age INTEGER,
    gender TEXT,
    email TEXT,
    phone INTEGER,
    course TEXT,
    admission_year INTEGER,
    sat_scores INTEGER,
    senior_year_gpa REAL,
    volunteering_years INTEGER,
    tuition_fees REAL,
    scholarship REAL,
    financial_aid REAL
    );
''')
conn.commit()


def insert_student(student_data):
    query = "INSERT INTO students (first_name, last_name, roll_no, is_international, is_on_campus, age, gender, email, phone, course, tuition_fees, scholarship, financial_aid, admission_year,sat_scores,senior_year_gpa,volunteering_years) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?)"
    cursor.execute(query, student_data)
    conn.commit()
    print("Student inserted successfully!")


# Function to retrieve all students
def get_all_students():
    query = "SELECT * FROM students"
    cursor.execute(query)
    return cursor.fetchall()


# Function to update student details
def update_student(student_id, new_data):
    query = "UPDATE students SET first_name=?, last_name=?, roll_no=?, is_international=?, is_on_campus=?, age=?, gender=?, email=?, phone=?, course=?, tuition_fees=?, scholarship=?, financial_aid=?, admission_year=?, sat_scores=?, senior_year_gpa=?,volunteering_years=? WHERE id=?"
    new_data_with_id = new_data + (student_id,)
    cursor.execute(query, new_data_with_id)
    conn.commit()
    print("-------Student updated successfully!-------")


# Function to delete a student
def delete_student(student_id):
    query = "DELETE FROM students WHERE roll_no = ?"
    cursor.execute(query, (student_id,))
    conn.commit()
    print("-------Student deleted successfully!-------")


# Function to display international students and local students separately
def display_international_and_local():
    international_query = "SELECT * FROM students WHERE is_international = 1"
    local_query = "SELECT * FROM students WHERE is_international = 0"
    cursor.execute(international_query)
    international_students = cursor.fetchall()
    cursor.execute(local_query)
    local_students = cursor.fetchall()

    print("\n" + "=" * 60)
    print("International Students")
    print("-" * 60)
    for student in international_students:
        print(student)

    print("\n" + "=" * 60)
    print("Local Students")
    print("-" * 60)
    for student in local_students:
        print(student)


# Function to display on campus and off campus students separately
def display_on_campus_and_off_campus():
    on_campus_query = "SELECT * FROM students WHERE is_on_campus = 1"
    off_campus_query = "SELECT * FROM students WHERE is_on_campus = 0"
    cursor.execute(on_campus_query)
    on_campus_students = cursor.fetchall()
    cursor.execute(off_campus_query)
    off_campus_students = cursor.fetchall()

    print("\n" + "=" * 60)
    print("On Campus Students")
    print("-" * 60)
    for student in on_campus_students:
        print(student)

    print("\n" + "=" * 60)
    print("Off Campus Students")
    print("-" * 60)
    for student in off_campus_students:
        print(student)


# Function to sort students course wise
def sort_students_by_course():
    query = "SELECT * FROM students ORDER BY course"
    cursor.execute(query)
    sorted_students = cursor.fetchall()
    print("\n" + "=" * 60)
    print("Sorted Students by Course")
    print("-" * 60)
    return sorted_students


# Function to display students awarded with scholarship and final tuition fees
def display_scholarship_students():
    query = "SELECT * FROM students WHERE scholarship > 0"
    cursor.execute(query)
    scholarship_students = cursor.fetchall()
    print("\n" + "=" * 60)
    print("Scholarship Students")
    print("-" * 60)
    for student in scholarship_students:
        final_tuition = student[11] - student[12] - student[13]  # tuition_fees - scholarship
        print(f"{student} \n Final Tuition Fees: {final_tuition}")


# Function to display students on financial aid and final tuition fees
def display_financial_aid_students():
    query = "SELECT * FROM students WHERE financial_aid > 0"
    cursor.execute(query)
    financial_aid_students = cursor.fetchall()
    print("\n" + "=" * 60)
    print("Financial Aid Students")
    print("-" * 60)
    for student in financial_aid_students:
        final_tuition = student[12] - student[13] - student[14]  # tuition_fees - financial_aid
        print(f"{student} - Final Tuition Fees: {final_tuition}")


def get_students_by_campus(is_on_campus):
    query = "SELECT * FROM students WHERE is_on_campus = ?"
    cursor.execute(query, (is_on_campus,))
    return cursor.fetchall()


def get_scholarship_students():
    query = "SELECT * FROM students WHERE scholarship > 0"
    cursor.execute(query)
    return cursor.fetchall()


def get_financial_aid_students():
    query = "SELECT * FROM students WHERE financial_aid > 0"
    cursor.execute(query)
    return cursor.fetchall()


# Function to get student by ID
def get_student_by_roll_number(roll_number):
    query = "SELECT * FROM students WHERE roll_no = ?"
    cursor.execute(query, (roll_number,))
    return cursor.fetchone()


# Function to get students by course
def get_students_by_course(course):
    query = "SELECT * FROM students WHERE course = ?"
    cursor.execute(query, (course,))
    return cursor.fetchall()


# Function to display students in a neat table
def display_students_table(students):
    headers = ["First Name", "Last Name", "ID", "International", "On Campus", "Age", "Gender", "Email",
               "Phone", "Course", "Volunteering Hours", "Tuition Fees", "Scholarship", "Financial Aid", "Admission Year", "SAT Scores", "Senior Year GPA", "Final Tuition Fees"]

    formatted_students = []
    for student in students:
        final_tuition_fees = student[12] - student[13] - student[14]  # tuition_fees - scholarship - financial_aid
        formatted_student = list(student)
        formatted_student.append(final_tuition_fees)
        formatted_students.append(formatted_student)

    table = tabulate(formatted_students, headers=headers, tablefmt="grid")
    print(table)


def get_international_students():
    query = "SELECT * FROM students WHERE is_international = 1"
    cursor.execute(query)
    return cursor.fetchall()


def get_local_students():
    query = "SELECT * FROM students WHERE is_international = 0"
    cursor.execute(query)
    local_students = cursor.fetchall()
    return local_students


if __name__ == '__main__':
    while True:
        print("\n" + "=" * 60)
        print("Student Database Management System")
        print("=" * 60)
        print("1. Insert Student")
        print("2. Display Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Display International and Local Students")
        print("6. Display On Campus and Off Campus Students")
        print("7. Sort Students by Course")
        print("8. Display Scholarship Students")
        print("9. Display Financial Aid Students")
        print("10. Get Student by ID")
        print("11. Get Students by Course")
        print("12. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            roll_no = input("ID: ")
            is_international = int(input("Is International (1 for yes, 0 for no): "))
            is_on_campus = int(input("Is On Campus (1 for yes, 0 for no): "))
            age = int(input("Age: "))
            gender = input("Gender: ")
            email = input("Email: ")
            phone = input("Phone: ")
            phone = ''.join(filter(str.isdigit, phone))
            course = input("Course: ").lower()
            admission_year = int(input("Admission Year: "))  # New field
            sat_scores = int(input("SAT Scores: "))  # New field
            senior_year_gpa = float(input("Senior Year GPA: "))  # New field
            volunteering_years = int(input("Volunteering Hours: "))  # New field
            tuition_fees = float(input("Tuition Fees: "))
            scholarship = float(input("Scholarship: "))
            financial_aid = float(input("Financial Aid: "))
            student_data = (
                first_name, last_name, roll_no, is_international, is_on_campus, age, gender, email, int(phone), course,
                admission_year, sat_scores, senior_year_gpa, volunteering_years, tuition_fees, scholarship,
                financial_aid
            )
            insert_student(student_data)


        elif choice == '2':
            students = get_all_students()
            if not students:
                print("=" * 60)
                print("---No student data provided---")
                print("=" * 60)
            else:
                display_students_table(students)

        elif choice == '3':
            student_id = int(input("Enter student ID to update: "))
            new_first_name = input("New First Name: ")
            new_last_name = input("New Last Name: ")
            roll_no = input("New ID: ")
            is_international = int(input("Is International (1 for yes, 0 for no): "))
            is_on_campus = int(input("Is On Campus (1 for yes, 0 for no): "))
            new_age = int(input("New Age: "))
            new_gender = input("New Gender: ")
            new_email = input("New Email: ")
            new_phone = input("New Phone: ")
            new_phone = ''.join(filter(str.isdigit, new_phone))
            new_gpa = float(input("New Senior Year GPA: "))
            new_course = input("New Course: ")
            new_admission_year = input("New Admission Year: ")
            new_tuition_fees = float(input("New Tuition Fees: "))
            new_volunteering_hours = float(input("New Volunteering Hours: "))
            new_sat_scores = float(input("New Sat Scores: "))
            new_scholarship = float(input("New Scholarship: "))
            new_financial_aid = float(input("New Financial Aid: "))
            new_data = (
                new_first_name, new_last_name, roll_no, is_international, is_on_campus, new_age, new_gender, new_email,
                int(new_phone), new_course, new_admission_year,new_sat_scores,new_gpa,new_volunteering_hours,new_tuition_fees,new_scholarship,new_financial_aid)
            update_student(student_id, new_data)
        elif choice == '4':
            student_id = int(input("Enter student ID to delete: "))
            delete_student(student_id)

        elif choice == '5':
            international_students = get_international_students()
            local_students = get_local_students()
            if not international_students:
                print("--- No International Student Data Provided ---")
            else:
                print("\n" + "=" * 60)
                print("International Students")
                display_students_table(international_students)
            print("\n" + "=" * 60)
            if not local_students:
                print("--- No Local Student Data Provided ---")
            else:
                print("Local Students")
                display_students_table(local_students)
        elif choice == '6':
            on_campus_students = get_students_by_campus(1)
            off_campus_students = get_students_by_campus(0)
            print("\n" + "=" * 60)
            print("On Campus Students")
            display_students_table(on_campus_students)
            print("\n" + "=" * 60)
            print("Off Campus Students")
            display_students_table(off_campus_students)

        elif choice == '7':
            sorted_students = sort_students_by_course()
            display_students_table(sorted_students)

        elif choice == '8':
            scholarship_students = get_scholarship_students()
            print("\n" + "=" * 60)
            print("Scholarship Students")
            display_students_table(scholarship_students)

        elif choice == '9':
            financial_aid_students = get_financial_aid_students()
            print("\n" + "=" * 60)
            print("Financial Aid Students")
            display_students_table(financial_aid_students)

        elif choice == '10':
            student_id = int(input("Enter student ID: "))
            student = get_student_by_roll_number(student_id)
            if student:
                print("Student found:")
                display_students_table([student])
            else:
                print("No student found with that ID.")

        elif choice == '11':
            course = input("Enter course name: ").lower()
            students_in_course = get_students_by_course(course)
            print("\n" + "=" * 60)
            print(f"Students in Course '{course}'")
            display_students_table(students_in_course)

        elif choice == '12':
            print("\n" + "=" * 60)
            print("Exiting the program. Goodbye!")
            print("=" * 60)
            break

        else:
            print("\n" + "=" * 60)
            print("Invalid choice. Please select a valid option.")
            print("=" * 60)
