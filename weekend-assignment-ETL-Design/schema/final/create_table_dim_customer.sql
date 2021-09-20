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