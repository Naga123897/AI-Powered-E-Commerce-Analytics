USE ecommerce_analytics;

-- 1. Payment Method Distribution
SELECT
    payment_type,
    COUNT(*) AS payment_count
FROM order_payments
GROUP BY payment_type
ORDER BY payment_count DESC;

-- 2. Payment Value by Method
SELECT
    payment_type,
    ROUND(SUM(payment_value), 2) AS total_payment_value
FROM order_payments
GROUP BY payment_type
ORDER BY total_payment_value DESC;

-- 3. Average Payment Value
SELECT
    payment_type,
    ROUND(AVG(payment_value), 2) AS average_payment_value
FROM order_payments
GROUP BY payment_type
ORDER BY average_payment_value DESC;

-- 4. Installment Distribution
SELECT
    payment_installments,
    COUNT(*) AS payment_count
FROM order_payments
GROUP BY payment_installments
ORDER BY payment_installments;

-- 5. Average Installments by Payment Method
SELECT
    payment_type,
    ROUND(AVG(payment_installments), 2) AS average_installments
FROM order_payments
GROUP BY payment_type
ORDER BY average_installments DESC;