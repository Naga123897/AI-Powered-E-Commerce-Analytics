import pandas as pd

customers = pd.read_csv(
    "data/raw/olist_customers_dataset.csv"
)
print("Customers loaded:", customers.shape)

print("\nMissing values:")
print(customers.isnull().sum())

print("\nDuplicate rows:")
print(customers.duplicated().sum())

print("\nUnique customer_id:")
print(customers["customer_id"].nunique())

print("\nTotal customer rows:")
print(len(customers))

# Check text columns
print("\nEmpty customer cities:")
print((customers["customer_city"] == "").sum())

print("\nEmpty customer states:")
print((customers["customer_state"] == "").sum())

# Basic Text cleaning

customers["customer_city"] = customers["customer_city"].str.strip()
customers["customer_state"] = customers["customer_state"].str.strip()

# Save the cleaned customers dataset to a new CSV file
customers.to_csv("data/cleaned/customers.csv", index=False)

# =========================
# Clean Orders Data
# =========================

orders = pd.read_csv(
    "data/raw/olist_orders_dataset.csv"
)

# Convert date columns from text to datetime
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )

# Remove completely duplicated rows
orders = orders.drop_duplicates()

# Save cleaned orders
orders.to_csv(
    "data/cleaned/orders.csv",
    index=False
)

print("\nOrders cleaned successfully.")
print("Orders shape after cleaning:", orders.shape)

# =========================
# Clean Order Items Data
# =========================

order_items = pd.read_csv(
    "data/raw/olist_order_items_dataset.csv"
)

# Convert shipping date to datetime
order_items["shipping_limit_date"] = pd.to_datetime(
    order_items["shipping_limit_date"],
    errors="coerce"
)

# Remove completely duplicated rows
order_items = order_items.drop_duplicates()

# Make sure price and freight_value are numeric
order_items["price"] = pd.to_numeric(
    order_items["price"],
    errors="coerce"
)

order_items["freight_value"] = pd.to_numeric(
    order_items["freight_value"],
    errors="coerce"
)

# Save cleaned order items
order_items.to_csv(
    "data/cleaned/order_items.csv",
    index=False
)

print("\nOrder Items cleaned successfully.")
print("Order Items shape after cleaning:", order_items.shape)

# =========================
# Clean Products Data
# =========================

products = pd.read_csv(
    "data/raw/olist_products_dataset.csv"
)

# Clean product category text
products["product_category_name"] = (
    products["product_category_name"].str.strip()
)

# Convert numeric columns to numeric data types
numeric_columns = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

for column in numeric_columns:
    products[column] = pd.to_numeric(
        products[column],
        errors="coerce"
    )

# Remove completely duplicated rows
products = products.drop_duplicates()

# Save cleaned products
products.to_csv(
    "data/cleaned/products.csv",
    index=False
)

print("\nProducts cleaned successfully.")
print("Products shape after cleaning:", products.shape)

# =========================
# Clean Payments Data
# =========================

payments = pd.read_csv(
    "data/raw/olist_order_payments_dataset.csv"
)

# Clean payment type text
payments["payment_type"] = payments["payment_type"].str.strip()

# Convert numeric columns
payments["payment_sequential"] = pd.to_numeric(
    payments["payment_sequential"],
    errors="coerce"
)

payments["payment_installments"] = pd.to_numeric(
    payments["payment_installments"],
    errors="coerce"
)

payments["payment_value"] = pd.to_numeric(
    payments["payment_value"],
    errors="coerce"
)

# Remove completely duplicated rows
payments = payments.drop_duplicates()

# Save cleaned payments
payments.to_csv(
    "data/cleaned/order_payments.csv",
    index=False
)

print("\nPayments cleaned successfully.")
print("Payments shape after cleaning:", payments.shape)

# =========================
# Clean Reviews Data
# =========================

reviews = pd.read_csv(
    "data/raw/olist_order_reviews_dataset.csv"
)

# Clean text columns
reviews["review_comment_title"] = (
    reviews["review_comment_title"].str.strip()
)

reviews["review_comment_message"] = (
    reviews["review_comment_message"].str.strip()
)

# Convert review score to numeric
reviews["review_score"] = pd.to_numeric(
    reviews["review_score"],
    errors="coerce"
)

# Convert date columns
review_date_columns = [
    "review_creation_date",
    "review_answer_timestamp"
]

for column in review_date_columns:
    reviews[column] = pd.to_datetime(
        reviews[column],
        errors="coerce"
    )

# Remove completely duplicated rows
reviews = reviews.drop_duplicates()

# Save cleaned reviews
reviews.to_csv(
    "data/cleaned/order_reviews.csv",
    index=False
)

print("\nReviews cleaned successfully.")
print("Reviews shape after cleaning:", reviews.shape)

# =========================
# Clean Category Translation
# =========================

category_translation = pd.read_csv(
    "data/raw/product_category_name_translation.csv"
)

# Clean text columns
category_translation["product_category_name"] = (
    category_translation["product_category_name"].str.strip()
)

category_translation["product_category_name_english"] = (
    category_translation["product_category_name_english"].str.strip()
)

# Remove completely duplicated rows
category_translation = category_translation.drop_duplicates()

# Save cleaned category translation
category_translation.to_csv(
    "data/cleaned/product_category_name_translation.csv",
    index=False
)

print("\nCategory Translation cleaned successfully.")
print(
    "Category Translation shape after cleaning:",
    category_translation.shape
)

print("\n===== STEP 4 COMPLETED =====")
print("All 7 datasets have been cleaned and saved.")

