INSERT INTO dim_status(status_type)
SELECT DISTINCT(UPPER(active)) FROM raw_product;