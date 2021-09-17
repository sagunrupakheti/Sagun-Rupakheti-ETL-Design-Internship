**TRANSFORMATION DOCUMENTATION TIMESHEET DATA**

**1. Requirements Gathered**

* Employee_id remains in string format as it is client supplied data
* Department_id remains in string format as it is client supplied data
* Shift_start_time needs to be parsed into timestamp format without timezone
* Shift_end_time needs to be parsed into timestamp format without timezone
* The shift_date needs to be parsed into date format
* The shift_type needs to be added by calculating if the employee works in the morning or after noon
* The total_hours is the total hours worked by the employee in a particular day, needs
to be parsed to float type
* The attendance column contains boolean depending on the fact if the employee has worked in the particular day or not.
Needs to be boolean type
* The has_taken_break column gives boolean depending on whether the employee has taken any breaks
in a particular day or not
* The break_hour is the total number of hours the employee has taken break, needs to be float type
* The was_charge column gives boolean depending on whether the employee was in charge
in a particular day or not
* The charge hour is the total number of hours the employee was in charge, needs to be float type
* The was_on_call column gives boolean depending on whether the employee was on call
in a particular day or not
* The on_call_hour is the total number of hours the employee was on call, needs to be float type

**2. Creating the table for adding the transformed data**

~~~sql
CREATE TABLE transform_timesheet(
    employee_id  VARCHAR(255),
    department_Id VARCHAR(255),
    shift_start_time TIMESTAMP,
    shift_end_time TIMESTAMP,
    shift_date DATE,
    shift_type VARCHAR(255),
    hours_worked FLOAT,
    attendance bool,
    has_taken_break bool,
    break_hour FLOAT,
    was_charge bool,
    charge_hour FLOAT,
    was_on_call bool,
    on_call_hour FLOAT,
    num_teammates_absent INT
)
~~~

All the necessary requirements are taken into consideration while creating the table

**3. Formulating the query**

~~~sql
    employee_id AS employee_id,
    cost_center AS department_id,
~~~
Getting the employee_id and department_id

~~~sql
MIN(TO_TIMESTAMP(punch_in_time,'YYYY-MM-DD HH24:mi:SS'))::timestamp without time zone AS shift_start_time,
~~~
*Calculating the minimum of punch_in_time without time zone to get the first punch_in_time of the day
*Falls under data validation and summarization

~~~sql
MAX(TO_TIMESTAMP(punch_out_time,'YYYY-MM-DD HH24:mi:SS'))::timestamp without time zone shift_end_time,
~~~
* Calculating the maximum of punch_out_time without time zone to get the last punch_out_time of the day
* Falls under data validation and summarization

~~~sql
date(punch_apply_date) AS shift_date,
~~~
* Parsing the string type to date
* Falls under data validation

~~~sql
 (CASE  WHEN MAX(TO_TIMESTAMP(punch_out_time,'YYYY-MM-DD HH24:MI:SS')::time) <
    CAST ('12:00:00' as time) THEN 'A.M.' ELSE 'P.M.' END) AS shift_type,
~~~
* Getting the maximum of the punch_out_date to evaluate if it falls in the morning or after noon
* Before 12 is A.M and after 12 is P.M.  
* Falls under aggregation, data validation, derivation and summarization

~~~sql
SUM(CAST(hours_worked as float)) AS hours_worked,
~~~
* total hours worked by an employee in a day
~~~sql
 CASE  WHEN MAX(TO_TIMESTAMP(punch_out_time,'YYYY-MM-DD HH24:MI:SS')::time) = CAST ('00:00:00' as time) THEN false ELSE true END AS attendance,
~~~
* checking the maximum of attendance to not be 0:00 for the employee to work
* Falls under aggregation, data validation, derivation and summarization

~~~sql
 CASE WHEN string_agg(paycode,',') like '%BREAK%' THEN true ELSE false END AS has_taken_break,
~~~
* string_agg gets all the values when aggregated by group by from a column
* The value BREAK is checked if it is present int the list
* Falls under aggregation, derivation and summarization

~~~sql
(SELECT SUM(CAST(hours_worked as float)) FROM raw_timesheet WHERE rw.employee_id= employee_id AND paycode='BREAK') AS break_hour,
~~~
* The total hours of break taken by the employee in a day
* Falls under aggregation, derivation and summarization
~~~sql
 CASE WHEN string_agg(paycode,',') like '%CHARGE%' THEN true ELSE false END AS was_charge,
~~~
* Check if the employee was on charge in a day
* Falls under aggregation, derivation and summarization
~~~sql
  (SELECT SUM(CAST(hours_worked as float)) FROM raw_timesheet WHERE rw.employee_id= employee_id AND paycode='CHARGE') AS charge_hour,
~~~
* The total hours of charge hours of an employee in a day
* Falls under aggregation, derivation and summarization
~~~sql
 CASE WHEN string_agg(paycode,',') like '%ON_CALL%' THEN true ELSE false END AS was_on_call,
~~~
* Check if the employee was on call in a day
* Falls under aggregation, derivation and summarization
~~~sql
(CASE WHEN string_agg(paycode,',') like '%ON_CALL%' THEN CAST(hours_worked as float) ELSE 0 END) AS on_call_hour
~~~
* The total hours of on call hours by the employee in a day
* Falls under aggregation, derivation and summarization
~~~sql
 (SELECT COUNT(*) from raw_timesheet WHERE cost_center=rw.cost_center AND paycode= 'ABSENT')
~~~
* Get the total number of absentees from the department