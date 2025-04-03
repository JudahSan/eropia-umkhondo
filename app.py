import streamlit as st
from auth_manager import AuthManager
import pages.login as login_page
import pages.register as register_page
import pages.dashboard as dashboard_page

# Set page configuration
st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for current page if not set
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"

# Define our app navigation structure
def main():
    # Handle page routing
    if st.session_state.current_page == "login":
        login_page.app()
    elif st.session_state.current_page == "register":
        register_page.app()
    elif st.session_state.current_page == "dashboard":
        # Display logout in the sidebar
        with st.sidebar:
            st.title("Finance Tracker")
            st.image("generated-icon.png", width=80)
            
            if "username" in st.session_state:
                st.write(f"Logged in as: {st.session_state.username}")
                
                if st.button("Logout"):
                    # Clear session state and go back to login
                    for key in list(st.session_state.keys()):
                        if key != "current_page":
                            del st.session_state[key]
                    
                    st.session_state.current_page = "login"
                    st.rerun()
        
        # Show the dashboard content
        dashboard_page.app()
    else:
        # Default to login if an invalid page is somehow set
        st.session_state.current_page = "login"
        st.rerun()

if __name__ == "__main__":
    main()