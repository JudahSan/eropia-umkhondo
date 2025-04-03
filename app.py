import streamlit as st
from auth_manager import AuthManager
import pages.login as login_page
import pages.register as register_page
import pages.dashboard as dashboard_page
import pages.landing as landing_page
import pages.budget as budget_page

# Set page configuration
st.set_page_config(
    page_title="Eropia umkhondo - Money Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for current page if not set
if "current_page" not in st.session_state:
    st.session_state.current_page = "landing"

# Define our app navigation structure
def main():
    # Set up sidebar navigation
    with st.sidebar:
        st.title("Eropia umkhondo")
        st.image("generated-icon.png", width=80)
        
        # Check if user is logged in
        if "username" in st.session_state:
            st.write(f"Logged in as: {st.session_state.username}")
            
            # Show dashboard button
            if st.button("Dashboard", key="dashboard_btn"):
                st.session_state.current_page = "dashboard"
                st.rerun()
                
            # Show budget planner button
            if st.button("Budget Planner", key="budget_btn"):
                st.session_state.current_page = "budget"
                st.rerun()
            
            st.markdown("---")  # Divider
            
            # Show logout button
            if st.button("Logout", key="logout_btn"):
                # Clear session state and go back to landing
                for key in list(st.session_state.keys()):
                    if key != "current_page":
                        del st.session_state[key]
                
                st.session_state.current_page = "landing"
                st.rerun()
        else:
            # Show home button
            if st.button("Home", key="home_btn"):
                st.session_state.current_page = "landing"
                st.rerun()
                
            # Only show login/register buttons if not logged in
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Login", key="login_btn"):
                    st.session_state.current_page = "login"
                    st.rerun()
            
            with col2:
                if st.button("Register", key="register_btn"):
                    st.session_state.current_page = "register"
                    st.rerun()
    
    # Handle page routing
    if "username" in st.session_state:
        # If user is logged in, route to appropriate page
        if st.session_state.current_page == "dashboard":
            dashboard_page.app()
        elif st.session_state.current_page == "budget":
            budget_page.app()
        else:
            # Default to dashboard for authenticated users
            dashboard_page.app()
    else:
        # Only if user is not logged in, show landing/login/register pages
        if st.session_state.current_page == "landing":
            landing_page.app()
        elif st.session_state.current_page == "login":
            login_page.app()
        elif st.session_state.current_page == "register":
            register_page.app()
        else:
            # Default to landing if an invalid page is somehow set
            st.session_state.current_page = "landing"
            st.rerun()

if __name__ == "__main__":
    main()