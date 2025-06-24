import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import sqlite3
import os
import shutil
from datetime import datetime
from PIL import Image, ImageTk # type: ignore
import pandas as pd # type: ignore
import ttkthemes # type: ignore

# ---------- Global Style Configuration ----------
def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure colors
    primary_color = "#2196F3"  # Material Blue
    secondary_color = "#1976D2"  # Darker Blue
    bg_color = "#F5F5F5"  # Light Gray
    text_color = "#212121"  # Dark Gray
    
    # Configure common styles
    style.configure(".", font=("Segoe UI", 10), background=bg_color)
    style.configure("TLabel", padding=5, font=("Segoe UI", 10))
    style.configure("TButton",
                   padding=10,
                   font=("Segoe UI", 10),
                   background=primary_color,
                   foreground="white")
    style.map("TButton",
              background=[("active", secondary_color)],
              foreground=[("active", "white")])
    
    # Configure Treeview
    style.configure("Treeview",
                   background="white",
                   fieldbackground="white",
                   rowheight=25)
    style.configure("Treeview.Heading",
                   font=("Segoe UI", 10, "bold"),
                   padding=5)
    style.map("Treeview",
              background=[("selected", primary_color)],
              foreground=[("selected", "white")])
    
    # Configure Entry fields
    style.configure("TEntry", padding=5)
    
    return {
        "primary_color": primary_color,
        "secondary_color": secondary_color,
        "bg_color": bg_color,
        "text_color": text_color
    }

# Create custom styles for different buttons
def create_custom_buttons(style):
    # Primary button
    style.configure("Primary.TButton",
                   font=("Segoe UI", 10, "bold"),
                   background="#2196F3",
                   padding=10)
    
    # Danger button
    style.configure("Danger.TButton",
                   font=("Segoe UI", 10),
                   background="#f44336",
                   padding=10)
    
    # Success button
    style.configure("Success.TButton",
                   font=("Segoe UI", 10),
                   background="#4CAF50",
                   padding=10)

# ---------- Database Connection ----------
def connect_db():
    return sqlite3.connect("attendance_system.db")

# ---------- Main Dashboard ----------
def main_dashboard():
    for widget in root.winfo_children():
        widget.destroy()
    
    # Configure the main window
    root.configure(bg="#F5F5F5")
    root.title("Office Attendance System")
    
    # Create main frame
    main_frame = ttk.Frame(root, style="Main.TFrame")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Header with logo and title
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(fill="x", pady=(0, 30))
    
    title_label = ttk.Label(header_frame,
                           text="Office Attendance System",
                           font=("Segoe UI", 24, "bold"),
                           foreground="#2196F3")
    title_label.pack(pady=(20, 10))
    
    subtitle_label = ttk.Label(header_frame,
                              text="Welcome to the attendance management system",
                              font=("Segoe UI", 12))
    subtitle_label.pack()
    
    # Buttons frame
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(expand=True)
    
    # Admin button with icon
    admin_btn = ttk.Button(button_frame,
                          text="Admin Login",
                          style="Primary.TButton",
                          width=25,
                          command=admin_login_screen)
    admin_btn.pack(pady=10)
    
    # Employee button
    emp_btn = ttk.Button(button_frame,
                         text="Employee Login",
                         style="Primary.TButton",
                         width=25,
                         command=employee_login_screen)
    emp_btn.pack(pady=10)
    
    # Footer
    footer_frame = ttk.Frame(main_frame)
    footer_frame.pack(side="bottom", fill="x", pady=20)
    footer_label = ttk.Label(footer_frame,
                            text="© 2024 Office Attendance System",
                            font=("Segoe UI", 8))
    footer_label.pack()

# ---------- Admin Login ----------
def admin_login_screen():
    login_win = tk.Toplevel(root)
    login_win.title("Admin Login")
    login_win.geometry("400x500")
    login_win.configure(bg="#F5F5F5")
    
    # Make window modal
    login_win.transient(root)
    login_win.grab_set()
    
    # Center the window
    login_win.update_idletasks()
    width = login_win.winfo_width()
    height = login_win.winfo_height()
    x = (login_win.winfo_screenwidth() // 2) - (width // 2)
    y = (login_win.winfo_screenheight() // 2) - (height // 2)
    login_win.geometry(f"{width}x{height}+{x}+{y}")
    
    # Main frame
    main_frame = ttk.Frame(login_win)
    main_frame.pack(expand=True, fill="both", padx=40, pady=40)
    
    # Title
    title_label = ttk.Label(main_frame,
                           text="Admin Login",
                           font=("Segoe UI", 20, "bold"),
                           foreground="#2196F3")
    title_label.pack(pady=(0, 30))
    
    # Login form
    form_frame = ttk.Frame(main_frame)
    form_frame.pack(fill="x", padx=20)
    
    username_label = ttk.Label(form_frame,
                              text="Username",
                              font=("Segoe UI", 10))
    username_label.pack(anchor="w", pady=(0, 5))
    
    username_entry = ttk.Entry(form_frame, width=40)
    username_entry.pack(fill="x", pady=(0, 15))
    
    password_label = ttk.Label(form_frame,
                              text="Password",
                              font=("Segoe UI", 10))
    password_label.pack(anchor="w", pady=(0, 5))
    
    password_entry = ttk.Entry(form_frame, show="•", width=40)
    password_entry.pack(fill="x", pady=(0, 20))
    
    def validate_login():
        username = username_entry.get()
        password = password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Input Error",
                                 "Please enter both username and password",
                                 parent=login_win)
            return
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE username=? AND password=?",
                      (username, password))
        
        if cursor.fetchone():
            login_win.destroy()
            open_admin_dashboard()
        else:
            messagebox.showerror("Login Failed",
                               "Invalid username or password",
                               parent=login_win)
        conn.close()
    
    # Login button
    login_button = ttk.Button(form_frame,
                             text="Login",
                             style="Primary.TButton",
                             command=validate_login)
    login_button.pack(fill="x", pady=20)
    
    # Cancel button
    cancel_button = ttk.Button(form_frame,
                              text="Cancel",
                              style="Danger.TButton",
                              command=login_win.destroy)
    cancel_button.pack(fill="x")

# ---------- Employee Login ----------
def employee_login_screen():
    login_win = tk.Toplevel(root)
    login_win.title("Employee Login")
    login_win.geometry("400x500")
    login_win.configure(bg="#F5F5F5")
    
    # Make window modal
    login_win.transient(root)
    login_win.grab_set()
    
    # Center the window
    login_win.update_idletasks()
    width = login_win.winfo_width()
    height = login_win.winfo_height()
    x = (login_win.winfo_screenwidth() // 2) - (width // 2)
    y = (login_win.winfo_screenheight() // 2) - (height // 2)
    login_win.geometry(f"{width}x{height}+{x}+{y}")
    
    # Main frame
    main_frame = ttk.Frame(login_win)
    main_frame.pack(expand=True, fill="both", padx=40, pady=40)
    
    # Title
    title_label = ttk.Label(main_frame,
                           text="Employee Login",
                           font=("Segoe UI", 20, "bold"),
                           foreground="#2196F3")
    title_label.pack(pady=(0, 30))
    
    # Login form
    form_frame = ttk.Frame(main_frame)
    form_frame.pack(fill="x", padx=20)
    
    email_label = ttk.Label(form_frame,
                           text="Email",
                           font=("Segoe UI", 10))
    email_label.pack(anchor="w", pady=(0, 5))
    
    email_entry = ttk.Entry(form_frame, width=40)
    email_entry.pack(fill="x", pady=(0, 15))
    
    def validate_login():
        email = email_entry.get().strip()
        
        if not email:
            messagebox.showwarning("Input Error",
                                 "Please enter your email",
                                 parent=login_win)
            return
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM employees WHERE email=?", (email,))
        employee = cursor.fetchone()
        conn.close()
        
        if employee:
            login_win.destroy()
            open_employee_dashboard(employee[0], employee[1])  # Pass employee_id and name
        else:
            messagebox.showerror("Login Failed",
                               "Invalid email or employee not found",
                               parent=login_win)
    
    # Login button
    login_button = ttk.Button(form_frame,
                             text="Login",
                             style="Primary.TButton",
                             command=validate_login)
    login_button.pack(fill="x", pady=20)
    
    # Cancel button
    cancel_button = ttk.Button(form_frame,
                              text="Cancel",
                              style="Danger.TButton",
                              command=login_win.destroy)
    cancel_button.pack(fill="x")

# ---------- Admin Dashboard ----------
def open_admin_dashboard():
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Dashboard")
    admin_window.geometry("800x600")
    admin_window.configure(bg="#F5F5F5")
    
    # Make window modal
    admin_window.transient(root)
    admin_window.grab_set()
    
    # Center the window
    admin_window.update_idletasks()
    width = admin_window.winfo_width()
    height = admin_window.winfo_height()
    x = (admin_window.winfo_screenwidth() // 2) - (width // 2)
    y = (admin_window.winfo_screenheight() // 2) - (height // 2)
    admin_window.geometry(f"{width}x{height}+{x}+{y}")
    
    # Create main container
    main_container = ttk.Frame(admin_window)
    main_container.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Header
    header_frame = ttk.Frame(main_container)
    header_frame.pack(fill="x", pady=(0, 20))
    
    title_label = ttk.Label(header_frame,
                           text="Admin Dashboard",
                           font=("Segoe UI", 24, "bold"),
                           foreground="#2196F3")
    title_label.pack(side="left")
    
    # Logout button
    logout_btn = ttk.Button(header_frame,
                           text="Logout",
                           style="Danger.TButton",
                           command=admin_window.destroy)
    logout_btn.pack(side="right")
    
    # Create notebook for different sections
    notebook = ttk.Notebook(main_container)
    notebook.pack(expand=True, fill="both")
    
    # Employee Management Tab
    emp_frame = ttk.Frame(notebook)
    notebook.add(emp_frame, text="Employee Management")
    
    emp_actions_frame = ttk.Frame(emp_frame)
    emp_actions_frame.pack(fill="x", padx=10, pady=10)
    
    ttk.Button(emp_actions_frame,
               text="Add Employee",
               style="Primary.TButton",
               command=open_add_employee_form).pack(side="left", padx=5)
    
    ttk.Button(emp_actions_frame,
               text="Delete Employee",
               style="Danger.TButton",
               command=delete_employee).pack(side="left", padx=5)
    
    # Employee list
    emp_list_frame = ttk.Frame(emp_frame)
    emp_list_frame.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Create Treeview for employee list
    emp_tree = ttk.Treeview(emp_list_frame,
                           columns=("ID", "Name", "Email", "Phone", "Gender", "Role"),
                           show='headings')
    
    # Configure columns
    emp_tree.heading("ID", text="ID")
    emp_tree.heading("Name", text="Name")
    emp_tree.heading("Email", text="Email")
    emp_tree.heading("Phone", text="Phone")
    emp_tree.heading("Gender", text="Gender")
    emp_tree.heading("Role", text="Role")
    
    # Set column widths
    emp_tree.column("ID", width=50)
    emp_tree.column("Name", width=150)
    emp_tree.column("Email", width=200)
    emp_tree.column("Phone", width=120)
    emp_tree.column("Gender", width=80)
    emp_tree.column("Role", width=150)
    
    # Add scrollbar
    emp_scrollbar = ttk.Scrollbar(emp_list_frame, orient="vertical", command=emp_tree.yview)
    emp_tree.configure(yscrollcommand=emp_scrollbar.set)
    
    emp_scrollbar.pack(side="right", fill="y")
    emp_tree.pack(expand=True, fill="both")
    
    # Load employee data
    def load_employee_data():
        for item in emp_tree.get_children():
            emp_tree.delete(item)
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, phone, Gender, Role FROM employees")
        for row in cursor.fetchall():
            emp_tree.insert("", tk.END, values=row)
        conn.close()
    
    load_employee_data()
    
    # Refresh button
    ttk.Button(emp_actions_frame,
               text="Refresh",
               style="Success.TButton",
               command=load_employee_data).pack(side="right", padx=5)
    
    # Leave Management Tab
    leave_frame = ttk.Frame(notebook)
    notebook.add(leave_frame, text="Leave Management")
    
    # Leave requests table
    leave_tree = ttk.Treeview(leave_frame,
                             columns=("ID", "Employee", "Date", "Reason", "Status"),
                             show='headings')
    
    # Configure columns
    leave_tree.heading("ID", text="ID")
    leave_tree.heading("Employee", text="Employee")
    leave_tree.heading("Date", text="Date")
    leave_tree.heading("Reason", text="Reason")
    leave_tree.heading("Status", text="Status")
    
    # Set column widths
    leave_tree.column("ID", width=50)
    leave_tree.column("Employee", width=150)
    leave_tree.column("Date", width=100)
    leave_tree.column("Reason", width=250)
    leave_tree.column("Status", width=100)
    
    # Add scrollbar
    leave_scrollbar = ttk.Scrollbar(leave_frame, orient="vertical", command=leave_tree.yview)
    leave_tree.configure(yscrollcommand=leave_scrollbar.set)
    
    leave_scrollbar.pack(side="right", fill="y")
    leave_tree.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Leave action buttons
    leave_actions_frame = ttk.Frame(leave_frame)
    leave_actions_frame.pack(fill="x", padx=10, pady=10)
    
    def load_leave_requests():
        for item in leave_tree.get_children():
            leave_tree.delete(item)
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.id, e.name, l.date, l.reason, l.status
            FROM leaves l
            JOIN employees e ON l.employee_id = e.id
            WHERE l.status = 'Pending'
        """)
        for row in cursor.fetchall():
            leave_tree.insert("", tk.END, values=row)
        conn.close()
    
    def update_leave_status(status):
        selected_item = leave_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required",
                                 "Please select a leave request to update",
                                 parent=admin_window)
            return
        
        leave_id = leave_tree.item(selected_item[0])['values'][0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE leaves SET status = ? WHERE id = ?", (status, leave_id))
        conn.commit()
        conn.close()
        
        load_leave_requests()
        messagebox.showinfo("Success",
                          f"Leave request {status.lower()} successfully",
                          parent=admin_window)
    
    ttk.Button(leave_actions_frame,
               text="Approve Selected",
               style="Success.TButton",
               command=lambda: update_leave_status('Approved')).pack(side="left", padx=5)
    
    ttk.Button(leave_actions_frame,
               text="Reject Selected",
               style="Danger.TButton",
               command=lambda: update_leave_status('Rejected')).pack(side="left", padx=5)
    
    ttk.Button(leave_actions_frame,
               text="Refresh",
               style="Primary.TButton",
               command=load_leave_requests).pack(side="right", padx=5)
    
    # Load initial leave data
    load_leave_requests()

# ---------- Add Employee Form ----------
def open_add_employee_form():
    add_employee_window = tk.Toplevel(root)
    add_employee_window.title("Add Employee")
    add_employee_window.geometry("500x600")
    add_employee_window.configure(bg="#F5F5F5")
    
    # Make window modal
    add_employee_window.transient(root)
    add_employee_window.grab_set()
    
    # Center the window
    add_employee_window.update_idletasks()
    width = add_employee_window.winfo_width()
    height = add_employee_window.winfo_height()
    x = (add_employee_window.winfo_screenwidth() // 2) - (width // 2)
    y = (add_employee_window.winfo_screenheight() // 2) - (height // 2)
    add_employee_window.geometry(f"{width}x{height}+{x}+{y}")
    
    # Main container
    main_frame = ttk.Frame(add_employee_window)
    main_frame.pack(expand=True, fill="both", padx=40, pady=40)
    
    # Title
    title_label = ttk.Label(main_frame,
                           text="Add New Employee",
                           font=("Segoe UI", 20, "bold"),
                           foreground="#2196F3")
    title_label.pack(pady=(0, 30))
    
    # Form frame
    form_frame = ttk.Frame(main_frame)
    form_frame.pack(fill="x")
    
    # Create form fields
    fields = [
        ("Name", "name"),
        ("Email", "email"),
        ("Phone", "phone"),
        ("Gender", "gender"),
        ("Role", "role")
    ]
    
    entries = {}
    
    for label_text, field_name in fields:
        # Field container
        field_frame = ttk.Frame(form_frame)
        field_frame.pack(fill="x", pady=10)
        
        # Label
        label = ttk.Label(field_frame,
                         text=label_text,
                         font=("Segoe UI", 10))
        label.pack(anchor="w")
        
        # Entry
        if field_name == "gender":
            entry = ttk.Combobox(field_frame,
                               values=["Male", "Female", "Other"],
                               state="readonly")
            entry.set("Select Gender")
        elif field_name == "role":
            entry = ttk.Combobox(field_frame,
                               values=["Manager", "Developer", "HR", "Designer", "Other"],
                               state="readonly")
            entry.set("Select Role")
        else:
            entry = ttk.Entry(field_frame)
        
        entry.pack(fill="x", pady=(5, 0))
        entries[field_name] = entry
    
    def validate_email(email):
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(phone):
        import re
        pattern = r'^\+?1?\d{9,15}$'
        return re.match(pattern, phone) is not None
    
    def save_employee():
        # Get values
        name = entries['name'].get().strip()
        email = entries['email'].get().strip()
        phone = entries['phone'].get().strip()
        gender = entries['gender'].get()
        role = entries['role'].get()
        
        # Validation
        if not all([name, email, phone, gender, role]):
            messagebox.showwarning("Input Error",
                                 "All fields are required!",
                                 parent=add_employee_window)
            return
        
        if not validate_email(email):
            messagebox.showwarning("Invalid Email",
                                 "Please enter a valid email address",
                                 parent=add_employee_window)
            return
        
        if not validate_phone(phone):
            messagebox.showwarning("Invalid Phone",
                                 "Please enter a valid phone number",
                                 parent=add_employee_window)
            return
        
        if gender == "Select Gender":
            messagebox.showwarning("Invalid Gender",
                                 "Please select a gender",
                                 parent=add_employee_window)
            return
        
        if role == "Select Role":
            messagebox.showwarning("Invalid Role",
                                 "Please select a role",
                                 parent=add_employee_window)
            return
        
        # Save to database
        try:
            conn = connect_db()
            cursor = conn.cursor()
            
            # Check for duplicate email
            cursor.execute("SELECT * FROM employees WHERE email = ?", (email,))
            if cursor.fetchone():
                messagebox.showerror("Duplicate Email",
                                   "An employee with this email already exists",
                                   parent=add_employee_window)
                conn.close()
                return
            
            # Insert new employee
            cursor.execute("""
                INSERT INTO employees (name, email, phone, Gender, Role)
                VALUES (?, ?, ?, ?, ?)
            """, (name, email, phone, gender, role))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success",
                              "Employee added successfully!",
                              parent=add_employee_window)
            add_employee_window.destroy()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error",
                               f"An error occurred: {str(e)}",
                               parent=add_employee_window)
    
    # Buttons frame
    button_frame = ttk.Frame(form_frame)
    button_frame.pack(fill="x", pady=30)
    
    # Save button
    save_button = ttk.Button(button_frame,
                            text="Save Employee",
                            style="Primary.TButton",
                            command=save_employee)
    save_button.pack(side="left", padx=5)
    
    # Cancel button
    cancel_button = ttk.Button(button_frame,
                              text="Cancel",
                              style="Danger.TButton",
                              command=add_employee_window.destroy)
    cancel_button.pack(side="right", padx=5)

# ---------- View Employee List ----------
def view_employee_list():
    view_window = tk.Toplevel(root)
    view_window.title("Employee List")
    view_window.geometry("600x300")

    tree = ttk.Treeview(view_window, columns=("ID", "Name", "Email", "Phone", "Gender", "Role"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Email", text="Email")
    tree.heading("Phone", text="Phone")
    tree.heading("Gender", text="Gender")
    tree.heading("Role", text="Role")
    tree.pack(fill=tk.BOTH, expand=True)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, phone, Gender, Role FROM employees")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()

# ---------- Delete Employee ----------
def delete_employee():
    del_window = tk.Toplevel(root)
    del_window.title("Delete Employee")
    del_window.geometry("300x150")

    tk.Label(del_window, text="Enter Employee ID to Delete").pack(pady=10)
    emp_id_entry = tk.Entry(del_window)
    emp_id_entry.pack(pady=5)

    def delete_from_db():
        emp_id = emp_id_entry.get()
        if not emp_id.isdigit():
            messagebox.showerror("Invalid Input", "Enter a valid Employee ID")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
        if cursor.fetchone() is None:
            messagebox.showerror("Error", "Employee ID not found")
        else:
            cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
            conn.commit()
            messagebox.showinfo("Deleted", f"Employee ID {emp_id} deleted successfully")
        conn.close()
        del_window.destroy()

    tk.Button(del_window, text="Delete", command=delete_from_db).pack(pady=10)

# ---------- Leave Management ----------
def manage_leaves():
    leave_window = tk.Toplevel(root)
    leave_window.title("Leave Management")
    leave_window.geometry("500x400")

    tk.Label(leave_window, text="Employee ID").pack(pady=5)
    emp_id_entry = tk.Entry(leave_window)
    emp_id_entry.pack(pady=5)

    tk.Label(leave_window, text="Leave Date (YYYY-MM-DD)").pack(pady=5)
    leave_date_entry = tk.Entry(leave_window)
    leave_date_entry.pack(pady=5)

    tk.Label(leave_window, text="Reason").pack(pady=5)
    reason_entry = tk.Entry(leave_window)
    reason_entry.pack(pady=5)

    def apply_leave():
        emp_id = emp_id_entry.get()
        leave_date = leave_date_entry.get()
        reason = reason_entry.get()

        if not emp_id or not leave_date or not reason:
            messagebox.showwarning("Input Error", "All fields must be filled!")
            return
        try:
            leave_date_obj = datetime.strptime(leave_date, "%Y-%m-%d").date()
            today = datetime.now().date()
            
            if leave_date_obj < today:
                messagebox.showerror("Invalid Date", "You can only apply for upcoming dates.")
                return
        except ValueError:
            messagebox.showerror("Invalid Format", "Enter the date in YYYY-MM-DD format.")
            return
        
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO leaves (employee_id, date, reason, status) VALUES (?, ?, ?, 'Pending')",
                       (emp_id, leave_date, reason))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Leave applied successfully!")

    ttk.Button(leave_window, text="Apply Leave", command=apply_leave).pack(pady=10)

# ---------- Approve Leaves ----------
def approve_leaves():
    approve_window = tk.Toplevel(root)
    approve_window.title("Approve/Reject Leaves")
    approve_window.geometry("700x400")

    tree = ttk.Treeview(approve_window, columns=("ID", "Employee ID", "Date", "Reason", "Status"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Employee ID", text="Employee ID")
    tree.heading("Date", text="Date")
    tree.heading("Reason", text="Reason")
    tree.heading("Status", text="Status")
    tree.pack(fill=tk.BOTH, expand=True)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, employee_id, date, reason, status FROM leaves WHERE status = 'Pending'")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

    def update_leave_status(status):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "No leave selected")
            return

        leave_id = tree.item(selected_item[0])['values'][0]
        cursor.execute("UPDATE leaves SET status = ? WHERE id = ?", (status,leave_id))
        conn.commit()
        messagebox.showinfo("Success", f"Leave {status.lower()} successfully!")
        approve_window.destroy()
        conn.close()

    ttk.Button(approve_window, text="Approve Selected", command=lambda: update_leave_status('Approved')).pack(pady=5)
    ttk.Button(approve_window, text="Reject Selected", command=lambda: update_leave_status('Rejected')).pack(pady=5)

# ---------- Employee Dashboard ----------
def open_employee_dashboard(employee_id, employee_name):
    emp_window = tk.Toplevel(root)
    emp_window.title(f"Employee Dashboard - {employee_name}")
    emp_window.geometry("800x600")
    emp_window.configure(bg="#F5F5F5")
    
    # Make window modal
    emp_window.transient(root)
    emp_window.grab_set()
    
    # Center the window
    emp_window.update_idletasks()
    width = emp_window.winfo_width()
    height = emp_window.winfo_height()
    x = (emp_window.winfo_screenwidth() // 2) - (width // 2)
    y = (emp_window.winfo_screenheight() // 2) - (height // 2)
    emp_window.geometry(f"{width}x{height}+{x}+{y}")
    
    # Main container
    main_container = ttk.Frame(emp_window)
    main_container.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Header
    header_frame = ttk.Frame(main_container)
    header_frame.pack(fill="x", pady=(0, 20))
    
    title_label = ttk.Label(header_frame,
                           text=f"Welcome, {employee_name}",
                           font=("Segoe UI", 24, "bold"),
                           foreground="#2196F3")
    title_label.pack(side="left")
    
    # Logout button
    logout_btn = ttk.Button(header_frame,
                           text="Logout",
                           style="Danger.TButton",
                           command=emp_window.destroy)
    logout_btn.pack(side="right")
    
    # Create notebook for different sections
    notebook = ttk.Notebook(main_container)
    notebook.pack(expand=True, fill="both")
    
    # Attendance Tab
    attendance_frame = ttk.Frame(notebook)
    notebook.add(attendance_frame, text="Attendance")
    
    # Attendance actions frame
    attendance_actions = ttk.Frame(attendance_frame)
    attendance_actions.pack(fill="x", padx=10, pady=10)
    
    def mark_attendance():
        mark_attendance_manually(emp_window, employee_id)
    
    # Mark attendance button
    mark_btn = ttk.Button(attendance_actions,
                         text="Mark Attendance",
                         style="Primary.TButton",
                         command=mark_attendance)
    mark_btn.pack(side="left", padx=5)
    
    # Attendance history label
    history_label = ttk.Label(attendance_frame,
                            text="Attendance History",
                            font=("Segoe UI", 14, "bold"),
                            foreground="#2196F3")
    history_label.pack(pady=(20, 10))

    # Filter frame
    filter_frame = ttk.Frame(attendance_frame)
    filter_frame.pack(fill="x", padx=10, pady=5)

    # Month filter
    month_label = ttk.Label(filter_frame, text="Select Month:")
    month_label.pack(side="left", padx=(0, 5))
    
    months = ["All", "January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    month_var = tk.StringVar(value="All")
    month_combo = ttk.Combobox(filter_frame, 
                              values=months,
                              textvariable=month_var,
                              state="readonly",
                              width=15)
    month_combo.pack(side="left", padx=5)

    # Year filter
    year_label = ttk.Label(filter_frame, text="Select Year:")
    year_label.pack(side="left", padx=(20, 5))
    
    current_year = datetime.now().year
    years = ["All"] + [str(year) for year in range(current_year, current_year-5, -1)]
    year_var = tk.StringVar(value="All")
    year_combo = ttk.Combobox(filter_frame,
                             values=years,
                             textvariable=year_var,
                             state="readonly",
                             width=10)
    year_combo.pack(side="left", padx=5)

    # Statistics frame
    stats_frame = ttk.LabelFrame(attendance_frame, text="Monthly Statistics")
    stats_frame.pack(fill="x", padx=10, pady=10)

    # Statistics labels
    stats_grid = ttk.Frame(stats_frame)
    stats_grid.pack(padx=10, pady=5)

    present_label = ttk.Label(stats_grid, text="Present: 0")
    present_label.grid(row=0, column=0, padx=20, pady=5)

    absent_label = ttk.Label(stats_grid, text="Absent: 0")
    absent_label.grid(row=0, column=1, padx=20, pady=5)

    total_label = ttk.Label(stats_grid, text="Total Days: 0")
    total_label.grid(row=0, column=2, padx=20, pady=5)

    # Attendance table frame
    attendance_table_frame = ttk.Frame(attendance_frame)
    attendance_table_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # Create Treeview for attendance
    attendance_tree = ttk.Treeview(attendance_table_frame,
                                 columns=("Date", "Day", "Time", "Status"),
                                 show='headings')

    # Configure columns
    attendance_tree.heading("Date", text="Date")
    attendance_tree.heading("Day", text="Day")
    attendance_tree.heading("Time", text="Time")
    attendance_tree.heading("Status", text="Status")

    # Set column widths
    attendance_tree.column("Date", width=100)
    attendance_tree.column("Day", width=100)
    attendance_tree.column("Time", width=100)
    attendance_tree.column("Status", width=100)

    # Add scrollbar
    attendance_scrollbar = ttk.Scrollbar(attendance_table_frame,
                                       orient="vertical",
                                       command=attendance_tree.yview)
    attendance_tree.configure(yscrollcommand=attendance_scrollbar.set)

    attendance_scrollbar.pack(side="right", fill="y")
    attendance_tree.pack(expand=True, fill="both")

    def update_statistics(records):
        present_count = sum(1 for r in records if r[3] == 'Present')
        total_count = len(records)
        absent_count = total_count - present_count

        present_label.config(text=f"Present: {present_count}")
        absent_label.config(text=f"Absent: {absent_count}")
        total_label.config(text=f"Total Days: {total_count}")

    def load_attendance_history():
        # Clear existing items
        for item in attendance_tree.get_children():
            attendance_tree.delete(item)

        # Get filter values
        selected_month = month_var.get()
        selected_year = year_var.get()

        # Prepare SQL query based on filters
        query = """
            SELECT date, time, status
            FROM attendance
            WHERE employee_id = ?
        """
        params = [employee_id]

        if selected_year != "All":
            query += " AND strftime('%Y', date) = ?"
            params.append(selected_year)

        if selected_month != "All":
            month_num = str(months.index(selected_month)).zfill(2)
            query += " AND strftime('%m', date) = ?"
            params.append(month_num)

        query += " ORDER BY date DESC, time DESC"

        # Load attendance history from database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(query, params)
        records = cursor.fetchall()
        
        # Process and display records
        display_records = []
        for date_str, time_str, status in records:
            # Convert date string to datetime
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            # Get day name
            day_name = date_obj.strftime("%A")
            # Format date for display
            formatted_date = date_obj.strftime("%d-%m-%Y")
            
            display_records.append((formatted_date, day_name, time_str, status))
            attendance_tree.insert("", "end", values=(formatted_date, day_name, time_str, status))

        conn.close()

        # Update statistics
        update_statistics(display_records)

    # Bind filter changes to reload attendance
    month_combo.bind('<<ComboboxSelected>>', lambda e: load_attendance_history())
    year_combo.bind('<<ComboboxSelected>>', lambda e: load_attendance_history())

    # Add refresh button for attendance
    refresh_btn = ttk.Button(filter_frame,
                            text="Refresh",
                            style="Success.TButton",
                            command=load_attendance_history)
    refresh_btn.pack(side="right", padx=5)

    # Load initial attendance history
    load_attendance_history()

    # Leave Management Tab
    leave_frame = ttk.Frame(notebook)
    notebook.add(leave_frame, text="Leave Management")
    
    # Leave request form
    leave_form_frame = ttk.LabelFrame(leave_frame, text="Request Leave")
    leave_form_frame.pack(fill="x", padx=10, pady=10)
    
    # Date picker frame
    date_frame = ttk.Frame(leave_form_frame)
    date_frame.pack(fill="x", padx=10, pady=10)
    
    ttk.Label(date_frame, text="Leave Date:").pack(side="left", padx=(0, 10))
    
    # Date entry (you might want to add a calendar widget here)
    date_entry = ttk.Entry(date_frame)
    date_entry.pack(side="left", expand=True, fill="x")
    ttk.Label(date_frame, text="(YYYY-MM-DD)").pack(side="left", padx=(5, 0))
    
    # Reason frame
    reason_frame = ttk.Frame(leave_form_frame)
    reason_frame.pack(fill="x", padx=10, pady=10)
    
    ttk.Label(reason_frame, text="Reason:").pack(anchor="w")
    reason_text = tk.Text(reason_frame, height=4)
    reason_text.pack(fill="x", pady=(5, 0))
    
    def submit_leave_request():
        leave_date = date_entry.get().strip()
        reason = reason_text.get("1.0", "end-1c").strip()
        
        if not leave_date or not reason:
            messagebox.showwarning("Input Error",
                                 "Please fill in all fields",
                                 parent=emp_window)
            return
        
        try:
            # Validate date format
            datetime.strptime(leave_date, "%Y-%m-%d")
            
            # Save to database
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO leaves (employee_id, date, reason, status)
                VALUES (?, ?, ?, 'Pending')
            """, (employee_id, leave_date, reason))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success",
                              "Leave request submitted successfully!",
                              parent=emp_window)
            
            # Clear form
            date_entry.delete(0, "end")
            reason_text.delete("1.0", "end")
            
            # Refresh leave history
            load_leave_history()
            
        except ValueError:
            messagebox.showerror("Invalid Date",
                               "Please enter date in YYYY-MM-DD format",
                               parent=emp_window)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error",
                               f"An error occurred: {str(e)}",
                               parent=emp_window)
    
    # Submit button
    submit_btn = ttk.Button(leave_form_frame,
                           text="Submit Request",
                           style="Primary.TButton",
                           command=submit_leave_request)
    submit_btn.pack(pady=10)
    
    # Leave history
    history_frame = ttk.LabelFrame(leave_frame, text="Leave History")
    history_frame.pack(expand=True, fill="both", padx=10, pady=10)
    
    leave_tree = ttk.Treeview(history_frame,
                             columns=("Date", "Reason", "Status"),
                             show='headings')
    
    # Configure columns
    leave_tree.heading("Date", text="Date")
    leave_tree.heading("Reason", text="Reason")
    leave_tree.heading("Status", text="Status")
    
    # Set column widths
    leave_tree.column("Date", width=100)
    leave_tree.column("Reason", width=300)
    leave_tree.column("Status", width=100)
    
    # Add scrollbar
    leave_scrollbar = ttk.Scrollbar(history_frame,
                                   orient="vertical",
                                   command=leave_tree.yview)
    leave_tree.configure(yscrollcommand=leave_scrollbar.set)
    
    leave_scrollbar.pack(side="right", fill="y")
    leave_tree.pack(expand=True, fill="both")
    
    def load_leave_history():
        # Clear existing items
        for item in leave_tree.get_children():
            leave_tree.delete(item)
        
        # Load leave history from database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, reason, status
            FROM leaves
            WHERE employee_id = ?
            ORDER BY date DESC
        """, (employee_id,))
        
        for row in cursor.fetchall():
            leave_tree.insert("", "end", values=row)
        
        conn.close()
    
    # Load initial leave history
    load_leave_history()

def mark_attendance_manually(parent_window, employee_id):
    # Get current date and time
    current_datetime = datetime.now()
    current_date = current_datetime.strftime("%Y-%m-%d")
    current_time = current_datetime.strftime("%H:%M:%S")
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Check if attendance already marked for today
        cursor.execute("""
            SELECT * FROM attendance
            WHERE employee_id = ? AND date = ?
        """, (employee_id, current_date))
        
        if cursor.fetchone():
            messagebox.showinfo("Already Marked",
                              "Attendance already marked for today",
                              parent=parent_window)
        else:
            # Mark attendance
            cursor.execute("""
                INSERT INTO attendance (employee_id, date, time, status)
                VALUES (?, ?, ?, 'Present')
            """, (employee_id, current_date, current_time))
            
            conn.commit()
            messagebox.showinfo("Success",
                              "Attendance marked successfully!",
                              parent=parent_window)
        
        conn.close()
        
    except sqlite3.Error as e:
        messagebox.showerror("Database Error",
                           f"An error occurred: {str(e)}",
                           parent=parent_window)

# ---------- Run Application ----------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Office Attendance System")
    root.geometry("800x600")
    root.configure(bg="#F5F5F5")
    
    # Configure styles
    styles = configure_styles()
    create_custom_buttons(ttk.Style())
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Show main dashboard
    main_dashboard()
    
    # Start the application
    root.mainloop()
