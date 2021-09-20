INSERT INTO fact_employee(client_employee_id,department_id,manager_id,role_id,salary,weekly_hours)
SELECT
employee_id AS client_employee_id,
(SELECT department_id FROM dim_department WHERE name=INITCAP(re.department_name)) AS department_id,
CASE WHEN '-'<> manager_employee_id THEN manager_employee_id ELSE NULL END AS manager_id,
(SELECT role_id FROM dim_role WHERE name=re.employee_role) AS role_id,
CAST(salary AS FLOAT) AS salary,
40*CAST(fte AS FLOAT) AS weekly_hours
FROM raw_employee re