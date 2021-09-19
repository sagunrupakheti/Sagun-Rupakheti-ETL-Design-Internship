CREATE TABLE fact_product_sales(
    sales_id SERIAL PRIMARY KEY,
    product_id int NOT NULL,
    date TIMESTAMP NOT NULL,
    period_id int NOT NULL,
    total_buyings int NOT NULL,
    sales_without_tax FLOAT NOT NULL,
    average_order_value FLOAT NOT NULL
)