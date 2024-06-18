import sqlite3
conn = sqlite3.connect('attendance.db')
c = conn.cursor()
students = [(roll_no,) for roll_no in range(202202001, 202202061)]
c.executemany('INSERT INTO students (roll_no) VALUES (?)', students)
conn.commit()
conn.close()
