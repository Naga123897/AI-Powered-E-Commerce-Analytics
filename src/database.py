import os
from sqlalchemy import create_engine, text

# MySQL connection details
username = os.getenv("MYSQL_USER", "root")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST", "localhost")
port = int(os.getenv("MYSQL_PORT", "3306"))
database = os.getenv("MYSQL_DATABASE", "ecommerce_analytics")

# Create database connection
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

# Test the connection
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE();"))
        print("Connected successfully!")
        print("Current database:", result.scalar())

except Exception as e:
    print("Connection failed.")
    print("Error:", e)