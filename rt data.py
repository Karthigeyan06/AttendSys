import sqlite3
import datetime

def fetch_attendance_for_day(selected_date):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    selected_datetime = datetime.datetime.strptime(selected_date, '%Y-%m-%d').date()

    c.execute('''
        SELECT students.roll_no, attendance.timestamp
        FROM attendance
        INNER JOIN students ON students.roll_no = attendance.student_roll_no
        WHERE DATE(attendance.timestamp) = ?
    ''', (selected_datetime,))
    
    attendance_records = c.fetchall()

    for record in attendance_records:
        print(f"Roll No: {record[0]}, Timestamp: {record[1]}")
    
    conn.close()

selected_date = '2024-06-17'
fetch_attendance_for_day(selected_date)
