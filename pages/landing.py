import streamlit as st

def app():
    # Custom CSS for better styling of the landing page
    st.markdown("""
    <style>
    /* Main container styling */
    .block-container {
        max-width: 100%;
        padding: 0;
    }
    
    /* Hero section */
    .hero-container {
        text-align: center;
        padding: 4rem 1rem;
        background: linear-gradient(135deg, #1E3A8A 0%, #1E88E5 100%);
        color: white;
        border-radius: 0px;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 3.5rem;
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
    .feature-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 2rem;
        padding: 2rem 1rem;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 1.5rem;
        max-width: 300px;
        text-align: center;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #1E88E5;
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #1E3A8A;
    }
    
    .feature-text {
        font-size: 1rem;
        color: #4B5563;
    }
    
    /* CTA section */
    .cta-container {
        text-align: center;
        padding: 3rem 1rem;
        background-color: #F3F4F6;
        border-radius: 8px;
        margin-bottom: 2rem;
    }
    
    .cta-title {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #1E3A8A;
    }
    
    .cta-text {
        font-size: 1.1rem;
        margin-bottom: 2rem;
        color: #4B5563;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Button styling */
    .stButton button {
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 500;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .primary-button button {
        background-color: #1E88E5;
        color: white;
        border: none;
    }
    
    .primary-button button:hover {
        background-color: #1976D2;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    
    .secondary-button button {
        background-color: white;
        color: #1E88E5;
        border: 2px solid #1E88E5;
    }
    
    .secondary-button button:hover {
        background-color: #F3F4F6;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    /* Responsive styling */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
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
            max-width: 100%;
        }
        
        .cta-title {
            font-size: 1.8rem;
        }
        
        .cta-text {
            font-size: 1rem;
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
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Eropia umkhondo</h1>
        <p class="hero-subtitle">Track your money, build your future. A simple and powerful financial tracker combining personal and M-Pesa transactions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Section
    st.markdown("""
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
    """, unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div class="cta-container">
        <h2 class="cta-title">Start Your Financial Journey Today</h2>
        <p class="cta-text">Join thousands of users who have taken control of their finances with Eropia umkhondo. It's free to start!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<div class="primary-button">', unsafe_allow_html=True)
            if st.button("Create Account", use_container_width=True):
                st.session_state.current_page = "register"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_right:
            st.markdown('<div class="secondary-button">', unsafe_allow_html=True)
            if st.button("Login", use_container_width=True):
                st.session_state.current_page = "login"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Cultural Context Section
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 1rem;">
        <h3 style="color: #1E3A8A; margin-bottom: 1rem;">About "Eropia umkhondo"</h3>
        <p style="color: #4B5563; max-width: 800px; margin: 0 auto;">
            "Eropia" is a Maasai word meaning "money" or "wealth", and "umkhondo" comes from Zulu meaning "track" or "trail". 
            Together, they represent our mission to help you track your money across different cultures and financial systems,
            bringing traditional values of saving and wise resource management into the digital age.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()