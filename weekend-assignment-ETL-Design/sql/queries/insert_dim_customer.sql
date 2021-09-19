INSERT INTO dim_customer(client_customer_id,user_name,first_name,last_name,location_id,status_id)
SELECT
customer_id AS client_customer_id,
user_name AS user_name,
first_name AS first_name,
last_name AS last_name,
(SELECT location_id FROM dim_location WHERE location_name= INITCAP(rc.town)) AS location_id,
(SELECT status_id FROM dim_status WHERE status_type= UPPER(rc.active)) AS status_id
FROM raw_customer rc;