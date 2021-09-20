INSERT INTO dim_department(department_id,NAME)
SELECT DISTINCT(CAST(department_id AS int)),department_name FROM raw_employee