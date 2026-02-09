import streamlit as st
import requests
import pandas as pd


st.set_page_config(
    page_title="HOSPITAL INQUIRY",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    :root {
        --bg-dark: #050810;
        --card-bg: rgba(16, 24, 40, 0.4);
        --accent-blue: #38bdf8;
        --accent-glow: rgba(56, 189, 248, 0.25);
        --text-main: #f1f5f9;
        --text-dim: #94a3b8;
        --border-glow: rgba(56, 189, 248, 0.15);
    }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-dark);
        color: var(--text-main);
    }

    /* Professional Sidebar */
    [data-testid="stSidebar"] {
        background-color: #080c16;
        border-right: 1px solid rgba(255, 255, 255, 0.03);
    }
    
    /* Animation Keyframes */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 15px rgba(56, 189, 248, 0.05); }
        50% { box-shadow: 0 0 30px rgba(56, 189, 248, 0.15); }
        100% { box-shadow: 0 0 15px rgba(56, 189, 248, 0.05); }
    }

    /* Global Glassmorphism Card Style */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .glass-card:hover {
        border-color: var(--accent-blue);
        transform: translateY(-5px);
        box-shadow: 0 15px 45px rgba(56, 189, 248, 0.1);
    }

    /* Medical Custom Metrics (Bio-Cards) */
    .bio-card {
        background: rgba(255, 255, 255, 0.02);
        padding: 18px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
        animation: float 4s ease-in-out infinite;
    }
    .bio-val { font-size: 1.6rem; font-weight: 700; color: #fff; text-shadow: 0 2px 10px rgba(56, 189, 248, 0.3); }
    .bio-lbl { color: var(--text-dim); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.15em; font-weight: 600; }
    .bio-icon { font-size: 1.2rem; color: var(--accent-blue); margin-bottom: 2px; }

    /* Decision Protocol Styling */
    .decision-container {
        border-radius: 20px;
        padding: 24px;
        background: radial-gradient(circle at top left, rgba(56, 189, 248, 0.08), transparent);
        border: 1px solid rgba(56, 189, 248, 0.15);
        animation: pulse-glow 6s infinite ease-in-out;
    }

    /* Top Banner Refinement */
    .dash-header {
        background: linear-gradient(135deg, #0f172a 0%, #070b14 100%);
        padding: 45px;
        border-radius: 30px;
        margin-bottom: 35px;
        border-bottom: 2px solid var(--accent-blue);
        position: relative;
        overflow: hidden;
    }
    .dash-header::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.03) 0%, transparent 60%);
        pointer-events: none;
    }

    /* Tab Aesthetics */
    .stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.02); border-radius: 12px; padding: 6px; }
    .stTabs [data-baseweb="tab"] { font-weight: 600; font-size: 0.85rem; border: none !important; }

    h1, h2, h3 { font-family: 'Outfit', sans-serif; letter-spacing: -0.01em; }
    p { line-height: 1.7; color: var(--text-dim); }
    
    hr { opacity: 0.05; border-color: #fff; }
</style>
""", unsafe_allow_html=True)


def bio_card(label, value, icon="🧬"):
    return f"""
    <div class="bio-card">
        <div class="bio-icon">{icon}</div>
        <div class="bio-val">{value}</div>
        <div class="bio-lbl">{label}</div>
    </div>
    """


if 'view' not in st.session_state: st.session_state['view'] = 'welcome'
if 'result_data' not in st.session_state: st.session_state['result_data'] = None


with st.sidebar:
    st.markdown("<h2 style='font-size: 1.5rem; margin-bottom: 20px;'>🛡️ MISSION CONTROL</h2>", unsafe_allow_html=True)
    
    
    with st.expander("👤 Patient Details", expanded=True):
        st.write("PATIENT ID.")
        p_id = st.number_input("patient ID", min_value=1, value=1001, key="p_id_input", label_visibility="collapsed")
        if st.button(" ANALYSIS", width="stretch"):
            with st.spinner("Analizing..."):
                r = requests.post("http://localhost:8000/analyze", json={"patient_id": p_id})
                if r.status_code == 200:
                    st.session_state['result_data'] = r.json()
                    st.session_state['view'] = 'patient_details'
                    st.rerun()
                else: st.error("ID Invalid")

    st.markdown("---")

    
    with st.expander(" INQUIRY", expanded=True):
        st.write(" search data.")
        query_text = st.text_area("INQUIRY", placeholder="e.g., 'c patients named ' or ' risk'", height=80, label_visibility="collapsed")
        if st.button(" SEARCH", width="stretch"):
            if query_text.strip():
                with st.spinner("Searching..."):
                    r = requests.post("http://localhost:8000/hospital/inquiry", json={"query": query_text})
                    if r.status_code == 200:
                        st.session_state['result_data'] = r.json()
                        st.session_state['view'] = 'inquiry_results'
                        st.rerun()
                    else: st.error(" Search Failed")

    st.markdown("<br>"*8, unsafe_allow_html=True)
    if st.button("🧹 RESET", width="stretch"):
        st.session_state.clear()
        st.rerun()



if st.session_state['view'] == 'welcome':
    st.markdown("""
    <div class="dash-header">
        <h1 style='margin:0; font-size: 2.8rem;'>HOSPITAL PATIENT DASHBOARD</h1>
        <p style='color: #38bdf8; font-size: 1.1rem; margin-top: 5px; font-weight: 500;'>Real-Time Intelligence & Decision Support</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1.2, 0.8])
    with col_a:
        st.markdown("""
        <div class="glass-card">
            <h3>⚡ PRO-GRADE FEATURES</h3>
            <ul style='color: #94a3b8; font-size: 1rem; line-height: 2;'>
                <li><b>Agent-Driven Query:</b> LLM parses your intent into precise SQL.</li>
                <li><b>Medical RAG:</b> Direct extraction from guidelines and policies.</li>
                <li><b>Clinical Decoder:</b> Deep risk assessment for individual patients.</li>
                <li><b>Integrated Analytics:</b> View matched records, diagnoses, and policies in one view.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.info("👋 Welcome. The System is initialized and ready for deployment. Use the Mission Control on the left to start.")

elif st.session_state['view'] == 'patient_details':
    data = st.session_state['result_data']
    ps = data['patient_summary']
    ds = data['decision_support']
    
    st.markdown(f"""
    <div class="dash-header">
        <div style="font-size: 0.8rem; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.2em; font-weight:700;">Patient Analysis Dashboard</div>
        <h1 style='margin-bottom: 0;'>{ps['patient_name']}</h1>
        <p style='color: #94a3b8;'>Internal ID: <b>{ps['patient_id']}</b> | {ps['gender']} | {ps['age']} Years | Visit: {ps['visit_date']}</p>
    </div>
    """, unsafe_allow_html=True)

  
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(bio_card("Diagnosis", ps.get("diagnosis","N/A"), "🩺"), unsafe_allow_html=True)
    c2.markdown(bio_card("Risk Rating", ps.get("risk_level","N/A"), "⚠️"), unsafe_allow_html=True)
    c3.markdown(bio_card("Priority", ps.get("care_priority","N/A"), "🏷️"), unsafe_allow_html=True)
    c4.markdown(bio_card("Vitals", f"{ps.get('blood_pressure','N/A')}", "❤️"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    
    col_l, col_chart = st.columns([1, 1.4])
    with col_l:
        st.markdown("### 🔍 CLINICAL SUPPORT")
        risk_color = "#f43f5e" if "High" in ds['decision'] else "#fbbf24" if "Medium" in ds['decision'] else "#10b981"
        st.markdown(f"""
        <div class="decision-container" style="border-left: 4px solid {risk_color};">
            <h4 style="color: {risk_color}; margin-top:0;">{ds['decision']} Protocol Active</h4>
            <div style="margin-top: 15px;">
                {"".join([f'<div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; margin-bottom: 12px; font-size: 0.95rem; border-left: 2px solid {risk_color};">{r}</div>' for r in ds['why']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📝 AI CLINICAL CONSULTATION")
        st.markdown(f"""
        <div class="glass-card" style="font-size: 1rem; line-height: 1.8; color: #cbd5e1;">
            {ds['llm_explanation']}
        </div>
        """, unsafe_allow_html=True)

    with col_chart:
        st.markdown("### 📊 VITALS TRENDVIS")
       
        import numpy as np
        chart_data = pd.DataFrame(
            np.random.randint(60, 160, size=(10, 2)),
            columns=['BP (Systolic)', 'Heart Rate']
        )
        st.area_chart(chart_data, height=300)
        
        st.markdown("### 📚 PDF CLINICAL EVIDENCE")
        for ev in data.get("pdf_evidence", {}).get("clinical_evidence", []):
            st.success(ev)

elif st.session_state['view'] == 'inquiry_results':
    res = st.session_state['result_data']
    mode = res.get("display_mode", "ANALYTICS_GRID")
    
    st.markdown(f"""
    <div class="dash-header" style="padding: 25px;">
        <h2 style='margin:0;'>INQUIRY AGENT REPORT</h2>
        <p style='color: #94a3b8; font-size:0.9rem;'>Mode: <span style="color:#38bdf8; font-weight:600;">{mode.replace('_', ' ')}</span> | Query: <i>"{res['query']}"</i></p>
    </div>
    """, unsafe_allow_html=True)

   
    if mode == "PATIENT_SPOTLIGHT" and res['total_count'] > 0:
        p = res['matched_records'][0]
        st.markdown(f"### 🎯 Subject Spotlight: {p['patient_name']}")
        
        col_main, col_stats = st.columns([1.5, 1])
        with col_main:
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
                    {bio_card("Diagnosis", p['diagnosis'], "🩺")}
                    {bio_card("Risk", p['risk_level'], "⚠️")}
                    {bio_card("Meds", p.get('medication','N/A'), "💊")}
                    {bio_card("Score", p.get('care_priority','N/A'), "📈")}
                </div>
                <hr style="margin: 25px 0; opacity: 0.1;">
                <h4 style="margin-top:0;">🤖 AGENT SUMMARY</h4>
                <p style="color:#cbd5e1; line-height:1.7;">{res['deep_explanation']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col_stats:
            st.markdown("#### Vitals Visualization")
            import numpy as np
            st.area_chart(np.random.randint(60, 150, size=(10, 1)), height=180)
            
            st.markdown("#### Clinical Guidelines")
            for ev in res['pdf_evidence']['clinical_evidence'][:3]:
                st.success(ev)
            if res['pdf_evidence']['insurance_evidence']:
                st.markdown("#### Policy snapshot")
                for ev in res['pdf_evidence']['insurance_evidence'][:2]:
                    st.warning(ev)

    
    elif mode == "POLICY_FOCUS":
        st.markdown("### 🛡️ Policy & Coverage Deep-Dive")
        
        tab_ev, tab_ai = st.tabs(["📚 EVIDENCE PROTOCOLS", "🤖 CLINICAL INTERPRETATION"])
        with tab_ev:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### 📘 Guidelines")
                for e in res['pdf_evidence']['clinical_evidence']: st.success(e)
            with c2:
                st.markdown("#### 📜 Policy Clauses")
                if res['pdf_evidence']['insurance_evidence']:
                    for e in res['pdf_evidence']['insurance_evidence']: st.warning(e)
                else: st.info("No specific policy clauses detected.")
        
        with tab_ai:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid #38bdf8;">
                {res['deep_explanation']}
            </div>
            """, unsafe_allow_html=True)

  
    else:
        st.markdown(f"### 👥 Analytics Matrix (Subjects: {res['total_count']})")
        
        tab_list, tab_matrix = st.tabs(["📋 PATIENT ROSTER", "🤖 MATRIX EXPLORER"])
        with tab_list:
            if res['total_count'] > 0:
                df = pd.DataFrame(res['matched_records'])
                relevant_cols = ["patient_name", "age", "gender", "diagnosis", "risk_level", "care_priority", "medication"]
                display_cols = [c for c in relevant_cols if c in df.columns]
                st.dataframe(df[display_cols], width="stretch")
            else: st.warning("No subjects matched the search matrix.")

        with tab_matrix:
            col_l, col_r = st.columns([1, 1])
            with col_l:
                st.markdown("#### Neural Summary")
                st.markdown(f"""<div class="glass-card">{res['deep_explanation']}</div>""", unsafe_allow_html=True)
            with col_r:
                st.markdown("#### Policy Context")
                if res['pdf_evidence']['insurance_evidence']:
                    for e in res['pdf_evidence']['insurance_evidence']: st.warning(e)
                else: st.info("No specific insurance context for this group.")
