from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import pymysql
import subprocess
import os

app = Flask(__name__)

# MySQL connection setup
db = pymysql.connect(host="localhost", user="root", password="abc@123", database="payrolldb", cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def index():
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
    return render_template("index.html", employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        designation = request.form['designation']
        salary = float(request.form['salary'])
        hometown = request.form['hometown']
        with db.cursor() as cursor:
            cursor.execute("INSERT INTO employees (name, department, designation, salary, hometown) VALUES (%s, %s, %s, %s, %s)",
                        (name, department, designation, salary, hometown))
            db.commit()
        return redirect(url_for('index'))
    return render_template("add.html")

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM employees WHERE id = %s", (id,))
        emp = cursor.fetchone()
    if not emp:
        return "Employee not found", 404

    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        designation = request.form['designation']
        salary = float(request.form['salary'])
        hometown = request.form['hometown']
        with db.cursor() as cursor:
            cursor.execute("UPDATE employees SET name=%s, department=%s, designation=%s, salary=%s, hometown=%s WHERE id=%s",
                        (name, department, designation, salary, hometown, id))
            db.commit()
        return redirect(url_for('index'))

    return render_template("update.html", emp=emp)

@app.route('/delete/<int:id>')
def delete_employee(id):
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM employees WHERE id = %s", (id,))
        db.commit()
    return redirect(url_for('index'))

@app.route('/generate_pdf/<int:id>')
def generate_pdf(id):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM employees WHERE id = %s", (id,))
        emp = cursor.fetchone()

    if not emp:
        return "Employee not found", 404

    # Construct the command for the Java program to generate the PDF
    args = [
        "java", "-cp", "C:/Users/bharg/Downloads/employee_payroll/salary-slip/libs/itextpdf-5.5.13.3.jar;C:/Users/bharg/Downloads/employee_payroll/salary-slip/libs/json-20210307.jar;C:/Users/bharg/Downloads/employee_payroll/salary-slip/target/classes",
        "com.payroll.EmployeeSalarySlip", 
        str(emp['id']), emp['name'], emp['department'], emp['designation'], 
        str(emp['salary']), emp['hometown']
    ]

    try:
        # Run the Java program using subprocess
        subprocess.run(args, capture_output=True, text=True, check=True)
        pdf_filename = f"employee_{emp['id']}_salary_slip.pdf"
        
        # Return the generated PDF to the client
        return send_from_directory("static", pdf_filename, as_attachment=True)
    
    except subprocess.CalledProcessError as e:
        # Log the error in the server (console)
        print("Java program failed:", e.stderr)

        # Redirect back to the same page and show a failure message in the alert
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
