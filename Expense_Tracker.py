import streamlit as st
import pandas as pd
import numpy as np
import pymysql
import plotly.express as px

# MySQL Database Configuration (Change these details)
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Password7"
DB_NAME = "expense_db"

# Establish connection
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Password7",
        database="expense_db",
        cursorclass=pymysql.cursors.DictCursor
    )

# Sidebar Title
st.sidebar.title("Expense Tracker Menu")

# Sidebar Selectbox (Dropdown)
page = st.sidebar.selectbox("Go to", ["Home", "Queries", "Charts" , "Analysis"])

if page == "Home":
    st.title("Expense Tracker and Analysis")

    st.write(
            "### Annual Expense Table")
    st.write("Below is the breakdown of Monthly Expenses")

    df=pd.read_csv("C:/Users/Mansi/.vscode/Annual_expense.csv")
    st.write(df)

    # Convert 'date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    st.subheader("Filter Expenses")

    start_date, end_date = st.date_input("Select Date Range", [df['Date'].min(), df['Date'].max()])
    filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

    Category = st.selectbox("Filter by Category", ["All"] + list(df["Category"].unique()))
    if Category != "All":
        filtered_df = filtered_df[filtered_df["Category"] == Category]

    min_amount, max_amount = st.slider("Filter by Amount", 
                                    int(df["Amount"].min()), 
                                    int(df["Amount"].max()), 
                                    (int(df["Amount"].min()), int(df["Amount"].max())))
    filtered_df = filtered_df[(filtered_df["Amount"] >= min_amount) & (filtered_df["Amount"] <= max_amount)]

    sort_by = st.radio("Sort By", ["Date", "Amount"])
    if sort_by == "Amount":
        filtered_df = filtered_df.sort_values(by="Amount", ascending=False)
    else:
        filtered_df = filtered_df.sort_values(by="Date", ascending=False)


    st.write("### Filtered Expenses 📜")
    st.dataframe(filtered_df)

    if st.checkbox("Show Summary Statistics"):
        st.write(filtered_df.describe())

elif page == "Queries":
    # ✅ Class to Handle MySQL Queries Efficiently
    class DatabaseManager: 
        def __init__(self):
            """Initialize connection to MySQL"""
            self.conn = pymysql.connect(
                host="localhost",
                user="root",
                password="Password7",
                database="expense_db"
            )
            self.cursor = self.conn.cursor()

        def run_query(self, query):
            """Run a SQL query and return results as DataFrame"""
            try:
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                columns = [desc[0] for desc in self.cursor.description]
                return pd.DataFrame(result, columns=columns)
            except Exception as e:
                st.error(f"Error executing query: {e}")
                return pd.DataFrame()

        def close_connection(self):
            """Close the database connection"""
            self.cursor.close()
            self.conn.close()


    # ✅ Streamlit App
    st.title("SQL Queries on Expenses 🛠️")

    # ✅ Create a single instance of DatabaseManager
    db = DatabaseManager()

    # Define queries
    queries = {
        "Query 1 : The Total Amount spent on each Category.": "SELECT Category, SUM(amount) AS total_amount FROM df3 GROUP BY Category ORDER BY total_amount DESC;",
        "Query 2 : The Total Amount spent using each Payment Mode. ": "SELECT 'Payment Mode',SUM(amount) AS total_spent FROM df3 GROUP BY 'Payment Mode' ORDER BY total_spent DESC;",
        "Query 3 : The Total Cashback received in all transactions.": "SELECT SUM(Cashback) AS total_Cashback FROM df3;",
        "Query 4 : The Top five most expensive Categories in terms of spendings. ": "SELECT Category, SUM(amount) AS total_spent FROM df3 GROUP BY Category ORDER by total_spent DESC LIMIT 5;",
        "Query 5 : Total Spendings on Transportation using different Payment Modes. ": "SELECT 'Payment Mode',SUM(amount) AS total_spent FROM df3 WHERE Category = 'Transport' GROUP BY 'Payment Mode' ORDER BY total_spent DESC;",
        "Query 6 : The Transactions resulted in Cashback": "SELECT * FROM df3 WHERE Cashback>0;",
        "Query 7 : The Total spending in each month of the year": "SELECT MONTHNAME(Date) AS month, SUM(amount) AS total_spent FROM df3 GROUP BY MONTH(Date), MONTHNAME(Date) ORDER BY MONTH(Date);",
        "Query 8 : The Months having highest spending in categories like 'Travel', 'Entertainment' and 'Shopping'.": "SELECT DATE_FORMAT(date,'%Y,%m') AS month, Category, SUM(amount) AS total_spent FROM df3 WHERE Category IN('Travel','Entertainment','Shopping')GROUP BY month, Category ORDER BY total_spent DESC;",
        "Query 9 : To check for any recurring expenses that occur during specific months of the year.": "SELECT DATE_FORMAT(date,'%m') AS month, Category, COUNT(*) AS OCCURRENCE_count, SUM(amount) AS total_spent FROM df3 GROUP BY month, Category HAVING COUNT(*)>=2 ORDER BY month, total_spent DESC;",
        "Query 10 : Numbers of Cashbacks or rewards were earned in each month.": "SELECT DATE_FORMAT(date,'%Y-%m') AS month, SUM(amount) AS total_rewards FROM df3 WHERE Cashback>0 GROUP BY month ORDER BY month;",
        "Query 11 : To check overall spending changed overtime.": "SELECT DATE_FORMAT(date,'%Y-%m') AS month, SUM(amount) AS total_spent FROM df3 GROUP BY month ORDER BY month;",   
        "Query 12 : The typical costs associated with Travelling.":"SELECT Category AS Travel_type, AVG(amount) AS avg_cost, MIN(amount) AS min_cost, MAX(amount) AS max_cost, SUM(amount) AS total_spent, COUNT(*) AS num_transactions FROM df3 WHERE Category IN('Travel','Transport') GROUP BY travel_type ORDER BY total_spent DESC;",
        "Query 13 : To Analysis the patterns in grocery spendings.": "SELECT DAYNAME(date) AS day_of_week, SUM(amount) AS total_spent, COUNT(*) AS num_transactions FROM df3 WHERE Category = 'Food' GROUP BY day_of_week ORDER BY FIELD(day_of_week,'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday');",
        "Query 14 : To define High and Low priority Categories": "SELECT Category, SUM(amount) AS total_spent, CASE WHEN SUM(amount)>=45000 then 'High Priority' WHEN SUM(amount) BETWEEN 40000 AND 30000 THEN 'Medium Priority' ELSE 'low Priority' END AS priority FROM df3 GROUP BY Category ORDER BY total_spent DESC;",
        "Query 15 : The Categories contributing the highest Percentage of the total spendings": "SELECT Category, SUM(amount) AS total_spent, (SUM(amount)/(SELECT SUM(amount)FROM df3)*100) AS Percentage FROM df3 GROUP BY Category ORDER BY total_spent DESC LIMIT 1;"
        
    }

    # ✅ Dropdown to select a query
    selected_query = st.selectbox("Select a Query:", list(queries.keys()))

    # ✅ Button to run query
    if st.button("Run Selected Query"):
        df = db.run_query(queries[selected_query])
        if not df.empty:
            st.dataframe(df)
        else:
            st.warning("No results found!")

    # ✅ Close DB connection when done
    db.close_connection()


elif page == "Charts":
    def get_data():
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="Password7",
            database="expense_db"
         )
        query = "SELECT Date, Category, amount FROM df3;"
        df = pd.read_sql(query, conn)
        conn.close()
        return df

# ✅ Load Data
    st.title("📊 Expense Analysis & Charts")

    df = get_data()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%Y-%m')

    # 📈 Line Chart - Monthly Expense Trends
    st.subheader("📈 Monthly Expense Trend")
    monthly_expense = df.groupby('Month')['amount'].sum().reset_index()
    fig1 = px.line(monthly_expense, x='Month', y='amount', title="Monthly Expenses")
    st.plotly_chart(fig1)

    # 📊 Bar Chart - Expense by Category
    st.subheader("📊 Category-wise Spending")
    category_expense = df.groupby('Category')['amount'].sum().reset_index()
    fig2 = px.bar(category_expense, x='Category', y='amount', title="Expenses by Category", color='Category')
    st.plotly_chart(fig2)

    # 🎂 Pie Chart - Expense Distribution
    st.subheader("🎂 Expense Breakdown by Category")
    fig3 = px.pie(category_expense, names='Category', values='amount', title="Expense Distribution")
    st.plotly_chart(fig3)

    # 📊 Histogram - Grocery Spending Over the Week
    st.subheader("🛒 Weekly Grocery Spending Pattern")

    # ✅ Convert 'date' column to datetime format
    df["date"] = pd.to_datetime(df["Date"])

    # ✅ Extract weekday name from 'date'
    df["day_of_week"] = df["Date"].dt.day_name()

    grocery_expense = df[df['Category'].str.lower() == 'food']  # Filter only grocery expenses

    if not grocery_expense.empty:
        
        fig4 = px.histogram(
            grocery_expense, 
            x='day_of_week', 
            y='amount', 
            title="Total Grocery Expenses by Weekday",
            category_orders={"day_of_week": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},  
            color='day_of_week'
        )
        st.plotly_chart(fig4)
    else:
        st.warning("No grocery expenses found in the dataset.")
        
elif page == "Analysis":
    def get_data(): #create a connection to mysql
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="Password7",
            database="expense_db"
         )
        query = "SELECT Date, Category, amount FROM df3;" #to read the data
        df = pd.read_sql(query, conn)
        conn.close()
        return df
     
    df = get_data()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Total Expenses, Monthly Average, Highest Spending Month
    total_spent = df["amount"].sum()
    monthly_avg = df.groupby(df["Date"].dt.to_period("M"))["amount"].sum().mean()
    highest_month = df.groupby(df["Date"].dt.strftime("%Y-%m"))["amount"].sum().idxmax()

    st.metric(label="💰 Total Expenses", value=f"₹{total_spent:,.2f}")
    st.metric(label="📅 Monthly Average", value=f"₹{monthly_avg:,.2f}")
    st.metric(label="🏆 Highest Spending Month", value=highest_month)    
    weekday_spending = df.groupby(df["Date"].dt.day_name())["amount"].sum()

    # Find highest spending weekday
    highest_day = weekday_spending.idxmax()
    st.write(f"📌 You spend the most on **{highest_day}s**.")

    # Find category with highest % of spending
    category_spending = df.groupby("Category")["amount"].sum()
    highest_category = category_spending.idxmax()
    percent_spent = (category_spending.max() / total_spent) * 100
    st.write(f"📌 Your highest spending category is **{highest_category}** (📊 {percent_spent:.2f}% of total spending).")
    st.write("Due to running out of time, He/She is using more transport vehicle to reach even short distance Destinations. So, He/She could prepare itself for next tour or can use bicycle for nearby places. This change will be very helpful for him or her.")

    # Monthly Spending Change Indicator
    df["Month"] = df["Date"].dt.strftime("%Y-%m")
    monthly_expenses = df.groupby("Month")["amount"].sum().reset_index()

    if len(monthly_expenses) > 1:
        last_month = monthly_expenses.iloc[-2]["amount"]
        this_month = monthly_expenses.iloc[-1]["amount"]
        diff = this_month - last_month
        percentage_change = (diff / last_month) * 100

        
        st.write(f"📈 Your spending increased by **{percentage_change:.2f}%** this month.")

    # Highlight High & Low Spending Categories
    low_spending_category = category_spending.idxmin()
    st.write(f"🟢 You spend the least on **{low_spending_category}**. ")
    st.write(f"🔴 You spend the most on **{highest_category}**.")
        
    # Grocery tips
    if "Food" in df["Category"].unique():
     st.write("🛒 **Grocery Tip:** Buying in bulk and shopping during discount sales can help reduce food expenses.")

    # Track impulse purchases
    high_expense_purchases = df[df["amount"] > 450] 
    if not high_expense_purchases.empty:
        st.write("⚠️ **Large Purchases Detected!**")
        st.dataframe(high_expense_purchases)
        st.write("💡 Before making big purchases, ask yourself: 'Do I really need this?'")

    # Monthly Savings 
    monthly_income = st.number_input("Enter your estimated monthly income:", min_value=1000, step=500)
    if monthly_income:
        suggested_savings = monthly_income * 0.10
        st.write(f"💰 **Try saving at least ₹{suggested_savings:,.2f} every month!** Small savings add up over time.")
    

    
   