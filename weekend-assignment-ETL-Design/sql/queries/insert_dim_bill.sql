INSERT INTO dim_bill(client_bill_id ,bill_no,bill_date,location_id,customer_id,product_id,price ,gross_price ,tax_amount ,total_bill_amount)
    SELECT
    CAST(id AS INT) AS client_bill_id,
    CAST(bill_no AS INT) AS bill_no,
    CASE WHEN bill_date <> '2017-02-30 11:00:00' THEN TO_TIMESTAMP(bill_date,'YYYY-MM-DD HH24:mi:SS')::timestamp without time zone
    ELSE TO_TIMESTAMP('2017-03-01 11:00:00','YYYY-MM-DD HH24:mi:SS')::timestamp without time zone END AS bill_date,
    (SELECT location_id FROM dim_location WHERE INITCAP(rs.bill_location) = location_name) AS location_id,
    (SELECT customer_id FROM dim_customer WHERE rs.customer_id = client_customer_id) AS customer_id,
    (SELECT product_id FROM dim_product WHERE rs.product_id = client_product_id) AS customer_id,
    CAST(price AS FLOAT) AS price,
    CAST(gross_price AS FLOAT) AS gross_price,
    CAST(tax_amt AS FLOAT) AS tax_amount,
    CAST(net_bill_amt AS FLOAT) AS total_bill_amount
    FROM raw_sales rs
