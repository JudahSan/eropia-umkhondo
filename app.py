import streamlit as st
from auth_manager import AuthManager
import pages.login as login_page
import pages.register as register_page
import pages.dashboard as dashboard_page
import pages.landing as landing_page
import pages.profile as profile_page
import pages.mpesa_simulator as mpesa_simulator_page

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
    # Debug info to see the state of the session
    if st.session_state.get("debug", False):
        st.write("Debug Information:")
        st.write(f"Current Page: {st.session_state.get('current_page', 'None')}")
        st.write(f"Username: {st.session_state.get('username', 'Not logged in')}")
        st.write(f"Authentication Status: {'Logged in' if 'username' in st.session_state else 'Not logged in'}")
    
    # Set up sidebar navigation
    with st.sidebar:
        st.title("Eropia umkhondo")
        st.image("generated-icon.png", width=80)
        
        # Add debug toggle in sidebar
        if st.checkbox("Show Debug Info", value=st.session_state.get("debug", False)):
            st.session_state.debug = True
        else:
            st.session_state.debug = False
        
        # Check if user is logged in
        if "username" in st.session_state:
            st.write(f"Logged in as: {st.session_state.username}")
            
            # Add an attractive container for the navigation
            st.markdown("""
            <style>
            .nav-container {
                background-color: #f0f8ff;
                border-radius: 10px;
                padding: 10px;
                margin: 10px 0;
                border-left: 3px solid #4682b4;
            }
            </style>
            <div class="nav-container">
            <p style="font-weight: bold; color: #1E3A8A; margin-bottom: 10px;">Navigation</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add styling for the buttons
            st.markdown("""
            <style>
            .stButton>button {
                background-color: #1E88E5;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                width: 100%;
                margin-bottom: 8px;
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                background-color: #1565C0;
                transform: translateY(-2px);
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }
            .logout-button>button {
                background-color: #e57373;
            }
            .logout-button>button:hover {
                background-color: #c62828;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Create menu tabs for navigation
            st.markdown('<div class="nav-container">', unsafe_allow_html=True)
            
            # Show dashboard button
            if st.button("Dashboard", key="dashboard_btn", help="View your financial dashboard"):
                st.session_state.current_page = "dashboard"
                st.rerun()
            
            # Show profile button
            if st.button("Profile", key="profile_btn", help="Edit your profile settings"):
                st.session_state.current_page = "profile"
                st.rerun()
                
            # Show M-Pesa simulator button
            if st.button("M-Pesa Simulator", key="mpesa_simulator_btn", help="Test M-Pesa API integration"):
                st.session_state.current_page = "mpesa_simulator"
                st.rerun()
                
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add styling for the logout button
            st.markdown('<div class="logout-button">', unsafe_allow_html=True)
            # Show logout button
            if st.button("Logout", key="logout_btn", help="Sign out of your account"):
                # Clear session state and go back to landing
                for key in list(st.session_state.keys()):
                    if key != "current_page":
                        del st.session_state[key]
                
                st.session_state.current_page = "landing"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
        else:
            # Add styling for the buttons
            st.markdown("""
            <style>
            .stButton>button {
                background-color: #1E88E5;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                width: 100%;
                margin-bottom: 8px;
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                background-color: #1565C0;
                transform: translateY(-2px);
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }
            .register-button>button {
                background-color: #66bb6a;
            }
            .register-button>button:hover {
                background-color: #43a047;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Only show login/register buttons if not logged in
            st.write("### Get Started")
            
            if st.button("Login", key="login_btn", help="Log in to your account"):
                st.session_state.current_page = "login"
                st.rerun()
                
            # Use a div with a specific class for different styling
            st.markdown('<div class="register-button">', unsafe_allow_html=True)
            if st.button("Register", key="register_btn", help="Create a new account"):
                st.session_state.current_page = "register"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle page routing
    if st.session_state.current_page == "dashboard":
        # Always show dashboard when that page is selected
        dashboard_page.app()
    elif st.session_state.current_page == "profile" and "username" in st.session_state:
        # Show profile page for logged in users
        profile_page.app()
    elif st.session_state.current_page == "mpesa_simulator" and "username" in st.session_state:
        # Show M-Pesa simulator page for logged in users
        mpesa_simulator_page.app()
    elif st.session_state.current_page == "landing":
        # Show landing page regardless of login status
        landing_page.app()
    elif "username" not in st.session_state:
        # Only if user is not logged in, show login/register pages
        if st.session_state.current_page == "login":
            login_page.app()
        elif st.session_state.current_page == "register":
            register_page.app()
        else:
            # Default to landing if an invalid page is somehow set
            st.session_state.current_page = "landing"
            st.rerun()
    else:
        # If user is logged in and tries to access login/register, redirect to dashboard
        dashboard_page.app()

if __name__ == "__main__":
    main()