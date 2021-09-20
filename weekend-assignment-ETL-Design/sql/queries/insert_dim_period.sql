INSERT INTO dim_period(start_date,end_date)
select DISTINCT cast(date_trunc('week', bill_date) as date) + 0 ,cast(date_trunc('week', bill_date) as date) + 7 FROM dim_bill
ORDER BY cast(date_trunc('week', bill_date) as date) + 0 asc;