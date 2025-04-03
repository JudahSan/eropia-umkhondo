import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from data_manager import DataManager
from visualization import (
    plot_transaction_overview,
    plot_spending_by_category,
    plot_spending_trend,
    plot_income_vs_expense
)

def app():
    if "username" not in st.session_state:
        st.warning("Please log in to access your dashboard.")
        st.session_state.current_page = "login"
        st.rerun()
        return
    
    username = st.session_state.username
    
    st.title(f"Financial Dashboard - {username}")
    
    # Initialize the data manager with the user's data
    data_manager = DataManager(username=username)
    data_manager.ensure_data_file_exists()
    
    # Get all transactions
    transactions_df = data_manager.get_transactions()
    
    if transactions_df.empty:
        st.info("No transactions found. Add some transactions to see your financial insights.")
        return

    # Dashboard metrics
    col1, col2, col3 = st.columns(3)
    
    # Calculate total income and expenses
    income = transactions_df[transactions_df['type'] == 'income']['amount'].sum()
    expenses = transactions_df[transactions_df['type'] == 'expense']['amount'].sum()
    balance = income - expenses
    
    # Display metrics
    with col1:
        st.metric(label="Total Income", value=f"KSh {income:,.2f}", delta=None)
    
    with col2:
        st.metric(label="Total Expenses", value=f"KSh {expenses:,.2f}", delta=None)
    
    with col3:
        st.metric(label="Balance", value=f"KSh {balance:,.2f}", delta=None)
    
    st.write("---")
    
    # Filtering options
    st.subheader("Filter Transactions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Date range filter
        default_start_date = datetime.now() - timedelta(days=30)
        default_end_date = datetime.now()
        
        start_date = st.date_input("Start Date", value=default_start_date)
        end_date = st.date_input("End Date", value=default_end_date)
    
    with col2:
        # Category filter
        categories = ["All"] + sorted(transactions_df['category'].unique().tolist())
        selected_category = st.selectbox("Category", categories)
    
    with col3:
        # Transaction type filter
        transaction_types = ["All", "income", "expense"]
        selected_type = st.selectbox("Transaction Type", transaction_types)
    
    # Apply filters
    filtered_df = transactions_df.copy()
    
    # Date filter
    filtered_df = filtered_df[
        (filtered_df['date'] >= pd.Timestamp(start_date)) & 
        (filtered_df['date'] <= pd.Timestamp(end_date))
    ]
    
    # Category filter
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    # Transaction type filter
    if selected_type != "All":
        filtered_df = filtered_df[filtered_df['type'] == selected_type]
    
    st.write("---")
    
    # Visualizations
    st.subheader("Financial Insights")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Spending by Category", "Monthly Trend", "Income vs. Expense"])
    
    with tab1:
        st.plotly_chart(plot_transaction_overview(filtered_df), use_container_width=True)
    
    with tab2:
        st.plotly_chart(plot_spending_by_category(filtered_df), use_container_width=True)
    
    with tab3:
        st.plotly_chart(plot_spending_trend(filtered_df), use_container_width=True)
    
    with tab4:
        st.plotly_chart(plot_income_vs_expense(filtered_df), use_container_width=True)
    
    st.write("---")
    
    # Transactions table
    st.subheader("Transaction History")
    
    if not filtered_df.empty:
        # Convert date to string for display
        display_df = filtered_df.copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        
        # Format amount for display
        display_df['amount'] = display_df['amount'].apply(lambda x: f"KSh {x:,.2f}")
        
        # Customize columns and order
        display_df = display_df[['date', 'description', 'amount', 'type', 'category']]
        display_df.columns = ['Date', 'Description', 'Amount', 'Type', 'Category']
        
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No transactions match your filters.")

if __name__ == "__main__":
    app()