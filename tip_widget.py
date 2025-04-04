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
        st.session_state.current_tip_index = (
            st.session_state.current_tip_index + 1) % len(st.session_state.contextual_tips)


def previous_tip():
    """Show the previous tip in the list"""
    if len(st.session_state.contextual_tips) > 0:
        st.session_state.current_tip_index = (
            st.session_state.current_tip_index - 1) % len(st.session_state.contextual_tips)


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

    # Create custom styled button
    button_style = """
    <style>
    .tip-widget-button {
        background-color: #4682b4;
        color: white;
        padding: 10px 15px;
        border-radius: 8px;
        text-align: center;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        margin: 10px 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .tip-widget-button:hover {
        background-color: #36648b;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        transform: translateY(-2px);
    }
    .tip-widget-icon {
        font-size: 1.2em;
        margin-right: 8px;
    }
    .sidebar .tip-widget-button {
        width: 100%;
    }
    </style>
    """

    # Create the button with JavaScript for click handling
    button_html = f"""
    <div class="tip-widget-button" id="tip-button" onclick="toggleTip()">
        <span class="tip-widget-icon">💡</span> Financial Tips
    </div>
    
    <script>
    function toggleTip() {{
        // Use Streamlit's API to run the Python function
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: true,
            dataType: 'jsonString', 
            componentId: 'toggle_tip'
        }}, '*');
    }}
    </script>
    """

    # Create a container for the button
    if location == "sidebar":
        with st.sidebar:
            # Add a hidden component to capture the click
            if st.session_state.get('toggle_tip', False):
                toggle_tip_widget()
                st.session_state['toggle_tip'] = False

            # Display the regular button as fallback
            st.button(
                "💡 Financial Tips",
                on_click=toggle_tip_widget,
                help="Show or hide financial tips based on your spending patterns",
                use_container_width=True,
                key="tip_button_sidebar"
            )

            # Add styling to make the button stand out
            st.markdown("""
            <style>
            [data-testid="stButton"] button {
                background-color: #4682b4;
                color: white;
            }
            [data-testid="stButton"] button:hover {
                background-color: #36648b;
                border-color: #36648b;
            }
            </style>
            """, unsafe_allow_html=True)
    else:
        # Add a hidden component to capture the click
        if st.session_state.get('toggle_tip', False):
            toggle_tip_widget()
            st.session_state['toggle_tip'] = False

        # Display the regular button as fallback for main area
        st.button(
            "💡 Financial Tips",
            on_click=toggle_tip_widget,
            help="Show or hide financial tips based on your spending patterns",
            use_container_width=False,
            key="tip_button_main"
        )

        # Add styling for the main button
        st.markdown("""
        <style>
        [data-testid="stButton"] button {
            background-color: #4682b4;
            color: white;
        }
        [data-testid="stButton"] button:hover {
            background-color: #36648b;
            border-color: #36648b;
        }
        </style>
        """, unsafe_allow_html=True)


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
            # Create a styled box for the popup with improved design and contextual indicator
            tip_content = st.session_state.contextual_tips[st.session_state.current_tip_index] if st.session_state.contextual_tips else st.session_state.tip_of_the_day or "Set clear financial goals to help guide your spending decisions."

            # Determine if tip is contextual based on transaction data
            is_contextual = transactions_df is not None and not transactions_df.empty
            contextual_badge = """<span style="background-color: #4682b4; color: white; padding: 3px 8px; border-radius: 10px; font-size: 0.7em; margin-left: 10px;">Personalized</span>""" if is_contextual else ""

            # Apply CSS for the tip widget
            st.markdown("""
            <style>
            .tip-container {
                background-color: #f0f8ff;
                border-radius: 12px;
                padding: 20px;
                border-left: 5px solid #4682b4;
                margin: 15px auto; /* Center the card */
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
                position: relative;
                overflow: hidden;
                max-width: 600px; /* Make the card smaller */
            }
            .tip-container::before {
                content: '';
                position: absolute;
                top: 0;
                right: 0;
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, transparent 50%, rgba(70, 130, 180, 0.1) 50%);
            }
            .tip-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                border-bottom: 1px solid rgba(70, 130, 180, 0.2);
                padding-bottom: 10px;
            }
            .tip-title {
                color: #4682b4;
                margin: 0;
                font-weight: bold;
                display: flex;
                align-items: center;
            }
            .tip-icon {
                margin-right: 8px;
                font-size: 1.3em;
            }
            .tip-content {
                font-size: 1.1em;
                line-height: 1.6;
                color: #2c3e50;
                padding: 5px 0;
            }
            .tip-footer {
                font-size: 0.85em;
                color: #4682b4;
                font-style: italic;
                margin-top: 10px;
                text-align: right;
            }
            </style>
            """, unsafe_allow_html=True)

            # Create the tip content HTML
            tip_html = f"""
            <div class="tip-container">
                <div class="tip-header">
                    <h3 class="tip-title">
                        <span class="tip-icon">💡</span> Financial Tip {contextual_badge}
                    </h3>
                </div>
                <p class="tip-content">
                    {tip_content}
                </p>
                <p class="tip-footer">
                    Tip {st.session_state.current_tip_index + 1}/{len(st.session_state.contextual_tips) if st.session_state.contextual_tips else 1}
                </p>
            </div>
            """
            st.markdown(tip_html, unsafe_allow_html=True)

            # Improved navigation buttons with updated icons
            if len(st.session_state.contextual_tips) > 1:
                cols = st.columns([1, 1, 3, 1, 1])
                with cols[0]:
                    st.button("⬅️ Previous", key="prev_tip_btn",
                              on_click=previous_tip, help="Previous tip")
                with cols[1]:
                    st.button("➡️ Next", key="next_tip_btn",
                              on_click=next_tip, help="Next tip")
                with cols[3]:
                    st.button("🔄 Refresh", key="refresh_tip_btn", on_click=lambda: load_tips(
                        transactions_df), help="Refresh tips")
                with cols[4]:
                    st.button("✖️ Close", key="close_tip_btn",
                              on_click=toggle_tip_widget, help="Close tips")
            else:
                cols = st.columns([5, 1, 1])
                with cols[1]:
                    st.button("🔄 Refresh", key="refresh_tip_btn_single", on_click=lambda: load_tips(
                        transactions_df), help="Refresh tips")
                with cols[2]:
                    st.button("✖️ Close", key="close_tip_btn_single",
                              on_click=toggle_tip_widget, help="Close tips")
