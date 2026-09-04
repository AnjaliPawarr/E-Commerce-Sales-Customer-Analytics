# E-Commerce Sales & Customer Analytics

## 📌 Project Overview

E-Commerce Sales & Customer Analytics is a data analytics project designed to analyze
sales performance, customer behavior, product performance, and revenue trends.

The project uses Python, SQL, SQLite, and Power BI to transform raw e-commerce
transaction data into meaningful business insights.

---

## 🎯 Objectives

- Analyze overall sales and revenue performance
- Identify top-performing products and categories
- Analyze customer purchasing behavior
- Identify high-value customers using RFM analysis
- Analyze repeat and one-time customers
- Compare revenue across cities and genders
- Analyze monthly revenue trends
- Build an interactive Power BI dashboard

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- SQL
- SQLite
- Power BI
- DAX
- Git & GitHub

---

## 📂 Project Structure

```text
E-Commerce-Sales-Customer-Analytics
│
├── data
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   └── ecommerce.db
│
├── python
│   ├── generate_dataset.py
│   ├── load_database.py
│   ├── analysis.py
│   ├── run_sql_analysis.py
│   └── create_dashboard_data.py
│
├── sql
│   └── analysis.sql
│
├── outputs
│   ├── monthly_revenue.png
│   ├── category_sales.png
│   ├── top_10_customers.png
│   ├── customer_segments.png
│   ├── customer_rfm_analysis.csv
│   └── dashboard_data.csv
│
├── dashboard
│   └── E-Commerce-Sales-Customer-Analytics.pbix
│
└── README.md

🚀 How to Run the Project
1. Clone the Repository
git clone <your-github-repository-url>
2. Install Required Libraries
pip install pandas numpy matplotlib
3. Generate the Dataset
python python/generate_dataset.py
4. Create SQLite Database
python python/load_database.py
5. Run Python Analysis
python python/analysis.py
6. Run SQL Analysis
python python/run_sql_analysis.py
7. Create Power BI Dataset
python python/create_dashboard_data.py
8. Open Power BI Dashboard

Open:

dashboard/E-Commerce-Sales-Customer-Analytics.pbix

using Power BI Desktop.

