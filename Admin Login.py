import streamlit as st


# --- SESSION STATE INITIALIZATION ---
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False
if "show_emergency" not in st.session_state:
    st.session_state["show_emergency"] = False

# --- CONFIGURATION & SECRETS ---
# Constants from your Node.js logic
MASTER_RECOVERY_KEY = "HOSPITAL-EMERGENCY-2025-RECOVER"
HOSPITAL_DOMAIN = "@hospital.com"

# Fetching standard password from secrets, env, or default
admin_pwd = st.secrets.get("ADMIN_PASSWORD") or os.environ.get("ADMIN_PASSWORD") or "admin123"

st.title("🏥 Hospital Staff Login")

# --- UI LOGIC ---
if not st.session_state["show_emergency"]:
    # STANDARD LOGIN FORM
    with st.container():
        admin_email = st.text_input("Official Email", placeholder="name@hospital.com")
        admin_key = st.text_input("Password", type="password")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("LOGIN TO PORTAL", use_container_width=True):
                # Logic: Must end with @hospital.com AND match the admin password
                is_staff_valid = (
                    admin_email.lower().endswith(HOSPITAL_DOMAIN) and 
                    admin_key == admin_pwd
                )
                
                if is_staff_valid:
                    st.session_state["is_admin"] = True
                    st.success("Authenticated. Redirecting...")
                    st.switch_page("pages/Admin Portal.py")
                else:
                    st.error(f"Access Denied! Use official {HOSPITAL_DOMAIN} email.")

        with col2:
            if st.button("MASTER RESET KEY", type="secondary", use_container_width=True):
                st.session_state["show_emergency"] = True
                st.rerun()

else:
    # EMERGENCY BYPASS FORM
    st.warning("⚠️ EMERGENCY BYPASS MODE")
    master_key = st.text_input("Enter Master Key", type="password", help="Use the global recovery key.")
    
    col_em1, col_em2 = st.columns(2)
    
    with col_em1:
        if st.button("UNLOCK SYSTEM", type="primary", use_container_width=True):
            if master_key == MASTER_RECOVERY_KEY:
                st.session_state["is_admin"] = True
                st.session_state["admin_email"] = "MASTER-RECOVERY"
                st.success("Emergency Access Granted.")
                st.switch_page("pages/Admin Portal.py")
            else:
                st.error("Invalid Master Recovery Key.")
                
    with col_em2:
        if st.button("Back to Login", use_container_width=True):
            st.session_state["show_emergency"] = False
            st.rerun()
