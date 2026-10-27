import tkinter as tk
from tkinter import messagebox, filedialog
import pickle
import os

class StudentRecordManager:
    """
    A complete desktop record management utility built with tkinter.
    Captures user details via various widgets and persists the data to disk.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("GUI Student Record Manager")
        self.root.geometry("400x500")
        
        # Define Tkinter variables for dynamic widget binding
        self.name_var = tk.StringVar()
        self.id_var = tk.StringVar()
        self.gender_var = tk.StringVar(value="Not Specified")
        self.enrolled_var = tk.BooleanVar()
        
        self.create_widgets()

    def create_widgets(self):
        """Builds the multi-field entry forms, radiobuttons, checkbuttons, and text widgets."""
        # 1. Multi-field entry forms for basic details
        tk.Label(self.root, text="Student Name:").pack(pady=(10, 0))
        tk.Entry(self.root, textvariable=self.name_var, width=30).pack()
        
        tk.Label(self.root, text="Student ID:").pack(pady=(10, 0))
        tk.Entry(self.root, textvariable=self.id_var, width=30).pack()
        
        # 2. Dynamic Radiobutton selections for Gender
        tk.Label(self.root, text="Gender:").pack(pady=(10, 0))
        gender_frame = tk.Frame(self.root)
        gender_frame.pack()
        tk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male").pack(side=tk.LEFT)
        tk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female").pack(side=tk.LEFT)
        tk.Radiobutton(gender_frame, text="Other", variable=self.gender_var, value="Other").pack(side=tk.LEFT)
        
        # 3. Dynamic Checkbutton selection for Enrollment Status
        tk.Checkbutton(self.root, text="Currently Enrolled", variable=self.enrolled_var).pack(pady=(10, 0))
        
        # 4. Text widget for multi-line notes or address
        tk.Label(self.root, text="Additional Notes/Address:").pack(pady=(10, 0))
        self.notes_text = tk.Text(self.root, height=5, width=40)
        self.notes_text.pack()
        
        # 5. Action Buttons triggering native file dialogs
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Save Record", command=self.save_record, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Load Record", command=self.load_record, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Clear Form", command=self.clear_form, width=12).pack(side=tk.LEFT, padx=5)

    def save_record(self):
        """Gathers data from widgets and uses object persistence to write to disk."""
        student_data = {
            "name": self.name_var.get(),
            "id": self.id_var.get(),
            "gender": self.gender_var.get(),
            "enrolled": self.enrolled_var.get(),
            "notes": self.notes_text.get("1.0", tk.END).strip()
        }
        
        if not student_data["name"] or not student_data["id"]:
            messagebox.showwarning("Validation Error", "Name and ID are required fields.")
            return
            
        # Native file dialog to select save destination
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pkl", 
            filetypes=[("Pickle Data", "*.pkl"), ("All Files", "*.*")],
            title="Save Student Record"
        )
        
        if filepath:
            try:
                with open(filepath, 'wb') as file:
                    pickle.dump(student_data, file)
                messagebox.showinfo("Success", "Student record successfully saved!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save record: {e}")

    def load_record(self):
        """Retrieves object records visually alongside native file dialogs."""
        filepath = filedialog.askopenfilename(
            filetypes=[("Pickle Data", "*.pkl"), ("All Files", "*.*")],
            title="Open Student Record"
        )
        
        if filepath and os.path.exists(filepath):
            try:
                with open(filepath, 'rb') as file:
                    student_data = pickle.load(file)
                    
                # Populate the form visually with retrieved data
                self.name_var.set(student_data.get("name", ""))
                self.id_var.set(student_data.get("id", ""))
                self.gender_var.set(student_data.get("gender", "Not Specified"))
                self.enrolled_var.set(student_data.get("enrolled", False))
                
                self.notes_text.delete("1.0", tk.END)
                self.notes_text.insert("1.0", student_data.get("notes", ""))
                
                messagebox.showinfo("Success", "Student record loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load record: {e}")

    def clear_form(self):
        """Deletes the current data visually from the form."""
        self.name_var.set("")
        self.id_var.set("")
        self.gender_var.set("Not Specified")
        self.enrolled_var.set(False)
        self.notes_text.delete("1.0", tk.END)

def main():
    """Main execution function to run the GUI desktop record manager."""
    root = tk.Tk()
    app = StudentRecordManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()