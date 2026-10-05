from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# =========================
# Customers
# =========================

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String(50), primary_key=True)
    customer_unique_id = Column(String(50))
    customer_zip_code_prefix = Column(Integer)
    customer_city = Column(String(100))
    customer_state = Column(String(10))


# =========================
# Orders
# =========================

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String(50), primary_key=True)

    customer_id = Column(
        String(50),
        ForeignKey("customers.customer_id")
    )

    order_status = Column(String(30))

    order_purchase_timestamp = Column(DateTime)
    order_approved_at = Column(DateTime)
    order_delivered_carrier_date = Column(DateTime)
    order_delivered_customer_date = Column(DateTime)
    order_estimated_delivery_date = Column(DateTime)


# =========================
# Products
# =========================

class Product(Base):
    __tablename__ = "products"

    product_id = Column(String(50), primary_key=True)
    product_category_name = Column(String(100))
    product_name_lenght = Column(Integer)
    product_description_lenght = Column(Integer)
    product_photos_qty = Column(Integer)
    product_weight_g = Column(Float)
    product_length_cm = Column(Float)
    product_height_cm = Column(Float)
    product_width_cm = Column(Float)


# =========================
# Order Items
# =========================

class OrderItem(Base):
    __tablename__ = "order_items"

    order_id = Column(
        String(50),
        ForeignKey("orders.order_id"),
        primary_key=True
    )

    order_item_id = Column(
        Integer,
        primary_key=True
    )

    product_id = Column(
        String(50),
        ForeignKey("products.product_id")
    )

    seller_id = Column(String(50))
    shipping_limit_date = Column(DateTime)
    price = Column(Float)
    freight_value = Column(Float)


# =========================
# Order Payments
# =========================

class OrderPayment(Base):
    __tablename__ = "order_payments"

    order_id = Column(
        String(50),
        ForeignKey("orders.order_id"),
        primary_key=True
    )

    payment_sequential = Column(
        Integer,
        primary_key=True
    )

    payment_type = Column(String(30))
    payment_installments = Column(Integer)
    payment_value = Column(Float)


# =========================
# Order Reviews
# =========================

class OrderReview(Base):
    __tablename__ = "order_reviews"

    review_key = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    review_id = Column(String(50))

    order_id = Column(
        String(50),
        ForeignKey("orders.order_id")
    )

    review_score = Column(Integer)
    review_comment_title = Column(String(300))
    review_comment_message = Column(String(1000))
    review_creation_date = Column(DateTime)
    review_answer_timestamp = Column(DateTime)
# =========================
# Category Translation
# =========================

class CategoryTranslation(Base):
    __tablename__ = "product_category_name_translation"

    product_category_name = Column(
        String(100),
        primary_key=True
    )

    product_category_name_english = Column(String(100))