import streamlit as st
import pandas as pd
import datetime
import os
from data_manager import DataManager
from mpesa_api import MPesaAPI
from visualization import (
    plot_transaction_overview,
    plot_spending_by_category,
    plot_spending_trend,
    plot_income_vs_expense
)
from utils import categorize_transaction

# Set page configuration
st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if not already set
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()
    
if 'mpesa_api' not in st.session_state:
    st.session_state.mpesa_api = MPesaAPI()

if 'show_transaction_form' not in st.session_state:
    st.session_state.show_transaction_form = False
    
if 'show_mpesa_form' not in st.session_state:
    st.session_state.show_mpesa_form = False

if 'current_view' not in st.session_state:
    st.session_state.current_view = "dashboard"

if 'filter_date_range' not in st.session_state:
    st.session_state.filter_date_range = None
    
if 'filter_category' not in st.session_state:
    st.session_state.filter_category = None
    
if 'filter_type' not in st.session_state:
    st.session_state.filter_type = None
    
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

def toggle_transaction_form():
    st.session_state.show_transaction_form = not st.session_state.show_transaction_form
    st.session_state.show_mpesa_form = False

def toggle_mpesa_form():
    st.session_state.show_mpesa_form = not st.session_state.show_mpesa_form
    st.session_state.show_transaction_form = False

def change_view(view):
    st.session_state.current_view = view

def add_personal_transaction(date, description, amount, transaction_type, category):
    new_transaction = {
        'date': date,
        'description': description,
        'amount': float(amount),
        'type': transaction_type,
        'category': category,
        'source': 'manual'
    }
    
    st.session_state.data_manager.add_transaction(new_transaction)
    st.success(f"Added {transaction_type} transaction: {description} for {amount}")
    st.session_state.show_transaction_form = False
    st.rerun()

def import_mpesa_transactions(phone_number, start_date, end_date):
    try:
        with st.spinner("Fetching M-Pesa transactions..."):
            transactions = st.session_state.mpesa_api.get_transactions(
                phone_number, start_date, end_date
            )
            
            if transactions:
                count = 0
                for transaction in transactions:
                    # Auto-categorize the transaction based on description
                    category = categorize_transaction(transaction['description'])
                    transaction['category'] = category
                    transaction['source'] = 'mpesa'
                    
                    # Add to our data manager
                    st.session_state.data_manager.add_transaction(transaction)
                    count += 1
                    
                st.success(f"Successfully imported {count} M-Pesa transactions")
                st.session_state.show_mpesa_form = False
                st.rerun()
            else:
                st.warning("No transactions found for the specified period")
    except Exception as e:
        st.error(f"Error importing M-Pesa transactions: {str(e)}")

def filter_transactions(transactions_df):
    filtered_df = transactions_df.copy()
    
    # Apply date range filter
    if st.session_state.filter_date_range:
        start_date, end_date = st.session_state.filter_date_range
        filtered_df = filtered_df[(filtered_df['date'] >= start_date) & 
                                  (filtered_df['date'] <= end_date)]
    
    # Apply category filter
    if st.session_state.filter_category and st.session_state.filter_category != "All":
        filtered_df = filtered_df[filtered_df['category'] == st.session_state.filter_category]
    
    # Apply transaction type filter
    if st.session_state.filter_type and st.session_state.filter_type != "All":
        filtered_df = filtered_df[filtered_df['type'] == st.session_state.filter_type]
    
    # Apply search query
    if st.session_state.search_query:
        query = st.session_state.search_query.lower()
        filtered_df = filtered_df[filtered_df['description'].str.lower().str.contains(query)]
    
    return filtered_df

# Sidebar for navigation and filters
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/financial-growth.png", width=80)
    st.title("Finance Tracker")
    
    st.markdown("### Navigation")
    if st.button("Dashboard", use_container_width=True):
        change_view("dashboard")
    if st.button("Transactions", use_container_width=True):
        change_view("transactions")
    if st.button("Analytics", use_container_width=True):
        change_view("analytics")
        
    st.markdown("---")
    st.markdown("### Add Transactions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Personal", use_container_width=True):
            toggle_transaction_form()
    with col2:
        if st.button("M-Pesa", use_container_width=True):
            toggle_mpesa_form()
            
    st.markdown("---")
    st.markdown("### Filters")
    
    # Date range filter
    date_range = st.date_input(
        "Date Range",
        value=(datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()),
        key="date_filter"
    )
    if len(date_range) == 2:
        st.session_state.filter_date_range = date_range
    
    # Get all transactions for other filters
    transactions_df = st.session_state.data_manager.get_transactions()
    
    if not transactions_df.empty:
        # Category filter
        categories = ["All"] + sorted(transactions_df['category'].unique().tolist())
        st.session_state.filter_category = st.selectbox("Category", categories)
        
        # Transaction type filter
        types = ["All"] + sorted(transactions_df['type'].unique().tolist())
        st.session_state.filter_type = st.selectbox("Type", types)
        
        # Search filter
        st.session_state.search_query = st.text_input("Search", value=st.session_state.search_query)
        
    st.markdown("---")
    st.markdown("### About")
    st.info("This app helps you track and visualize your personal and M-Pesa transactions.")

# Main content area
if st.session_state.show_transaction_form:
    st.subheader("Add Personal Transaction")
    
    with st.form("transaction_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input("Date", value=datetime.date.today())
            amount = st.number_input("Amount", min_value=0.01, step=0.01)
            transaction_type = st.selectbox("Type", ["expense", "income", "transfer"])
            
        with col2:
            description = st.text_input("Description")
            category = st.selectbox(
                "Category", 
                ["Food", "Transport", "Housing", "Utilities", "Entertainment", 
                 "Health", "Education", "Shopping", "Travel", "Other"]
            )
            
        submitted = st.form_submit_button("Add Transaction")
        
        if submitted:
            add_personal_transaction(date, description, amount, transaction_type, category)

if st.session_state.show_mpesa_form:
    st.subheader("Import M-Pesa Transactions")
    
    with st.form("mpesa_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            phone_number = st.text_input("Phone Number (2547XXXXXXXX)")
            
        with col2:
            col21, col22 = st.columns(2)
            with col21:
                start_date = st.date_input("Start Date", value=datetime.date.today() - datetime.timedelta(days=7))
            with col22:
                end_date = st.date_input("End Date", value=datetime.date.today())
        
        submitted = st.form_submit_button("Import Transactions")
        
        if submitted:
            if not phone_number:
                st.error("Please enter a phone number")
            elif not phone_number.startswith("254") or len(phone_number) != 12:
                st.error("Please enter a valid Kenyan phone number in the format 2547XXXXXXXX")
            elif end_date < start_date:
                st.error("End date must be after start date")
            else:
                import_mpesa_transactions(phone_number, start_date, end_date)

# Get and filter transactions
transactions_df = st.session_state.data_manager.get_transactions()
filtered_transactions = filter_transactions(transactions_df) if not transactions_df.empty else pd.DataFrame()

# Main content views
if st.session_state.current_view == "dashboard":
    st.title("Financial Dashboard")
    
    if transactions_df.empty:
        st.info("No transactions found. Add transactions to see your financial dashboard.")
    else:
        # Key metrics
        expense_total = filtered_transactions[filtered_transactions['type'] == 'expense']['amount'].sum()
        income_total = filtered_transactions[filtered_transactions['type'] == 'income']['amount'].sum()
        balance = income_total - expense_total
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Income", f"KSh {income_total:,.2f}")
        
        with col2:
            st.metric("Total Expenses", f"KSh {expense_total:,.2f}")
        
        with col3:
            st.metric("Balance", f"KSh {balance:,.2f}", delta=f"{balance/income_total*100:.1f}%" if income_total > 0 else "N/A")
            
        with col4:
            transaction_count = len(filtered_transactions)
            st.metric("Transactions", transaction_count)
        
        # Charts
        st.subheader("Transaction Overview")
        overview_chart = plot_transaction_overview(filtered_transactions)
        st.plotly_chart(overview_chart, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Spending by Category")
            category_chart = plot_spending_by_category(filtered_transactions)
            st.plotly_chart(category_chart, use_container_width=True)
        
        with col2:
            st.subheader("Income vs Expenses")
            income_expense_chart = plot_income_vs_expense(filtered_transactions)
            st.plotly_chart(income_expense_chart, use_container_width=True)

elif st.session_state.current_view == "transactions":
    st.title("Transaction History")
    
    if transactions_df.empty:
        st.info("No transactions found. Add transactions to see your transaction history.")
    else:
        # Display transaction table with formatting
        st.dataframe(
            filtered_transactions.sort_values('date', ascending=False)
            .style.format({
                'amount': 'KSh {:.2f}',
                'date': lambda x: x.strftime('%Y-%m-%d')
            })
            .applymap(
                lambda x: 'color: red' if x == 'expense' else 'color: green',
                subset=['type']
            ),
            use_container_width=True
        )
        
        # Export options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Export to CSV"):
                csv = filtered_transactions.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="transactions.csv",
                    mime="text/csv",
                )
                
        # Allow editing of transactions directly
        with st.expander("Edit Transaction Categories"):
            st.write("Select a transaction to update its category:")
            
            # Create a selection box of transactions
            transaction_options = filtered_transactions.apply(
                lambda row: f"{row['date'].strftime('%Y-%m-%d')} - {row['description']} (KSh {row['amount']:.2f})", 
                axis=1
            ).tolist()
            
            selected_transaction = st.selectbox("Select transaction", transaction_options)
            
            if selected_transaction:
                selected_idx = transaction_options.index(selected_transaction)
                transaction_id = filtered_transactions.iloc[selected_idx].name
                current_category = filtered_transactions.iloc[selected_idx]['category']
                
                new_category = st.selectbox(
                    "Update category",
                    ["Food", "Transport", "Housing", "Utilities", "Entertainment", 
                    "Health", "Education", "Shopping", "Travel", "Other"],
                    index=["Food", "Transport", "Housing", "Utilities", "Entertainment", 
                           "Health", "Education", "Shopping", "Travel", "Other"].index(current_category) 
                           if current_category in ["Food", "Transport", "Housing", "Utilities", "Entertainment", 
                                                 "Health", "Education", "Shopping", "Travel", "Other"] else 0
                )
                
                if st.button("Update Category"):
                    st.session_state.data_manager.update_transaction_category(transaction_id, new_category)
                    st.success(f"Updated category to {new_category}")
                    st.rerun()

elif st.session_state.current_view == "analytics":
    st.title("Financial Analytics")
    
    if transactions_df.empty:
        st.info("No transactions found. Add transactions to see your financial analytics.")
    else:
        tab1, tab2, tab3 = st.tabs(["Spending Trends", "Category Analysis", "Income Analysis"])
        
        with tab1:
            st.subheader("Monthly Spending Trends")
            trend_chart = plot_spending_trend(filtered_transactions)
            st.plotly_chart(trend_chart, use_container_width=True)
            
            # Add insights about spending trends
            if not filtered_transactions.empty:
                # Monthly average expenses
                monthly_expenses = filtered_transactions[filtered_transactions['type'] == 'expense'].copy()
                monthly_expenses['month'] = monthly_expenses['date'].dt.strftime('%Y-%m')
                monthly_avg = monthly_expenses.groupby('month')['amount'].sum().mean()
                
                # Monthly saving rate
                monthly_income = filtered_transactions[filtered_transactions['type'] == 'income'].copy()
                monthly_income['month'] = monthly_income['date'].dt.strftime('%Y-%m')
                monthly_income_avg = monthly_income.groupby('month')['amount'].sum().mean()
                
                if monthly_income_avg > 0:
                    saving_rate = (monthly_income_avg - monthly_avg) / monthly_income_avg * 100
                    st.metric("Average Monthly Saving Rate", f"{saving_rate:.1f}%")
                
                st.metric("Average Monthly Expenses", f"KSh {monthly_avg:,.2f}")
            
        with tab2:
            st.subheader("Spending by Category Analysis")
            
            # Category breakdown
            expenses_by_category = filtered_transactions[filtered_transactions['type'] == 'expense'].groupby('category')['amount'].sum().reset_index()
            
            if not expenses_by_category.empty:
                expenses_by_category = expenses_by_category.sort_values('amount', ascending=False)
                
                # Calculate percentage of total
                total_expenses = expenses_by_category['amount'].sum()
                expenses_by_category['percentage'] = (expenses_by_category['amount'] / total_expenses * 100).round(1)
                
                # Display as a table
                st.dataframe(
                    expenses_by_category.style.format({
                        'amount': 'KSh {:.2f}',
                        'percentage': '{:.1f}%'
                    }),
                    use_container_width=True
                )
                
                # Highlight top spending category
                top_category = expenses_by_category.iloc[0]['category']
                top_amount = expenses_by_category.iloc[0]['amount']
                top_percentage = expenses_by_category.iloc[0]['percentage']
                
                st.info(f"Your highest spending category is **{top_category}** at **KSh {top_amount:,.2f}** ({top_percentage}% of total expenses)")
            
        with tab3:
            st.subheader("Income Analysis")
            
            income_data = filtered_transactions[filtered_transactions['type'] == 'income']
            
            if not income_data.empty:
                # Income sources breakdown
                income_by_category = income_data.groupby('category')['amount'].sum().reset_index()
                income_by_category = income_by_category.sort_values('amount', ascending=False)
                
                # Calculate percentage of total
                total_income = income_by_category['amount'].sum()
                income_by_category['percentage'] = (income_by_category['amount'] / total_income * 100).round(1)
                
                # Display as a table
                st.dataframe(
                    income_by_category.style.format({
                        'amount': 'KSh {:.2f}',
                        'percentage': '{:.1f}%'
                    }),
                    use_container_width=True
                )
                
                # Income over time chart
                income_data['month'] = income_data['date'].dt.strftime('%Y-%m')
                income_by_month = income_data.groupby('month')['amount'].sum().reset_index()
                
                import plotly.express as px
                fig = px.line(
                    income_by_month, 
                    x='month', 
                    y='amount',
                    markers=True,
                    title="Income Trend by Month"
                )
                fig.update_layout(
                    xaxis_title="Month",
                    yaxis_title="Amount (KSh)",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No income transactions found in the selected date range.")
