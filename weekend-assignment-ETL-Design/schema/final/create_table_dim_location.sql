CREATE TABLE dim_location(
    location_id SERIAL PRIMARY KEY,
    location_name VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL
);
