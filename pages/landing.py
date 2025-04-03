import streamlit as st

def app():
    # Custom CSS for better styling of the landing page
    st.markdown("""
    <style>
    /* Hide sidebar completely */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Main container styling */
    .block-container {
        max-width: 100% !important;
        padding: 0 !important;
    }
    
    .appview-container .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    /* Navigation bar */
    .nav-container {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 1rem 2rem;
        background-color: #FFFFFF;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
    }
    
    .nav-logo {
        margin-right: auto;
        font-size: 1.5rem;
        font-weight: 700;
        color: #1E3A8A;
    }
    
    .nav-links {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    /* Navigation buttons */
    .nav-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-button.primary {
        background-color: #1E88E5;
        color: white;
        border: none;
    }
    
    .nav-button.primary:hover {
        background-color: #1976D2;
    }
    
    .nav-button.secondary {
        background-color: white;
        color: #1E88E5;
        border: 2px solid #1E88E5;
    }
    
    .nav-button.secondary:hover {
        background-color: #F3F4F6;
    }
    
    /* Navigation icons for mobile */
    .nav-icon {
        display: none;
        background: none;
        border: none;
        font-size: 1.4rem;
        color: #1E88E5;
        padding: 0.5rem;
        cursor: pointer;
        margin-left: 0.5rem;
    }
    
    /* Hero section */
    .hero-container {
        text-align: center;
        padding: 7rem 1rem 5rem 1rem; /* Extra padding at top for fixed navbar */
        background: linear-gradient(135deg, #1E3A8A 0%, #1E88E5 100%);
        color: white;
        margin-bottom: 3rem;
        width: 100%;
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        margin-bottom: 2rem;
        font-weight: 300;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Feature section */
    .feature-section {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 1rem;
        text-align: center;
    }
    
    .feature-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 3rem;
    }
    
    .feature-card {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        padding: 2rem;
        width: 300px;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        color: #1E88E5;
    }
    
    .feature-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        color: #1E3A8A;
    }
    
    .feature-text {
        font-size: 1.1rem;
        color: #4B5563;
        line-height: 1.6;
    }
    
    /* CTA section */
    .cta-container {
        text-align: center;
        padding: 4rem 1rem;
        background-color: #F3F4F6;
        margin-bottom: 3rem;
        width: 100%;
    }
    
    .cta-title {
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        color: #1E3A8A;
    }
    
    .cta-text {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        color: #4B5563;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.7;
    }
    
    .cta-buttons {
        display: flex;
        justify-content: center;
        gap: 1rem;
        max-width: 500px;
        margin: 0 auto;
    }
    
    /* Button styling */
    .button {
        display: inline-block;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 500;
        border-radius: 8px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 180px;
    }
    
    .button.primary {
        background-color: #1E88E5;
        color: white;
        border: none;
    }
    
    .button.primary:hover {
        background-color: #1976D2;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        transform: translateY(-3px);
    }
    
    .button.secondary {
        background-color: white;
        color: #1E88E5;
        border: 2px solid #1E88E5;
    }
    
    .button.secondary:hover {
        background-color: #F3F4F6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-3px);
    }
    
    /* Cultural context section */
    .context-section {
        text-align: center;
        padding: 3rem 1rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .context-title {
        color: #1E3A8A;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
    }
    
    .context-text {
        color: #4B5563;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    
    /* Footer styling */
    .footer-container {
        text-align: center;
        padding: 3rem 1rem;
        background-color: #1E3A8A;
        color: white;
        margin-top: 2rem;
        width: 100%;
    }
    
    .footer-text {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
    }
    
    /* Streamlit specific overrides */
    .stButton>button, .stTextInput>div>div>input {
        width: 100%; 
    }
    
    /* Responsive styling */
    @media (max-width: 768px) {
        .nav-container {
            padding: 0.8rem 1rem;
        }
        
        .nav-button {
            display: none;
        }
        
        .nav-icon {
            display: inline-flex;
        }
        
        .hero-container {
            padding: 6rem 1rem 3rem 1rem;
        }
        
        .hero-title {
            font-size: 2.8rem;
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
        }
        
        .feature-container {
            flex-direction: column;
            align-items: center;
        }
        
        .feature-card {
            width: 100%;
        }
        
        .cta-title {
            font-size: 2rem;
        }
        
        .cta-text {
            font-size: 1.1rem;
        }
        
        .cta-buttons {
            flex-direction: column;
            gap: 1rem;
        }
        
        .button {
            width: 100%;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Hide the main menu and footer
    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Navigation Bar
    st.markdown("""
    <div class="nav-container">
        <div class="nav-logo">Eropia umkhondo</div>
        <div class="nav-links">
            <!-- Desktop buttons -->
            <a class="nav-button secondary" id="login-btn">Login</a>
            <a class="nav-button primary" id="register-btn">Register</a>
            
            <!-- Mobile icons -->
            <a class="nav-icon" id="login-icon">👤</a>
            <a class="nav-icon" id="register-icon">➕</a>
        </div>
    </div>
    
    <script>
        // Add event listeners to navigation elements
        document.getElementById('login-btn').addEventListener('click', function() {
            // This will be picked up by Streamlit's event handler
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'login'}, '*');
        });
        
        document.getElementById('register-btn').addEventListener('click', function() {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'register'}, '*');
        });
        
        document.getElementById('login-icon').addEventListener('click', function() {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'login'}, '*');
        });
        
        document.getElementById('register-icon').addEventListener('click', function() {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'register'}, '*');
        });
    </script>
    """, unsafe_allow_html=True)
    
    # Create hidden buttons for navigation that will be triggered by JavaScript
    if st.button("Login Hidden", key="login_hidden", help="Hidden button for login", label_visibility="collapsed"):
        st.session_state.current_page = "login"
        st.rerun()
        
    if st.button("Register Hidden", key="register_hidden", help="Hidden button for register", label_visibility="collapsed"):
        st.session_state.current_page = "register"
        st.rerun()
        
    # JavaScript to listen for messages and click the corresponding hidden button
    st.markdown("""
    <script>
        // Listen for messages from our custom HTML elements
        window.addEventListener('message', function(event) {
            if (event.data.type === 'streamlit:setComponentValue') {
                if (event.data.value === 'login') {
                    // Find and click the hidden login button
                    document.querySelector('button[data-testid="login_hidden"]').click();
                } else if (event.data.value === 'register') {
                    // Find and click the hidden register button
                    document.querySelector('button[data-testid="register_hidden"]').click();
                }
            }
        });
    </script>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Eropia umkhondo</h1>
        <p class="hero-subtitle">Track your money, build your future. A simple and powerful financial tracker combining personal and M-Pesa transactions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Section
    st.markdown("""
    <div class="feature-section">
        <div class="feature-container">
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3 class="feature-title">Visual Analytics</h3>
                <p class="feature-text">See where your money goes with intuitive charts and reports that help you understand your spending habits.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📱</div>
                <h3 class="feature-title">M-Pesa Integration</h3>
                <p class="feature-text">Automatically import your M-Pesa transactions to keep track of all your mobile money activities.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <h3 class="feature-title">Secure & Private</h3>
                <p class="feature-text">Your financial data stays private and secure. We use industry-standard security practices to protect your information.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div class="cta-container">
        <h2 class="cta-title">Start Your Financial Journey Today</h2>
        <p class="cta-text">Join thousands of users who have taken control of their finances with Eropia umkhondo. It's free to start!</p>
        
        <div class="cta-buttons">
            <a class="button primary" id="cta-register-btn">Create Account</a>
            <a class="button secondary" id="cta-login-btn">Login</a>
        </div>
    </div>
    
    <script>
        // Add event listeners to CTA buttons
        document.getElementById('cta-register-btn').addEventListener('click', function() {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'register'}, '*');
        });
        
        document.getElementById('cta-login-btn').addEventListener('click', function() {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'login'}, '*');
        });
    </script>
    """, unsafe_allow_html=True)
    
    # Cultural Context Section
    st.markdown("""
    <div class="context-section">
        <h3 class="context-title">About "Eropia umkhondo"</h3>
        <p class="context-text">
            "Eropia" is a Maasai word meaning "money" or "wealth", and "umkhondo" comes from Zulu meaning "track" or "trail". 
            Together, they represent our mission to help you track your money across different cultures and financial systems,
            bringing traditional values of saving and wise resource management into the digital age.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer-container">
        <p class="footer-text">© 2025 Eropia umkhondo - Your personal finance journey</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()