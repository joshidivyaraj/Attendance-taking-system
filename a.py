import tkinter as tk
from datetime import datetime
from tkcalendar import DateEntry
import mysql.connector

window = tk.Tk()
window.title("Attendance System")
window.geometry("800x700")
students = {'Axit': '1', 'Dev': '2','Varun': '3', 'Elesh': '4', 'Deep': '5','Jay': '6','Meet': '7','Aditya':'8','Sahil':'9','Malay':'10'}
present_students = []
subjects = ['Python', 'Operating System', 'DCN', 'NEN', 'Web programming']
selected_subject = tk.StringVar()
selected_date = None

title_label = tk.Label(window, text="Attendance System", font=("Times new roman", 26))
title_label.pack()

date_frame = tk.Frame(window)
date_frame.pack(pady=10)

date_label = tk.Label(date_frame, text="Select date", font=("Times new roman", 18))
date_label.pack(side="left")

date_picker = DateEntry(
    date_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
date_picker.pack(side="left")

subject_label = tk.Label(window, text="Select subject", font=("Times new roman", 18))
subject_label.pack(pady=10)

subject_frame = tk.Frame(window)
subject_frame.pack()

for subject in subjects:
    subject_checkbox = tk.Checkbutton(
        subject_frame, text=subject, variable=selected_subject, onvalue=subject, offvalue="", font=("Times new roman", 18))
    subject_checkbox.pack(side="left")

students_frame = tk.Frame(window)
students_frame.pack()

buttons_frame = tk.Frame(window)
buttons_frame.pack()

present_label = tk.Label(
    students_frame, text="Take Attendance", font=("Times new roman", 18))
present_label.pack()

present_listbox = tk.Listbox(students_frame, selectmode="multiple", height=10 ,font=("Times new roman", 18))
present_listbox.pack(side="left")

absent_listbox = tk.Listbox(students_frame, selectmode="multiple", height=10 ,font=("Times new roman", 18))
absent_listbox.pack(side="right")

for student in students:
    absent_listbox.insert(tk.END, f"{student} ({students[student]})")

present_button = tk.Button(
    buttons_frame, text="Mark Present", command=lambda: mark_present(), font=("Times new roman", 18))
present_button.pack(side="left")

absent_button = tk.Button(
    buttons_frame, text="Mark Absent", command=lambda: mark_absent(), font=("Times new roman", 18))
absent_button.pack(side="right")

submit_button = tk.Button(window, text="Submit", command=lambda: submit(), font=("Times new roman", 18))
submit_button.pack(pady=10)

def mark_present():
    global present_students
    for student in absent_listbox.curselection():
        name = absent_listbox.get(student)
        present_listbox.insert(tk.END, name)
        absent_listbox.delete(student)
        present_students.append(name)

def mark_absent():
    global present_students
    for student in present_listbox.curselection():
        name = present_listbox.get(student)
        absent_listbox.insert(tk.END, name)
        present_listbox.delete(student)
        present_students.remove(name)

def submit():
    global selected_subject, selected_date, present_students
    subject = selected_subject.get()
    if not subject:
        tk.showerror("Error", "Please select a subject")
        return
    selected_date = date_picker.get_date().strftime("%Y-%m-%d")
    filename = f"attendance_{subject}_{selected_date}.txt"

    with open(filename, "w") as f:
        for student in present_students:
            f.write(student + "\n")

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mydatabase"
    )

    mycursor = mydb.cursor()

    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS attendance (id INT AUTO_INCREMENT PRIMARY KEY, student_name VARCHAR(255), subject VARCHAR(255), date DATE)")

    subject = selected_subject.get()
    date = selected_date

    for student in present_students:
        sql = "INSERT INTO attendance (student_name, subject, date) VALUES (%s, %s, %s)"
        val = (student.split(" ")[0], subject, date)
        mycursor.execute(sql, val)

    mydb.commit()

    mydb.close()

window.mainloop()