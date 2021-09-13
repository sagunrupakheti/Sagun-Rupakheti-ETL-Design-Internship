import psycopg2
try:
    connection = psycopg2.connect(
        host="localhost",
        database="ETLweek1",
        user="postgres",
        password="sagun",
        port=5432
    )
    cursor = connection.cursor()

    # department table (DIMENSION TABLE)
    cursor.execute("CREATE TABLE department(department_id INT PRIMARY KEY,department_name TEXT NOT NULL);")

    # attendance table (DIMENSION TABLE)
    cursor.execute("CREATE TABLE attendance(attendance_id SERIAL PRIMARY KEY,punch_apply_date DATE NOT NULL,paycode TEXT NOT NULL)")

    # employee table (DIMENSION TABLE)
    cursor.execute("CREATE TABLE employee(employee_id int PRIMARY KEY,first_name TEXT NOT NULL,last_name TEXT NOT NULL,"
                   "dob DATE NOT NULL, manager_employee_id int NOT NULL, employee_role TEXT NOT NULL, salary int NOT NULL,"
                   "fte float NOT NULL,hire_date DATE NOT NULL, terminated_date DATE, terminated_reason TEXT,location TEXT,department_id int NOT NULL,"
                   "CONSTRAINT fk_employee_id FOREIGN KEY (manager_employee_id) REFERENCES employee(employee_id),"
                   "CONSTRAINT fk_department_id FOREIGN KEY (department_id) REFERENCES department(department_id) )")

    #employee_work table (FACT TABLE)
    cursor.execute("CREATE TABLE employee_work(employee_work_id SERIAL PRIMARY KEY,employee_id int NOT NULL,department_id int NOT NULL,attendance_id int NOT NULL,"
                   "punch_in_time TIMESTAMP NOT NULL,punch_out_time TIMESTAMP NOT NULL,hours_worked float NOT NULL,"
                   "CONSTRAINT fk_employee_id FOREIGN KEY (employee_id) REFERENCES employee(employee_id),"
                   "CONSTRAINT fk_department_id FOREIGN KEY (department_id) REFERENCES department(department_id),"
                   "CONSTRAINT fk_attendance_id FOREIGN KEY (attendance_id) REFERENCES attendance(attendance_id))")

    connection.commit()
    cursor.close()
    connection.close()
except Exception as e:
    print(e)