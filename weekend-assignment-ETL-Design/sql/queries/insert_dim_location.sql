INSERT INTO dim_location(location_name,country)
SELECT DISTINCT(INITCAP(town)),INITCAP(country) FROM raw_customer