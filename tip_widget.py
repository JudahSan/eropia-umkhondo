"""
Tip Widget Module for Eropia umkhondo

This module provides UI components for displaying financial tips in a popup widget.
"""

import streamlit as st
from financial_tips import get_contextual_tips, get_tip_of_the_day
import pandas as pd

def initialize_tip_state():
    """Initialize session state variables for tip widget"""
    if "show_tip_widget" not in st.session_state:
        st.session_state.show_tip_widget = False
    if "tip_of_the_day" not in st.session_state:
        st.session_state.tip_of_the_day = None
    if "contextual_tips" not in st.session_state:
        st.session_state.contextual_tips = []
    if "current_tip_index" not in st.session_state:
        st.session_state.current_tip_index = 0
    if "tip_widget_initialized" not in st.session_state:
        st.session_state.tip_widget_initialized = False

def toggle_tip_widget():
    """Toggle the visibility of the tip widget"""
    st.session_state.show_tip_widget = not st.session_state.show_tip_widget

def next_tip():
    """Show the next tip in the list"""
    if len(st.session_state.contextual_tips) > 0:
        st.session_state.current_tip_index = (st.session_state.current_tip_index + 1) % len(st.session_state.contextual_tips)

def previous_tip():
    """Show the previous tip in the list"""
    if len(st.session_state.contextual_tips) > 0:
        st.session_state.current_tip_index = (st.session_state.current_tip_index - 1) % len(st.session_state.contextual_tips)

def load_tips(transactions_df=None):
    """Load financial tips based on transaction data
    
    Args:
        transactions_df (pandas.DataFrame, optional): Transaction data
    """
    # Get tip of the day
    st.session_state.tip_of_the_day = get_tip_of_the_day(transactions_df)
    
    # Get contextual tips (more than one for navigation)
    st.session_state.contextual_tips = get_contextual_tips(transactions_df, 5)
    
    # Reset tip index
    st.session_state.current_tip_index = 0
    
    # Mark as initialized
    st.session_state.tip_widget_initialized = True

def tip_widget_button(location="sidebar"):
    """Display a button to toggle the tip widget
    
    Args:
        location (str): Where to display the button ("sidebar" or "main")
    """
    # Initialize state if needed
    initialize_tip_state()
    
    # Create the button
    if location == "sidebar":
        with st.sidebar:
            st.button(
                "💡 Financial Tips", 
                on_click=toggle_tip_widget,
                help="Show or hide financial tips based on your spending patterns",
                use_container_width=True
            )
    else:
        st.button(
            "💡 Financial Tips", 
            on_click=toggle_tip_widget,
            help="Show or hide financial tips based on your spending patterns",
            use_container_width=False
        )

def display_tip_widget(transactions_df=None):
    """Display the financial tips popup widget
    
    Args:
        transactions_df (pandas.DataFrame, optional): Transaction data
    """
    # Initialize state if needed
    initialize_tip_state()
    
    # Load tips if not already initialized or if we have new transaction data
    if not st.session_state.tip_widget_initialized or transactions_df is not None:
        load_tips(transactions_df)
    
    # Only display if session state shows it should be visible
    if st.session_state.show_tip_widget:
        # Create a container for the popup
        with st.container():
            # Create a styled box for the popup
            st.markdown("""
            <style>
            .tip-container {
                background-color: #f0f8ff;
                border-radius: 10px;
                padding: 20px;
                border-left: 5px solid #4682b4;
                margin: 10px 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .tip-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }
            .tip-title {
                color: #4682b4;
                margin: 0;
                font-weight: bold;
            }
            .tip-content {
                font-size: 1.1em;
                line-height: 1.5;
                color: #2c3e50;
            }
            </style>
            <div class="tip-container">
                <div class="tip-header">
                    <h3 class="tip-title">Financial Tip</h3>
                </div>
                <p class="tip-content">
                    {tip}
                </p>
            </div>
            """.format(
                tip=st.session_state.contextual_tips[st.session_state.current_tip_index] 
                    if st.session_state.contextual_tips 
                    else st.session_state.tip_of_the_day or "Set clear financial goals to help guide your spending decisions."
            ), unsafe_allow_html=True)
            
            # Navigation buttons
            if len(st.session_state.contextual_tips) > 1:
                cols = st.columns([1, 1, 4, 1])
                with cols[0]:
                    st.button("⬅️", key="prev_tip_btn", on_click=previous_tip)
                with cols[1]:
                    st.button("➡️", key="next_tip_btn", on_click=next_tip)
                with cols[3]:
                    st.button("✖️", key="close_tip_btn", on_click=toggle_tip_widget)
            else:
                cols = st.columns([6, 1])
                with cols[1]:
                    st.button("✖️", key="close_tip_btn_single", on_click=toggle_tip_widget)