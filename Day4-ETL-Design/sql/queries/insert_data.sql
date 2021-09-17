INSERT INTO transform_timesheet
SELECT
    employee_id AS employee_id,
    cost_center AS department_id,
    MIN(TO_TIMESTAMP(punch_in_time,'YYYY-MM-DD HH24:mi:SS'))::timestamp without time zone AS shift_start_time,
    MAX(TO_TIMESTAMP(punch_out_time,'YYYY-MM-DD HH24:mi:SS'))::timestamp without time zone shift_end_time,
    date(punch_apply_date) AS shift_date,
    (CASE  WHEN MAX(TO_TIMESTAMP(punch_out_time,'YYYY-MM-DD HH24:MI:SS')::time) <
    CAST ('12:00:00' as time) THEN 'A.M.' ELSE 'P.M.' END) AS shift_type,
    SUM(CAST(hours_worked as float)) AS hours_worked,
    CASE  WHEN MAX(TO_TIMESTAMP(punch_out_time,'YYYY-MM-DD HH24:MI:SS')::time) = CAST ('00:00:00' as time) THEN false ELSE true END AS attendance,
    CASE WHEN string_agg(paycode,',') like '%BREAK%' THEN true ELSE false END AS has_taken_break,
    (SELECT SUM(CAST(hours_worked as float)) FROM raw_timesheet WHERE rw.employee_id= employee_id AND paycode='BREAK') AS break_hour,
    CASE WHEN string_agg(paycode,',') like '%CHARGE%' THEN true ELSE false END AS was_charge,
    (SELECT SUM(CAST(hours_worked as float)) FROM raw_timesheet WHERE rw.employee_id= employee_id AND paycode='CHARGE') AS charge_hour,
    CASE WHEN string_agg(paycode,',') like '%ON_CALL%' THEN true ELSE false END AS was_on_call,
    (SELECT SUM(CAST(hours_worked as float)) FROM raw_timesheet WHERE rw.employee_id= employee_id AND paycode='ON_CALL') AS on_call_hour,
    (SELECT COUNT(*) from raw_timesheet WHERE cost_center=rw.cost_center AND paycode= 'ABSENT')
FROM raw_timesheet rw
GROUP BY date(punch_apply_date),employee_id,cost_center;