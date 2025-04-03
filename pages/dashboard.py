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
import os
from mpesa_api import MPesaAPI
from typing import List, Dict, Any, Union, Optional

def app():
    # Custom CSS for better mobile responsiveness
    st.markdown("""
    <style>
    .block-container {
        max-width: 95%;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Responsive adjustments for mobile */
    @media (max-width: 768px) {
        .block-container {
            padding: 0.5rem;
        }
        h1 {
            font-size: 1.8rem !important;
            margin-bottom: 0.5rem !important;
        }
        h2 {
            font-size: 1.5rem !important;
        }
        h3 {
            font-size: 1.2rem !important;
        }
        .stButton>button {
            width: 100%;
        }
        /* Stack columns on mobile */
        .row-widget.stHorizontal {
            flex-wrap: wrap;
        }
        /* Make metric cards stack better */
        [data-testid="stMetricValue"] {
            font-size: 1rem !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
        }
        /* Adjust dataframe for mobile */
        .stDataFrame {
            overflow-x: auto;
        }
        /* Better expander styling for mobile */
        .streamlit-expanderHeader {
            font-size: 1rem !important;
        }
    }
    
    /* Form styling and improvements */
    .stForm {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    /* Improved tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        overflow-x: auto;
    }
    
    .stTabs [data-baseweb="tab"] {
        white-space: nowrap;
        font-size: 0.8rem;
        padding: 0.5rem 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

    if "username" not in st.session_state:
        st.warning("Please log in to access your dashboard.")
        st.session_state.current_page = "login"
        st.rerun()
        return
    
    username = st.session_state.username
    
    st.title(f"Financial Dashboard")
    st.caption(f"Welcome, {username}")
    
    # Initialize the data manager with the user's data
    data_manager = DataManager(username=username)
    data_manager.ensure_data_file_exists()
    
    # Get all transactions
    transactions_df = data_manager.get_transactions()
    
    # Add Transaction section
    st.subheader("Add Transaction")
    
    # Transaction input tabs for better mobile experience
    transaction_tab1, transaction_tab2 = st.tabs(["Add Manual Transaction", "Import M-Pesa Transactions"])
    
    with transaction_tab1:
        with st.form("add_transaction_form"):
            # Use full width for inputs on mobile
            transaction_date = st.date_input("Date", value=datetime.now())
            description = st.text_input("Description", placeholder="What was this transaction for?")
            amount = st.number_input("Amount (KSh)", min_value=0.0, step=100.0)
            transaction_type = st.selectbox("Type", ["expense", "income"])
            
            # Simplified category list with common categories first
            category_options = ["Food", "Transport", "Housing", "Entertainment", "Utilities", 
                               "Healthcare", "Education", "Shopping", "Salary", "Investment", 
                               "Gift", "Other"]
            category = st.selectbox("Category", category_options)
            
            submitted = st.form_submit_button("Add Transaction", use_container_width=True)
            
            if submitted:
                # Validate input
                if description.strip() == "":
                    st.error("Please add a description for the transaction")
                elif amount <= 0:
                    st.error("Amount must be greater than zero")
                else:
                    new_transaction = {
                        "date": transaction_date,
                        "description": description,
                        "amount": float(amount),
                        "type": transaction_type,
                        "category": category
                    }
                    
                    success = data_manager.add_transaction(new_transaction)
                    
                    if success:
                        st.success("Transaction added successfully!")
                        # Refresh the page to show the new transaction
                        st.rerun()
                    else:
                        st.error("Failed to add transaction. Please try again.")
    
    # M-Pesa Integration Section
    with transaction_tab2:
        st.write("Import your M-Pesa transactions directly from Safaricom.")
        
        # Check if M-Pesa API credentials are set
        mpesa_credentials_set = os.getenv("MPESA_CONSUMER_KEY") and os.getenv("MPESA_CONSUMER_SECRET")
        
        if not mpesa_credentials_set:
            st.warning("""
            M-Pesa API credentials not set. To use this feature, you need to set the following environment variables:
            
            - MPESA_CONSUMER_KEY: Your M-Pesa API consumer key
            - MPESA_CONSUMER_SECRET: Your M-Pesa API consumer secret
            - MPESA_API_URL (optional): API URL (defaults to sandbox)
            
            Contact your administrator to set up these credentials.
            """)
        else:
            from auth_manager import AuthManager
            auth_manager = AuthManager()
            mpesa_api = MPesaAPI(username=username, auth_manager=auth_manager)
            
            with st.form("import_mpesa_form"):
                import_start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
                import_end_date = st.date_input("End Date", value=datetime.now())
                
                import_submitted = st.form_submit_button("Import Transactions", use_container_width=True)
                
                if import_submitted:
                    try:
                        # Get user's phone number
                        phone_number = auth_manager.get_user_phone_number(username)
                        
                        if not phone_number:
                            st.error("Phone number not found in your profile. Please update your profile with a valid phone number.")
                        else:
                            with st.spinner("Fetching M-Pesa transactions..."):
                                # This would call the M-Pesa API in a real implementation
                                transactions = mpesa_api.get_transactions(phone_number, import_start_date, import_end_date)
                                
                                # Add the transactions to the data store
                                if transactions:
                                    success_count = 0
                                    for transaction in transactions:
                                        if data_manager.add_transaction(transaction):
                                            success_count += 1
                                    
                                    st.success(f"Successfully imported {success_count} transactions!")
                                    st.rerun()
                                else:
                                    st.info("No transactions found for the selected date range.")
                    except ValueError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
    
    st.write("---")
    
    if transactions_df.empty:
        st.info("No transactions found. Add some transactions above to see your financial insights.")
        # Add budget planner link even if no transactions
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("📊 Budget Planner", key="go_to_budget_btn_empty", help="Go to Budget Planner"):
                st.session_state.current_page = "budget"
                st.rerun()
        return

    # Financial Overview Section with Budget Link
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Financial Overview")
    with col2:
        if st.button("📊 Budget Planner", key="go_to_budget_btn", help="Go to Budget Planner"):
            st.session_state.current_page = "budget"
            st.rerun()
    
    # Dashboard metrics - make more mobile friendly
    # Use different column ratios for better mobile display
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Calculate total income and expenses
    income = transactions_df[transactions_df['type'] == 'income']['amount'].sum()
    expenses = transactions_df[transactions_df['type'] == 'expense']['amount'].sum()
    balance = income - expenses
    
    # Display metrics with improved formatting
    with col1:
        st.metric(label="Total Income", value=f"KSh {income:,.0f}", delta=None)
    
    with col2:
        st.metric(label="Total Expenses", value=f"KSh {expenses:,.0f}", delta=None)
    
    with col3:
        delta = None
        if balance > 0:
            delta = f"+KSh {balance:,.0f}"
        elif balance < 0:
            delta = f"-KSh {abs(balance):,.0f}"
            
        st.metric(label="Balance", value=f"KSh {balance:,.0f}", delta=delta)
    
    st.write("---")
    
    # Filtering options - simplified for mobile
    st.subheader("Filter Transactions")
    
    # Use responsive layout for filters
    with st.container():
        # Date range filter - first row for dates
        default_start_date = datetime.now() - timedelta(days=30)
        default_end_date = datetime.now()
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=default_start_date)
        with col2:
            end_date = st.date_input("End Date", value=default_end_date)
        
        # Second row for category and type
        col1, col2 = st.columns(2)
        with col1:
            # Category filter
            categories = ["All"] + sorted(transactions_df['category'].unique().tolist())
            selected_category = st.selectbox("Category", categories)
        with col2:
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
    
    # Visualizations - with more compact layout
    st.subheader("Financial Insights")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "By Category", "Monthly", "Income/Expense"])
    
    with tab1:
        st.plotly_chart(plot_transaction_overview(filtered_df), use_container_width=True, config={"displayModeBar": False})
    
    with tab2:
        st.plotly_chart(plot_spending_by_category(filtered_df), use_container_width=True, config={"displayModeBar": False})
    
    with tab3:
        st.plotly_chart(plot_spending_trend(filtered_df), use_container_width=True, config={"displayModeBar": False})
    
    with tab4:
        st.plotly_chart(plot_income_vs_expense(filtered_df), use_container_width=True, config={"displayModeBar": False})
    
    st.write("---")
    
    # Transactions table - more mobile friendly
    st.subheader("Transaction History")
    
    if not filtered_df.empty:
        # Convert date to string for display
        display_df = filtered_df.copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        
        # Format amount for display
        display_df['amount'] = display_df['amount'].apply(lambda x: f"KSh {x:,.0f}")
        
        # Customize columns and order - simplified for mobile
        display_df = display_df[['date', 'description', 'amount', 'type', 'category']]
        display_df.columns = ['Date', 'Description', 'Amount', 'Type', 'Category']
        
        # More mobile-friendly dataframe with limited height
        st.dataframe(
            display_df, 
            use_container_width=True,
            height=300
        )
    else:
        st.info("No transactions match your filters.")

if __name__ == "__main__":
    app()