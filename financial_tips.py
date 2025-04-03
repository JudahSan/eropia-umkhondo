"""
Financial Tips Module for Eropia umkhondo

This module provides contextual financial tips based on user transaction data.
Tips are categorized and selected based on spending patterns and financial behavior.
"""

import random
import pandas as pd
from datetime import datetime, timedelta

# Dictionary of financial tips categorized by topic
FINANCIAL_TIPS = {
    "general": [
        "Set clear financial goals to help guide your spending and saving decisions.",
        "Create an emergency fund that covers 3-6 months of expenses.",
        "Review your spending regularly to identify areas where you can cut back.",
        "Consider automating your savings to make it easier to save consistently.",
        "Prioritize paying off high-interest debt before focusing on other financial goals."
    ],
    "budgeting": [
        "Use the 50/30/20 rule: 50% for needs, 30% for wants, and 20% for savings.",
        "Track your expenses for a month to identify spending patterns and areas for improvement.",
        "Set realistic spending limits for discretionary categories like dining and entertainment.",
        "Review and adjust your budget regularly to ensure it remains relevant to your needs.",
        "Consider using a budgeting app or spreadsheet to make tracking easier."
    ],
    "saving": [
        "Start small if needed - even saving 5% of your income is a good beginning.",
        "Set up automatic transfers to a savings account on payday.",
        "Look for ways to increase your savings rate by 1% every few months.",
        "Consider saving windfalls like tax refunds or bonuses rather than spending them.",
        "Review your savings goals regularly and adjust as needed."
    ],
    "food": [
        "Plan your meals for the week to reduce food waste and unnecessary purchases.",
        "Cook at home more often to save on food expenses.",
        "Use a shopping list to avoid impulse buys at the grocery store.",
        "Consider buying in bulk for non-perishable items you use regularly.",
        "Look for sales and use coupons to reduce your grocery expenses."
    ],
    "transport": [
        "Consider carpooling or using public transportation to reduce transport costs.",
        "Maintain your vehicle regularly to avoid costly repairs later.",
        "Compare fuel prices and try to fill up at stations with better rates.",
        "If possible, combine errands to reduce the number of trips and save on fuel.",
        "Consider walking or cycling for short distances to save money and improve health."
    ],
    "utilities": [
        "Turn off lights and appliances when not in use to reduce electricity bills.",
        "Consider energy-efficient appliances and light bulbs to reduce utility costs.",
        "Monitor your water usage and fix leaks promptly to avoid high water bills.",
        "Adjust your thermostat by a few degrees to save on heating and cooling costs.",
        "Review your utility plans to ensure you're on the most cost-effective option."
    ],
    "high_spending": [
        "Review your recent high-expense transactions to identify areas for potential savings.",
        "Consider setting spending alerts to notify you when you exceed budget limits.",
        "Look for more affordable alternatives for products and services you use regularly.",
        "Before making large purchases, wait 24-48 hours to avoid impulse buying.",
        "Set clear spending limits for discretionary categories to curb overspending."
    ],
    "income_boost": [
        "Consider developing a side hustle to increase your income.",
        "Look for opportunities to earn passive income through investments.",
        "Develop new skills that could lead to higher-paying job opportunities.",
        "Consider selling items you no longer use to generate extra cash.",
        "Research potential tax deductions you might be eligible for."
    ],
    "debt_management": [
        "Focus on paying off high-interest debt first (debt avalanche method).",
        "Consider consolidating high-interest debts to secure a lower interest rate.",
        "Make more than the minimum payment on debts when possible.",
        "Create a debt payoff plan with specific milestones and timelines.",
        "Review your credit report regularly to ensure accuracy and address issues."
    ],
    "seasonal": [
        "Budget for expected holiday expenses well in advance.",
        "Look for off-season deals on clothing and seasonal items.",
        "Set aside funds for annual expenses like insurance premiums and taxes.",
        "Plan ahead for expensive months with birthdays or special events.",
        "Take advantage of sales during major shopping events like Black Friday."
    ]
}

def get_general_tip():
    """Return a random general financial tip.
    
    Returns:
        str: A general financial tip
    """
    return random.choice(FINANCIAL_TIPS["general"])

def get_tips_by_category(category, limit=1):
    """Get financial tips for a specific category.
    
    Args:
        category (str): The category to get tips for
        limit (int): Maximum number of tips to return
        
    Returns:
        list: List of financial tips
    """
    if category in FINANCIAL_TIPS:
        return random.sample(FINANCIAL_TIPS[category], min(limit, len(FINANCIAL_TIPS[category])))
    return [get_general_tip()]

def get_seasonal_tip():
    """Return a seasonal financial tip based on the current month.
    
    Returns:
        str: A seasonal financial tip
    """
    return random.choice(FINANCIAL_TIPS["seasonal"])

def analyze_spending_patterns(transactions_df):
    """Analyze spending patterns to identify areas for targeted tips.
    
    Args:
        transactions_df (pandas.DataFrame): Transaction data
        
    Returns:
        dict: Analysis results with relevant categories for tips
    """
    if transactions_df is None or transactions_df.empty:
        return {"categories": ["general", "budgeting"], "has_data": False}
    
    result = {"categories": [], "has_data": True}
    
    # Filter for expenses only
    expenses_df = transactions_df[transactions_df["type"] == "expense"]
    if expenses_df.empty:
        return {"categories": ["general", "saving"], "has_data": False}
    
    # Analyze spending by category
    category_spending = expenses_df.groupby("category")["amount"].sum()
    
    # Check if there's enough historical data
    earliest_date = transactions_df["date"].min()
    latest_date = transactions_df["date"].max()
    if earliest_date and latest_date:
        date_range = (latest_date - earliest_date).days
        if date_range < 7:
            # Not enough historical data
            return {"categories": ["general", "budgeting"], "has_data": False}
    
    # Add specific categories based on spending patterns
    if not category_spending.empty:
        # Find top spending categories
        top_categories = category_spending.nlargest(2).index.tolist()
        
        # Add relevant tips for top categories
        for category in top_categories:
            if category.lower() == "food":
                result["categories"].append("food")
            elif category.lower() in ["transport", "transportation"]:
                result["categories"].append("transport")
            elif category.lower() in ["utilities", "bills"]:
                result["categories"].append("utilities")
        
        # Check for high spending
        if len(expenses_df) > 5:
            result["high_spending"] = True
            result["categories"].append("high_spending")
    
    # Add basic categories if we don't have enough
    if len(result["categories"]) < 2:
        if "general" not in result["categories"]:
            result["categories"].append("general")
        if "budgeting" not in result["categories"]:
            result["categories"].append("budgeting")
    
    # Add seasonal tip
    result["categories"].append("seasonal")
    
    return result

def get_contextual_tips(transactions_df, limit=3):
    """Get contextual financial tips based on transaction data.
    
    Args:
        transactions_df (pandas.DataFrame): Transaction data
        limit (int): Maximum number of tips to return
        
    Returns:
        list: List of contextual financial tips
    """
    analysis = analyze_spending_patterns(transactions_df)
    
    tips = []
    categories = analysis.get("categories", ["general", "budgeting"])
    
    # Ensure we don't exceed available categories
    num_categories = min(limit, len(categories))
    
    # Get tips from each category
    for i in range(num_categories):
        category = categories[i]
        category_tips = get_tips_by_category(category, 1)
        tips.extend(category_tips)
    
    # If we still need more tips, add general ones
    while len(tips) < limit:
        general_tip = get_general_tip()
        if general_tip not in tips:
            tips.append(general_tip)
    
    return tips

def get_tip_of_the_day(transactions_df=None):
    """Get the financial tip of the day.
    
    Args:
        transactions_df (pandas.DataFrame, optional): Transaction data
        
    Returns:
        str: Financial tip of the day
    """
    if transactions_df is not None and not transactions_df.empty:
        # Get a contextual tip based on transaction data
        tips = get_contextual_tips(transactions_df, 1)
        if tips:
            return tips[0]
    
    # Default to a general tip if no transaction data
    return get_general_tip()