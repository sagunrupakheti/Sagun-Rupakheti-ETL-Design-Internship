INSERT INTO dim_status(name)
SELECT DISTINCT(INITCAP(paycode)) FROM raw_timesheet;