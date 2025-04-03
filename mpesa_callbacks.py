"""
M-Pesa Callbacks Module for Eropia umkhondo

This module handles webhook callbacks from the M-Pesa API for C2B payments
and STK push payments. It processes the callbacks and stores the transaction data.
"""

import os
import json
import streamlit as st
from datetime import datetime
from mpesa_api import MPesaAPI
from auth_manager import AuthManager
from data_manager import DataManager
from utils import categorize_transaction

def process_c2b_callback(request_data):
    """Process a C2B callback request from M-Pesa API
    
    Args:
        request_data (dict): Callback data from M-Pesa API
        
    Returns:
        dict: Processing result
    """
    try:
        # Extract transaction details from callback data
        transaction_id = request_data.get("TransID")
        amount = float(request_data.get("TransAmount", 0))
        msisdn = request_data.get("MSISDN")  # Customer phone number
        business_short_code = request_data.get("BusinessShortCode")
        bill_ref_number = request_data.get("BillRefNumber")
        invoice_number = request_data.get("InvoiceNumber", "")
        transaction_type = request_data.get("TransactionType")
        
        # Format the transaction date
        transaction_date_str = request_data.get("TransTime", "")
        if transaction_date_str:
            try:
                transaction_date = datetime.strptime(transaction_date_str, "%Y%m%d%H%M%S")
            except ValueError:
                transaction_date = datetime.now()
        else:
            transaction_date = datetime.now()
        
        # Initialize API
        mpesa_api = MPesaAPI()
        
        # Convert to transaction format for storage
        transaction = {
            'date': transaction_date.date(),
            'description': f"M-PESA Payment to {business_short_code} Reference: {bill_ref_number or invoice_number}",
            'amount': amount,
            'type': 'expense',
            'category': categorize_transaction(f"M-PESA Payment Reference: {bill_ref_number or invoice_number}"),
            'phone_number': msisdn,
            'status': 'completed',
            'reference': bill_ref_number or invoice_number,
            'transaction_id': transaction_id
        }
        
        # Find a user with the matching phone number to associate this transaction
        auth_manager = AuthManager()
        users = auth_manager._load_credentials().get('credentials', {}).get('usernames', {})
        
        # Try to find a matching user by phone number
        username = None
        for user, user_info in users.items():
            user_phone = user_info.get('phone_number', '')
            if user_phone and msisdn and user_phone.endswith(msisdn[-9:]):  # Match last 9 digits
                username = user
                break
        
        # Store the transaction in the appropriate user's data
        data_manager = DataManager(username=username)
        data_manager.ensure_data_file_exists()
        data_manager.add_transaction(transaction)
        
        # Return success response for the webhook
        return {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }
        
    except Exception as e:
        print(f"Error processing C2B callback: {e}")
        return {
            "ResultCode": 1,
            "ResultDesc": f"Failed to process: {str(e)}"
        }

def process_stk_callback(request_data):
    """Process an STK Push callback request from M-Pesa API
    
    Args:
        request_data (dict): Callback data from M-Pesa API
        
    Returns:
        dict: Processing result
    """
    try:
        body = request_data.get("Body", {})
        stk_callback = body.get("stkCallback", {})
        result_code = stk_callback.get("ResultCode")
        
        # Only process successful transactions
        if result_code == 0:
            # Extract item from callback metadata
            metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
            
            # Extract transaction details
            amount = next((item.get("Value") for item in metadata if item.get("Name") == "Amount"), 0)
            mpesa_receipt = next((item.get("Value") for item in metadata if item.get("Name") == "MpesaReceiptNumber"), "")
            transaction_date_str = next((item.get("Value") for item in metadata if item.get("Name") == "TransactionDate"), "")
            phone_number = next((item.get("Value") for item in metadata if item.get("Name") == "PhoneNumber"), "")
            
            # Format the transaction date
            if transaction_date_str:
                try:
                    transaction_date = datetime.strptime(str(transaction_date_str), "%Y%m%d%H%M%S")
                except ValueError:
                    transaction_date = datetime.now()
            else:
                transaction_date = datetime.now()
            
            # Convert to transaction format for storage
            transaction = {
                'date': transaction_date.date(),
                'description': f"M-PESA STK Push Payment Receipt: {mpesa_receipt}",
                'amount': float(amount),
                'type': 'expense',
                'category': 'Other',  # Default category, can be updated by user
                'phone_number': phone_number,
                'status': 'completed',
                'reference': mpesa_receipt,
                'transaction_id': mpesa_receipt
            }
            
            # Find a user with the matching phone number to associate this transaction
            auth_manager = AuthManager()
            users = auth_manager._load_credentials().get('credentials', {}).get('usernames', {})
            
            # Try to find a matching user by phone number
            username = None
            for user, user_info in users.items():
                user_phone = user_info.get('phone_number', '')
                if user_phone and user_phone.endswith(str(phone_number)[-9:]):  # Match last 9 digits
                    username = user
                    break
            
            # Store the transaction in the appropriate user's data
            data_manager = DataManager(username=username)
            data_manager.ensure_data_file_exists()
            data_manager.add_transaction(transaction)
            
            return {
                "ResultCode": 0,
                "ResultDesc": "Accepted"
            }
        else:
            # Transaction failed at M-Pesa level
            result_desc = stk_callback.get("ResultDesc", "Transaction failed")
            print(f"STK transaction failed: {result_desc}")
            return {
                "ResultCode": result_code,
                "ResultDesc": result_desc
            }
            
    except Exception as e:
        print(f"Error processing STK callback: {e}")
        return {
            "ResultCode": 1,
            "ResultDesc": f"Failed to process: {str(e)}"
        }

# Add webhook endpoints using Streamlit pages or a separate API server
# This would typically be handled by a framework like Flask or FastAPI
# For demo purposes, you could add a "secret" page in Streamlit to simulate callbacks

def simulate_c2b_callback():
    """Simulate a C2B callback for testing purposes"""
    st.title("Simulate M-Pesa C2B Callback")
    
    with st.form("simulate_c2b_form"):
        transaction_id = st.text_input("Transaction ID", value=f"OEI2{datetime.now().strftime('%Y%m%d%H%M%S')}")
        amount = st.number_input("Amount", min_value=1.0, value=1000.0)
        phone_number = st.text_input("Phone Number", value="254712345678")
        bill_ref_number = st.text_input("Bill Reference Number", value="TEST123")
        business_short_code = st.text_input("Business Short Code", value="174379")
        
        submitted = st.form_submit_button("Submit Callback")
        
        if submitted:
            callback_data = {
                "TransID": transaction_id,
                "TransAmount": str(amount),
                "MSISDN": phone_number,
                "BillRefNumber": bill_ref_number,
                "BusinessShortCode": business_short_code,
                "TransTime": datetime.now().strftime("%Y%m%d%H%M%S"),
                "TransactionType": "Pay Bill"
            }
            
            result = process_c2b_callback(callback_data)
            
            if result["ResultCode"] == 0:
                st.success(f"Callback processed successfully: {result['ResultDesc']}")
            else:
                st.error(f"Failed to process callback: {result['ResultDesc']}")
            
            st.json(callback_data)

def simulate_stk_callback():
    """Simulate an STK Push callback for testing purposes"""
    st.title("Simulate M-Pesa STK Push Callback")
    
    with st.form("simulate_stk_form"):
        receipt_number = st.text_input("M-Pesa Receipt Number", value=f"OEI2{datetime.now().strftime('%Y%m%d%H%M%S')}")
        amount = st.number_input("Amount", min_value=1.0, value=1000.0)
        phone_number = st.text_input("Phone Number", value="254712345678")
        result_code = st.selectbox("Result Code", options=[0, 1, 1032], index=0, 
                                 format_func=lambda x: f"{x} - {'Success' if x == 0 else 'Failed' if x == 1 else 'Cancelled'}")
        
        submitted = st.form_submit_button("Submit Callback")
        
        if submitted:
            callback_data = {
                "Body": {
                    "stkCallback": {
                        "MerchantRequestID": "29115-34620561-1",
                        "CheckoutRequestID": "ws_CO_191220191020363925",
                        "ResultCode": result_code,
                        "ResultDesc": "The service request is processed successfully." if result_code == 0 else "Failed",
                        "CallbackMetadata": {
                            "Item": [
                                {
                                    "Name": "Amount",
                                    "Value": amount
                                },
                                {
                                    "Name": "MpesaReceiptNumber",
                                    "Value": receipt_number
                                },
                                {
                                    "Name": "TransactionDate",
                                    "Value": int(datetime.now().strftime("%Y%m%d%H%M%S"))
                                },
                                {
                                    "Name": "PhoneNumber",
                                    "Value": phone_number
                                }
                            ]
                        }
                    }
                }
            }
            
            result = process_stk_callback(callback_data)
            
            if result["ResultCode"] == 0:
                st.success(f"Callback processed successfully: {result['ResultDesc']}")
            else:
                st.error(f"Failed to process callback: {result['ResultDesc']}")
            
            st.json(callback_data)