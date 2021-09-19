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