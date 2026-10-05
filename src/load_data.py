import pandas as pd
from database import engine
from sqlalchemy import text


# 1. Customers
customers = pd.read_csv("data/cleaned/customers.csv")
customers.to_sql(
    "customers",
    con=engine,
    if_exists="append",
    index=False
)
print("Customers loaded:", len(customers))


# 2. Products
products = pd.read_csv("data/cleaned/products.csv")
products.to_sql(
    "products",
    con=engine,
    if_exists="append",
    index=False
)
print("Products loaded:", len(products))


# 3. Category Translation
category_translation = pd.read_csv(
    "data/cleaned/product_category_name_translation.csv"
)
category_translation.to_sql(
    "product_category_name_translation",
    con=engine,
    if_exists="append",
    index=False
)
print("Category Translation loaded:", len(category_translation))


# 4. Orders
orders = pd.read_csv("data/cleaned/orders.csv")
orders.to_sql(
    "orders",
    con=engine,
    if_exists="append",
    index=False
)
print("Orders loaded:", len(orders))


# 5. Order Items
order_items = pd.read_csv("data/cleaned/order_items.csv")
order_items.to_sql(
    "order_items",
    con=engine,
    if_exists="append",
    index=False
)
print("Order Items loaded:", len(order_items))


# 6. Payments
payments = pd.read_csv("data/cleaned/order_payments.csv")
payments.to_sql(
    "order_payments",
    con=engine,
    if_exists="append",
    index=False
)
print("Payments loaded:", len(payments))


# 7. Reviews
reviews = pd.read_csv("data/cleaned/order_reviews.csv")
reviews.to_sql(
    "order_reviews",
    con=engine,
    if_exists="append",
    index=False
)
print("Reviews loaded:", len(reviews))


# Verify counts
print("\n===== MYSQL TABLE COUNTS =====")

tables = [
    "customers",
    "orders",
    "order_items",
    "products",
    "order_payments",
    "order_reviews",
    "product_category_name_translation"
]

with engine.connect() as connection:
    for table in tables:
        result = connection.execute(
            text(f"SELECT COUNT(*) FROM `{table}`")
        )
        count = result.scalar()
        print(f"{table}: {count}")


print("\n===== STEP 7 COMPLETED =====")
