Use ecommerce_analytics;

-- Total Unique Customers
SELECT COUNT(DISTINCT customer_unique_id) AS unique_customers
FROM customers;

-- Customers Who placed Orders

SELECT COUNT(DISTINCT c.customer_unique_id) AS customers_with_orders
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id;

-- Orders Per customer

SELECT c.customer_unique_id, COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_unique_id
ORDER BY total_orders DESC;

-- Repeated Customers

SELECT COUNT(*) AS repeat_customers
FROM (
    SELECT c.customer_unique_id
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
    HAVING COUNT(o.order_id) > 1
) AS repeat_customers;


-- One-Time Customers

-- 5. One-Time Customers
SELECT
    COUNT(*) AS one_time_customers
FROM (
    SELECT
        c.customer_unique_id
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY
        c.customer_unique_id
    HAVING COUNT(o.order_id) = 1
) AS one_time_customer_list;


-- Customer Revenue

-- 6. Customer Revenue
SELECT
    c.customer_unique_id,
    SUM(oi.price) AS customer_revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_unique_id
ORDER BY
    customer_revenue DESC;


-- Top 10 Customers by Revenue

    -- 7. Top 10 Customers by Revenue
SELECT
    c.customer_unique_id,
    SUM(oi.price) AS customer_revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_unique_id
ORDER BY
    customer_revenue DESC
LIMIT 10;


-- Average Orders Per Customer

SELECT
    COUNT(o.order_id) * 1.0 /
    COUNT(DISTINCT c.customer_unique_id) AS average_orders_per_customer
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id;