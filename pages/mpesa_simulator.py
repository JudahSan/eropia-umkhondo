"""
M-Pesa Simulator Page for Eropia umkhondo

This page provides a simulation interface for testing M-Pesa API integration.
It allows users to:
1. Test STK Push
2. Test C2B Simulation
3. View/test transaction status query
4. Test webhooks
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from mpesa_api import MPesaAPI
from auth_manager import AuthManager
from mpesa_callbacks import simulate_c2b_callback, simulate_stk_callback

def app():
    """M-Pesa Simulator Page"""
    st.title("M-Pesa API Simulator")
    
    # Check if user is logged in
    if "username" not in st.session_state:
        st.warning("Please log in to access this page.")
        return
    
    # Get the username and phone number
    username = st.session_state.username
    auth_manager = AuthManager()
    user_phone = auth_manager.get_user_phone_number(username)
    
    # Initialize MPesaAPI
    mpesa_api = MPesaAPI(username=username, auth_manager=auth_manager)
    
    st.info("""
    This is a simulation page for testing M-Pesa API integration. In a production environment,
    you would integrate with the actual M-Pesa Daraja API. This simulation uses the demo mode
    to simulate transactions without making real API calls.
    """)
    
    if not user_phone:
        st.warning("Please set your phone number in your profile first.")
        
        if st.button("Go to Profile"):
            st.session_state.current_page = "profile"
            st.rerun()
        
        return
    
    # Display the user's phone number
    st.write(f"Your phone number: **{user_phone}**")
    
    # Create tabs for different simulation features
    tab1, tab2, tab3, tab4 = st.tabs([
        "STK Push", 
        "C2B Simulation", 
        "Transaction Status", 
        "Webhook Simulation"
    ])
    
    with tab1:
        st.subheader("Lipa Na M-Pesa Online (STK Push)")
        st.write("Simulate an STK Push to make a payment directly from your M-Pesa account.")
        
        with st.form("stk_push_form"):
            phone_number = st.text_input("Phone Number", value=user_phone)
            amount = st.number_input("Amount", min_value=1.0, value=100.0, step=10.0)
            description = st.text_input("Description", value="Payment for services")
            reference = st.text_input("Reference", value=f"REF{datetime.now().strftime('%Y%m%d%H%M%S')}")
            
            submitted = st.form_submit_button("Initiate STK Push")
            
            if submitted:
                with st.spinner("Processing STK Push request..."):
                    # Call the lipa_na_mpesa_online method
                    result = mpesa_api.lipa_na_mpesa_online(
                        phone_number=phone_number,
                        amount=amount,
                        description=description,
                        reference=reference
                    )
                    
                    if "error" in result:
                        st.error(f"Error initiating STK Push: {result['error']}")
                    else:
                        st.success("STK Push initiated successfully!")
                        
                        if "transactionId" in result:
                            st.info(f"Transaction ID: {result['transactionId']}")
                            st.session_state.last_transaction_id = result['transactionId']
                        
                        if "CheckoutRequestID" in result:
                            st.info(f"Checkout Request ID: {result['CheckoutRequestID']}")
                            st.session_state.last_checkout_request_id = result['CheckoutRequestID']
                        
                        st.json(result)
    
    with tab2:
        st.subheader("Customer to Business (C2B) Simulation")
        st.write("Simulate a customer making a payment to your business.")
        
        with st.form("c2b_sim_form"):
            phone_number = st.text_input("Phone Number", value=user_phone, key="c2b_phone")
            amount = st.number_input("Amount", min_value=1.0, value=100.0, step=10.0, key="c2b_amount")
            reference = st.text_input("Reference", value=f"REF{datetime.now().strftime('%Y%m%d%H%M%S')}", key="c2b_ref")
            
            submitted = st.form_submit_button("Simulate C2B Payment")
            
            if submitted:
                with st.spinner("Processing C2B payment simulation..."):
                    # Call the simulate_c2b_payment method
                    result = mpesa_api.simulate_c2b_payment(
                        phone_number=phone_number,
                        amount=amount,
                        reference=reference
                    )
                    
                    if "error" in result:
                        st.error(f"Error simulating C2B payment: {result['error']}")
                    else:
                        st.success("C2B payment simulated successfully!")
                        
                        if "transactionId" in result:
                            st.info(f"Transaction ID: {result['transactionId']}")
                            st.session_state.last_transaction_id = result['transactionId']
                        
                        st.json(result)
    
    with tab3:
        st.subheader("Transaction Status Query")
        st.write("Check the status of a transaction using its ID.")
        
        with st.form("tx_status_form"):
            # Use the last transaction ID if available
            default_tx_id = st.session_state.get("last_transaction_id", "")
            transaction_id = st.text_input("Transaction ID", value=default_tx_id)
            
            query_submitted = st.form_submit_button("Query Transaction Status")
            
            if query_submitted:
                if not transaction_id:
                    st.error("Please enter a transaction ID.")
                else:
                    with st.spinner("Querying transaction status..."):
                        # Call the query_transaction_status method
                        result = mpesa_api.query_transaction_status(transaction_id)
                        
                        if "error" in result:
                            st.error(f"Error querying transaction status: {result['error']}")
                        elif "ErrorCode" in result:
                            st.error(f"Error: {result['ErrorMessage']}")
                        else:
                            st.success("Transaction status query successful!")
                            st.json(result)
        
        # STK Push Status Query
        st.subheader("STK Push Status Query")
        st.write("Check the status of an STK Push request.")
        
        with st.form("stk_status_form"):
            # Use the last checkout request ID if available
            default_checkout_id = st.session_state.get("last_checkout_request_id", "")
            checkout_request_id = st.text_input("Checkout Request ID", value=default_checkout_id)
            
            stk_query_submitted = st.form_submit_button("Query STK Status")
            
            if stk_query_submitted:
                if not checkout_request_id:
                    st.error("Please enter a checkout request ID.")
                else:
                    with st.spinner("Querying STK status..."):
                        # Call the query_stk_status method
                        result = mpesa_api.query_stk_status(checkout_request_id)
                        
                        if "error" in result:
                            st.error(f"Error querying STK status: {result['error']}")
                        elif "ResponseCode" in result and result["ResponseCode"] != "0":
                            st.warning(f"STK Push was not successful: {result['ResponseDescription']}")
                        else:
                            st.success("STK status query successful!")
                            st.json(result)
    
    with tab4:
        st.subheader("Webhook Simulation")
        st.write("Simulate M-Pesa API callbacks to test webhook handling.")
        
        webhook_type = st.selectbox(
            "Select Webhook Type",
            ["C2B Callback", "STK Push Callback"]
        )
        
        if webhook_type == "C2B Callback":
            simulate_c2b_callback()
        else:
            simulate_stk_callback()
    
    # Display demo information
    st.markdown("---")
    st.subheader("M-Pesa API Integration Information")
    
    st.info("""
    In a real production environment, the M-Pesa integration would include:
    
    1. **Authentication** via OAuth with the Daraja API
    2. **C2B URL Registration** to receive real-time payment notifications
    3. **STK Push** for initiating payments directly from the app
    4. **Transaction Status Queries** to check payment statuses
    5. **Webhook Processing** for handling callbacks from M-Pesa
    
    The current implementation uses a demo mode that simulates these features
    without making actual API calls to the M-Pesa Daraja API.
    """)
    
    # Security information
    st.warning("""
    **Security Considerations:**
    
    In a production environment, the following security measures would be implemented:
    
    1. API keys stored securely in environment variables
    2. Encrypted communication with the API (HTTPS)
    3. IP whitelisting for API access
    4. Authentication of callback requests
    5. Validation of all transaction data
    """)

if __name__ == "__main__":
    app()