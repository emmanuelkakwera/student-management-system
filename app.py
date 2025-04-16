import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import os


class Database:
    def __init__(self, students_file="students.csv", modules_file="modules.csv"):
        """Initialize student and module storage with CSV files."""
        self.students_file = students_file
        self.modules_file = modules_file
        self.students = {}  # {student_id: [name, age, course, phone]}
        self.modules = {}   # {student_id: [(module_name, grade), ...]}
        self.load_data()

    def load_data(self):
        """Load data from CSV files if they exist."""
        # Load students data
        if os.path.exists(self.students_file):
            try:
                with open(self.students_file, 'r', newline='') as f:
                    reader = csv.reader(f)
                    next(reader, None)  # Skip header
                    for row in reader:
                        if len(row) >= 5:  # Ensure we have all required fields
                            student_id, name, age, course, phone = row[:5]
                            self.students[student_id] = [name, int(age), course, phone]
            except (csv.Error, IOError, ValueError) as e:
                messagebox.showerror("Error", f"Failed to load students data: {str(e)}")
                self.students = {}

        # Load modules data
        if os.path.exists(self.modules_file):
            try:
                with open(self.modules_file, 'r', newline='') as f:
                    reader = csv.reader(f)
                    next(reader, None)  # Skip header
                    for row in reader:
                        if len(row) >= 3:  # Ensure we have all required fields
                            student_id, module_name, grade = row[:3]
                            if student_id not in self.modules:
                                self.modules[student_id] = []
                            self.modules[student_id].append((module_name, float(grade)))
            except (csv.Error, IOError, ValueError) as e:
                messagebox.showerror("Error", f"Failed to load modules data: {str(e)}")
                self.modules = {}

    def save_data(self):
        """Save data to CSV files."""
        # Save students data
        try:
            with open(self.students_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['student_id', 'name', 'age', 'course', 'phone'])  # Header
                for student_id, data in self.students.items():
                    writer.writerow([student_id] + data)
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save students data: {str(e)}")

        # Save modules data
        try:
            with open(self.modules_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['student_id', 'module_name', 'grade'])  # Header
                for student_id, modules in self.modules.items():
                    for module in modules:
                        writer.writerow([student_id, module[0], module[1]])
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save modules data: {str(e)}")

    def add_student(self, student_id, name, age, course, phone):
        """Add a new student."""
        if student_id in self.students:
            return False  # Student already exists
        self.students[student_id] = [name, age, course, phone]
        self.modules[student_id] = []
        self.save_data()
        return True

    def get_students(self):
        """Retrieve all students."""
        return [(id, *data) for id, data in self.students.items()]

    def add_module(self, student_id, module_name, grade):
        """Add a module and grade for a student."""
        if student_id in self.modules:
            self.modules[student_id].append((module_name, grade))
            self.save_data()

    def get_modules(self, student_id):
        """Retrieve all modules for a student."""
        return self.modules.get(student_id, [])

    def delete_module(self, student_id, module_name):
        """Remove a module from the student."""
        if student_id in self.modules:
            self.modules[student_id] = [mod for mod in self.modules[student_id] if mod[0] != module_name]
            self.save_data()

    def delete_student(self, student_id):
        """Delete a student from the database."""
        if student_id in self.students:
            del self.students[student_id]
        if student_id in self.modules:
            del self.modules[student_id]
        self.save_data()
        return True

    def update_module_grade(self, student_id, module_name, new_grade):
        """Update a module's grade for a student."""
        if student_id in self.modules:
            for i, (mod_name, _) in enumerate(self.modules[student_id]):
                if mod_name == module_name:
                    self.modules[student_id][i] = (module_name, new_grade)
                    self.save_data()
                    return True
        return False

    def calculate_GPA(self, student_id):
        """Calculate the GPA for a student."""
        grades = [grade for _, grade in self.modules.get(student_id, [])]
        if grades:
            return round(sum(grades) / len(grades), 2)
        return 0.0


class StudentManagementApp:
    def __init__(self, master):
        """Initialize the GUI."""
        self.master = master
        self.master.title("Student Management System")
        self.master.geometry("700x600")

        # Add window close handler
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        self.db = Database()
        self.create_dashboard()

    def on_close(self):
        """Handle window close event."""
        # Data is already saved automatically after each operation
        self.master.destroy()

    def create_dashboard(self):
        """Main dashboard."""
        self.clear_window()
        tk.Label(self.master, text="Student Management System", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.master, text="Add Student", command=self.add_student_window).pack(pady=5)
        tk.Button(self.master, text="View Students", command=self.view_students).pack(pady=5)

    def add_student_window(self):
        """Window to add a new student."""
        self.clear_window()
        tk.Label(self.master, text="Add New Student", font=("Arial", 16)).pack(pady=10)

        # Create a frame for student details
        student_frame = tk.Frame(self.master)
        student_frame.pack(pady=5)
        
           # Student details
        tk.Label(student_frame, text="Student ID:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.student_id_entry = tk.Entry(student_frame)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(student_frame, text="Name:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.name_entry = tk.Entry(student_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(student_frame, text="Age:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.age_entry = tk.Entry(student_frame)
        self.age_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(student_frame, text="Course:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.course_entry = tk.Entry(student_frame)
        self.course_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(student_frame, text="Phone:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.phone_entry = tk.Entry(student_frame)
        self.phone_entry.grid(row=4, column=1, padx=5, pady=5)

        # Module addition section
        module_frame = tk.LabelFrame(self.master, text="Add Modules", padx=10, pady=10)
        module_frame.pack(pady=10, fill=tk.X, padx=20)

        tk.Label(module_frame, text="Module Name:").grid(row=0, column=0, padx=5, pady=5)
        self.module_entry = tk.Entry(module_frame)
        self.module_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(module_frame, text="Grade:").grid(row=1, column=0, padx=5, pady=5)
        self.grade_entry = tk.Entry(module_frame)
        self.grade_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # List to store temporary modules before saving student
        self.temp_modules = []

