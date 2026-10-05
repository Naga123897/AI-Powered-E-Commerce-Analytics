import pandas as pd

customers = pd.read_csv("data/raw/olist_customers_dataset.csv")
orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
order_items = pd.read_csv("data/raw/olist_order_items_dataset.csv")
products = pd.read_csv("data/raw/olist_products_dataset.csv")
payments = pd.read_csv("data/raw/olist_order_payments_dataset.csv")
reviews = pd.read_csv("data/raw/olist_order_reviews_dataset.csv")
category_translation = pd.read_csv(
    "data/raw/product_category_name_translation.csv"
)

print("All 7 files loaded successfully.")

# Check the size of every dataset

print("\nDataset sizes:")
print("Customers:", customers.shape)
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)
print("Products:", products.shape)
print("Payments:", payments.shape)
print("Reviews:", reviews.shape)
print("Category Translation:", category_translation.shape)

# See the columns of every dataset

print("\nCustomers columns:")
print(customers.columns.tolist())

print("\nOrders columns:")
print(orders.columns.tolist())

print("\nOrder Items columns:")
print(order_items.columns.tolist())

print("\nProducts columns:")
print(products.columns.tolist())

print("\nPayments columns:")
print(payments.columns.tolist())

print("\nReviews columns:")
print(reviews.columns.tolist())

print("\nCategory Translation columns:")
print(category_translation.columns.tolist())

# Print the first five rows of every dataset

print("\n--- CUSTOMERS ---")
print(customers.head())

print("\n--- ORDERS ---")
print(orders.head())

print("\n--- ORDER ITEMS ---")
print(order_items.head())

print("\n--- PRODUCTS ---")
print(products.head())

print("\n--- PAYMENTS ---")
print(payments.head())

print("\n--- REVIEWS ---")
print(reviews.head())

print("\n--- CATEGORY TRANSLATION ---")
print(category_translation.head())

# Check data types of every dataset

print("\n--- CUSTOMERS DATA TYPES ---")
print(customers.dtypes)

print("\n--- ORDERS DATA TYPES ---")
print(orders.dtypes)

print("\n--- ORDER ITEMS DATA TYPES ---")
print(order_items.dtypes)

print("\n--- PRODUCTS DATA TYPES ---")
print(products.dtypes)

print("\n--- PAYMENTS DATA TYPES ---")
print(payments.dtypes)

print("\n--- REVIEWS DATA TYPES ---")
print(reviews.dtypes)

print("\n--- CATEGORY TRANSLATION DATA TYPES ---")
print(category_translation.dtypes)

# Check for missing values in every dataset

print("\n--- MISSING VALUES ---")

print("\nCustomers:")
print(customers.isnull().sum())

print("\nOrders:")
print(orders.isnull().sum())

print("\nOrder Items:")
print(order_items.isnull().sum())

print("\nProducts:")
print(products.isnull().sum())

print("\nPayments:")
print(payments.isnull().sum())

print("\nReviews:")
print(reviews.isnull().sum())

print("\nCategory Translation:")
print(category_translation.isnull().sum())

# Check for duplicates in every dataset

print("\n--- DUPLICATE ROWS ---")

print("Customers:", customers.duplicated().sum())
print("Orders:", orders.duplicated().sum())
print("Order Items:", order_items.duplicated().sum())
print("Products:", products.duplicated().sum())
print("Payments:", payments.duplicated().sum())
print("Reviews:", reviews.duplicated().sum())
print("Category Translation:", category_translation.duplicated().sum())

# Check for important ID uniqueness in every dataset

print("\n--- ID CHECKS ---")

print("Unique customer_id:",
      customers["customer_id"].nunique())

print("Unique order_id:",
      orders["order_id"].nunique())

print("Unique product_id:",
      products["product_id"].nunique())

print("Unique review_id:",
      reviews["review_id"].nunique())


# Understand order_items

print("\n--- ORDER ITEMS CHECK ---")

print("Total order item rows:",
      len(order_items))

print("Unique orders in order_items:",
      order_items["order_id"].nunique())

print("Unique products in order_items:",
      order_items["product_id"].nunique())

print("Maximum item number within an order:",
      order_items["order_item_id"].max())


# Check the customer relationship

print("\n--- CUSTOMER CHECK ---")

print("Total customer rows:",
      len(customers))

print("Unique customer_id:",
      customers["customer_id"].nunique())

print("Unique customer_unique_id:",
      customers["customer_unique_id"].nunique())