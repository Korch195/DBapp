from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Taras2020",
    database="assistantship"
)
cursor = db.cursor()

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add_assistantship', methods=['GET', 'POST'])
def add_assistantship():
    if request.method == 'POST':
        student_id = request.form['StudentID']
        professor_id = request.form['ProfessorID']
        department_code = request.form['DepartmentCode']
        duration = request.form['Duration']
        salary = request.form['Salary']
        starting_date = request.form['StartingDate']

        cursor.execute("""
            INSERT INTO Assistantship (StudentID, ProfessorID, DepartmentCode, Duration, Salary, StartingDate)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (student_id, professor_id, department_code, duration, salary, starting_date))
        db.commit()
        return redirect('/')

    cursor.execute("SELECT PassportSeries FROM Student")
    students = cursor.fetchall()
    cursor.execute("SELECT EmployeeID FROM Professor")
    professors = cursor.fetchall()
    cursor.execute("SELECT DepartmentCode FROM Department")
    departments = cursor.fetchall()
    return render_template('add_assistantship.html', students=students, professors=professors, departments=departments)

@app.route('/update_schedule', methods=['GET', 'POST'])
def update_schedule():
    if request.method == 'POST':
        schedule_id = request.form['ScheduleID']
        weekday = request.form['WeekDay']
        start_time = request.form['StartTime']
        end_time = request.form['EndTime']
        task = request.form['TaskDescription']
        location = request.form['Location']

        cursor.execute("""
            UPDATE schedule
            SET WeekDay = %s, StartTime = %s, EndTime = %s,
                TaskDescription = %s, Location = %s
            WHERE ScheduleID = %s
        """, (weekday, start_time, end_time, task, location, schedule_id))
        db.commit()
        return redirect('/')
    cursor.execute("SELECT ScheduleID FROM schedule")
    schedule_ids = cursor.fetchall()
    return render_template('update_schedule.html', schedule_ids=schedule_ids)


@app.route('/delete_review', methods=['GET', 'POST'])
def delete_review():
    if request.method == 'POST':
        review_id = request.form['ReviewID']

        cursor.execute("DELETE FROM review WHERE ReviewID = %s", (review_id,))
        db.commit()
        return redirect('/')

    cursor.execute("SELECT ReviewID FROM review")
    review_ids = cursor.fetchall()
    return render_template('delete_review.html', review_ids=review_ids)


if __name__ == '__main__':
    app.run(debug=True)
