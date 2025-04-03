import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
import json

from auth_manager import AuthManager
from data_manager import DataManager
from budget_manager import BudgetManager
from utils import format_currency


def app():
    """Budget planning and tracking application"""
    
    # Initialize managers with user's username from session state
    auth_manager = AuthManager()
    username = st.session_state.get('username', None)
    
    if not username:
        st.warning("Please login to access the budget planning features.")
        return
    
    data_manager = DataManager(username)
    budget_manager = BudgetManager(username)
    
    # Set up the page
    st.title("Budget Planner")
    
    # Create tabs for different budget functions
    tab1, tab2, tab3 = st.tabs(["Budget Overview", "Manage Budgets", "Budget vs. Actual"])
    
    with tab1:
        display_budget_overview(budget_manager, data_manager)
    
    with tab2:
        manage_budgets(budget_manager)
    
    with tab3:
        budget_vs_actual(budget_manager, data_manager)


def display_budget_overview(budget_manager, data_manager):
    """Display budget overview dashboard"""
    st.header("Budget Overview")
    
    # Get active budgets
    active_budgets = budget_manager.get_active_budgets()
    
    if active_budgets.empty:
        st.info("You don't have any active budgets. Go to the 'Manage Budgets' tab to create your first budget.")
        return
    
    # Calculate budget progress
    progress_df = budget_manager.calculate_budget_progress(data_manager)
    
    if progress_df.empty:
        st.info("No budget progress data available.")
        return
    
    # Show key metrics
    total_budget = progress_df['budget_amount'].sum()
    total_spent = progress_df['actual_amount'].sum()
    total_remaining = progress_df['remaining'].sum()
    avg_pct_used = progress_df['percentage_used'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Budget", format_currency(total_budget))
    col2.metric("Total Spent", format_currency(total_spent))
    col3.metric("Remaining", format_currency(total_remaining))
    col4.metric("Average Used", f"{avg_pct_used:.1f}%")
    
    # Create a visualization of budget progress
    st.subheader("Budget Progress by Category")
    
    # Prepare data for visualization
    progress_df = progress_df.sort_values(by='percentage_used', ascending=False)
    
    # Bar chart of budget vs. actual per category
    fig = go.Figure()
    
    # Add bars for budget amount
    fig.add_trace(go.Bar(
        x=progress_df['category'],
        y=progress_df['budget_amount'],
        name='Budget',
        marker_color='lightblue'
    ))
    
    # Add bars for actual amount
    fig.add_trace(go.Bar(
        x=progress_df['category'],
        y=progress_df['actual_amount'],
        name='Actual Spending',
        marker_color='coral'
    ))
    
    # Update layout
    fig.update_layout(
        title='Budget vs. Actual by Category',
        xaxis_title='Category',
        yaxis_title='Amount (KSh)',
        barmode='group',
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Progress bars for each category
    st.subheader("Budget Utilization")
    
    # Create a progress bar for each category
    for _, row in progress_df.iterrows():
        col1, col2 = st.columns([3, 1])
        
        # Calculate percentage capped at 100%
        pct = min(row['percentage_used'], 100)
        
        # Determine color based on percentage
        color = 'green'
        if pct > 75:
            color = 'orange'
        if pct > 90:
            color = 'red'
        
        with col1:
            st.markdown(f"**{row['category']}** ({format_currency(row['actual_amount'])} of {format_currency(row['budget_amount'])})")
            st.progress(int(pct)/100)
        
        with col2:
            st.markdown(f"<h3 style='color:{color};text-align:center;'>{pct:.1f}%</h3>", unsafe_allow_html=True)
            
        st.write("---")


def manage_budgets(budget_manager):
    """Interface for creating, updating, and deleting budgets"""
    st.header("Manage Budgets")
    
    # Get existing budgets
    budgets = budget_manager.get_budgets()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Current Budgets")
        
        if budgets.empty:
            st.info("You don't have any budgets yet. Use the form to create your first budget.")
        else:
            # Display budgets in a dataframe
            display_df = budgets.copy()
            
            # Format dates for display
            display_df['start_date'] = display_df['start_date'].dt.strftime('%Y-%m-%d')
            display_df['end_date'] = display_df['end_date'].dt.strftime('%Y-%m-%d')
            
            # Drop the timestamp columns
            display_df = display_df.drop(columns=['created_at', 'modified_at'])
            
            # Show the dataframe
            st.dataframe(display_df, use_container_width=True)
            
            # Budget management actions
            st.subheader("Budget Actions")
            
            # Select a budget to modify or delete
            budget_options = budgets['category'].tolist()
            budget_index = st.selectbox("Select a budget to modify or delete:", 
                                       range(len(budget_options)), 
                                       format_func=lambda x: budget_options[x])
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Delete Selected Budget", type="primary", use_container_width=True):
                    try:
                        budget_manager.delete_budget(budget_index)
                        st.success(f"Budget for '{budget_options[budget_index]}' has been deleted.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting budget: {str(e)}")
    
    with col2:
        st.subheader("Add New Budget")
        
        # Form for adding a new budget
        with st.form("add_budget_form"):
            # Get unique categories from existing transactions
            default_categories = ['Food', 'Transportation', 'Housing', 'Utilities', 'Entertainment', 'Healthcare', 'Savings', 'Other']
            
            # Create budget form
            category = st.text_input("Budget Category", help="Enter a category for your budget")
            amount = st.number_input("Budget Amount (KSh)", min_value=0.0, help="Enter the budget amount")
            
            period = st.selectbox("Budget Period", 
                                 options=["weekly", "monthly", "yearly"],
                                 index=1,  # Default to monthly
                                 help="Select the period for this budget")
            
            start_date = st.date_input("Start Date", value=date.today(), help="When does this budget start?")
            
            # Calculate default end date based on period
            default_end_date = None
            if period == "weekly":
                from datetime import timedelta
                default_end_date = start_date + timedelta(days=7)
            elif period == "monthly":
                # Simple approximation for one month later
                year = start_date.year + (start_date.month == 12)
                month = (start_date.month % 12) + 1
                default_end_date = date(year, month, min(start_date.day, 28))
            elif period == "yearly":
                default_end_date = date(start_date.year + 1, start_date.month, start_date.day)
            
            end_date = st.date_input("End Date", value=default_end_date, help="When does this budget end?")
            
            # Submit button
            submitted = st.form_submit_button("Add Budget", type="primary", use_container_width=True)
            
            if submitted:
                if not category:
                    st.error("Please enter a category name.")
                elif amount <= 0:
                    st.error("Please enter an amount greater than zero.")
                elif end_date <= start_date:
                    st.error("End date must be after start date.")
                else:
                    try:
                        # Create budget dictionary
                        budget_item = {
                            'category': category,
                            'amount': amount,
                            'period': period,
                            'start_date': start_date,
                            'end_date': end_date
                        }
                        
                        # Add to budget manager
                        budget_manager.add_budget(budget_item)
                        st.success(f"Budget for '{category}' has been added!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding budget: {str(e)}")


def budget_vs_actual(budget_manager, data_manager):
    """Compare budget vs actual spending over time"""
    st.header("Budget vs. Actual")
    
    # Get active budgets
    active_budgets = budget_manager.get_active_budgets()
    
    if active_budgets.empty:
        st.info("You don't have any active budgets. Go to the 'Manage Budgets' tab to create your first budget.")
        return
    
    # Calculate budget progress
    progress_df = budget_manager.calculate_budget_progress(data_manager)
    
    if progress_df.empty:
        st.info("No budget progress data available.")
        return
    
    # Visualization options
    viz_type = st.radio("Visualization Type:", ["Bar Chart", "Pie Chart", "Budget Status"], horizontal=True)
    
    if viz_type == "Bar Chart":
        # Bar chart comparing budget vs actual
        fig = px.bar(
            progress_df,
            x="category",
            y=["budget_amount", "actual_amount"],
            barmode="group",
            labels={
                "value": "Amount (KSh)",
                "category": "Budget Category",
                "variable": "Type"
            },
            title="Budget vs. Actual Spending by Category",
            color_discrete_map={
                "budget_amount": "royalblue",
                "actual_amount": "firebrick"
            },
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
    elif viz_type == "Pie Chart":
        # Create two columns for the pie charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart of budget allocation
            fig1 = px.pie(
                progress_df,
                values="budget_amount",
                names="category",
                title="Budget Allocation",
                height=400
            )
            st.plotly_chart(fig1, use_container_width=True)
            
        with col2:
            # Pie chart of actual spending
            fig2 = px.pie(
                progress_df,
                values="actual_amount",
                names="category",
                title="Actual Spending",
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)
            
    else:  # Budget Status
        # Create a dataframe for the status
        status_df = progress_df.copy()
        
        # Add status column
        def determine_status(row):
            pct = row['percentage_used']
            if pct < 50:
                return "Good"
            elif pct < 80:
                return "Watch"
            elif pct < 100:
                return "Warning"
            else:
                return "Over Budget"
        
        status_df['status'] = status_df.apply(determine_status, axis=1)
        
        # Create a styled dataframe
        st.dataframe(
            status_df[['category', 'budget_amount', 'actual_amount', 'remaining', 'percentage_used', 'status']],
            column_config={
                "category": "Category",
                "budget_amount": st.column_config.NumberColumn("Budget", format="₹%.2f"),
                "actual_amount": st.column_config.NumberColumn("Spent", format="₹%.2f"),
                "remaining": st.column_config.NumberColumn("Remaining", format="₹%.2f"),
                "percentage_used": st.column_config.ProgressColumn("% Used", format="%.1f%%", min_value=0, max_value=100),
                "status": st.column_config.TextColumn("Status"),
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Summary statistics
        st.subheader("Budget Summary")
        
        # Count budgets by status
        status_counts = status_df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        # Create horizontal bar chart
        fig = px.bar(
            status_counts,
            y='Status',
            x='Count',
            color='Status',
            orientation='h',
            title="Budget Status Summary",
            color_discrete_map={
                "Good": "green",
                "Watch": "blue", 
                "Warning": "orange",
                "Over Budget": "red"
            },
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    app()