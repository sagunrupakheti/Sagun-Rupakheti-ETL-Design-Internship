##Creating the Pipeline

Steps:
* The respective tables are made for loading the raw data
* Archive tables are made to store the raw data for future reference
* The final dimension and fact tables are made and data is transformed and loaded into those tables

###1. Raw Tables

~~~sql
CREATE TABLE raw_customer(
	customer_id VARCHAR(255),
	user_name VARCHAR(255),
	first_name VARCHAR(255),
	last_name VARCHAR(255),
	country VARCHAR(255),
	town VARCHAR(255),
	active VARCHAR(255)
)
~~~
Creating raw table for importing data from .csv file of customer

~~~sql
CREATE TABLE raw_product(
	product_id VARCHAR(255),
	product_name VARCHAR(255),
	description VARCHAR(255),
	price VARCHAR(255),
	mrp VARCHAR(255),
	pieces_per_case VARCHAR(255),
	weight_per_piece VARCHAR(255),
	uom VARCHAR(255),
	brand VARCHAR(255),
	category VARCHAR(255),
	tax_percent VARCHAR(255),
	active VARCHAR(255),
	created_by VARCHAR(255),
	created_date VARCHAR(255),
	updated_by VARCHAR(255),
	updated_date VARCHAR(255)
)
~~~
Creating raw table for importing data from .csv file of product
~~~sql
CREATE TABLE raw_sales(
	id VARCHAR(255),
	transaction_id VARCHAR(255),
	bill_no VARCHAR(255),
	bill_date VARCHAR(255),
	bill_location VARCHAR(255),
	customer_id VARCHAR(255),
	product_id VARCHAR(255),
	qty VARCHAR(255),
	uom VARCHAR(255),
	price VARCHAR(255),
	gross_price VARCHAR(255),
	tax_pc VARCHAR(255),
	tax_amt VARCHAR(255),
	discount_pc VARCHAR(255),
	discount_amt VARCHAR(255),
	net_bill_amt VARCHAR(255),
	created_by VARCHAR(255),
	updated_by VARCHAR(255),
	created_date VARCHAR(255),
	updated_date VARCHAR(255)
)
~~~
Creating raw table for importing data from .csv file of sales

###2. Archive Tables

~~~sql
CREATE TABLE raw_customer_archive(
	customer_id VARCHAR(255),
	user_name VARCHAR(255),
	first_name VARCHAR(255),
	last_name VARCHAR(255),
	country VARCHAR(255),
	town VARCHAR(255),
	active VARCHAR(255),
	filename VARCHAR(255)
)
~~~
Creating archive table to insert data loaded into raw tables
~~~sql
CREATE TABLE raw_product_archive(
	product_id VARCHAR(255),
	product_name VARCHAR(255),
	description VARCHAR(255),
	price VARCHAR(255),
	mrp VARCHAR(255),
	pieces_per_case VARCHAR(255),
	weight_per_piece VARCHAR(255),
	uom VARCHAR(255),
	brand VARCHAR(255),
	category VARCHAR(255),
	tax_percent VARCHAR(255),
	active VARCHAR(255),
	created_by VARCHAR(255),
	created_date VARCHAR(255),
	updated_by VARCHAR(255),
	updated_date VARCHAR(255),
	filename VARCHAR(255)
)
~~~
Creating archive table to insert data loaded into raw table product
~~~sql
CREATE TABLE raw_sales_archive(
	id VARCHAR(255),
	transaction_id VARCHAR(255),
	bill_no VARCHAR(255),
	bill_date VARCHAR(255),
	bill_location VARCHAR(255),
	customer_id VARCHAR(255),
	product_id VARCHAR(255),
	qty VARCHAR(255),
	uom VARCHAR(255),
	price VARCHAR(255),
	gross_price VARCHAR(255),
	tax_pc VARCHAR(255),
	tax_amt VARCHAR(255),
	discount_pc VARCHAR(255),
	discount_amt VARCHAR(255),
	net_bill_amt VARCHAR(255),
	created_by VARCHAR(255),
	updated_by VARCHAR(255),
	created_date VARCHAR(255),
	updated_date VARCHAR(255),
	filename VARCHAR(255)
)
~~~
Creating archive table to insert data loaded into raw table sales

###3. Dimension and Fact Tables Creation

~~~sql
CREATE TABLE fact_product_sales(
    sales_id SERIAL PRIMARY KEY,
    product_id int NOT NULL,
    date TIMESTAMP NOT NULL,
    period_id int NOT NULL,
    total_buyings int NOT NULL,
    sales_without_tax FLOAT NOT NULL,
    average_order_value FLOAT NOT NULL
)
~~~
fact_product_sales table
~~~sql
CREATE TABLE dim_bill(
    bill_id SERIAL PRIMARY KEY,
    client_bill_id INT NOT NULL,
    bill_no INT NOT NULL,
    bill_date TIMESTAMP NOT NULL,
    location_id INT NOT NULL,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    price FLOAT NOT NULL,
    gross_price FLOAT NOT NULL,
    tax_amount FLOAT NOT NULL,
    total_bill_amount FLOAT NOT NULL,
    CONSTRAINT fk_location_id FOREIGN KEY (location_id) REFERENCES dim_location (location_id),
    CONSTRAINT fk_customer_id FOREIGN KEY (customer_id) REFERENCES dim_customer (customer_id),
    CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES dim_product (product_id)
)
~~~
dim_bill table
~~~sql
CREATE TABLE dim_brand(
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(255) NOT NULL
)
~~~

~~~sql
CREATE TABLE dim_category(
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL
)
~~~
dim_category table
~~~sql
CREATE TABLE dim_customer(
    customer_id SERIAL PRIMARY KEY,
    client_customer_id VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    location_id INT NOT NULL,
    status_id INT NOT NULL,
    CONSTRAINT fk_location_id FOREIGN KEY (location_id) REFERENCES dim_location (location_id),
    CONSTRAINT fk_status_id FOREIGN KEY (status_id) REFERENCES dim_status (status_id)
)
~~~
dim_customer table
~~~sql
CREATE TABLE dim_location(
    location_id SERIAL PRIMARY KEY,
    location_name VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL
);

~~~
dim_location table
~~~sql
CREATE TABLE dim_period(
    period_id SERIAL PRIMARY KEY,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL
)
~~~
dim_period table
~~~sql
CREATE TABLE dim_product(
    product_id SERIAL PRIMARY KEY,
    client_product_id VARCHAR(255) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    description VARCHAR(500) NOT NULL,
    price FLOAT NOT NULL,
    mrp FLOAT NOT NULL,
    pieces_per_case INT NOT NULL,
    weight_per_piece FLOAT NOT NULL,
    brand_id INT NOT NULL,
    category_id INT NOT NULL,
    status_id INT NOT NULL,
    CONSTRAINT fk_brand_id FOREIGN KEY (brand_id) REFERENCES dim_brand (brand_id),
    CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES dim_category (category_id),
    CONSTRAINT fk_status_id FOREIGN KEY (status_id) REFERENCES dim_status (status_id)
)
~~~
dim_product table
~~~sql
CREATE TABLE dim_status(
    status_id SERIAL PRIMARY KEY,
    status_type VARCHAR(255) NOT NULL
)
~~~
dim_status table

---
###3. Dimension and Fact Tables Insertion

Now, the data from raw tables is transformed and inserted into the fact and dimension tables.

~~~sql
INSERT INTO dim_brand(brand_name)
SELECT DISTINCT(brand) FROM raw_product;
~~~
* Unique brand names are added from raw_product table
~~~sql
INSERT INTO dim_category(category_name)
SELECT DISTINCT(INITCAP(category)) FROM raw_product;
~~~
* Unique category names are added from raw_product table
* The value is capitalized
~~~sql
INSERT INTO dim_location(location_name,country)
SELECT DISTINCT(INITCAP(town)),INITCAP(country) FROM raw_customer
~~~
* Unique location name as well as its country are added from raw_product table
* The values are capitalized

~~~sql
INSERT INTO dim_period(start_date,end_date)
select DISTINCT cast(date_trunc('week', bill_date) as date) + 0 ,cast(date_trunc('week', bill_date) as date) + 7 FROM dim_bill
ORDER BY cast(date_trunc('week', bill_date) as date) + 0 asc;
~~~
* The time period is taken with a gap of a week
~~~sql
INSERT INTO dim_status(status_type)
SELECT DISTINCT(UPPER(active)) FROM raw_product;
~~~
* The active status Y/N is added
~~~sql
INSERT INTO dim_customer(client_customer_id,user_name,first_name,last_name,location_id,status_id)
SELECT
customer_id AS client_customer_id,
user_name AS user_name,
first_name AS first_name,
last_name AS last_name,
(SELECT location_id FROM dim_location WHERE location_name= INITCAP(rc.town)) AS location_id,
(SELECT status_id FROM dim_status WHERE status_type= UPPER(rc.active)) AS status_id
FROM raw_customer rc;
~~~
* All necessary values are added from raw_customer table

~~~sql
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

~~~
* All necessary values are added from raw_sales table

~~~sql
INSERT INTO dim_product(client_product_id,product_name,description,price,mrp,pieces_per_case,weight_per_piece,brand_id,category_id,status_id)
SELECT
product_id AS client_product_id,
product_name AS product_name,
description AS description,
CAST(price AS FLOAT) AS price,
CAST(mrp AS FLOAT) AS mrp,
CAST(pieces_per_case AS INT) AS pieces_per_case,
CAST(weight_per_piece AS FLOAT) AS weight_per_piece,
(SELECT brand_id FROM dim_brand WHERE brand_name=rp.brand) AS brand_id,
(SELECT category_id FROM dim_category WHERE INITCAP(rp.category)= category_name) AS category_id,
(SELECT status_id FROM dim_status WHERE UPPER(rp.active)= status_type) AS status_id
FROM raw_product rp
~~~
* From raw_product table, information of the product is added
* Foreign key values are also added -> brand, category, status
~~~sql
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

~~~
* A common table expression is used to get the totals that reflect the values of the product sales

