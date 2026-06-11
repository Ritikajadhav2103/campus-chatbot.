import streamlit as st
import json
import os
import time
from datetime import datetime
from auth_utils import register_user, verify_login

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

st.set_page_config(
    page_title="Solapur Colleges Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Session State ────────────────────────────────────────────────────────────
for key, default in [("authenticated", False), ("user_name", ""), ("user_email", ""),
                     ("page", "login"), ("messages", []), ("campus_messages", []),
                     ("groq_key", "")]:
    if key not in st.session_state:
        st.session_state[key] = default

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
.user-bubble {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; padding: 0.9rem 1.3rem;
    border-radius: 20px 20px 5px 20px;
    margin: 0.5rem 0 0.5rem auto; max-width: 72%;
    box-shadow: 0 4px 10px rgba(102,126,234,0.3);
    word-wrap: break-word;
}
.bot-bubble {
    background: white; color: #333;
    padding: 0.9rem 1.3rem;
    border-radius: 20px 20px 20px 5px;
    margin: 0.5rem auto 0.5rem 0; max-width: 78%;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    word-wrap: break-word; line-height: 1.6;
}
.timestamp { font-size: 0.68rem; color: #aaa; margin-top: 0.3rem; }
.chip {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white; padding: 0.25rem 0.75rem;
    border-radius: 20px; margin: 0.2rem;
    font-size: 0.8rem; font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ─── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    with open("solapur_colleges_database.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    colleges = []
    for category in data.get("categories", {}).values():
        colleges.extend(category.get("colleges", []))
    return data, colleges

# ─── Rich Knowledge Base ───────────────────────────────────────────────────────
# Extra info that augments the JSON database for richer answers
EXTRA_INFO = {
    "WIT": {
        "hostel": "WIT has separate hostels for boys and girls. Boys hostel accommodates 300+ students with mess, WiFi, 24/7 security and gym. Girls hostel accommodates 200+ students with warden, CCTV, mess and recreation room.",
        "fees": "Engineering B.Tech: ₹1,10,000 – ₹1,40,000 per year depending on branch. Management quota seats have higher fees. Scholarships available for meritorious and backward-class students.",
        "placement": "WIT has an excellent placement record. Average package: ₹4–6 LPA, highest: ₹18 LPA. Top recruiters: TCS, Infosys, Wipro, Cognizant, L&T, Persistent, Capgemini. 85%+ students placed annually.",
        "courses": "B.Tech in Computer Science, IT, Mechanical, Civil, Electronics, Electrical, Chemical. M.Tech in CSE and Mechanical. MBA program also available.",
        "facilities": "Central library with 50,000+ books, e-journals. 20+ computer labs, robotics lab, IoT lab, innovation hub. Sports complex with cricket ground, basketball, volleyball. Cafeteria, medical room, NSS, NCC.",
        "admission": "Admission through MHT-CET / JEE Main score. Apply via CAP rounds on dtemaharashtra.gov.in. Management quota (20%) direct admission. Cut-off varies: CSE ~150 in MHT-CET percentile.",
        "history": "Established in 1947, WIT is one of the oldest and most prestigious engineering colleges in Solapur. Affiliated to Solapur University. NAAC A grade, NBA accredited for major branches.",
        "ranking": "Ranked among top 10 engineering colleges in Maharashtra. NIRF rank 201-300 band.",
        "accreditation": "NAAC A grade, NBA accredited for CSE, Mechanical, Civil branches. ISO 9001:2015 certified.",
    },
    "Orchid Engineering": {
        "hostel": "Orchid has separate hostels for boys and girls with modern amenities — WiFi, mess, laundry, 24/7 security and CCTV.",
        "fees": "B.Tech: ₹90,000 – ₹1,20,000 per year. Scholarships available under government schemes.",
        "placement": "Active placement cell. Recruiters include TCS, Infosys, Wipro, HCL. Average package ₹3.5–5 LPA.",
        "courses": "B.Tech: CSE, IT, Mechanical, Civil, Electronics. M.Tech available in select branches.",
        "facilities": "Well-stocked library, computer labs, mechanical and civil workshops, seminar halls, sports ground.",
        "admission": "MHT-CET / JEE Main based. CAP rounds via DTE Maharashtra.",
        "history": "Established in 2008. Affiliated to Solapur University. Known for strong industry connections.",
    },
    "AGPIT": {
        "hostel": "Hostel facility available for both boys and girls with mess and WiFi.",
        "fees": "B.Tech: ₹85,000 – ₹1,10,000 per year.",
        "placement": "Placement cell active. Companies like TCS, Wipro, Infosys visit regularly.",
        "courses": "B.Tech: CSE, Mechanical, Civil, Electronics, IT.",
        "facilities": "Library, computer labs, workshops, sports ground, canteen.",
        "admission": "MHT-CET / JEE Main. Apply through DTE CAP rounds.",
    },
    "Solapur University": {
        "hostel": "University has hostel facilities for boys and girls on campus.",
        "fees": "UG fees: ₹15,000–₹40,000/year. PG fees: ₹20,000–₹60,000/year depending on course.",
        "courses": "100+ UG, PG and Ph.D. programs across Science, Commerce, Arts, Engineering, Law, Education.",
        "facilities": "Massive central library, research centres, sports complex, conference halls, WiFi campus.",
        "admission": "UG: 12th marks based + entrance for professional courses. PG: Graduation marks + SET/NET. Apply at su.ac.in.",
        "history": "Established in 2004. Affiliates 250+ colleges across Solapur and Osmanabad districts.",
    },
    "Govt Medical College": {
        "hostel": "Hostel available for MBBS and PG medical students with mess facility.",
        "fees": "MBBS: ₹30,000–₹70,000/year (government college, heavily subsidised). PG: varies by specialization.",
        "courses": "MBBS, MD, MS in various specializations — Surgery, Medicine, Paediatrics, Gynaecology, etc.",
        "facilities": "Attached 1000+ bed hospital, labs, dissection hall, library, sports ground.",
        "admission": "NEET rank based. State quota through DMER Maharashtra. Management quota through university.",
        "placement": "Graduates join government hospitals, do PG entrance exams, or pursue MS/MD. High demand for government doctors.",
    },
    "HN Commerce College": {
        "fees": "B.Com: ₹10,000–₹20,000/year. M.Com: ₹15,000–₹25,000/year.",
        "courses": "B.Com, M.Com, BBA, MBA, CA Foundation coaching.",
        "facilities": "Commerce labs, library, seminar hall, sports.",
        "admission": "12th Commerce stream. Direct admission based on marks.",
        "placement": "Students placed in banking, finance, accounting firms. CA firms actively recruit.",
    },
}

# General Solapur knowledge for questions not about a specific college
GENERAL_KNOWLEDGE = {
    "solapur": "Solapur is a major educational hub in Maharashtra. It has 2 universities, 7+ engineering colleges, 4 medical colleges, 4 commerce colleges, and 15+ arts/science colleges. Total 30+ institutions serving 1 lakh+ students.",
    "engineering": "Top engineering colleges in Solapur: 1) WIT (est. 1947, NAAC A), 2) Orchid Engineering, 3) AGPIT, 4) Sinhgad COE, 5) KBP Engineering, 6) DYP Engineering, 7) Govt Polytechnic. Admission through MHT-CET/JEE Main via DTE Maharashtra CAP rounds.",
    "medical": "Medical colleges in Solapur: 1) Dr. Vaishampayan Memorial Govt Medical College (MBBS, govt), 2) Ashwini Rural Medical College (private), 3) PDU Dental College (BDS), 4) Solapur Institute of Nursing. Admission through NEET.",
    "commerce": "Commerce colleges: 1) HN Commerce College, 2) Sangameshwar College, 3) KPMIMDR (MBA), 4) Siddheshwar Commerce College. Offer B.Com, M.Com, BBA, MBA programs.",
    "arts_science": "Arts & Science colleges: Dayanand College, Walchand College of Arts & Science, Global Village College, Siddheshwar College, Shivaji Mahavidyalaya. Offer BA, B.Sc, MA, M.Sc programs.",
    "neet": "For MBBS in Solapur, clear NEET. Govt Medical College requires ~500+ marks. Private colleges have lower cut-offs. Apply through DMER Maharashtra (dmer.org).",
    "mhtcet": "MHT-CET is required for engineering admission in Maharashtra. Apply at mahacet.org. Then participate in DTE CAP rounds at dtemaharashtra.gov.in for college allotment.",
    "scholarship": "Scholarships available: EBC (Economically Backward Class), OBC, SC/ST government scholarships. Apply via mahadbt.maharashtra.gov.in. Most colleges also have merit scholarships.",
    "affiliation": "Most Solapur colleges are affiliated to Punyashlok Ahilyadevi Holkar Solapur University (su.ac.in). MIT VPU is autonomous. Medical colleges affiliated to Maharashtra University of Health Sciences (MUHS).",
}

# ─── Intent & Search Engine ────────────────────────────────────────────────────
INTENTS = {
    "hostel":     ["hostel", "accommodation", "dormitory", "stay", "residence", "boarding", "pg", "room", "lodge"],
    "fees":       ["fee", "fees", "cost", "price", "charge", "tuition", "expense", "money", "rupee", "payment"],
    "courses":    ["course", "courses", "program", "branch", "department", "stream", "degree", "subject", "btech", "mtech", "bcom", "mba", "mbbs", "ba", "bsc"],
    "admission":  ["admission", "admit", "join", "enroll", "eligibility", "entrance", "apply", "cut off", "cutoff", "procedure", "mhtcet", "neet", "jee", "cap round"],
    "placement":  ["placement", "job", "recruit", "company", "package", "salary", "career", "lpa", "campus", "hire"],
    "facilities": ["facilit", "infrastructure", "lab", "library", "sport", "gym", "wifi", "canteen", "campus", "amenity"],
    "location":   ["location", "address", "where", "situated", "area", "map", "direction", "distance"],
    "contact":    ["contact", "phone", "mobile", "call", "email", "mail", "reach", "number", "website"],
    "history":    ["history", "established", "founded", "about", "overview", "background", "naac", "nba", "rank", "accredit"],
    "hostel":     ["hostel", "accommodation", "dormitory", "stay", "residence", "boarding", "pg", "room", "lodge"],
}

CATEGORY_KEYWORDS = {
    "engineering": ["engineering", "engineer", "btech", "b.tech", "polytechnic", "technical", "iit", "mhtcet"],
    "medical":     ["medical", "mbbs", "doctor", "neet", "nursing", "dental", "medicine", "bds", "health"],
    "commerce":    ["commerce", "bcom", "b.com", "management", "mba", "bba", "business", "ca", "finance"],
    "arts_science":["arts", "science", "bsc", "b.sc", "ba", "humanities", "physics", "chemistry"],
    "universities":["university", "universities"],
    "all":         ["all colleges", "list all", "show all", "every college", "colleges in solapur"],
}

GREETINGS = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "namaste", "hii", "hlo"]
THANKS     = ["thank", "thanks", "thank you", "thnk", "thx", "great", "nice", "awesome", "good"]
HELP_WORDS = ["help", "what can you do", "how to use", "guide", "options"]

def detect_intents(query):
    q = query.lower()
    return [intent for intent, kws in INTENTS.items() if any(k in q for k in kws)]

def detect_category(query):
    q = query.lower()
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(k in q for k in kws):
            return cat
    return None

def build_search_index(colleges):
    """Pre-build a fast lookup: short_name_lower -> college"""
    return {c["short_name"].lower(): c for c in colleges}

def find_college(query, colleges, index):
    q = query.lower()
    words = set(q.split())

    # 1. Exact short name
    if q in index: return index[q]
    # 2. Short name as word in query
    for sn, c in index.items():
        if sn in words: return c
    # 3. Short name words all in query
    for sn, c in index.items():
        sn_words = set(sn.split())
        if sn_words and sn_words.issubset(words): return c
    # 4. College full name contains query or vice versa
    for c in colleges:
        if q in c["name"].lower() or c["name"].lower() in q: return c
    # 5. 2+ name words match
    for c in colleges:
        name_words = set(c["name"].lower().split())
        if len(words & name_words) >= 2: return c
    return None

def get_extra(short_name, intent):
    return EXTRA_INFO.get(short_name, {}).get(intent, None)

# ─── Response Builder ──────────────────────────────────────────────────────────
def _build_college_response(college, intents, query):
    """Build response for a specific college with optional intent."""
    sn   = college["short_name"]
    name = college["name"]

    if intents:
        intent = intents[0]
        extra  = get_extra(sn, intent)

        if intent == "hostel":
            text = extra or ""
            if not extra:
                hostel_facs = [f for f in college.get("facilities", []) if "hostel" in f.lower()]
                text = "\n".join(f"• {f}" for f in hostel_facs) if hostel_facs else "• Hostel available — contact college for details."
                text += f"\n\n📞 {college.get('contact','N/A')} | 🌐 {college.get('website','N/A')}"
            return {"type": "text", "text": f"🏠 **Hostel — {name}**\n\n{text}"}

        if intent == "fees":
            text = extra or f"Please contact the college for exact fee structure.\n📞 {college.get('contact','N/A')}"
            return {"type": "text", "text": f"💰 **Fee Structure — {name}**\n\n{text}"}

        if intent == "courses":
            extra_text = extra or ""
            courses = college.get("courses", [])
            course_list = "\n".join(f"• {c}" for c in courses) if courses else "• Contact college for course details."
            return {"type": "text", "text": f"📚 **Courses at {name}**\n\n{course_list}\n\n{extra_text}".strip()}

        if intent == "admission":
            text = extra or f"Admission at {name} is based on entrance exam scores."
            text += f"\n\n🌐 {college.get('website','N/A')}\n📞 {college.get('contact','N/A')}"
            return {"type": "text", "text": f"📝 **Admission — {name}**\n\n{text}"}

        if intent == "placement":
            text = extra or f"Active placement cell. Visit website for latest records.\n🌐 {college.get('website','N/A')}"
            return {"type": "text", "text": f"💼 **Placements — {name}**\n\n{text}"}

        if intent == "facilities":
            extra_text = extra or ""
            facs = college.get("facilities", [])
            fac_list = "\n".join(f"• {f}" for f in facs) if facs else "• Contact college for facility details."
            return {"type": "text", "text": f"🏫 **Facilities at {name}**\n\n{fac_list}\n\n{extra_text}".strip()}

        if intent == "location":
            return {"type": "text", "text": f"📍 **Location — {name}**\n\n{college.get('location','N/A')}\n\n🌐 {college.get('website','N/A')}"}

        if intent == "contact":
            return {"type": "text", "text": f"📞 **Contact — {name}**\n\n📍 {college.get('location','N/A')}\n📞 {college.get('contact','N/A')}\n📧 {college.get('email','N/A')}\n🌐 {college.get('website','N/A')}"}

        if intent == "history":
            text      = get_extra(sn, "history") or college.get("description", "Information not available.")
            rank      = get_extra(sn, "ranking") or ""
            accr      = get_extra(sn, "accreditation") or college.get("affiliation", "")
            extra_str = (f"\n\n🏅 **Ranking:** {rank}" if rank else "") + (f"\n🎖️ **Accreditation:** {accr}" if accr else "")
            return {"type": "text", "text": f"📖 **About {name}**\n\n{text}{extra_str}"}

    # No intent — show full college card with ALL details
    return {"type": "college", "college": college, "text": f"Here's everything about **{name}**:"}


def build_response(query, colleges, data, index):
    q = query.lower().strip()
    words = set(q.split())

    # Greeting — word boundary check only
    if any(g == q or q.startswith(g + " ") or q == g for g in GREETINGS) or words.issubset(set(GREETINGS)):
        return {"type": "text", "text": "👋 Hello! I'm your Solapur Colleges Assistant. I can help you with:\n\n• College courses & admissions\n• Fees structure\n• Hostel facilities\n• Placement records\n• Contact & location details\n\nJust ask something like *\"Tell me about WIT\"* or *\"Engineering colleges in Solapur\"*!"}

    # Thanks
    if any(t in words for t in THANKS):
        return {"type": "text", "text": "😊 You're welcome! Feel free to ask anything about colleges in Solapur. I'm here to help!"}

    # Help
    if any(h in q for h in HELP_WORDS):
        return {"type": "text", "text": "🤖 **What I can help with:**\n\n**College Info:**\n• Tell me about WIT / Orchid / AGPIT\n• WIT courses / fees / hostel / placement\n\n**Category Search:**\n• Engineering colleges in Solapur\n• Medical colleges / Commerce colleges\n\n**Admission Help:**\n• How to get admission in WIT\n• MHT-CET cutoff for engineering\n\n**Comparisons:**\n• Best engineering college in Solapur\n• Government vs private college fees\n\nJust type your question naturally!"}

    # ── If query is clearly about a specific college, handle it directly ──
    _early_college = find_college(query, colleges, index)
    _early_intents = detect_intents(query)
    if _early_college:
        return _build_college_response(_early_college, _early_intents, query)

    # Best / comparison queries (before college search)
    if "best" in q:
        return {"type": "text", "text": "🏆 **Top Colleges in Solapur:**\n\n**Engineering:** WIT (NAAC A, est. 1947) is the most reputed. Orchid, AGPIT, Sinhgad COE are also excellent.\n\n**Medical:** Govt Medical College is top choice (subsidised MBBS). Ashwini Medical College for private MBBS.\n\n**Commerce/MBA:** HN Commerce College & KPMIMDR are highly regarded.\n\n**University:** Solapur University (state) and MIT VPU (private autonomous)."}

    if ("compare" in q or "vs" in q) and not find_college(query, colleges, index):
        return {"type": "text", "text": "🔍 To compare colleges, ask me specifically:\n• *\"WIT vs Orchid College fees\"*\n• *\"WIT placement vs AGPIT\"*\n\nOr ask about each college individually!"}

    # Government / private filter
    if ("government" in q or "govt" in q) and not find_college(query, colleges, index):
        govt = [c for c in colleges if "government" in c.get("type","").lower() or "govt" in c["name"].lower() or "government" in c["name"].lower()]
        if govt:
            return {"type": "list", "colleges": govt, "text": f"🏛️ **Government colleges in Solapur ({len(govt)}):**"}

    if "private" in q and not find_college(query, colleges, index):
        private = [c for c in colleges if "private" in c.get("type","").lower()]
        if private:
            return {"type": "list", "colleges": private, "text": f"🏢 **Private colleges in Solapur ({len(private)}):**"}

    # Category search — BEFORE general knowledge so "engineering"/"medical" show list
    cat = detect_category(query)
    if cat and not find_college(query, colleges, index):
        cat_map = {"engineering":"engineering","medical":"medical",
                   "commerce":"commerce_management","arts_science":"arts_science","universities":"universities"}
        if cat == "all":
            cat_colleges = colleges
        else:
            cat_key = cat_map.get(cat)
            cat_colleges = data["categories"].get(cat_key, {}).get("colleges", []) if cat_key else []
        if cat_colleges:
            label = cat.replace("_", " ").title()
            return {"type": "list", "colleges": cat_colleges,
                    "text": f"🎓 **{label} Colleges in Solapur ({len(cat_colleges)}):**"}

    # Find specific college
    college = find_college(query, colleges, index)
    intents = detect_intents(query)

    if college:
        return _build_college_response(college, intents, query)

    # General Solapur knowledge (fallback for specific topic queries)
    for key, info in GENERAL_KNOWLEDGE.items():
        if key in q:
            return {"type": "text", "text": f"ℹ️ {info}"}

    # Fallback with suggestions
    return {"type": "suggest", "text": "🤔 I didn't quite get that. Try asking:\n\n• *\"Tell me about WIT\"*\n• *\"Fees of Orchid Engineering\"*\n• *\"Engineering colleges in Solapur\"*\n• *\"Hostel in AGPIT\"*\n• *\"Medical colleges\"*\n• *\"Best college in Solapur\"*"}

# ─── Auth Pages ────────────────────────────────────────────────────────────────
def show_login():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div style='text-align:center; padding:2rem 0 1.5rem 0;'>
            <span style='font-size:3.5rem;'>🎓</span>
            <h2 style='color:#667eea; margin:0.5rem 0 0.3rem 0;'>Welcome Back</h2>
            <p style='color:#888; margin:0;'>Login to Solapur Colleges Chatbot</p>
        </div>""", unsafe_allow_html=True)

        with st.form("login_form"):
            email    = st.text_input("📧 Email", placeholder="your.email@example.com")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            submit   = st.form_submit_button("🚀 Login", use_container_width=True)
            if submit:
                if email and password:
                    ok, result = verify_login(email, password)
                    if ok:
                        st.session_state.authenticated = True
                        st.session_state.user_name  = result
                        st.session_state.user_email = email
                        st.session_state.page       = "chatbot"
                        st.rerun()
                    else:
                        st.error(f"❌ {result}")
                else:
                    st.warning("⚠️ Please fill in all fields")

        st.markdown("<p style='text-align:center; color:#888; margin-top:1rem;'>Don't have an account?</p>", unsafe_allow_html=True)
        if st.button("📝 Create Account", use_container_width=True, key="go_signup"):
            st.session_state.page = "signup"
            st.rerun()

def show_signup():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div style='text-align:center; padding:2rem 0 1.5rem 0;'>
            <span style='font-size:3.5rem;'>📝</span>
            <h2 style='color:#667eea; margin:0.5rem 0 0.3rem 0;'>Create Account</h2>
            <p style='color:#888; margin:0;'>Join Solapur Colleges Chatbot</p>
        </div>""", unsafe_allow_html=True)

        with st.form("signup_form"):
            name             = st.text_input("👤 Full Name", placeholder="John Doe")
            email            = st.text_input("📧 Email", placeholder="your.email@example.com")
            password         = st.text_input("🔒 Password", type="password", placeholder="At least 6 characters")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter password")
            submit           = st.form_submit_button("✨ Sign Up", use_container_width=True)
            if submit:
                if name and email and password and confirm_password:
                    if password != confirm_password:
                        st.error("❌ Passwords don't match!")
                    else:
                        ok, msg = register_user(name, email, password)
                        if ok:
                            st.success(f"✅ {msg} Please login.")
                            st.session_state.page = "login"
                            time.sleep(0.8)
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
                else:
                    st.warning("⚠️ Please fill in all fields")

        st.markdown("<p style='text-align:center; color:#888; margin-top:1rem;'>Already have an account?</p>", unsafe_allow_html=True)
        if st.button("🔙 Back to Login", use_container_width=True, key="go_login"):
            st.session_state.page = "login"
            st.rerun()

# ─── Chatbot Page ──────────────────────────────────────────────────────────────
def show_chatbot():
    data, colleges = load_data()
    index = build_search_index(colleges)

    # Header
    hcol1, hcol2 = st.columns([5, 1])
    with hcol1:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
                    padding:1.5rem 2rem; border-radius:15px; color:white;
                    box-shadow:0 8px 20px rgba(102,126,234,0.35); margin-bottom:1.5rem;'>
            <h1 style='margin:0; font-size:2rem;'>🎓 Campus Assistant</h1>
            <p style='margin:0.3rem 0 0 0; opacity:0.9;'>
                Hi {st.session_state.user_name}! College info + AI student assistant in one place.
            </p>
        </div>""", unsafe_allow_html=True)
    with hcol2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            for k in ["authenticated","user_name","user_email","messages","campus_messages"]:
                st.session_state[k] = False if k == "authenticated" else ([] if k in ["messages","campus_messages"] else "")
            st.session_state.page = "login"
            st.rerun()

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2 = st.tabs(["🏫 College Info", "🧠 EduMentor AI"])

    # ═══════════════════════════════════════════════════
    # TAB 1 — College Info
    # ═══════════════════════════════════════════════════
    with tab1:
        _show_college_tab(data, colleges, index)

    # ═══════════════════════════════════════════════════
    # TAB 2 — CampusBot
    # ═══════════════════════════════════════════════════
    with tab2:
        _show_campusbot_tab()


def _show_college_tab(data, colleges, index):
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚡ Quick Actions")
        quick = {
            "🏛️ Universities":   "Universities in Solapur",
            "⚙️ Engineering":    "Engineering colleges",
            "🏥 Medical":        "Medical colleges",
            "💼 Commerce/MBA":   "Commerce colleges",
            "🏆 Best Colleges":  "Best college in Solapur",
            "📋 All Colleges":   "Show all colleges",
            "🏛️ Govt Colleges":  "Government colleges",
        }
        for label, q in quick.items():
            if st.button(label, key=f"qa_{label}", use_container_width=True):
                st.session_state.quick_query = q

        st.markdown("---")
        st.markdown("### 💡 Try These Questions")
        prompts = [
            "Tell me about WIT",
            "WIT placement record",
            "Hostel in Orchid College",
            "Fees of AGPIT",
            "Admission in Govt Medical",
            "Courses in Solapur University",
            "Best engineering college",
            "How to apply MHT-CET",
        ]
        for p in prompts:
            if st.button(p, key=f"p_{p}", use_container_width=True):
                st.session_state.quick_query = p

        st.markdown("---")
        st.markdown("### 💬 Chat History")
        count = len(st.session_state.messages)
        if count:
            st.markdown(f"**{count} messages**")
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        else:
            st.caption("No messages yet")

        st.markdown("---")
        st.metric("Total Colleges", len(colleges))
        st.metric("Response Time", "< 0.1s ⚡")

    # Chat area
    chat_col, tip_col = st.columns([3, 1])

    with chat_col:
        # Show messages
        for msg in st.session_state.messages:
            ts = msg.get("timestamp", "")
            if msg["role"] == "user":
                st.markdown(f'<div class="user-bubble">{msg["content"]}<div class="timestamp">{ts}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-bubble">{msg["content"]}<div class="timestamp">{ts}</div></div>', unsafe_allow_html=True)

                if "college_data" in msg:
                    _render_college_card(msg["college_data"])

                if "college_list" in msg:
                    mi = st.session_state.messages.index(msg)
                    _render_college_list(msg["college_list"], mi)

        # Input
        if "quick_query" in st.session_state:
            prompt = st.session_state.pop("quick_query")
        else:
            prompt = st.chat_input("💬 Ask about any college in Solapur...")

        if prompt:
            ts = datetime.now().strftime("%I:%M %p")
            st.session_state.messages.append({"role":"user","content":prompt,"timestamp":ts})

            resp = build_response(prompt, colleges, data, index)

            bot = {"role":"assistant","content":resp["text"],"timestamp":ts}
            if resp["type"] == "college":
                bot["college_data"] = resp["college"]
            elif resp["type"] == "list":
                bot["college_list"] = resp["colleges"]

            st.session_state.messages.append(bot)
            st.rerun()

    with tip_col:
        st.markdown("### 🗂️ Topics")
        topics = ["📚 Courses","💰 Fees","🏠 Hostel","💼 Placement",
                  "📝 Admission","🏫 Facilities","📍 Location","📞 Contact"]
        for t in topics:
            st.markdown(f"<div style='background:white;padding:0.4rem 0.8rem;border-radius:8px;margin:0.3rem 0;font-size:0.85rem;color:#333;font-weight:500;box-shadow:0 1px 3px rgba(0,0,0,0.1);'>{t}</div>", unsafe_allow_html=True)

def _show_campusbot_tab():
    SYSTEM_PROMPT = """You are EduMentor AI, an expert educational assistant for engineering and diploma students.

Specializations: Computer Engineering, IT, AI, DSA, DBMS, OS, Computer Networks, Mobile App Dev, Cyber Security, Environmental Studies, Business Economics.

Rules:
- Use simple language with bullet points
- Give exam-oriented answers and highlight important points
- For notes: Heading → Definition → Key Points → Example → Exam Tips
- For MCQs: number them, show correct answer at end
- For coding: clean commented code
- For viva: Q&A format
- End every response with: 📌 Key Points to Remember
- Be encouraging and supportive"""

    # ── Header ──
    st.markdown("""
    <div style='background:linear-gradient(135deg,#4776e6,#8e54e9);
                padding:1.2rem 1.5rem;border-radius:14px;color:white;margin-bottom:1rem;'>
        <h3 style='margin:0;font-size:1.4rem;'>🧠 EduMentor AI — Engineering Student Assistant</h3>
        <p style='margin:0.3rem 0 0 0;opacity:0.9;font-size:0.85rem;'>
            Ask any education question • Notes • MCQs • Coding • Career • Study Plans
        </p>
    </div>""", unsafe_allow_html=True)

    # ── Layout: Notes panel (left) + Chatbot (right) ──
    notes_col, chat_col = st.columns([1, 2], gap="medium")

    # ══════════════════════════════════
    # LEFT — Static Notes & Resources
    # ══════════════════════════════════
    with notes_col:
        st.markdown("### 📚 Study Resources")

        STATIC_NOTES = {
            "💻 Data Structures": {
                "color": "#4776e6",
                "topics": ["Arrays & Strings", "Linked List", "Stack & Queue", "Trees & Graphs", "Sorting & Searching", "Hashing", "Dynamic Programming"],
                "tip": "Ask: *'Notes on linked list'* or *'10 MCQs on trees'*"
            },
            "🗄️ DBMS": {
                "color": "#8e54e9",
                "topics": ["ER Diagram", "Normalization (1NF–3NF)", "SQL Queries", "Transactions & ACID", "Indexing", "NoSQL vs SQL"],
                "tip": "Ask: *'Explain normalization with example'*"
            },
            "🖥️ Operating Systems": {
                "color": "#11998e",
                "topics": ["Process & Threads", "CPU Scheduling", "Deadlock", "Memory Management", "File Systems", "Virtual Memory"],
                "tip": "Ask: *'Viva questions on deadlock'*"
            },
            "🌐 Computer Networks": {
                "color": "#f093fb",
                "topics": ["OSI Model", "TCP/IP", "IP Addressing", "Routing Protocols", "HTTP/HTTPS", "DNS & DHCP", "Firewalls"],
                "tip": "Ask: *'Explain OSI model layers'*"
            },
            "🐍 Python / Coding": {
                "color": "#fa709a",
                "topics": ["OOP Concepts", "File Handling", "Exception Handling", "List / Dict / Set", "Recursion", "Algorithms"],
                "tip": "Ask: *'Write binary search in Python'*"
            },
            "🤖 AI & ML": {
                "color": "#4facfe",
                "topics": ["Types of ML", "Supervised Learning", "Neural Networks", "Regression & Classification", "Clustering", "NLP Basics"],
                "tip": "Ask: *'Explain machine learning with example'*"
            },
            "🔒 Cyber Security": {
                "color": "#43e97b",
                "topics": ["CIA Triad", "Types of Attacks", "Encryption", "Firewalls & VPN", "Ethical Hacking", "Social Engineering"],
                "tip": "Ask: *'Notes on cyber security'*"
            },
            "🚀 Career & Placement": {
                "color": "#f5576c",
                "topics": ["Resume Tips", "Interview Prep", "Top Certifications", "Internship Platforms", "GitHub Portfolio", "Aptitude & Reasoning"],
                "tip": "Ask: *'How to prepare for campus placement'*"
            },
        }

        for subject, info in STATIC_NOTES.items():
            with st.expander(subject, expanded=False):
                color = info["color"]
                tip   = info["tip"]
                topics_html = "".join([
                    f"<div style='padding:0.35rem 0.6rem;color:#1a1a2e;font-size:0.85rem;"
                    f"background:#f0f4ff;border-radius:6px;margin:0.2rem 0;"
                    f"border-left:3px solid {color};font-weight:500;'>&#9658; {t}</div>"
                    for t in info["topics"]
                ])
                st.markdown(f"""
                <div style='background:white;border-radius:10px;padding:0.8rem;
                            border:1px solid #e8e8f0;'>
                    {topics_html}
                    <div style='margin-top:0.7rem;background:#fffbe6;padding:0.5rem 0.7rem;
                                border-radius:6px;font-size:0.78rem;color:#7a6000;
                                border-left:3px solid #f5c518;'>
                        💡 {tip}
                    </div>
                </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🎯 Quick Ask")
        quick_topics = [
            "📝 Generate DSA notes",
            "❓ 10 MCQs on DBMS",
            "🎓 OS viva questions",
            "💻 Python OOP code",
            "📅 30-day study plan",
            "🏆 Placement tips",
            "🔐 Cyber security notes",
            "🤖 Explain AI/ML basics",
        ]
        for qt in quick_topics:
            if st.button(qt, key=f"qnote_{qt}", use_container_width=True):
                st.session_state.campus_quick = qt.split(" ", 1)[1]

    # ══════════════════════════════════
    # RIGHT — AI Chatbot
    # ══════════════════════════════════
    with chat_col:
        st.markdown("### 💬 Ask EduMentor AI")

        # API Key
        if not st.session_state.groq_key:
            st.markdown("""
            <div style='background:#f0f4ff;border-radius:12px;padding:1.5rem;
                        border-left:4px solid #4776e6;margin-bottom:1rem;'>
                <h4 style='color:#4776e6;margin:0 0 0.8rem 0;'>🔑 Activate EduMentor AI</h4>
                <p style='color:#555;font-size:0.9rem;margin:0 0 0.5rem 0;'>Enter your free Groq API key to start chatting:</p>
                <ol style='color:#555;font-size:0.88rem;margin:0;padding-left:1.2rem;line-height:1.8;'>
                    <li>Go to <a href='https://console.groq.com' target='_blank' style='color:#4776e6;font-weight:600;'>console.groq.com</a></li>
                    <li>Sign up free — no credit card</li>
                    <li>Create API Key → Copy it</li>
                    <li>Paste below and click Activate</li>
                </ol>
                <p style='color:#38a169;font-size:0.85rem;margin:0.8rem 0 0 0;'>✅ Free: 14,400 requests/day &nbsp;⚡ Speed: &lt;2 seconds</p>
            </div>""", unsafe_allow_html=True)

            k1, k2 = st.columns([3, 1])
            with k1:
                key_input = st.text_input("API Key", type="password",
                                          placeholder="gsk_xxxxxxxxxxxxxxxxxxxx",
                                          label_visibility="collapsed")
            with k2:
                if st.button("✅ Activate", use_container_width=True, key="activate_groq"):
                    if key_input.startswith("gsk_"):
                        st.session_state.groq_key = key_input
                        st.rerun()
                    else:
                        st.error("Must start with gsk_")
            return

        # Chat messages display
        chat_container = st.container()
        with chat_container:
            if not st.session_state.campus_messages:
                st.markdown("""
                <div style='text-align:center;padding:2rem;color:#888;'>
                    <div style='font-size:3rem;'>🧠</div>
                    <h4 style='color:#4776e6;'>EduMentor AI is ready!</h4>
                    <p style='font-size:0.9rem;'>Ask me anything about your studies.<br>
                    Use the quick prompts on the left or type your own question below.</p>
                    <div style='display:flex;flex-wrap:wrap;gap:0.5rem;justify-content:center;margin-top:1rem;'>
                        <span style='background:#eef2ff;color:#4776e6;padding:0.3rem 0.8rem;border-radius:20px;font-size:0.8rem;'>📚 Notes</span>
                        <span style='background:#f3e8ff;color:#8e54e9;padding:0.3rem 0.8rem;border-radius:20px;font-size:0.8rem;'>❓ MCQs</span>
                        <span style='background:#e8fff3;color:#11998e;padding:0.3rem 0.8rem;border-radius:20px;font-size:0.8rem;'>💻 Coding</span>
                        <span style='background:#fff0f6;color:#f5576c;padding:0.3rem 0.8rem;border-radius:20px;font-size:0.8rem;'>🚀 Career</span>
                        <span style='background:#e8f4ff;color:#4facfe;padding:0.3rem 0.8rem;border-radius:20px;font-size:0.8rem;'>🎓 Viva</span>
                    </div>
                </div>""", unsafe_allow_html=True)

            for msg in st.session_state.campus_messages:
                ts = msg.get("ts", "")
                if msg["role"] == "user":
                    st.markdown(f'<div class="user-bubble">{msg["content"]}<div class="timestamp">{ts}</div></div>',
                                unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bot-bubble" style="max-width:95%;">{msg["content"]}<div class="timestamp">{ts}</div></div>',
                                unsafe_allow_html=True)

        # Input area
        if "campus_quick" in st.session_state:
            user_input = st.session_state.pop("campus_quick")
        else:
            user_input = st.chat_input("💬 Ask anything — notes, MCQs, coding, career, exams...")

        if user_input:
            ts = datetime.now().strftime("%I:%M %p")
            st.session_state.campus_messages.append({"role": "user", "content": user_input, "ts": ts})

            try:
                client = Groq(api_key=st.session_state.groq_key)
                messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                for m in st.session_state.campus_messages[-8:]:
                    messages.append({"role": m["role"], "content": m["content"]})

                with st.spinner("🧠 EduMentor is thinking..."):
                    resp = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=messages,
                        max_tokens=1500,
                        temperature=0.7,
                    )
                answer = resp.choices[0].message.content

            except Exception as e:
                err = str(e)
                if "invalid_api_key" in err or "401" in err:
                    answer = "❌ Invalid API key. Please check your Groq key."
                    st.session_state.groq_key = ""
                elif "rate_limit" in err:
                    answer = "⏳ Rate limit hit. Please wait a moment and try again."
                else:
                    answer = f"❌ Error: {err}"

            st.session_state.campus_messages.append({"role": "assistant", "content": answer, "ts": ts})
            st.rerun()

        # Bottom controls
        if st.session_state.campus_messages:
            bc1, bc2 = st.columns([3, 1])
            with bc2:
                if st.button("🗑️ Clear Chat", key="clear_campus", use_container_width=True):
                    st.session_state.campus_messages = []
                    st.rerun()
            with bc1:
                st.caption(f"💬 {len(st.session_state.campus_messages)} messages • Model: llama-3.1-8b-instant")


def _render_college_card(college):
    with st.container():
        sn = college["short_name"]

        # Image
        local_image = f"data/college_images/{sn.lower().replace(' ', '_')}.jpg"
        img_url = local_image if os.path.exists(local_image) else college.get(
            "photo_url", "https://images.unsplash.com/photo-1562774053-701939374585?w=800")
        st.image(img_url, use_column_width=True)

        # Data
        desc      = get_extra(sn, "history") or college.get("description", "")
        fees      = get_extra(sn, "fees") or ""
        placement = get_extra(sn, "placement") or ""
        courses   = college.get("courses", [])

        # Course badges
        badges = " ".join(
            f"<span style='display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);"
            f"color:white;padding:0.25rem 0.75rem;border-radius:20px;margin:0.2rem;"
            f"font-size:0.8rem;'>{c}</span>"
            for c in courses[:8]
        )

        # Optional sections built as strings first
        fees_html = (
            f"<h4 style='color:#333;margin:1rem 0 0.3rem 0;'>💰 Fees</h4>"
            f"<p style='color:#555;margin:0 0 0.5rem 0;'>{fees}</p>"
        ) if fees else ""

        placement_html = (
            f"<h4 style='color:#333;margin:1rem 0 0.3rem 0;'>💼 Placements</h4>"
            f"<p style='color:#555;margin:0 0 0.5rem 0;'>{placement}</p>"
        ) if placement else ""

        website = college.get("website", "#")

        st.markdown(f"""
        <div style='background:white;border-radius:0 0 18px 18px;padding:1.5rem;
                    box-shadow:0 6px 20px rgba(0,0,0,0.08);margin-bottom:1rem;'>
            <h2 style='color:#667eea;margin:0 0 0.3rem 0;'>{college['name']}</h2>
            <p style='color:#888;margin:0 0 1rem 0;font-size:0.9rem;'>
                {college.get('type','')} &nbsp;|&nbsp; Est. {college.get('established','')}
                &nbsp;|&nbsp; {college.get('affiliation','')}
            </p>
            <p style='color:#555;line-height:1.7;margin:0 0 1rem 0;'>{desc[:350]}...</p>
            <h4 style='color:#333;margin:0.5rem 0;'>📚 Courses</h4>
            <div style='margin-bottom:0.5rem;'>{badges}</div>
            {fees_html}
            {placement_html}
            <h4 style='color:#333;margin:1rem 0 0.5rem 0;'>📍 Contact</h4>
            <p style='color:#555;line-height:1.8;margin:0;'>
                📍 {college.get('location','N/A')}<br>
                📞 {college.get('contact','N/A')}<br>
                📧 {college.get('email','N/A')}
            </p>
        </div>""", unsafe_allow_html=True)

        # Use st.link_button — always opens in new tab reliably
        _, btn_col, _ = st.columns([1, 2, 1])
        with btn_col:
            st.link_button("🌐 Visit Official Website", website, use_container_width=True)

def _render_college_list(college_list, msg_i):
    TYPE_ICON = {
        "engineering": "⚙️", "medical": "🏥", "dental": "🦷",
        "commerce": "💼", "management": "📊", "university": "🏛️",
        "arts": "🎨", "science": "🔬", "nursing": "💊",
        "polytechnic": "🔧", "law": "⚖️", "pharmacy": "💉",
        "hotel": "🏨", "social": "🤝",
    }
    GRADIENTS = [
        "#667eea,#764ba2", "#f093fb,#f5576c", "#4facfe,#00f2fe",
        "#43e97b,#38f9d7", "#fa709a,#fee140", "#a18cd1,#fbc2eb",
        "#fccb90,#d57eeb", "#a1c4fd,#c2e9fb", "#fd7043,#ff8a65",
        "#26c6da,#00acc1",
    ]

    def get_icon(college):
        t = (college.get("type", "") + " " + college["name"]).lower()
        for k, icon in TYPE_ICON.items():
            if k in t:
                return icon
        return "🎓"

    for idx, college in enumerate(college_list):
        sn = college["short_name"]
        icon = get_icon(college)
        grad = GRADIENTS[idx % len(GRADIENTS)]
        fees = get_extra(sn, "fees") or ""
        placement = get_extra(sn, "placement") or ""
        courses = college.get("courses", [])[:3]
        course_tags = "".join([
            f"<span style='background:rgba(255,255,255,0.25);color:white;"
            f"padding:0.15rem 0.5rem;border-radius:8px;font-size:0.72rem;"
            f"margin:0.1rem;display:inline-block;'>{c}</span>"
            for c in courses
        ])

        note = ""
        if fees:        note = f"<div style='color:#667eea;font-size:0.8rem;margin-top:0.4rem;'>💰 {fees[:65]}...</div>"
        elif placement: note = f"<div style='color:#38a169;font-size:0.8rem;margin-top:0.4rem;'>💼 {placement[:65]}...</div>"

        st.markdown(f"""
        <div style='background:white; border-radius:18px; overflow:hidden;
                    box-shadow:0 6px 20px rgba(0,0,0,0.10); margin:0.6rem 0;
                    border:1px solid #f0f0f0;'>
            <!-- Gradient header -->
            <div style='background:linear-gradient(135deg,{grad});
                        padding:1rem 1.2rem 0.8rem 1.2rem;
                        display:flex; align-items:center; gap:1rem;'>
                <div style='font-size:2.4rem; flex-shrink:0;'>{icon}</div>
                <div style='flex:1;'>
                    <div style='color:white; font-weight:700; font-size:1rem;
                                line-height:1.3;'>{college['name']}</div>
                    <div style='margin-top:0.4rem;'>{course_tags}</div>
                </div>
            </div>
            <!-- Info row -->
            <div style='padding:0.8rem 1.2rem; display:flex; align-items:center;
                        gap:0.5rem; flex-wrap:wrap;'>
                <span style='background:#eef2ff; color:#667eea; padding:0.25rem 0.7rem;
                             border-radius:10px; font-size:0.75rem; font-weight:600;'>
                    {college.get('type','N/A')}
                </span>
                <span style='background:#f0fff4; color:#38a169; padding:0.25rem 0.7rem;
                             border-radius:10px; font-size:0.75rem; font-weight:600;'>
                    Est. {college.get('established','')}
                </span>
                <span style='color:#888; font-size:0.78rem; margin-left:auto;'>
                    📍 {college.get('location','')[:35]}...
                </span>
            </div>
            {f"<div style='padding:0 1.2rem 0.8rem 1.2rem;'>{note}</div>" if note else ""}
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"🔍 View {college['short_name']} Details", key=f"vd_{msg_i}_{idx}", use_container_width=True):
            st.session_state.quick_query = f"Tell me about {college['name']}"
            st.rerun()

# ─── Router ────────────────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    if st.session_state.page == "signup":
        show_signup()
    else:
        show_login()
else:
    show_chatbot()
