
# 💰 Expense Tracker Project

This project is a SQL and Streamlit-based Expense Tracker designed to analyze and visualize personal spending data. It helps users gain insights into their financial habits, identify high-spending categories, and understand cashback and payment trends throughout the year.

---

## 📌 Project Overview

- 🔍 **Goal**: To analyze yearly expenses and generate meaningful insights using SQL and Python.
- 📊 **Dataset**: Generated using Python’s `faker` library for 12 months.
- 🧮 **Technologies Used**:  
  - **SQL** (MySQL Workbench)  
  - **Python (Pandas, Numpy)**  
  - **Streamlit**  
  - **Plotly Express**  
  - **VS Code**  
  - **GitHub**  

---

## 🗃️ Table Structure

| Column Name   | Description                                |
|---------------|--------------------------------------------|
| Date          | Date of the transaction                    |
| Category      | Expense category (e.g., Food, Travel)       |
| Amount        | Amount spent                               |
| Description   | Transaction details                        |
| Payment Mode  | Cash / Bank Transfer / Credit / UPI        |
| Cashback      | Cashback earned for the transaction        |

---

## 🚀 Key Features

- Monthly and category-wise breakdown of expenses.
- Top spending categories and most used payment methods.
- Detection of small but frequent transactions.
- Cashback trends and seasonal variations.
- Query page for dynamic SQL filtering.
- Visual dashboards with charts and insights.

---

## 📁 Project Structure

    ```bash
    ├── expense_tracker/
    │   ├── app.py                # Streamlit app
    │   ├── queries.sql           # SQL queries used
    │   ├── df3.csv               # Cleaned expense data
    │   ├── requirements.txt      # Python packages
    │   └── README.md             # This file

---

## 🧠 What I Learned

- Writing dynamic SQL queries for time-based filtering and grouping.

- Handling NULLs and missing values using IFNULL() and COALESCE().

- Creating dashboards using Streamlit and Plotly.

- Analyzing real-world spending behavior through visual insights.

- Using GitHub for version control and documentation.

---

## 📷 Sample Insights

- Top Spending Category: Transportation

- Most Active Spending Days: Friday and Saturday

- Most Cashback Earned From: Stationery

- Most Used Payment Mode: Bank Transfer

- Peak Spending Time: Night

- Category with Frequent Small Transactions: Food
