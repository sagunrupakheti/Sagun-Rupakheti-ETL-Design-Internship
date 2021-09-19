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