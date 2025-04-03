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
        .stButton>button {
            width: 100%;
            margin-bottom: 10px;
        }
    }
    
    /* Improved button styling */
    .stButton>button {
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
    
    /* Profile card styling */
    .profile-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if user is logged in
    if "username" not in st.session_state:
        st.warning("Please log in to view your profile.")
        st.session_state.current_page = "login"
        st.rerun()
        return
    
    username = st.session_state.username
    
    # Center content for better appearance
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("Your Profile")
        
        auth_manager = AuthManager()
        user_info = auth_manager.get_user_info(username)
        
        if not user_info:
            st.error("User information not found. Please contact support.")
            return
        
        # User information display
        with st.container():
            st.markdown('<div class="profile-card">', unsafe_allow_html=True)
            st.subheader("Account Information")
            st.write(f"**Username:** {username}")
            st.write(f"**Name:** {user_info.get('name', 'Not set')}")
            st.write(f"**Email:** {user_info.get('email', 'Not set')}")
            st.write(f"**Phone Number:** {user_info.get('phone_number', 'Not set')}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Update profile tabs
        update_tab1, update_tab2 = st.tabs(["Update Profile", "Change Password"])
        
        with update_tab1:
            with st.form("update_profile_form"):
                st.subheader("Update Your Information")
                new_name = st.text_input("Full Name", value=user_info.get('name', ''))
                new_email = st.text_input("Email", value=user_info.get('email', ''))
                new_phone = st.text_input(
                    "Phone Number (M-Pesa)", 
                    value=user_info.get('phone_number', ''),
                    help="Enter your M-Pesa registered phone number in the format 2547XXXXXXXX"
                )
                
                update_btn = st.form_submit_button("Update Profile", use_container_width=True)
                
                if update_btn:
                    # Validate phone number
                    if new_phone and (not new_phone.startswith("254") or len(new_phone) != 12 or not new_phone.isdigit()):
                        st.error("Please enter a valid Kenyan phone number in the format 2547XXXXXXXX")
                    else:
                        # Update user info
                        updates = {
                            'name': new_name,
                            'email': new_email,
                            'phone_number': new_phone
                        }
                        
                        if auth_manager.update_user_info(username, updates):
                            st.success("Profile updated successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to update profile. Please try again.")
        
        with update_tab2:
            with st.form("change_password_form"):
                st.subheader("Change Your Password")
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                
                password_btn = st.form_submit_button("Change Password", use_container_width=True)
                
                if password_btn:
                    # Basic validation
                    if not current_password or not new_password or not confirm_password:
                        st.error("Please fill in all password fields")
                    elif new_password != confirm_password:
                        st.error("New passwords do not match")
                    else:
                        # Note: In a real app, we'd verify the current password here
                        # For this demo, we'll skip that verification step
                        
                        if auth_manager.change_password(username, new_password):
                            st.success("Password changed successfully!")
                        else:
                            st.error("Failed to change password. Please try again.")
        
        st.write("---")
        
        # Button to return to dashboard
        if st.button("Back to Dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()

if __name__ == "__main__":
    app()