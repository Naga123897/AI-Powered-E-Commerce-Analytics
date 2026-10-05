# AI-Powered E-Commerce Analytics & Customer Insights

An end-to-end e-commerce analytics project built using Python, MySQL, SQL, Power BI, and a local Large Language Model (LLM). The project combines traditional business analytics with an AI-powered natural-language question-answering system.

## Project Overview

This project analyzes the Brazilian E-Commerce Public Dataset by Olist and provides business insights across sales, customers, products, delivery, payments, and reviews.

The project includes:

* Data cleaning using Python and Pandas
* Data storage and analysis using MySQL and SQL
* Database structure management using SQLAlchemy and Alembic
* Interactive business dashboards using Power BI
* AI-powered business question answering using Ollama and Qwen3 1.7B
* Web interface using Streamlit
* Containerized deployment using Docker

## Project Objective

The main objective is to build a complete analytics solution that can:

1. Clean and prepare e-commerce data.
2. Store the data in a relational MySQL database.
3. Perform business analysis using SQL.
4. Present important business insights through Power BI dashboards.
5. Allow users to ask supported business questions using natural language.
6. Retrieve verified metrics from MySQL.
7. Use a local LLM to convert verified results into simple business answers.
8. Run the application inside a Docker container.

## Project Architecture

```text
Olist CSV Data
       ↓
Python / Pandas
       ↓
Data Cleaning
       ↓
MySQL Database
       ↓
SQL Business Analysis
       ↓
Power BI Dashboards
       
MySQL
   ↓
SQLAlchemy + Python
   ↓
Verified Business Metrics
   ↓
JSON
   ↓
Ollama
   ↓
Qwen3 1.7B
   ↓
Streamlit Web Application
   ↓
Docker
```

## Technology Stack

| Technology | Purpose                                     |
| ---------- | ------------------------------------------- |
| Python     | Data processing and application logic       |
| Pandas     | Data cleaning and preparation               |
| MySQL      | Relational database                         |
| SQL        | Business analysis and metric extraction     |
| SQLAlchemy | Python-to-MySQL database connection         |
| PyMySQL    | MySQL database driver                       |
| Alembic    | Database migration management               |
| Power BI   | Interactive business dashboards             |
| Ollama     | Local LLM runtime                           |
| Qwen3 1.7B | Local language model                        |
| Streamlit  | Web application interface                   |
| Docker     | Application containerization and deployment |
| WSL 2      | Docker Desktop support on Windows           |
| VS Code    | Development environment                     |

## Dataset

The project uses the **Brazilian E-Commerce Public Dataset by Olist**.

The dataset contains e-commerce information covering areas such as:

* Customers
* Orders
* Order items
* Products
* Payments
* Reviews
* Product category translation

The original dataset files are kept outside the GitHub repository through `.gitignore` because the project does not need to upload the CSV data files to GitHub.

## Data Processing

The raw CSV files were loaded and inspected using Python and Pandas.

Seven dataset files were processed:

```text
olist_customers_dataset.csv
olist_orders_dataset.csv
olist_order_items_dataset.csv
olist_products_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
product_category_name_translation.csv
```

The cleaned data was then loaded into MySQL for further analysis.

## Database

The MySQL database used in the project is:

```text
ecommerce_analytics
```

Main tables:

```text
customers
orders
order_items
products
order_payments
order_reviews
product_category_name_translation
```

Alembic also creates:

```text
alembic_version
```

which is used to track database migration versions.

### Main Relationships

```text
customers
    ↓
orders
    ↓
order_items
    ↓
products
    ↓
product_category_name_translation

orders
    ↓
order_payments

orders
    ↓
order_reviews
```

## Power BI Dashboard

The project includes an interactive Power BI dashboard connected to the MySQL database.

The dashboard contains five pages covering the main business areas of the e-commerce data.

### 1. Executive Sales

Key areas:

* Total Revenue
* Total Orders
* Average Order Value
* Total Customers
* Total Freight
* Monthly Revenue
* Revenue by Category
* Revenue by State

![Executive Sales Dashboard](powerbi/screenshots/Executive_Sales.png)

### 2. Customer Analysis

Key areas:

* Total Customers
* Repeat Customers
* One-Time Customers
* Average Orders per Customer
* Customer Type Distribution
* Top Customers by Revenue
* State-level analysis

![Customer Analysis Dashboard](powerbi/screenshots/Customer_Analysis.png)

### 3. Product Analysis

Key areas:

* Total Products
* Items Sold
* Total Revenue
* Average Product Price
* Total Freight
* Revenue by Category
* Items by Category
* Top Products

![Product Analysis Dashboard](powerbi/screenshots/Product_Analysis.png)

### 4. Delivery & Reviews

Key areas:

* Average Delivery Days
* Late Delivery Percentage
* Average Review Score
* Delivery Performance by State
* Review Score Distribution
* Review Score vs Delivery Time

![Delivery and Reviews Dashboard](powerbi/screenshots/Delivery_Reviews.png)

### 5. Payment Analysis

Key areas:

* Total Payment Value
* Average Payment Value
* Payment Count
* Payment Method Distribution
* Payment Value by Payment Method
* Installment Distribution

![Payment Analysis Dashboard](powerbi/screenshots/Payment_Analysis.png)

### Power BI File

The Power BI dashboard file is included in the project:

```text
powerbi/
└── Ecommerce Dashboard.pbix
```

## AI-Powered Business Q&A

The project includes a natural-language business question-answering system.

The system does not ask the LLM to calculate business metrics directly.

Instead, the application follows this process:

```text
User Question
      ↓
Question Identification
      ↓
Supported Question Type
      ↓
SQL Query
      ↓
MySQL
      ↓
Verified Result
      ↓
JSON
      ↓
Qwen3 1.7B
      ↓
Simple Business Answer
```

### Why this approach?

MySQL is used as the source of truth for business metrics.

The LLM is used as a language layer to present the verified result in a simple and understandable way.

This helps prevent the LLM from inventing or changing business numbers.

### Supported Business Questions

The application supports questions covering:

* Total revenue
* Total orders
* Total customers
* Average order value
* Total freight
* Total products
* Items sold
* Average delivery days
* Total payment value
* Average payment value
* Average review score
* Review count
* Highest-revenue state
* Highest-revenue category
* Highest-revenue product
* Most common payment method
* Highest-selling category
* State with the highest number of orders
* Payment method with the highest payment value
* State with the longest delivery time
* Month with the highest revenue
* State with the highest review score

### Example

**Question:**

```text
Which state has the highest number of orders?
```

**Verified result from MySQL:**

```json
{
  "state": "SP",
  "total_orders": 41746
}
```

**AI answer:**

```text
The state with the highest number of orders is SP, totaling 41,746.
```

The AI answer is generated from the verified database result rather than allowing the LLM to independently calculate the metric.

## AI Technology

### Ollama

Ollama is used to run the LLM locally.

### Qwen3 1.7B

Qwen3 1.7B is the language model used by the application.

The model is used for:

* Understanding the verified result
* Generating a natural-language response
* Presenting the answer in simple English

The project does not use an external OpenAI API.

## Reliability and Validation

The application includes validation before sending data to the LLM.

The system:

* Accepts only supported business questions.
* Retrieves the corresponding SQL query.
* Gets the result directly from MySQL.
* Converts the result into JSON.
* Sends the verified result to Qwen3.
* Instructs the model not to invent or calculate new values.
* Returns an error message when a question is not supported.

For example:

```text
User:
What is the total profit?

Application:
This question is not currently supported.
```

Profit is not calculated because the available dataset does not contain the required cost/profit information.


## Streamlit Web Application

The AI business Q&A system is provided through a Streamlit web interface.

The application allows users to:

1. Enter a business question.
2. Identify the supported question type.
3. Retrieve verified data from MySQL.
4. Display the verified result.
5. Generate a simple AI answer using Qwen3 1.7B.

The main application file is:

```text id="b4v5h1"
app.py
```

The application can be started with:

```powershell id="3j3n9q"
streamlit run app.py
```

The web application provides three main outputs:

* Question Type
* Verified Data
* AI Answer

## Docker Deployment

Docker is used to containerize the Streamlit application and its Python environment.

The project contains:

```text id="u3a0xc"
Dockerfile
.dockerignore
requirements.txt
```

### Docker Image

The application image was built using:

```powershell id="a2yl80"
docker build -t ecommerce-ai-app .
```

The image was successfully created as:

```text id="b8rj3f"
ecommerce-ai-app:latest
```

### Running the Docker Container

The application was tested inside a Docker container with connections to:

* MySQL running on the host machine
* Ollama running on the host machine
* Qwen3 1.7B through Ollama
* Streamlit inside the Docker container

The container was run with environment variables for the database and Ollama connection.

The application was successfully accessed through:

```text id="7y5x5b"
http://localhost:8501
```

### Docker Architecture

```text id="x6p4gr"
Docker Container
│
├── Python
├── Streamlit
├── Project Code
└── SQLAlchemy
        │
        ├──────────────→ MySQL
        │
        └──────────────→ Ollama
                              │
                              ↓
                         Qwen3 1.7B
```

The Docker container packages the application environment so that the application can be run in a consistent environment.

## Project Structure

```text id="5k3q4m"
Ecommerce_AI_Analytics
│
├── data
│   ├── raw
│   └── cleaned
│
├── migrations
│
├── notebooks
│
├── powerbi
│   ├── Ecommerce Dashboard.pbix
│   └── screenshots
│
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd Ecommerce_AI_Analytics
```

### 2. Create a Python Virtual Environment

```powershell
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

The project uses:

```text
streamlit
ollama
sqlalchemy
pymysql
python-dotenv
alembic
pandas
```

### 4. Configure Environment Variables

Create a `.env` file with the required database configuration.

The `.env` file is intentionally excluded from GitHub because it can contain sensitive database credentials.

### 5. Set Up MySQL

Create the MySQL database:

```text
ecommerce_analytics
```

The required tables are created and managed as part of the project's database and migration workflow.

### 6. Run Database Migrations

```powershell
alembic upgrade head
```

### 7. Load the Cleaned Data

```powershell
python src/load_data.py
```

### 8. Install and Run Ollama

Install Ollama and download the required model:

```powershell
ollama pull qwen3:1.7b
```

The application uses Qwen3 1.7B through Ollama.

### 9. Run the Streamlit Application

```powershell
streamlit run app.py
```

The application will be available locally through Streamlit.

## Key Business Analysis Areas

The project analyzes:

* Sales performance
* Customer behavior
* Product performance
* Delivery performance
* Payment behavior
* Customer reviews

The SQL analysis is organized into separate files for these business areas.

## Data Quality and Business Rules

The project follows several important rules when generating AI answers:

* MySQL is treated as the source of verified business metrics.
* The LLM does not independently calculate business metrics.
* Unsupported questions are rejected.
* The system does not invent missing information.
* Profit is not reported because the dataset does not provide the required profit information.
* Payment metrics are based on payment records.
* Review metrics are based on available review records.
* Delivery metrics use orders with available delivery dates.

## Final Result

The completed project provides an end-to-end analytics workflow:

```text
Raw E-Commerce Data
        ↓
Python + Pandas
        ↓
Data Cleaning
        ↓
MySQL
        ↓
SQL Business Analysis
        ↓
Power BI Dashboard
        ↓
SQLAlchemy + Python
        ↓
Verified Business Metrics
        ↓
JSON
        ↓
Ollama + Qwen3 1.7B
        ↓
Streamlit
        ↓
Docker
```

The result is a business analytics solution that combines:

**Data Analytics + Business Intelligence + AI + Web Application + Containerization**

## Project Limitations

* The AI assistant currently supports a predefined set of business question types.
* Questions outside the supported question library are not processed.
* The LLM is not used as a source of numerical truth.
* Profit analysis is not available because the dataset does not contain the required cost/profit information.
* The Power BI dashboard requires Power BI to open the `.pbix` file.

## Author

**Thirumalesh**

B.Tech — Computer Science and Engineering
