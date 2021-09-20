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