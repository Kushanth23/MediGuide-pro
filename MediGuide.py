"""
MediGuide Pro — Final Production Edition
No JSON files. Cloud-safe authentication. Guest Login. Premium UI.
"""

import streamlit as st
import random
import time
import re
import hashlib
from datetime import datetime

st.set_page_config(
    page_title="MediGuide Pro | AI Health Companion",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 1. PREMIUM UI/UX
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background: linear-gradient(135deg, #0B1120 0%, #111827 100%); color: #F8FAFC; }
[data-testid="stSidebar"] { background: rgba(17, 24, 39, 0.7) !important; backdrop-filter: blur(20px); border-right: 1px solid rgba(255,255,255,0.05); }
[data-testid="stSidebar"] * { color: #E2E8F0 !important; }
[data-testid="stSidebar"] .stRadio label { padding: 10px 16px !important; border-radius: 12px; transition: all 0.3s; font-weight: 600; }
[data-testid="stSidebar"] .stRadio label:hover { background: rgba(56, 189, 248, 0.1); }
.gradient-text { background: linear-gradient(90deg, #38BDF8, #818CF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }
.hero-title { font-size: 3.2rem; line-height: 1.15; margin-bottom: 1rem; font-weight: 800; }
.hero-sub { font-size: 1.15rem; color: #94A3B8; max-width: 620px; line-height: 1.6; margin-bottom: 2rem; }
.glass-card { background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 1.8rem; margin-bottom: 1.5rem; transition: all 0.3s ease; }
.glass-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(56, 189, 248, 0.1); border-color: rgba(56, 189, 248, 0.3); }
div.stButton > button { background: linear-gradient(90deg, #3B82F6, #6366F1) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 0.7rem 1.5rem !important; font-weight: 700 !important; font-size: 0.95rem !important; transition: all 0.3s ease !important; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important; }
div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5) !important; }
.alert-red { background: rgba(239, 68, 68, 0.1); border: 1px solid #EF4444; color: #FCA5A5; padding: 1.5rem; border-radius: 16px; margin: 1rem 0; }
.alert-amber { background: rgba(245, 158, 11, 0.1); border: 1px solid #F59E0B; color: #FDE68A; padding: 1.5rem; border-radius: 16px; margin: 1rem 0; }
.alert-green { background: rgba(16, 185, 129, 0.1); border: 1px solid #10B981; color: #6EE7B7; padding: 1.5rem; border-radius: 16px; margin: 1rem 0; }
.ddx-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 0.8rem; display: flex; justify-content: space-between; align-items: center; }
.ddx-title { font-weight: 700; color: #F8FAFC; }
.ddx-desc { font-size: 0.85rem; color: #94A3B8; }
.badge { padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }
.badge-high { background: rgba(239, 68, 68, 0.2); color: #FCA5A5; }
.badge-med { background: rgba(245, 158, 11, 0.2); color: #FDE68A; }
.badge-low { background: rgba(16, 185, 129, 0.2); color: #6EE7B7; }
.chat-msg { padding: 1rem 1.2rem; border-radius: 16px; max-width: 85%; line-height: 1.5; margin-bottom: 0.8rem; }
.chat-user { background: #3B82F6; color: white; margin-left: auto; border-bottom-right-radius: 4px; }
.chat-ai { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #E2E8F0; border-bottom-left-radius: 4px; }
.term-card { background: rgba(56, 189, 248, 0.05); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 0.8rem; }
.term-name { color: #38BDF8; font-weight: 700; font-size: 1.05rem; }
.term-meaning { color: #CBD5E1; font-size: 0.9rem; margin-top: 4px; }
.auth-hero { text-align: center; padding: 3rem 1rem; }
.auth-hero h1 { font-size: 3rem; margin-bottom: 0.5rem; }
.auth-hero p { color: #94A3B8; font-size: 1.1rem; max-width: 500px; margin: 0 auto 2rem auto; }
.user-badge { display: inline-block; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3); color: #38BDF8; padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
div[data-baseweb="input"] input, div[data-baseweb="select"] > div { background: rgba(255,255,255,0.05) !important; color: white !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; }
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 2. CLOUD-SAFE AUTHENTICATION
# ============================================================
if "users_db" not in st.session_state:
    st.session_state.users_db = {}

def hash_password(password, salt=None):
    if salt is None: salt = "mediguide_salt_" + str(random.randint(1000, 9999))
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return hashed, salt

def verify_password(password, salt, stored_hash):
    computed, _ = hash_password(password, salt)
    return computed == stored_hash

def create_user(email, name, password):
    email = email.lower().strip()
    if email in st.session_state.users_db:
        return False, "An account with this email already exists."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if "@" not in email:
        return False, "Please enter a valid email address."
    hashed, salt = hash_password(password)
    st.session_state.users_db[email] = {
        "name": name.strip(),
        "password_hash": hashed,
        "salt": salt,
        "created": datetime.now().isoformat(),
    }
    return True, "Account created!"

def authenticate(email, password):
    email = email.lower().strip()
    if email not in st.session_state.users_db:
        return False, "No account found with this email. Please sign up."
    user = st.session_state.users_db[email]
    if verify_password(password, user["salt"], user["password_hash"]):
        return True, user["name"]
    return False, "Incorrect password."

# ============================================================
# 3. SESSION STATE
# ============================================================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_name" not in st.session_state: st.session_state.user_name = ""
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "page" not in st.session_state: st.session_state.page = "Home"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "ai", "text": "👋 Hi! I'm MediGuide AI. Ask me anything about symptoms, medicines, or medical terms."}]
if "report_data" not in st.session_state: st.session_state.report_data = None
if "bmi" not in st.session_state: st.session_state.bmi = None

def nav(page): st.session_state.page = page; st.rerun()
def logout():
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.user_email = ""
    st.session_state.page = "Home"
    st.session_state.chat_history = [{"role": "ai", "text": "👋 Hi! I'm MediGuide AI. Ask me anything about symptoms, medicines, or medical terms."}]
    st.rerun()

# ============================================================
# 4. LOGIN / SIGNUP / GUEST GATE
# ============================================================
if not st.session_state.logged_in:
    st.markdown("""
    <div class="auth-hero">
        <div style="font-size: 4rem; margin-bottom: 1rem;">✨</div>
        <h1 class="gradient-text">MediGuide Pro</h1>
        <p>Your AI-powered health companion. Secure, private, and clinically informed.</p>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 1.2, 1])
    with col_m:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

        with tab1:
            st.markdown("### Welcome back")
            login_email = st.text_input("Email", key="login_email", placeholder="you@example.com")
            login_password = st.text_input("Password", type="password", key="login_password", placeholder="••••••••")
            if st.button("Login →", use_container_width=True, key="btn_login"):
                if not login_email or not login_password:
                    st.error("Please enter both email and password.")
                else:
                    ok, msg = authenticate(login_email, login_password)
                    if ok:
                        st.session_state.logged_in = True
                        st.session_state.user_name = msg
                        st.session_state.user_email = login_email.lower().strip()
                        st.success(f"Welcome back, {msg}!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(msg)

        with tab2:
            st.markdown("### Create an account")
            signup_name = st.text_input("Full Name", key="signup_name", placeholder="John Doe")
            signup_email = st.text_input("Email", key="signup_email", placeholder="you@example.com")
            signup_password = st.text_input("Password (min 6 chars)", type="password", key="signup_password")
            signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")
            if st.button("Create Account →", use_container_width=True, key="btn_signup"):
                if not signup_name or not signup_email or not signup_password:
                    st.error("Please fill in all fields.")
                elif signup_password != signup_confirm:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = create_user(signup_email, signup_name, signup_password)
                    if ok:
                        st.success("Account created! Please log in.")
                        time.sleep(0.8)
                        st.rerun()
                    else:
                        st.error(msg)

        st.markdown("</div>", unsafe_allow_html=True)

        # ---------- GUEST LOGIN ----------
        st.markdown("""
        <div style='text-align:center; margin: 1rem 0 0.8rem 0; color:#64748B; font-size:0.85rem;'>
            — or —
        </div>
        """, unsafe_allow_html=True)

        if st.button("👤 Continue as Guest →", use_container_width=True, key="btn_guest"):
            guest_id = random.randint(1000, 9999)
            st.session_state.logged_in = True
            st.session_state.user_name = f"Guest #{guest_id}"
            st.session_state.user_email = f"guest_{guest_id}@mediguide.local"
            st.success("Welcome, Guest! Sign up anytime to save your account.")
            time.sleep(0.5)
            st.rerun()

        st.markdown("""
        <div style='text-align:center; color:#64748B; font-size:0.8rem; margin-top:1rem;'>
            🔒 Passwords are hashed with SHA-256. We never store plaintext.<br>
            Note: Accounts reset when the server restarts (educational demo).
        </div>
        """, unsafe_allow_html=True)
    st.stop()


# ============================================================
# 5. MEDICAL DATABASE
# ============================================================
SYMPTOMS = {
    "Headache": {"icon": "🤕", "about": "Pain in the head from tension, dehydration, migraine, or infection.", "emergency": ["Sudden severe 'worst headache of my life'", "Fever with stiff neck", "Neurological symptoms"], "meds": ["Paracetamol", "Ibuprofen", "Naproxen"], "severity": {"Mild": "Rest, hydrate.", "Moderate": "OTC painkiller.", "Severe": "See doctor."}},
    "Migraine": {"icon": "🧠", "about": "Throbbing headache with nausea or light sensitivity.", "emergency": ["Sudden severe headache", "Weakness, vision loss"], "meds": ["Paracetamol", "Ibuprofen"], "severity": {"Mild": "Dark room.", "Moderate": "NSAID at onset.", "Severe": "See doctor."}},
    "Fever": {"icon": "🌡️", "about": "Temperature ≥ 38°C — body's response to infection.", "emergency": ["Fever in baby < 3 months", "Stiff neck, rash, confusion"], "meds": ["Paracetamol", "Ibuprofen"], "severity": {"Mild": "Hydrate.", "Moderate": "Alternate meds.", "Severe": "Seek advice."}},
    "Cough (dry)": {"icon": "😮‍💨", "about": "Tickly cough from colds or allergies.", "emergency": ["Trouble breathing", "Coughing blood"], "meds": ["Dextromethorphan"], "severity": {"Mild": "Warm fluids.", "Moderate": "Cough suppressant.", "Severe": "See doctor."}},
    "Cough (productive)": {"icon": "🗣️", "about": "Chesty cough with mucus.", "emergency": ["Trouble breathing", "Blood in sputum"], "meds": ["Guaifenesin"], "severity": {"Mild": "Hydrate.", "Moderate": "Expectorant.", "Severe": "See doctor."}},
    "Sore throat": {"icon": "😷", "about": "Pain in the throat, usually viral.", "emergency": ["Unable to swallow saliva", "Drooling"], "meds": ["Paracetamol", "Benzocaine lozenges"], "severity": {"Mild": "Salt gargle.", "Moderate": "Lozenges.", "Severe": "See doctor."}},
    "Runny nose": {"icon": "🤧", "about": "Clear discharge from colds or allergies.", "emergency": ["Trouble breathing"], "meds": ["Saline nasal spray", "Cetirizine"], "severity": {"Mild": "Saline.", "Moderate": "Antihistamine.", "Severe": "See doctor."}},
    "Nasal congestion": {"icon": "👃", "about": "Blocked nose from colds or sinusitis.", "emergency": ["Swelling around eyes"], "meds": ["Saline nasal spray", "Oxymetazoline spray"], "severity": {"Mild": "Steam.", "Moderate": "Decongestant.", "Severe": "See doctor."}},
    "Sneezing": {"icon": "🤧", "about": "Allergic or irritant-driven reflex.", "emergency": ["Breathing difficulty"], "meds": ["Cetirizine", "Loratadine"], "severity": {"Mild": "Antihistamine.", "Moderate": "Daily antihistamine.", "Severe": "See allergist."}},
    "Ear pain": {"icon": "👂", "about": "Pain from infection, pressure, or injury.", "emergency": ["Swelling behind ear"], "meds": ["Paracetamol", "Ibuprofen"], "severity": {"Mild": "Warm compress.", "Moderate": "See doctor.", "Severe": "Urgent care."}},
    "Eye redness": {"icon": "👁️", "about": "Red eye from conjunctivitis or irritation.", "emergency": ["Sudden vision loss"], "meds": ["Artificial tears"], "severity": {"Mild": "Cool compress.", "Moderate": "See doctor.", "Severe": "Urgent care."}},
    "Stomach ache": {"icon": "🤢", "about": "Abdominal pain from indigestion or infection.", "emergency": ["Rigid abdomen", "Vomiting blood"], "meds": ["Paracetamol", "Simethicone"], "severity": {"Mild": "Rest.", "Moderate": "Antacid.", "Severe": "Urgent care."}},
    "Indigestion": {"icon": "🍽️", "about": "Upper abdominal discomfort after eating.", "emergency": ["Vomiting blood"], "meds": ["Calcium carbonate antacid", "Omeprazole"], "severity": {"Mild": "Antacid.", "Moderate": "PPI.", "Severe": "See doctor."}},
    "Heartburn": {"icon": "🔥", "about": "Burning behind breastbone from reflux.", "emergency": ["Chest pain with sweating"], "meds": ["Omeprazole", "Famotidine"], "severity": {"Mild": "Antacid.", "Moderate": "PPI.", "Severe": "See doctor."}},
    "Nausea": {"icon": "🤮", "about": "Feeling of wanting to vomit.", "emergency": ["Blood in vomit"], "meds": ["Dimenhydrinate", "Meclizine"], "severity": {"Mild": "Sip fluids.", "Moderate": "Anti-nausea meds.", "Severe": "Seek care."}},
    "Vomiting": {"icon": "🤢", "about": "Expelling stomach contents.", "emergency": ["Blood in vomit"], "meds": ["Oral rehydration salts"], "severity": {"Mild": "ORS.", "Moderate": "Anti-nausea.", "Severe": "Seek care."}},
    "Diarrhea": {"icon": "🚽", "about": "Loose or watery stools.", "emergency": ["Bloody stool"], "meds": ["Oral rehydration salts", "Loperamide"], "severity": {"Mild": "ORS.", "Moderate": "Loperamide.", "Severe": "Seek care."}},
    "Constipation": {"icon": "🚫", "about": "Infrequent or hard stools.", "emergency": ["Severe pain + vomiting"], "meds": ["Psyllium", "Polyethylene glycol"], "severity": {"Mild": "Fiber.", "Moderate": "PEG.", "Severe": "See doctor."}},
    "Bloating": {"icon": "🎈", "about": "Feeling of abdominal fullness.", "emergency": ["Severe pain"], "meds": ["Simethicone"], "severity": {"Mild": "Walk.", "Moderate": "Simethicone.", "Severe": "See doctor."}},
    "Muscle ache": {"icon": "💪", "about": "Pain in muscles from strain or illness.", "emergency": ["Chest pain", "Dark urine"], "meds": ["Paracetamol", "Ibuprofen"], "severity": {"Mild": "Rest.", "Moderate": "NSAID.", "Severe": "See doctor."}},
    "Joint pain": {"icon": "🦴", "about": "Pain in joints from injury or arthritis.", "emergency": ["Hot swollen joint with fever"], "meds": ["Paracetamol", "Ibuprofen"], "severity": {"Mild": "Rest.", "Moderate": "NSAID.", "Severe": "See doctor."}},
    "Back pain": {"icon": "🔙", "about": "Pain in the lower or upper back.", "emergency": ["Loss of bladder control"], "meds": ["Paracetamol", "Ibuprofen", "Naproxen"], "severity": {"Mild": "Heat.", "Moderate": "NSAID.", "Severe": "See doctor."}},
    "Sprain": {"icon": "🦶", "about": "Stretched or torn ligament.", "emergency": ["Deformity"], "meds": ["Paracetamol", "Ibuprofen", "Diclofenac gel"], "severity": {"Mild": "RICE.", "Moderate": "NSAID gel.", "Severe": "See doctor."}},
    "Insect bite": {"icon": "🐝", "about": "Local reaction to a bite or sting.", "emergency": ["Breathing difficulty"], "meds": ["Calamine lotion", "Hydrocortisone 1% cream"], "severity": {"Mild": "Calamine.", "Moderate": "Antihistamine.", "Severe": "Emergency."}},
    "Rash": {"icon": "🔴", "about": "Skin eruption from allergy or infection.", "emergency": ["Non-blanching with fever"], "meds": ["Hydrocortisone 1% cream", "Calamine lotion"], "severity": {"Mild": "Calamine.", "Moderate": "Steroid cream.", "Severe": "See doctor."}},
    "Itching": {"icon": "✋", "about": "Sensation that provokes scratching.", "emergency": ["Breathing difficulty"], "meds": ["Hydrocortisone 1% cream", "Cetirizine"], "severity": {"Mild": "Moisturize.", "Moderate": "Antihistamine.", "Severe": "See doctor."}},
    "Sunburn": {"icon": "☀️", "about": "Skin damage from UV rays.", "emergency": ["Severe blistering"], "meds": ["Calamine lotion", "Aloe vera gel"], "severity": {"Mild": "Aloe.", "Moderate": "Pain relief.", "Severe": "See doctor."}},
    "Dizziness": {"icon": "😵‍💫", "about": "Feeling faint or unsteady.", "emergency": ["Chest pain", "Fainting"], "meds": ["Meclizine", "Dimenhydrinate"], "severity": {"Mild": "Sit down.", "Moderate": "Anti-motion.", "Severe": "Urgent care."}},
    "Fatigue": {"icon": "😴", "about": "Persistent tiredness.", "emergency": ["Chest pain", "Suicidal thoughts"], "meds": ["Vitamin D", "Zinc supplements"], "severity": {"Mild": "Sleep.", "Moderate": "Review diet.", "Severe": "See doctor."}},
    "Insomnia": {"icon": "🌙", "about": "Difficulty falling or staying asleep.", "emergency": ["Suicidal thoughts"], "meds": ["Diphenhydramine"], "severity": {"Mild": "Sleep hygiene.", "Moderate": "Short-term meds.", "Severe": "See doctor."}},
    "Anxiety": {"icon": "😰", "about": "Excessive worry or fear.", "emergency": ["Chest pain with breathlessness"], "meds": [], "severity": {"Mild": "Breathing.", "Moderate": "Professional help.", "Severe": "Urgent support."}},
    "Cold sore": {"icon": "👄", "about": "Blister from herpes simplex virus.", "emergency": ["Eye involvement"], "meds": ["Paracetamol", "Petroleum jelly"], "severity": {"Mild": "Moisturize.", "Moderate": "Pain relief.", "Severe": "See doctor."}},
    "Mouth ulcer": {"icon": "👅", "about": "Painful sore inside the mouth.", "emergency": ["Difficulty swallowing"], "meds": ["Benzocaine lozenges"], "severity": {"Mild": "Rinse.", "Moderate": "Anesthetic.", "Severe": "See doctor."}},
    "Toothache": {"icon": "🦷", "about": "Pain in or around a tooth.", "emergency": ["Facial swelling"], "meds": ["Paracetamol", "Ibuprofen"], "severity": {"Mild": "Pain relief.", "Moderate": "See dentist.", "Severe": "Urgent care."}},
    "Urinary discomfort": {"icon": "🚻", "about": "Burning or urgency on urination.", "emergency": ["Fever with back pain"], "meds": ["Paracetamol"], "severity": {"Mild": "Hydrate.", "Moderate": "See doctor.", "Severe": "Urgent care."}},
    "Hemorrhoids": {"icon": "🔻", "about": "Swollen veins near the anus.", "emergency": ["Heavy bleeding"], "meds": ["Hydrocortisone rectal cream"], "severity": {"Mild": "Fiber.", "Moderate": "Cream.", "Severe": "See doctor."}},
    "Acne": {"icon": "🧴", "about": "Inflamed skin pores.", "emergency": ["Severe nodules with fever"], "meds": ["Benzoyl peroxide", "Salicylic acid topical"], "severity": {"Mild": "Cleanse.", "Moderate": "Topical.", "Severe": "See dermatologist."}},
    "Skin fungal infection": {"icon": "🍄", "about": "Fungal infection of skin.", "emergency": ["Fever with spreading rash"], "meds": ["Clotrimazole cream", "Terbinafine"], "severity": {"Mild": "Antifungal.", "Moderate": "Continue.", "Severe": "See doctor."}},
    "Allergic reaction (skin)": {"icon": "🌡️", "about": "Hives or rash from allergen.", "emergency": ["Breathing difficulty"], "meds": ["Cetirizine", "Hydrocortisone 1% cream"], "severity": {"Mild": "Antihistamine.", "Moderate": "Cream.", "Severe": "Emergency."}},
    "Bleeding gums": {"icon": "🩸", "about": "Gums bleeding on brushing.", "emergency": ["Heavy bleeding"], "meds": ["Paracetamol"], "severity": {"Mild": "Floss.", "Moderate": "See dentist.", "Severe": "Urgent dental."}},
    "Blurred vision": {"icon": "👁️", "about": "Loss of sharp vision.", "emergency": ["Sudden vision loss"], "meds": ["Artificial tears"], "severity": {"Mild": "Rest eyes.", "Moderate": "Optometrist.", "Severe": "Urgent care."}},
    "Bruising easily": {"icon": "🟣", "about": "Bruises without obvious cause.", "emergency": ["Large bruises after minor injury"], "meds": ["Vitamin C"], "severity": {"Mild": "Monitor.", "Moderate": "See doctor.", "Severe": "Urgent assessment."}},
    "Chest tightness": {"icon": "💔", "about": "Pressure or squeezing in the chest.", "emergency": ["Pain radiating to arm/jaw", "Shortness of breath"], "meds": ["Calcium carbonate antacid"], "severity": {"Mild": "Rest.", "Moderate": "See doctor.", "Severe": "Emergency."}},
    "Chills": {"icon": "🥶", "about": "Shivering with fever.", "emergency": ["Stiff neck"], "meds": ["Paracetamol"], "severity": {"Mild": "Rest.", "Moderate": "Monitor.", "Severe": "Urgent care."}},
    "Cramps (muscle)": {"icon": "🦵", "about": "Sudden painful muscle contraction.", "emergency": ["Dark urine"], "meds": ["Paracetamol", "Magnesium supplements"], "severity": {"Mild": "Stretch.", "Moderate": "Electrolytes.", "Severe": "See doctor."}},
    "Dark urine": {"icon": "🟤", "about": "Brown or dark yellow urine.", "emergency": ["Yellow skin"], "meds": [], "severity": {"Mild": "Hydrate.", "Moderate": "See doctor.", "Severe": "Urgent care."}},
    "Dry mouth": {"icon": "👄", "about": "Lack of saliva.", "emergency": ["Difficulty breathing"], "meds": [], "severity": {"Mild": "Sip water.", "Moderate": "Review meds.", "Severe": "See doctor."}},
    "Dry skin": {"icon": "🧴", "about": "Flaky or rough skin.", "emergency": ["Infection signs"], "meds": ["Hydrocortisone 1% cream", "Petroleum jelly"], "severity": {"Mild": "Moisturize.", "Moderate": "Steroid cream.", "Severe": "See dermatologist."}},
    "Ear ringing (tinnitus)": {"icon": "🔔", "about": "Ringing in the ears.", "emergency": ["Sudden hearing loss"], "meds": [], "severity": {"Mild": "Avoid noise.", "Moderate": "Audiologist.", "Severe": "ENT referral."}},
    "Excessive sweating": {"icon": "💦", "about": "Sweating more than usual.", "emergency": ["With chest pain"], "meds": [], "severity": {"Mild": "Antiperspirant.", "Moderate": "See doctor.", "Severe": "Investigate causes."}},
    "Fainting": {"icon": "💫", "about": "Brief loss of consciousness.", "emergency": ["With chest pain"], "meds": [], "severity": {"Mild": "Lie down.", "Moderate": "See doctor.", "Severe": "Emergency."}},
    "Foot pain": {"icon": "🦶", "about": "Pain in the foot or heel.", "emergency": ["Deformity"], "meds": ["Paracetamol", "Ibuprofen"], "severity": {"Mild": "Rest.", "Moderate": "NSAID.", "Severe": "See doctor."}},
    "Frequent urination": {"icon": "🚻", "about": "Urinating more often than usual.", "emergency": ["Fever with back pain"], "meds": ["Paracetamol"], "severity": {"Mild": "Reduce caffeine.", "Moderate": "See doctor.", "Severe": "Urgent care."}},
    "Hair loss": {"icon": "💇", "about": "Loss of hair from scalp or body.", "emergency": ["With rash"], "meds": ["Zinc supplements", "Vitamin D"], "severity": {"Mild": "Diet.", "Moderate": "Blood tests.", "Severe": "See dermatologist."}},
    "Hand numbness": {"icon": "🤚", "about": "Loss of sensation in the hand.", "emergency": ["Sudden one-sided numbness"], "meds": ["Ibuprofen"], "severity": {"Mild": "Stretch.", "Moderate": "See doctor.", "Severe": "Emergency if sudden."}},
    "Heel pain": {"icon": "👠", "about": "Pain at the heel.", "emergency": ["With fever"], "meds": ["Ibuprofen", "Diclofenac gel"], "severity": {"Mild": "Stretch.", "Moderate": "NSAID.", "Severe": "See podiatrist."}},
    "Hoarse voice": {"icon": "🗣️", "about": "Rough or strained voice.", "emergency": ["Difficulty breathing"], "meds": ["Paracetamol"], "severity": {"Mild": "Voice rest.", "Moderate": "See doctor.", "Severe": "Urgent care."}},
    "Hives": {"icon": "🔴", "about": "Itchy raised welts on the skin.", "emergency": ["Breathing difficulty"], "meds": ["Cetirizine", "Loratadine"], "severity": {"Mild": "Antihistamine.", "Moderate": "Daily meds.", "Severe": "Emergency."}},
    "Knee pain": {"icon": "🦵", "about": "Pain in the knee joint.", "emergency": ["Hot swollen knee with fever"], "meds": ["Paracetamol", "Ibuprofen"], "severity": {"Mild": "Rest.", "Moderate": "NSAID.", "Severe": "See doctor."}},
    "Loss of appetite": {"icon": "🍽️", "about": "Reduced desire to eat.", "emergency": ["Weight loss > 5%"], "meds": [], "severity": {"Mild": "Small meals.", "Moderate": "See doctor.", "Severe": "Urgent review."}},
    "Neck pain": {"icon": "🦒", "about": "Pain in the neck.", "emergency": ["Numbness or weakness"], "meds": ["Paracetamol", "Ibuprofen"], "severity": {"Mild": "Posture.", "Moderate": "NSAID.", "Severe": "See doctor."}},
    "Night sweats": {"icon": "💦", "about": "Drenching sweats at night.", "emergency": ["High fever and confusion"], "meds": [], "severity": {"Mild": "Cool room.", "Moderate": "See doctor.", "Severe": "Blood tests."}},
    "Palpitations": {"icon": "💓", "about": "Awareness of heartbeat.", "emergency": ["With chest pain"], "meds": [], "severity": {"Mild": "Reduce caffeine.", "Moderate": "ECG.", "Severe": "Emergency."}},
    "Post-nasal drip": {"icon": "👃", "about": "Mucus running down the back of throat.", "emergency": ["Trouble breathing"], "meds": ["Saline nasal spray", "Cetirizine"], "severity": {"Mild": "Saline.", "Moderate": "Antihistamine.", "Severe": "See doctor."}},
    "Sensitivity to light": {"icon": "☀️", "about": "Pain or discomfort from light.", "emergency": ["With fever and stiff neck"], "meds": ["Paracetamol"], "severity": {"Mild": "Dim lights.", "Moderate": "See doctor.", "Severe": "Emergency."}},
    "Shoulder pain": {"icon": "💪", "about": "Pain in the shoulder joint.", "emergency": ["With chest pain"], "meds": ["Paracetamol", "Ibuprofen"], "severity": {"Mild": "Rest.", "Moderate": "NSAID.", "Severe": "See specialist."}},
    "Stiff neck": {"icon": "🦒", "about": "Inability to move neck freely.", "emergency": ["With fever"], "meds": ["Paracetamol", "Ibuprofen"], "severity": {"Mild": "Warm compress.", "Moderate": "See doctor.", "Severe": "Emergency if fever."}},
    "Swallowing difficulty": {"icon": "🥤", "about": "Trouble swallowing food or liquid.", "emergency": ["Unable to swallow saliva"], "meds": [], "severity": {"Mild": "Small bites.", "Moderate": "See doctor.", "Severe": "Emergency."}},
    "Swollen glands": {"icon": "🫁", "about": "Enlarged lymph nodes.", "emergency": ["Rapidly enlarging"], "meds": ["Paracetamol"], "severity": {"Mild": "Rest.", "Moderate": "See doctor.", "Severe": "Urgent if hard."}},
    "Vision changes": {"icon": "👁️", "about": "Any change in vision.", "emergency": ["Sudden vision loss"], "meds": ["Artificial tears"], "severity": {"Mild": "Eye exam.", "Moderate": "Optometrist.", "Severe": "Emergency."}},
    "Watery eyes": {"icon": "💧", "about": "Excess tear production.", "emergency": ["Vision loss"], "meds": ["Artificial tears"], "severity": {"Mild": "Drops.", "Moderate": "Antihistamine.", "Severe": "See ophthalmologist."}},
    "Weight loss": {"icon": "⚖️", "about": "Unintentional loss of weight.", "emergency": ["Rapid severe loss"], "meds": [], "severity": {"Mild": "Track.", "Moderate": "Blood tests.", "Severe": "Urgent assessment."}},
    "Wrist pain": {"icon": "✋", "about": "Pain in the wrist.", "emergency": ["Deformity"], "meds": ["Paracetamol", "Ibuprofen"], "severity": {"Mild": "Rest.", "Moderate": "Splint + NSAID.", "Severe": "See doctor."}},
    "Other": {"icon": "❓", "about": "Any other symptom.", "emergency": ["Trouble breathing", "Chest pain"], "meds": [], "severity": {"Mild": "Monitor.", "Moderate": "See doctor.", "Severe": "Urgent care."}},
}

MEDICINES = {
    "Paracetamol": {"class": "Analgesic / Antipyretic", "adult_dose": "500–1000 mg q4–6h", "max": "4g/day", "warnings": ["Liver damage if overdose", "Check combination products"], "uses": ["Fever", "Pain"]},
    "Ibuprofen": {"class": "NSAID", "adult_dose": "200–400 mg q4–6h", "max": "1200 mg/day OTC", "warnings": ["Take with food", "Avoid in ulcers/kidney disease"], "uses": ["Pain", "Fever", "Inflammation"]},
    "Aspirin": {"class": "NSAID", "adult_dose": "300–600 mg q4–6h", "max": "4g/day", "warnings": ["Never under 16", "Bleeding risk"], "uses": ["Pain", "Fever", "Heart"]},
    "Naproxen": {"class": "NSAID", "adult_dose": "220–440 mg q8–12h", "max": "660 mg/day", "warnings": ["Take with food"], "uses": ["Pain"]},
    "Diclofenac gel": {"class": "Topical NSAID", "adult_dose": "Apply 2–4g qid", "max": "16g/joint/day", "warnings": ["Not on broken skin"], "uses": ["Joint pain"]},
    "Cetirizine": {"class": "Antihistamine", "adult_dose": "10 mg daily", "max": "10 mg/day", "warnings": ["Drowsiness possible"], "uses": ["Allergies", "Hives"]},
    "Loratadine": {"class": "Antihistamine", "adult_dose": "10 mg daily", "max": "10 mg/day", "warnings": ["Less sedating"], "uses": ["Allergies"]},
    "Fexofenadine": {"class": "Antihistamine", "adult_dose": "120–180 mg daily", "max": "180 mg/day", "warnings": ["Avoid fruit juice"], "uses": ["Hay fever"]},
    "Chlorpheniramine": {"class": "Antihistamine", "adult_dose": "4 mg q4–6h", "max": "24 mg/day", "warnings": ["Strongly sedating"], "uses": ["Allergies"]},
    "Diphenhydramine": {"class": "Antihistamine", "adult_dose": "25–50 mg q4–6h", "max": "300 mg/day", "warnings": ["Sedating"], "uses": ["Allergies", "Sleep aid"]},
    "Pseudoephedrine": {"class": "Decongestant", "adult_dose": "60 mg q4–6h", "max": "240 mg/day", "warnings": ["Raises BP"], "uses": ["Congestion"]},
    "Phenylephrine": {"class": "Decongestant", "adult_dose": "10 mg q4h", "max": "60 mg/day", "warnings": ["Raises BP"], "uses": ["Congestion"]},
    "Oxymetazoline spray": {"class": "Nasal spray", "adult_dose": "1–2 sprays q10–12h", "max": "3 days max", "warnings": ["Rebound congestion"], "uses": ["Congestion"]},
    "Saline nasal spray": {"class": "Saline spray", "adult_dose": "2–3 sprays prn", "max": "As needed", "warnings": ["Very safe"], "uses": ["Congestion"]},
    "Dextromethorphan": {"class": "Cough suppressant", "adult_dose": "10–20 mg q4h", "max": "120 mg/day", "warnings": ["Not for wet cough"], "uses": ["Dry cough"]},
    "Guaifenesin": {"class": "Expectorant", "adult_dose": "200–400 mg q4h", "max": "2400 mg/day", "warnings": ["Drink water"], "uses": ["Wet cough"]},
    "Benzocaine lozenges": {"class": "Anesthetic", "adult_dose": "1 lozenge q2h", "max": "Follow label", "warnings": ["Choking risk < 4y"], "uses": ["Sore throat"]},
    "Fluticasone nasal": {"class": "Corticosteroid", "adult_dose": "1–2 sprays daily", "max": "2 sprays/nostril", "warnings": ["Nosebleed possible"], "uses": ["Allergic rhinitis"]},
    "Hydrocortisone 1% cream": {"class": "Topical steroid", "adult_dose": "Apply 1–2x daily", "max": "7 days", "warnings": ["Avoid on infection"], "uses": ["Itching", "Eczema"]},
    "Clotrimazole cream": {"class": "Antifungal", "adult_dose": "Apply twice daily", "max": "2–4 weeks", "warnings": ["Not in eyes"], "uses": ["Ringworm"]},
    "Miconazole cream": {"class": "Antifungal", "adult_dose": "Apply twice daily", "max": "2–4 weeks", "warnings": ["Not in eyes"], "uses": ["Ringworm"]},
    "Calamine lotion": {"class": "Soothing topical", "adult_dose": "Apply prn", "max": "As needed", "warnings": ["External only"], "uses": ["Itching"]},
    "Loperamide": {"class": "Antidiarrheal", "adult_dose": "4 mg then 2 mg", "max": "16 mg/day", "warnings": ["Not with fever"], "uses": ["Diarrhea"]},
    "Bismuth subsalicylate": {"class": "Antidiarrheal", "adult_dose": "524 mg prn", "max": "8 doses/day", "warnings": ["Contains salicylate"], "uses": ["Diarrhea"]},
    "Oral rehydration salts": {"class": "ORS", "adult_dose": "Sip 200 mL", "max": "As needed", "warnings": ["Mix correctly"], "uses": ["Dehydration"]},
    "Psyllium": {"class": "Bulk laxative", "adult_dose": "1 tsp 3x daily", "max": "Follow label", "warnings": ["Drink water"], "uses": ["Constipation"]},
    "Polyethylene glycol": {"class": "Osmotic laxative", "adult_dose": "17 g daily", "max": "34 g/day", "warnings": ["Drink water"], "uses": ["Constipation"]},
    "Docusate": {"class": "Stool softener", "adult_dose": "100 mg twice daily", "max": "500 mg/day", "warnings": ["Drink water"], "uses": ["Constipation"]},
    "Bisacodyl": {"class": "Stimulant laxative", "adult_dose": "5–10 mg daily", "max": "Follow label", "warnings": ["Max 7 days"], "uses": ["Constipation"]},
    "Omeprazole": {"class": "PPI", "adult_dose": "20 mg daily", "max": "20 mg/day OTC", "warnings": ["Take before food"], "uses": ["Heartburn"]},
    "Calcium carbonate antacid": {"class": "Antacid", "adult_dose": "500–1000 mg prn", "max": "Follow label", "warnings": ["Constipation"], "uses": ["Heartburn"]},
    "Simethicone": {"class": "Antiflatulent", "adult_dose": "40–125 mg prn", "max": "Follow label", "warnings": ["Very safe"], "uses": ["Bloating"]},
    "Meclizine": {"class": "Antihistamine", "adult_dose": "25–50 mg pre-travel", "max": "50 mg/day", "warnings": ["Drowsiness"], "uses": ["Motion sickness"]},
    "Dimenhydrinate": {"class": "Antihistamine", "adult_dose": "50–100 mg q4–6h", "max": "400 mg/day", "warnings": ["Drowsiness"], "uses": ["Motion sickness"]},
    "Amoxicillin": {"class": "Antibiotic (Rx)", "adult_dose": "250–500 mg q8h", "max": "As prescribed", "warnings": ["Prescription only"], "uses": ["Infection"]},
    "Azithromycin": {"class": "Antibiotic (Rx)", "adult_dose": "500 mg then 250 mg", "max": "As prescribed", "warnings": ["Prescription only"], "uses": ["Infection"]},
    "Hydrocortisone rectal cream": {"class": "Corticosteroid", "adult_dose": "Apply up to 4x daily", "max": "7 days", "warnings": ["Not internally"], "uses": ["Hemorrhoids"]},
    "Benzoyl peroxide": {"class": "Topical antibacterial", "adult_dose": "Apply 1–2x daily", "max": "Follow label", "warnings": ["Bleaches fabric"], "uses": ["Acne"]},
    "Salicylic acid topical": {"class": "Keratolytic", "adult_dose": "Apply 1–3x daily", "max": "Follow label", "warnings": ["Avoid broken skin"], "uses": ["Acne"]},
    "Famotidine": {"class": "H2 blocker", "adult_dose": "10–20 mg twice daily", "max": "40 mg/day", "warnings": ["Max 14 days"], "uses": ["Heartburn"]},
    "Fluconazole": {"class": "Antifungal (Rx)", "adult_dose": "150 mg single dose", "max": "As prescribed", "warnings": ["Prescription only"], "uses": ["Fungal infection"]},
    "Terbinafine": {"class": "Antifungal", "adult_dose": "Apply 1–2x daily", "max": "1–2 weeks", "warnings": ["Not in eyes"], "uses": ["Athlete's foot"]},
    "Ketoconazole shampoo": {"class": "Antifungal", "adult_dose": "Twice weekly", "max": "8 weeks", "warnings": ["Avoid eyes"], "uses": ["Dandruff"]},
    "Mupirocin": {"class": "Topical antibiotic", "adult_dose": "Apply 3x daily", "max": "10 days", "warnings": ["Prescription only"], "uses": ["Skin infection"]},
    "Povidone-iodine": {"class": "Antiseptic", "adult_dose": "Apply to wound", "max": "Follow label", "warnings": ["Not on large wounds"], "uses": ["Wound care"]},
    "Artificial tears": {"class": "Eye drops", "adult_dose": "1–2 drops prn", "max": "As needed", "warnings": ["Discard after 30d"], "uses": ["Dry eyes"]},
    "Sodium cromoglicate eye drops": {"class": "Eye drops", "adult_dose": "1–2 drops 4x daily", "max": "Follow label", "warnings": ["Remove contacts"], "uses": ["Allergic eyes"]},
    "Salbutamol inhaler": {"class": "Bronchodilator (Rx)", "adult_dose": "1–2 puffs prn", "max": "As prescribed", "warnings": ["Prescription only"], "uses": ["Asthma"]},
    "Beclomethasone inhaler": {"class": "Inhaled steroid (Rx)", "adult_dose": "1–2 puffs twice daily", "max": "As prescribed", "warnings": ["Rinse mouth after"], "uses": ["Asthma"]},
    "Montelukast": {"class": "Leukotriene antagonist (Rx)", "adult_dose": "10 mg bedtime", "max": "10 mg/day", "warnings": ["Mood changes"], "uses": ["Asthma"]},
    "Prednisolone": {"class": "Oral steroid (Rx)", "adult_dose": "As prescribed", "max": "As prescribed", "warnings": ["Do not stop suddenly"], "uses": ["Inflammation"]},
    "Adrenaline auto-injector": {"class": "Emergency (Rx)", "adult_dose": "0.3 mg IM", "max": "Repeat 5–15 min", "warnings": ["Call emergency after use"], "uses": ["Anaphylaxis"]},
    "Lidocaine patch": {"class": "Topical anesthetic (Rx)", "adult_dose": "Up to 12h/day", "max": "3 patches", "warnings": ["Not on broken skin"], "uses": ["Localized pain"]},
    "Menthol rub": {"class": "Counterirritant", "adult_dose": "Apply thin layer", "max": "3–4x daily", "warnings": ["Avoid eyes"], "uses": ["Muscle ache"]},
    "Magnesium supplements": {"class": "Mineral", "adult_dose": "200–400 mg daily", "max": "Follow label", "warnings": ["Diarrhea"], "uses": ["Cramps"]},
    "Vitamin D": {"class": "Vitamin", "adult_dose": "400–1000 IU daily", "max": "4000 IU/day", "warnings": ["Do not exceed"], "uses": ["Deficiency"]},
    "Vitamin C": {"class": "Vitamin", "adult_dose": "500–1000 mg daily", "max": "2000 mg/day", "warnings": ["Diarrhea"], "uses": ["Deficiency"]},
    "Zinc supplements": {"class": "Mineral", "adult_dose": "10–25 mg daily", "max": "40 mg/day", "warnings": ["Interferes with antibiotics"], "uses": ["Deficiency"]},
    "Folic acid": {"class": "Vitamin", "adult_dose": "400 mcg daily", "max": "1000 mcg/day", "warnings": ["High dose needs supervision"], "uses": ["Deficiency"]},
    "Lactulose": {"class": "Osmotic laxative", "adult_dose": "15–30 mL daily", "max": "Follow label", "warnings": ["Takes 2–3 days"], "uses": ["Constipation"]},
    "Senna": {"class": "Stimulant laxative", "adult_dose": "7.5–15 mg at bedtime", "max": "Follow label", "warnings": ["Max 7 days"], "uses": ["Constipation"]},
    "Petroleum jelly": {"class": "Emollient", "adult_dose": "Apply prn", "max": "As needed", "warnings": ["Flammable"], "uses": ["Dry skin"]},
    "Aloe vera gel": {"class": "Soothing topical", "adult_dose": "Apply prn", "max": "As needed", "warnings": ["Use pure aloe"], "uses": ["Sunburn"]},
    "Triamcinolone cream": {"class": "Topical steroid (Rx)", "adult_dose": "Apply 1–2x daily", "max": "Prescription only", "warnings": ["Not on face"], "uses": ["Eczema"]},
    "Betamethasone cream": {"class": "Topical steroid (Rx)", "adult_dose": "Apply 1–2x daily", "max": "Prescription only", "warnings": ["Not on face"], "uses": ["Eczema"]},
    "Sertraline": {"class": "SSRI (Rx)", "adult_dose": "50 mg daily", "max": "As prescribed", "warnings": ["Monitor mood"], "uses": ["Depression"]},
    "Duloxetine": {"class": "SNRI (Rx)", "adult_dose": "30–60 mg daily", "max": "As prescribed", "warnings": ["Do not stop abruptly"], "uses": ["Depression", "Pain"]},
    "Pregabalin": {"class": "Anticonvulsant (Rx)", "adult_dose": "75 mg twice daily", "max": "As prescribed", "warnings": ["Controlled substance"], "uses": ["Neuropathic pain"]},
}

POSSIBLE_CONDITIONS = {
    "Headache": [("Tension headache", "Dull, pressure-like pain", "Most likely"), ("Migraine", "Throbbing one-sided", "Possible"), ("Sinus headache", "Facial pressure", "Less likely")],
    "Fever": [("Viral infection", "Cold/flu", "Most likely"), ("COVID-19", "Fever + cough", "Possible"), ("UTI", "Fever + burning urine", "Possible")],
    "Cough (dry)": [("Post-viral cough", "Tickly", "Most likely"), ("Allergic cough", "Triggers", "Possible")],
    "Cough (productive)": [("Bronchitis", "Chesty with mucus", "Most likely"), ("Pneumonia", "With breathlessness", "Possible")],
    "Sore throat": [("Viral pharyngitis", "Cold symptoms", "Most likely"), ("Strep throat", "Severe, no cough", "Possible")],
    "Stomach ache": [("Indigestion", "Post-eating", "Most likely"), ("Gastroenteritis", "With diarrhea", "Possible")],
    "Nausea": [("Gastroenteritis", "With diarrhea", "Most likely"), ("Motion sickness", "Travel-related", "Possible")],
    "Vomiting": [("Gastroenteritis", "With diarrhea", "Most likely"), ("Food poisoning", "After suspicious meal", "Possible")],
    "Diarrhea": [("Viral gastroenteritis", "Watery", "Most likely"), ("Food poisoning", "Sudden onset", "Possible")],
    "Chest tightness": [("Anxiety", "With stress", "Most likely"), ("GERD", "Burning", "Possible"), ("Angina", "With exertion", "Less likely")],
    "Back pain": [("Muscle strain", "After lifting", "Most likely"), ("Herniated disc", "Radiates to leg", "Possible")],
    "Dizziness": [("Orthostatic", "On standing", "Most likely"), ("Dehydration", "With thirst", "Possible")],
    "Fatigue": [("Poor sleep/stress", "Sleep debt", "Most likely"), ("Anemia", "With pale skin", "Possible")],
    "Rash": [("Contact dermatitis", "After irritant", "Most likely"), ("Eczema", "Dry itchy patches", "Possible")],
    "Anxiety": [("Generalized anxiety", "Persistent worry", "Most likely"), ("Panic disorder", "Sudden episodes", "Possible")],
}

GLOSSARY = {
    "Tachycardia": "Abnormally fast heart rate (>100 bpm).",
    "Bradycardia": "Abnormally slow heart rate (<60 bpm).",
    "Dyspnea": "Shortness of breath or difficulty breathing.",
    "Apnea": "Temporary cessation of breathing.",
    "Epistaxis": "Nosebleed.",
    "Hemoptysis": "Coughing up blood.",
    "Hematemesis": "Vomiting blood.",
    "Melena": "Black, tarry stools.",
    "Hematuria": "Blood in the urine.",
    "Dysuria": "Painful urination.",
    "Syncope": "Fainting or loss of consciousness.",
    "Vertigo": "Sensation of spinning.",
    "Photophobia": "Sensitivity to light.",
    "Emesis": "Vomiting.",
    "Dysphagia": "Difficulty swallowing.",
    "Anorexia": "Loss of appetite.",
    "Cachexia": "Severe weight loss and muscle wasting.",
    "Edema": "Swelling due to fluid retention.",
    "Ascites": "Fluid in the abdominal cavity.",
    "Tachypnea": "Abnormally fast breathing.",
    "Orthopnea": "Breathlessness when lying flat.",
    "Cyanosis": "Bluish discoloration from low oxygen.",
    "Pallor": "Unusually pale skin.",
    "Erythema": "Redness of the skin.",
    "Pruritus": "Itching.",
    "Urticaria": "Hives.",
    "Eczema": "Inflammatory itchy skin condition.",
    "Petechiae": "Small red/purple spots.",
    "Purpura": "Larger purple skin spots.",
    "Ecchymosis": "A bruise.",
    "Malaise": "General feeling of discomfort.",
    "Lethargy": "Abnormal drowsiness.",
    "Seizure": "Sudden electrical disturbance in the brain.",
    "Aura": "Sensory warning before migraine/seizure.",
    "Paresthesia": "Tingling or pins and needles.",
    "Neuropathy": "Nerve damage causing numbness/pain.",
    "Paresis": "Mild or partial paralysis.",
    "Plegia": "Complete paralysis.",
    "Ataxia": "Loss of coordination.",
    "Aphasia": "Difficulty with language.",
    "Dysarthria": "Slurred speech.",
    "Tinnitus": "Ringing in ears.",
    "Myalgia": "Muscle pain.",
    "Arthralgia": "Joint pain.",
    "Arthritis": "Joint inflammation.",
    "Myocarditis": "Inflammation of heart muscle.",
    "Pericarditis": "Inflammation of sac around heart.",
    "Thrombosis": "Blood clot formation.",
    "Embolism": "Clot traveling in bloodstream.",
    "Ischemia": "Reduced blood flow to tissue.",
    "Infarction": "Tissue death from lack of blood.",
    "Hypertension": "High blood pressure.",
    "Hypotension": "Low blood pressure.",
    "Hyperglycemia": "High blood sugar.",
    "Hypoglycemia": "Low blood sugar.",
    "Sepsis": "Life-threatening response to infection.",
    "Anaphylaxis": "Severe allergic reaction.",
    "Benign": "Non-cancerous.",
    "Malignant": "Cancerous.",
    "Metastasis": "Spread of cancer.",
    "Biopsy": "Removal of tissue for examination.",
    "Prognosis": "Expected outcome of a condition.",
    "Diagnosis": "Identification of a disease.",
    "Differential diagnosis": "List of possible conditions.",
    "Etiology": "Cause of a disease.",
    "Acute": "Sudden onset, short duration.",
    "Chronic": "Long-lasting, persistent.",
    "Idiopathic": "Of unknown cause.",
    "Congenital": "Present from birth.",
}

# ============================================================
# 6. AI CHATBOT
# ============================================================
def ai_respond(user_input):
    text = user_input.lower().strip()
    words = re.findall(r"[a-z]+", text)
    if any(w in words for w in ["hi", "hello", "hey"]):
        return f"Hello {st.session_state.user_name.split()[0]}! How can I help you today?"
    if any(w in words for w in ["thanks", "thank"]):
        return "You're welcome! Remember, I'm educational only — for real medical advice, see a doctor."
    if any(kw in text for kw in ["chest pain", "can't breathe", "severe bleeding", "unconscious", "stroke", "heart attack", "suicide"]):
        return "🚨 **This sounds like a medical emergency.** Call your local emergency number immediately."
    for term, meaning in GLOSSARY.items():
        if term.lower() in text:
            return f"**{term}** — {meaning}"
    for med_name, med in MEDICINES.items():
        if med_name.lower() in text:
            return (f"**{med_name}** ({med['class']})\n\n"
                    f"- **Dose:** {med['adult_dose']}\n"
                    f"- **Max:** {med['max']}\n"
                    f"- **Used for:** {', '.join(med['uses'])}\n"
                    f"- **⚠ Warnings:** {'; '.join(med['warnings'])}")
    matched = [s for s in SYMPTOMS if s.lower() in text]
    if matched:
        response = "Based on what you described:\n\n"
        for sym in matched:
            conditions = POSSIBLE_CONDITIONS.get(sym, [])
            if conditions:
                response += f"**{sym}** → Most likely: *{conditions[0][0]}* ({conditions[0][1]}).\n"
            if SYMPTOMS[sym]["meds"]:
                response += f"💊 OTC: {', '.join(SYMPTOMS[sym]['meds'][:3])}.\n"
            response += f"🚨 Emergency signs: {SYMPTOMS[sym]['emergency'][0]}.\n\n"
        response += "_Educational only. Please see a doctor for proper diagnosis._"
        return response
    if any(w in text for w in ["prevent", "diet", "exercise", "sleep", "hydration"]):
        return "**Wellness tips:** 💧 Water, 😴 7-9 hrs sleep, 🥗 balanced diet, 🚶 150 min activity/week, 🧼 hand hygiene."
    return "I can help with symptoms, medicines, or medical terms. Try *'What is tachycardia?'*, *'I have a fever'*, or *'Tell me about ibuprofen'*."

# ============================================================
# 7. SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("<h2 class='gradient-text'>✨ MediGuide Pro</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='user-badge'>👤 {st.session_state.user_name}</div>", unsafe_allow_html=True)
    st.caption(st.session_state.user_email)
    st.divider()
    PAGES = ["🏠 Home", "🔎 Symptom Checker", "🤖 AI Chat", "📊 Vitals & Tools", "💊 Drug Formulary", "📖 Medical Glossary", "👤 Profile"]
    current = st.radio("Navigate", PAGES, label_visibility="collapsed")
    mapping = {"🏠 Home": "Home", "🔎 Symptom Checker": "Symptom Checker", "🤖 AI Chat": "AI Chat", "📊 Vitals & Tools": "Tools", "💊 Drug Formulary": "Library", "📖 Medical Glossary": "Glossary", "👤 Profile": "Profile"}
    if mapping[current] != st.session_state.page:
        st.session_state.page = mapping[current]
        st.rerun()
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        logout()

# ============================================================
# 8. PAGES
# ============================================================
if st.session_state.page == "Home":
    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown(f"""
        <div class="hero-title">Hi {st.session_state.user_name.split()[0]}, <br><span class="gradient-text">Your Health Decoded.</span></div>
        <div class="hero-sub">Clinical-grade triage, differential diagnosis, and a chatbot that understands 74 symptoms, 85 medicines, and 70+ medical terms.</div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.button("Start Triage →", on_click=nav, args=("Symptom Checker",))
        with c2: st.button("Chat with AI 🤖", on_click=nav, args=("AI Chat",))
    with col2:
        st.markdown("<div class='glass-card' style='text-align:center; padding: 3rem 2rem;'><div style='font-size: 5rem;'>🩺</div><h3>Clinical Insight</h3><p style='color:#94A3B8;'>Real-time triage from a 74-symptom database.</p></div>", unsafe_allow_html=True)

elif st.session_state.page == "Symptom Checker":
    st.markdown("<h1 class='gradient-text'>Smart Triage</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        symptom = st.selectbox("Primary Symptom", sorted(SYMPTOMS.keys()))
        duration = st.selectbox("Duration", ["Started today", "1-3 days", "4-7 days", "> 1 week", "> 3 weeks"])
        severity = st.select_slider("Severity", options=["Mild", "Moderate", "Severe"])
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        age = st.selectbox("Age Group", ["Under 12", "13-64", "65+"])
        risk = st.checkbox("Pregnant, immunocompromised, or chronic condition")
        st.markdown("</div>", unsafe_allow_html=True)
    emergencies = st.multiselect("Are any of these happening?", SYMPTOMS[symptom]["emergency"])
    if st.button("Generate Clinical Report 🩺", use_container_width=True):
        with st.spinner("Analyzing..."):
            time.sleep(1.2)
            level = 3 if emergencies else (2 if severity == "Severe" else (1 if duration in ("> 1 week", "> 3 weeks") else 0))
            st.session_state.report_data = {"symptom": symptom, "level": level}
    if st.session_state.report_data:
        d = st.session_state.report_data
        st.markdown("---")
        if d["level"] == 3: st.markdown("<div class='alert-red'><h3>🚨 EMERGENCY</h3><p>Seek urgent care.</p></div>", unsafe_allow_html=True)
        elif d["level"] == 2: st.markdown("<div class='alert-amber'><h3>⚠️ CONSULT DOCTOR</h3><p>Book within 24h.</p></div>", unsafe_allow_html=True)
        else: st.markdown("<div class='alert-green'><h3>✅ SELF-CARE</h3><p>Manageable at home.</p></div>", unsafe_allow_html=True)
        st.markdown("#### Differential Diagnosis")
        for cond, desc, lik in POSSIBLE_CONDITIONS.get(d["symptom"], []):
            badge = "badge-high" if "Most" in lik else ("badge-med" if "Possible" in lik else "badge-low")
            st.markdown(f"<div class='ddx-card'><div><div class='ddx-title'>{cond}</div><div class='ddx-desc'>{desc}</div></div><span class='badge {badge}'>{lik}</span></div>", unsafe_allow_html=True)
        st.markdown("#### Recommended OTC")
        for m in SYMPTOMS[d["symptom"]]["meds"]:
            if m in MEDICINES:
                st.markdown(f"**{m}** ({MEDICINES[m]['class']}) — {MEDICINES[m]['adult_dose']}. *{MEDICINES[m]['warnings'][0]}*")

elif st.session_state.page == "AI Chat":
    st.markdown("<h1 class='gradient-text'>MediGuide AI</h1>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        cls = "chat-user" if msg["role"] == "user" else "chat-ai"
        st.markdown(f"<div class='chat-msg {cls}'>{msg['text']}</div>", unsafe_allow_html=True)
    user_input = st.chat_input("Ask anything...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        response = ai_respond(user_input)
        st.session_state.chat_history.append({"role": "ai", "text": response})
        st.rerun()

elif st.session_state.page == "Tools":
    st.markdown("<h1 class='gradient-text'>Health Tools</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='glass-card'><h3>📏 BMI</h3>", unsafe_allow_html=True)
        w = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
        h = st.number_input("Height (cm)", 100.0, 250.0, 175.0)
        if st.button("Calculate BMI"):
            bmi = w / ((h/100) ** 2)
            st.session_state.bmi = round(bmi, 1)
        st.markdown("</div>", unsafe_allow_html=True)
        if st.session_state.bmi:
            cat = "Underweight" if st.session_state.bmi < 18.5 else "Normal" if st.session_state.bmi < 25 else "Overweight" if st.session_state.bmi < 30 else "Obese"
            st.success(f"BMI: **{st.session_state.bmi}** ({cat})")
    with c2:
        st.markdown("<div class='glass-card'><h3>💧 Hydration</h3>", unsafe_allow_html=True)
        wh = st.number_input("Weight (kg)", 30.0, 200.0, 70.0, key="wh")
        act = st.selectbox("Activity", ["Sedentary", "Moderate", "Active"])
        mult = 30 if act == "Sedentary" else (35 if act == "Moderate" else 40)
        st.info(f"Target: **{wh * mult} ml** (~{wh * mult // 250} glasses) per day")
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "Library":
    st.markdown("<h1 class='gradient-text'>Drug Formulary</h1>", unsafe_allow_html=True)
    search = st.text_input("🔍 Search medications...")
    for name, med in MEDICINES.items():
        if search.lower() in name.lower() or search == "":
            with st.expander(f"**{name}** — {med['class']}"):
                st.markdown(f"**Adult dose:** {med['adult_dose']}")
                st.markdown(f"**Max:** {med['max']}")
                st.markdown(f"**Uses:** {', '.join(med['uses'])}")
                st.markdown(f"**⚠ Warnings:** {'; '.join(med['warnings'])}")

elif st.session_state.page == "Glossary":
    st.markdown("<h1 class='gradient-text'>Medical Glossary</h1>", unsafe_allow_html=True)
    search = st.text_input("🔍 Search terms...")
    for term, meaning in sorted(GLOSSARY.items()):
        if search.lower() in term.lower() or search == "":
            st.markdown(f"<div class='term-card'><div class='term-name'>{term}</div><div class='term-meaning'>{meaning}</div></div>", unsafe_allow_html=True)

elif st.session_state.page == "Profile":
    st.markdown("<h1 class='gradient-text'>Your Profile</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown(f"### 👤 {st.session_state.user_name}")
    st.markdown(f"**Email:** {st.session_state.user_email}")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("### Session Stats")
    c1, c2, c3 = st.columns(3)
    c1.metric("Messages", len(st.session_state.chat_history))
    c2.metric("Reports", 1 if st.session_state.report_data else 0)
    c3.metric("BMI Saved", "Yes" if st.session_state.bmi else "No")
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        logout()

st.markdown("""
<div style='text-align:center; color:#64748B; padding: 3rem 0 1rem 0; font-size:0.8rem;'>
    MediGuide Pro © 2026 — Premium AI Health Companion<br>
    <span style='color:#475569; font-size:0.75rem;'>Built with ❤️ by a small team of passionate student developers</span>
</div>
""", unsafe_allow_html=True)