INSERT INTO dim_role(name)
SELECT DISTINCT(INITCAP(employee_role)) from raw_employee