INSERT INTO dim_period(start_date,end_date)
select DISTINCT cast(date_trunc('week', punch_apply_date) as date) + 0 ,cast(date_trunc('week', punch_apply_date) as date) + 7 FROM raw_timesheet
ORDER BY cast(date_trunc('week', punch_apply_date) as date) + 0 asc;