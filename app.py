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
        
        # Module list display
        self.module_listbox = tk.Listbox(module_frame, height=5)
        self.module_listbox.grid(row=2, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        # Module buttons
        button_frame = tk.Frame(module_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=5)

        tk.Button(button_frame, text="Add Module", command=self.add_temp_module).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Remove Module", command=self.remove_temp_module).pack(side=tk.LEFT, padx=5)

        # Main buttons
        main_button_frame = tk.Frame(self.master)
        main_button_frame.pack(pady=10)

        tk.Button(main_button_frame, text="Save Student", command=self.add_student_with_modules).pack(side=tk.LEFT, padx=5)
        tk.Button(main_button_frame, text="Back", command=self.create_dashboard).pack(side=tk.LEFT, padx=5)
        
    def add_temp_module(self):
        """Add a module to the temporary list before saving the student."""
        module_name = self.module_entry.get()
        grade = self.grade_entry.get()

        if not module_name or not grade:
            messagebox.showerror("Error", "Both module name and grade are required!")
            return

        try:
            grade = float(grade)
            if not (0 <= grade <= 100):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Grade must be a number between 0 and 100!")
            return

        self.temp_modules.append((module_name, grade))
        self.update_module_listbox()
        self.module_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)

    def remove_temp_module(self):
        """Remove a module from the temporary list."""
        try:
            selection = self.module_listbox.curselection()
            if selection:
                index = selection[0]
                self.temp_modules.pop(index)
                self.update_module_listbox()
        except IndexError:
            messagebox.showerror("Error", "Please select a module to remove")

    def update_module_listbox(self):
        """Update the listbox with current modules."""
        self.module_listbox.delete(0, tk.END)
        for module, grade in self.temp_modules:
            self.module_listbox.insert(tk.END, f"{module}: {grade}")
        

    def add_student_with_modules(self):
        """Add a student with all their modules."""
        student_id = self.student_id_entry.get()
        name = self.name_entry.get()
        age = self.age_entry.get()
        course = self.course_entry.get()
        phone = self.phone_entry.get()

        if not student_id or not name or not age or not course or not phone:
            messagebox.showerror("Error", "All student fields are required!")
            return

        try:
            age = int(age)
            if age <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Age must be a positive integer!")
            return

        if self.db.add_student(student_id, name, age, course, phone):
            # Add all temporary modules to the database
            for module, grade in self.temp_modules:
                self.db.add_module(student_id, module, grade)

            messagebox.showinfo("Success", "Student and modules added successfully!")
            self.create_dashboard()
        else:
            messagebox.showerror("Error", "Student ID already exists!")
            
    def view_students(self):
        """View students and their GPA."""
        self.clear_window()
        tk.Label(self.master, text="Student List", font=("Arial", 16)).pack(pady=10)

        self.tree = ttk.Treeview(self.master, columns=("ID", "Name", "Age", "Course", "Phone", "GPA"), show="headings")
        for col in ("ID", "Name", "Age", "Course", "Phone", "GPA"):
            self.tree.heading(col, text=col)

        for student in self.db.get_students():
            GPA = self.db.calculate_GPA(student[0])
            self.tree.insert("", "end", values=(student[0], student[1], student[2], student[3], student[4],GPA))

        # Bind double-click for module management
        self.tree.bind("<Double-1>", self.student_options)

        # Bind right-click for context menu
        self.tree.bind("<Button-3>", self.show_context_menu)

        self.tree.pack(expand=True, fill=tk.BOTH)

        tk.Button(self.master, text="Back", command=self.create_dashboard).pack()        
        
    def show_context_menu(self, event):
        """Show context menu on right-click with delete and update options."""
        # Identify the item that was right-clicked
        item = self.tree.identify_row(event.y)
        if item:
            # Select the item
            self.tree.selection_set(item)

            # Create a popup menu
            menu = tk.Menu(self.master, tearoff=0)
            menu.add_command(label="Update Modules/Grades",
                             command=lambda: self.manage_modules(self.tree.item(item, "values")[0]))
            menu.add_command(label="Delete Student", command=lambda: self.delete_student(self.tree, item))
            menu.post(event.x_root, event.y_root)

    def delete_student(self, tree, item):
        """Delete the selected student."""
        student_id = tree.item(item, "values")[0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student {student_id}?"):
            if self.db.delete_student(student_id):
                messagebox.showinfo("Success", "Student deleted successfully!")
                self.view_students()  # Refresh the view
            else:
                messagebox.showerror("Error", "Failed to delete student")

    def student_options(self, event):
        """Handle double-click to manage modules."""
        item = event.widget.selection()[0]
        student_id = event.widget.item(item, "values")[0]
        self.manage_modules(student_id)
        
    def manage_modules(self, student_id):
        """Module management window."""
        self.clear_window()
        student = self.db.students.get(student_id, ["Unknown"])
        tk.Label(self.master, text=f"Manage Modules for {student[0]} (ID: {student_id})", font=("Arial", 16)).pack(pady=10)

        # Module List
        self.module_tree = ttk.Treeview(self.master, columns=("Module", "Grade"), show="headings")
        self.module_tree.heading("Module", text="Module")
        self.module_tree.heading("Grade", text="Grade")

        for module in self.db.get_modules(student_id):
            self.module_tree.insert("", "end", values=module)

        self.module_tree.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        # Bind right-click on module tree
        self.module_tree.bind("<Button-3>", lambda e: self.show_module_context_menu(e, student_id))

        # Add Module
        add_frame = tk.Frame(self.master)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Module Name:").pack(side=tk.LEFT)
        self.module_entry = tk.Entry(add_frame)
        self.module_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(add_frame, text="Grade:").pack(side=tk.LEFT)
        self.grade_entry = tk.Entry(add_frame)
        self.grade_entry.pack(side=tk.LEFT, padx=5)

        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Module", command=lambda: self.add_module(student_id)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back", command=self.view_students).pack(side=tk.LEFT, padx=5)