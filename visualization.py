import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

def plot_transaction_overview(df):
    """Create a transaction overview chart
    
    Args:
        df (pandas.DataFrame): Transaction data
        
    Returns:
        plotly.graph_objects.Figure: Transaction overview chart
    """
    if df.empty:
        # Return empty figure if no data
        fig = go.Figure()
        fig.update_layout(
            title="No transaction data available",
            xaxis_title="Date",
            yaxis_title="Amount"
        )
        return fig
    
    # Create copy of dataframe to avoid modifying original
    chart_df = df.copy()
    
    # Add sign to amount based on transaction type
    chart_df['signed_amount'] = chart_df.apply(
        lambda row: row['amount'] if row['type'] == 'income' else -row['amount'], 
        axis=1
    )
    
    # Group by date and calculate daily totals
    daily_totals = chart_df.groupby('date')['signed_amount'].sum().reset_index()
    
    # Calculate running balance
    daily_totals['balance'] = daily_totals['signed_amount'].cumsum()
    
    # Create figure with two y-axes
    fig = go.Figure()
    
    # Add bars for daily transactions
    fig.add_trace(
        go.Bar(
            x=daily_totals['date'],
            y=daily_totals['signed_amount'],
            name="Daily Net",
            marker_color=daily_totals['signed_amount'].apply(
                lambda x: 'green' if x >= 0 else 'red'
            )
        )
    )
    
    # Add line for running balance
    fig.add_trace(
        go.Scatter(
            x=daily_totals['date'],
            y=daily_totals['balance'],
            name="Running Balance",
            line=dict(color='royalblue', width=3),
            yaxis="y2"
        )
    )
    
    # Update layout with second y-axis
    fig.update_layout(
        title="Transaction Overview and Running Balance",
        xaxis_title="Date",
        yaxis_title="Daily Net (KSh)",
        yaxis2=dict(
            title="Running Balance (KSh)",
            titlefont=dict(color="royalblue"),
            tickfont=dict(color="royalblue"),
            overlaying="y",
            side="right"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def plot_spending_by_category(df):
    """Create a pie chart of spending by category
    
    Args:
        df (pandas.DataFrame): Transaction data
        
    Returns:
        plotly.graph_objects.Figure: Spending by category chart
    """
    if df.empty or 'expense' not in df['type'].values:
        # Return empty figure if no expense data
        fig = go.Figure()
        fig.update_layout(
            title="No expense data available",
        )
        return fig
    
    # Filter for expenses only
    expenses_df = df[df['type'] == 'expense']
    
    # Group by category and sum
    category_totals = expenses_df.groupby('category')['amount'].sum().reset_index()
    
    # Create pie chart
    fig = px.pie(
        category_totals, 
        values='amount', 
        names='category',
        title="Spending by Category",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Update layout
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Amount: KSh %{value:.2f}<br>Percentage: %{percent}'
    )
    
    return fig

def plot_spending_trend(df):
    """Create a line chart showing spending trends over time
    
    Args:
        df (pandas.DataFrame): Transaction data
        
    Returns:
        plotly.graph_objects.Figure: Spending trend chart
    """
    if df.empty or 'expense' not in df['type'].values:
        # Return empty figure if no expense data
        fig = go.Figure()
        fig.update_layout(
            title="No expense data available for trend analysis",
            xaxis_title="Date",
            yaxis_title="Amount"
        )
        return fig
    
    # Filter for expenses only
    expenses_df = df[df['type'] == 'expense'].copy()
    
    # Add month column for grouping
    expenses_df['month'] = expenses_df['date'].dt.strftime('%Y-%m')
    
    # Group by month and category
    monthly_by_category = expenses_df.groupby(['month', 'category'])['amount'].sum().reset_index()
    
    # Create line chart
    fig = px.line(
        monthly_by_category,
        x='month',
        y='amount',
        color='category',
        markers=True,
        title="Monthly Spending by Category",
        labels={'month': 'Month', 'amount': 'Amount (KSh)', 'category': 'Category'}
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount (KSh)",
        legend_title="Category",
        hovermode="x unified"
    )
    
    return fig

def plot_income_vs_expense(df):
    """Create a bar chart comparing income vs expenses
    
    Args:
        df (pandas.DataFrame): Transaction data
        
    Returns:
        plotly.graph_objects.Figure: Income vs Expense chart
    """
    if df.empty:
        # Return empty figure if no data
        fig = go.Figure()
        fig.update_layout(
            title="No transaction data available",
            xaxis_title="Month",
            yaxis_title="Amount"
        )
        return fig
    
    # Create copy of dataframe to avoid modifying original
    chart_df = df.copy()
    
    # Add month column for grouping
    chart_df['month'] = chart_df['date'].dt.strftime('%Y-%m')
    
    # Group by month and transaction type
    monthly_totals = chart_df.groupby(['month', 'type'])['amount'].sum().reset_index()
    
    # Filter to keep only income and expense
    monthly_totals = monthly_totals[monthly_totals['type'].isin(['income', 'expense'])]
    
    # Pivot the data
    pivot_df = monthly_totals.pivot(index='month', columns='type', values='amount').reset_index()
    
    # Fill NaN values with 0
    if 'income' not in pivot_df.columns:
        pivot_df['income'] = 0
    if 'expense' not in pivot_df.columns:
        pivot_df['expense'] = 0
    
    # Calculate net (income - expense)
    pivot_df['net'] = pivot_df['income'] - pivot_df['expense']
    
    # Create the figure
    fig = go.Figure()
    
    # Add income bars
    fig.add_trace(
        go.Bar(
            x=pivot_df['month'],
            y=pivot_df['income'],
            name="Income",
            marker_color='green'
        )
    )
    
    # Add expense bars
    fig.add_trace(
        go.Bar(
            x=pivot_df['month'],
            y=pivot_df['expense'],
            name="Expense",
            marker_color='red'
        )
    )
    
    # Add net line
    fig.add_trace(
        go.Scatter(
            x=pivot_df['month'],
            y=pivot_df['net'],
            name="Net",
            line=dict(color='blue', width=3),
            mode='lines+markers'
        )
    )
    
    # Update layout
    fig.update_layout(
        title="Monthly Income vs Expenses",
        xaxis_title="Month",
        yaxis_title="Amount (KSh)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        barmode='group'
    )
    
    return fig
