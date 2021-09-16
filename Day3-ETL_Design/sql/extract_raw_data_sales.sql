SELECT s.user_id, u.username, s.product_id, p.name, p.category_id, c.name, p.price, s.price, s.quantity,
(p.quantity-s.quantity),s.updated_at
FROM sales s
JOIN users u
ON u.id = s.user_id
JOIN products p
ON p.id = s.product_id
JOIN categories c
ON c.id = p.category_id;