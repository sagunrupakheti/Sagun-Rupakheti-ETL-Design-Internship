WITH cte1 AS(
    SELECT
    product_id AS product_id,
    bill_date AS date,
	gross_price,
	(SELECT period_id FROM dim_period WHERE bill_date BETWEEN start_date AND end_date) AS period_id
    FROM dim_bill
),
total_buyings AS(
    SELECT cte1.date, cte1.product_id, COUNT(*) AS total_buyings,SUM(cte1.gross_price) AS sales_without_tax, AVG(cte1.gross_price)
	AS average_order_value
	FROM cte1 GROUP BY cte1.product_id, cte1.date)
INSERT INTO fact_product_sales(product_id ,date ,period_id ,total_buyings ,sales_without_tax,average_order_value)
SELECT DISTINCT c.product_id,c.date,c.period_id,t.total_buyings,t.sales_without_tax, t.average_order_value
FROM cte1 c JOIN total_buyings t
ON c.product_id = t.product_id AND c.date = t.date;


--WITH cte1 AS(
--    SELECT
--    product_id AS product_id,
--    bill_date AS date,
--	gross_price
--    FROM dim_bill
--),
--period_id AS(
--    SELECT period_id FROM dim_period,cte1 WHERE cte1.date BETWEEN start_date AND end_date
--),
--total_buyings AS(
--    SELECT COUNT(*) AS total_buyings,date,product_id FROM cte1 GROUP BY cte1.product_id, cte1.date ORDER BY date asc),
--sales_without_tax AS(
--    SELECT SUM(cte1.gross_price) AS sales_without_tax FROM cte1 GROUP BY cte1.product_id, cte1.date),
--average_order_value AS(
--    SELECT AVG(SUM(cte1.gross_price)) AS average_order_value FROM cte1 GROUP BY cte1.product_id, cte1.date)
--INSERT INTO fact_product_sales(product_id ,date ,period_id ,total_buyings ,sales_without_tax,average_order_value,revenue)
--SELECT
--cte1.product_id AS product_id,
--cte1.bill_date AS date,
--period_id.period_id  AS date,
--total_buyings.total_buyings AS total_buyings,
--sales_without_tax.sales_without_tax AS sales_without_tax,
--average_order_value.average_order_value AS average_order_value,
--sales_without_tax*average_order_value AS revenue
--FROM dim_bill db
--GROUP BY product_id, date;
