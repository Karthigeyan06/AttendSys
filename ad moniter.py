import tkinter as tk
from tkinter import messagebox
import sqlite3
import cv2
from pyzbar.pyzbar import decode

DATABASE = 'attendance.db'

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Attendance System")

        
        self.scan_button = tk.Button(root, text="Scan QR Code", command=self.scan_qr)
        self.scan_button.grid(row=0, column=0, padx=10, pady=10)

    def get_db_connection(self):
        return sqlite3.connect(DATABASE)

    def scan_qr(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "Failed to open webcam")
                return

            decoded_objects = decode(frame)
            for obj in decoded_objects:
                roll_no = obj.data.decode('utf-8')
                self.record_attendance(roll_no)
                messagebox.showinfo("Success", f"Attendance recorded for roll no: {roll_no}")
                cap.release()
                cv2.destroyAllWindows()
                return

            cv2.imshow("Scan QR Code", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def record_attendance(self, roll_no):
        conn = self.get_db_connection()
        c = conn.cursor()
        c.execute('SELECT roll_no FROM students WHERE roll_no = ?', (roll_no,))
        student_roll_no = c.fetchone()
        if student_roll_no:
            c.execute('INSERT INTO attendance (student_roll_no) VALUES (?)', (student_roll_no[0],))
            conn.commit()
        else:
            messagebox.showerror("Error", "Student not found")
        conn.close()

if __name__ == '__main__':
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
