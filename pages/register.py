import streamlit as st
from auth_manager import AuthManager

def app():
    # Custom CSS for better mobile responsiveness and styling
    st.markdown("""
    <style>
    .block-container {
        max-width: 90%;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Responsive adjustments for mobile */
    @media (max-width: 768px) {
        .block-container {
            max-width: 95%;
            padding: 1rem;
        }
        h1 {
            font-size: 1.8rem !important;
        }
        h3 {
            font-size: 1.2rem !important;
        }
        .stButton>button, .stForm>div>div>div>div>div>button {
            width: 100%;
            margin-bottom: 10px;
        }
        /* Make columns stack for mobile */
        .row-widget.stHorizontal {
            flex-direction: column;
        }
        .row-widget.stHorizontal > div {
            width: 100%;
            flex: 1 1 100%;
            margin-bottom: 1rem;
        }
    }
    
    /* Improved button styling */
    .stButton>button, .stForm>div>div>div>div>div>button {
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    /* Fix padding and margins */
    div.row-widget.stButton {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Fix form element spacing */
    div.css-1r6slb0.e1tzin5v2 {
        padding: 1rem 0;
    }
    
    /* Form styling */
    .stForm {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Center content for better appearance
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.title("Register for Finance Tracker")
        
        auth_manager = AuthManager()
        
        with st.form("registration_form", clear_on_submit=True):
            st.subheader("Create a new account")
            
            # Use a single column layout for mobile and tablet
            username = st.text_input("Username", placeholder="Choose a username")
            name = st.text_input("Full Name", placeholder="Enter your full name")
            email = st.text_input("Email", placeholder="Enter your email")
            phone_number = st.text_input("Phone Number", placeholder="2547XXXXXXXX", 
                                        help="Enter your M-Pesa registered phone number in the format 2547XXXXXXXX")
            
            password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            submit = st.form_submit_button("Register", use_container_width=True)
            
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
        
        if st.button("Go to Login", use_container_width=True):
            st.session_state.current_page = "login"
            st.rerun()

if __name__ == "__main__":
    app()