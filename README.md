
#  Student Management System (Python + Tkinter + CSV)

This is a **Student Management System** built with Python's Tkinter for the GUI and CSV for persistent data storage. It allows full **CRUD operations**, GPA calculation, and module/grade tracking per student.

---

## 📁 Project Structure

```
Student-Management-System/
├── main.py                 # Main executable file (GUI)
├── students.csv            # Stores student data
├── modules.csv             # Stores modules and grades
├── README.md               # Project overview and usage
├── documentation.pdf       # Technical documentation
```

---

##    Features

✅ Add, View, Update, and Delete Student Records  
✅ Add multiple Modules and Grades per student  
✅ GPA Calculation (based on custom grading logic)  
✅ CSV-based data storage (no database needed)  
✅ Error Handling with user-friendly messages  
✅ Lightweight GUI using Tkinter  

---

##   Technologies Used

- **Python 3.x**
- **Tkinter** (Standard Python GUI library)
- **CSV Module** (for file operations)

---

##   Requirements

Make sure you have:

- Python 3 installed
- No external libraries required (Tkinter and CSV are built-in)

To run the project:
```bash
python main.py
```

---

## 🗂️ File Descriptions

| File Name       | Description                              |
|----------------|------------------------------------------|
| `main.py`       | Main GUI and application logic          |
| `students.csv`  | Stores student personal information     |
| `modules.csv`   | Stores modules and corresponding grades |
| `documentation.pdf` | Full technical documentation        |
| `README.md`     | This file                                |

---

##    GPA Calculation Logic

| Marks Range | Grade Point |
|-------------|-------------|
| 90–100      | 4.0         |
| 80–89       | 3.7         |
| 70–79       | 3.3         |
| 60–69       | 3.0         |
| 50–59       | 2.7         |
| Below 50    | 0.0         |

---

##   Sample Use Case

1. Launch the app via `main.py`.
2. Add a new student with ID, name, phone, and course.
3. Add modules (e.g. "Math", "English") and enter grades.
4. Save and view the student details.
5. Re-open later to view/edit data saved in CSV.

---

## 📄 Documentation

For a full breakdown of modules, functions, GUI layout, data flow, and error handling – see `documentation.pdf`.

---

##  Author

   Emmanuel noel Kakwera  
📍DMI st Johns The Baptist University, Mangochi Campus  
📧 emmanuelkakwera4@gmail.com

---

## 🏁 License

This project is for academic and personal use only. Not for commercial distribution.

---
