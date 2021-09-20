#Day 5 Documentation- Transformation and Loading

####1. For loading the data first, dimension and fact tables need to be created.
* The schema given is followed
* All the datatypes are selected according to the raw data supplied
* Appropriate constraints are applied

~~~sql
CREATE TABLE dim_department(
    department_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL);
~~~
**creating department dimension**

~~~sql
CREATE TABLE dim_period(
    id SERIAL PRIMARY KEY,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL
)
~~~
**creating period dimension**

~~~sql
CREATE TABLE dim_role(
    role_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
)
~~~
**creating role dimension**

~~~sql
CREATE TABLE dim_shift_type(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
)
~~~
**creating shift dimension**

~~~sql
INSERT INTO dim_status(name)
SELECT DISTINCT(INITCAP(paycode)) FROM raw_timesheet;
~~~

**creating status dimension**

~~~sql
CREATE TABLE fact_employee(
    employee_id SERIAL PRIMARY KEY,
    client_employee_id VARCHAR(255) NOT NULL,
    department_id INT NOT NULL,
    manager_id VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    salary FLOAT NOT NULL,
    weekly_hours FLOAT NOT NULL,
    CONSTRAINT fk_department_id FOREIGN KEY (department_id) REFERENCES department (department_id)
)
~~~

**creating employee fact**

~~~sql
CREATE TABLE fact_timesheet(
    employee_id  VARCHAR(255) NOT NULL,
    work_date DATE NOT NULL,
    department_id VARCHAR(255) NOT NULL,
    hours_worked FLOAT NOT NULL,
    shift_type_id VARCHAR(255) NOT NULL,
    punch_in_time TIMESTAMP NOT NULL,
    punch_out_time TIMESTAMP NOT NULL,
    time_period_id int NOT NULL,
    attendance bool NOT NULL,
    has_taken_break bool NOT NULL,
    break_hour FLOAT NOT NULL,
    was_charge bool NOT NULL,
    charge_hour FLOAT NOT NULL,
    was_on_call bool NOT NULL,
    on_call_hour FLOAT NOT NULL,
    is_weekend bool NOT NULL,
    num_teammates_absent INT NOT NULL,
    CONSTRAINT fk_department_id FOREIGN KEY (department_id) REFERENCES dim_department (department_id),
    CONSTRAINT fk_employee_id FOREIGN KEY (employee_id) REFERENCES fact_employee (employee_id),
)
~~~

**creating timesheet fact**
___
####2. Now, the data stoered in the raw tables need to be extracted and inserted in fact and dimension tables

* The data is inserted according to the datatypes and constraints

~~~sql
INSERT INTO dim_department(department_id,NAME)
SELECT DISTINCT(CAST(department_id AS int)),department_name FROM raw_employee
~~~
**getting the unique department names from raw employee table**

~~~sql
INSERT INTO dim_period(start_date,end_date)
select DISTINCT cast(date_trunc('week', punch_apply_date) as date) + 0 ,cast(date_trunc('week', punch_apply_date) as date) + 7 FROM raw_timesheet
ORDER BY cast(date_trunc('week', punch_apply_date) as date) + 0 asc;
~~~
**Inserting the period as in interval of 1 week**


~~~sql
INSERT INTO dim_role(name)
SELECT DISTINCT(INITCAP(employee_role)) from raw_employee
~~~

**Inserting the unique roles of the employees**

~~~sql
INSERT INTO dim_shift_type(name)
VALUES('Morning'),('Evening')
~~~

**To indicate time as Morning or Evening shift**

~~~sql
INSERT INTO fact_employee(client_employee_id,department_id,manager_id,role_id,salary,weekly_hours)
SELECT
employee_id AS client_employee_id,
(SELECT department_id FROM dim_department WHERE name=INITCAP(re.department_name)) AS department_id,
CASE WHEN '-'<> manager_employee_id THEN manager_employee_id ELSE NULL END AS manager_id,
(SELECT role_id FROM dim_role WHERE name=re.employee_role) AS role_id,
CAST(salary AS FLOAT) AS salary,
40*CAST(fte AS FLOAT) AS weekly_hours
FROM raw_employee re
~~~

**Add values in the fact_employee table**

---
####3. Finally, the tables are created and data is inserted using functions

~~~python
    def create_table_dim_fact(filePath):
        connection = connect()
        cursor = connection.cursor()
        with open(filePath) as file:
            sql = "".join(file.readlines())
            cursor.execute(sql)
            connection.commit()
~~~
**Function for creating the tables**

~~~python
    def insert_into_table(filePath):
        connection = connect()
        cursor = connection.cursor()

        with open(filePath) as file:
            sql = "".join(file.readlines())
            cursor.execute(sql)
            connection.commit()
~~~

**Function for inserting into tables**

