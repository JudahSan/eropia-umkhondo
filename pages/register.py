import streamlit as st
from auth_manager import AuthManager

def app():
    st.title("Register for Finance Tracker")
    
    auth_manager = AuthManager()
    
    with st.form("registration_form", clear_on_submit=True):
        st.subheader("Create a new account")
        
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username", placeholder="Choose a username")
            password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
        with col2:
            name = st.text_input("Full Name", placeholder="Enter your full name")
            email = st.text_input("Email", placeholder="Enter your email")
            phone_number = st.text_input("Phone Number", placeholder="2547XXXXXXXX")
        
        submit = st.form_submit_button("Register")
        
        if submit:
            # Validate form data
            if not username or not password or not name or not email or not phone_number:
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif not phone_number.startswith("254") or len(phone_number) != 12 or not phone_number.isdigit():
                st.error("Please enter a valid Kenyan phone number in the format 2547XXXXXXXX")
            else:
                # Try to register the user
                if auth_manager.register_user(username, name, password, email, phone_number):
                    st.success("Registration successful! You can now log in.")
                    st.info("Redirecting to login page...")
                    st.session_state.current_page = "login"
                    st.rerun()
                else:
                    st.error("Username already exists. Please choose a different username.")
    
    st.write("---")
    st.write("Already have an account?")
    
    if st.button("Go to Login"):
        st.session_state.current_page = "login"
        st.rerun()

if __name__ == "__main__":
    app()