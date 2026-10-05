-- Total Revenue

use ecommerce_analytics;
SELECT Sum(price) AS total_revenue
FROM order_items;

-- Total Number of Orders

SELECT Count(*) AS total_orders
From Orders;

-- Avg Order Value(AOV)

SELECT
    SUM(price) / COUNT(DISTINCT order_id) AS average_order_value
FROM order_items;

-- Total Freight Revenue/Value

SELECT
    SUM(freight_value) AS total_freight_value
FROM order_items;

-- Monthly Revenue

SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
    SUM(oi.price) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')
ORDER BY
    month;


-- Revenue by Product Category

SELECT
    COALESCE(t.product_category_name_english,
             oi_product.product_category_name,
             'Unknown') AS category,
    SUM(oi.price) AS revenue
FROM order_items oi
JOIN products oi_product
    ON oi.product_id = oi_product.product_id
LEFT JOIN product_category_name_translation t
    ON oi_product.product_category_name = t.product_category_name
GROUP BY
    COALESCE(t.product_category_name_english,
             oi_product.product_category_name,
             'Unknown')
ORDER BY
    revenue DESC;


-- Revenue by Customer State

SELECT
    c.customer_state AS state,
    SUM(oi.price) AS revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_state
ORDER BY
    revenue DESC;
