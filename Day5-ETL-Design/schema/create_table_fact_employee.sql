CREATE TABLE fact_employee(
    employee_id SERIAL PRIMARY KEY,
    client_employee_id VARCHAR(255) NOT NULL,
    department_id INT NOT NULL,
    manager_id VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    salary FLOAT NOT NULL,
    active_status_id bool NOT NULL,
    weekly_hours FLOAT NOT NULL,
    CONSTRAINT fk_department_id FOREIGN KEY (department_id) REFERENCES department (department_id)
)