USE ecommerce_analytics;

-- 1. Average Review Score
SELECT
    ROUND(AVG(review_score), 2) AS average_review_score
FROM order_reviews;

-- 2. Review Score Distribution
SELECT
    review_score,
    COUNT(*) AS review_count
FROM order_reviews
GROUP BY review_score
ORDER BY review_score;

-- 3. Low-Rated Reviews
SELECT
    COUNT(*) AS low_rated_reviews
FROM order_reviews
WHERE review_score <= 2;

-- 4. Review Score vs Delivery Time
SELECT
    r.review_score,
    ROUND(
        AVG(
            DATEDIFF(
                o.order_delivered_customer_date,
                o.order_purchase_timestamp
            )
        ), 2
    ) AS average_delivery_days
FROM order_reviews r
JOIN orders o
    ON r.order_id = o.order_id
WHERE o.order_delivered_customer_date IS NOT NULL
GROUP BY r.review_score
ORDER BY r.review_score;

-- 5. Review Score by Product Category
SELECT
    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'Unknown'
    ) AS category,
    ROUND(AVG(r.review_score), 2) AS average_review_score
FROM order_reviews r
JOIN order_items oi
    ON r.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation t
    ON p.product_category_name = t.product_category_name
GROUP BY
    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'Unknown'
    )
ORDER BY average_review_score DESC;

