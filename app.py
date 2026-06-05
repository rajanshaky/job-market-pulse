import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sqlalchemy as sal
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Job Market Pulse", page_icon="💼", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #1a1a2e; color: #e0e0e0; }
    .stApp { background-color: #1a1a2e; }
    section[data-testid="stSidebar"] { background-color: #16213e; border-right: 1px solid #2a2a4a; }
    .kpi-card { background-color: #16213e; border: 1px solid #2a2a4a; border-radius: 8px; padding: 24px; text-align: center; }
    .kpi-value { font-size: 42px; font-weight: 700; color: #ffffff; }
    .kpi-label { font-size: 13px; color: #888; margin-top: 6px; text-transform: uppercase; letter-spacing: 0.5px; }
    .page-title { text-align: center; font-size: 22px; font-weight: 700; color: #ffffff; margin-bottom: 4px; }
    .page-subtitle { text-align: center; font-size: 13px; color: #888; margin-bottom: 6px; }
    .insight-banner { background-color: #0f3460; border-radius: 8px; padding: 14px 20px; text-align: center; font-size: 13px; color: #aac8ff; margin-bottom: 20px; }
    .section-title { font-size: 15px; font-weight: 600; color: #cccccc; margin-bottom: 4px; }
    .insight-card { background-color: #16213e; border: 1px solid #2a2a4a; border-radius: 8px; padding: 20px; height: 100%; }
    .insight-card-title { font-size: 14px; font-weight: 600; color: #aac8ff; margin-bottom: 12px; }
    .insight-item { font-size: 12px; color: #aaaaaa; margin-bottom: 8px; padding-left: 10px; border-left: 2px solid #3a6ea8; }
    .headline-card { background-color: #0f3460; border-radius: 10px; padding: 20px; text-align: center; margin-bottom: 20px; }
    .headline-main { font-size: 22px; font-weight: 700; color: #ffffff; margin-bottom: 6px; }
    .headline-sub { font-size: 13px; color: #aac8ff; }
    div[data-baseweb="select"] > div { background-color: #0f3460 !important; border: 1px solid #2a2a4a !important; border-radius: 6px !important; color: #ffffff !important; }
    div[data-baseweb="select"] span { color: #ffffff !important; }
    li[role="option"] { background-color: #16213e !important; color: #cccccc !important; }
    li[role="option"]:hover { background-color: #0f3460 !important; color: #ffffff !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_engine():
    user = os.getenv('RAILWAY_MYSQL_USER', 'root')
    password = os.getenv('RAILWAY_MYSQL_PASSWORD', '')
    host = os.getenv('RAILWAY_MYSQL_HOST', 'localhost')
    port = os.getenv('RAILWAY_MYSQL_PORT', '3306')
    database = os.getenv('RAILWAY_MYSQL_DATABASE', 'job_market')
    return sal.create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

@st.cache_data(ttl=3600)
def load_data():
    try:
        engine = get_engine()
        df = pd.read_sql("SELECT * FROM job_listings", engine)
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

PLOTLY_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(22,33,62,0.6)',
    font_color='#cccccc', font_family='Inter',
    xaxis=dict(gridcolor='#2a2a4a', linecolor='#2a2a4a'),
    yaxis=dict(gridcolor='#2a2a4a', linecolor='#2a2a4a'),
)
BAR_COLOR = '#3a7ca8'

df_full = load_data()
if df_full.empty:
    st.warning("No data available. Check your database connection.")
    st.stop()

df_full.columns = [c.lower().strip() for c in df_full.columns]
role_col    = next((c for c in df_full.columns if 'role' in c or 'keyword' in c or 'category' in c), None)
city_col    = next((c for c in df_full.columns if 'city' in c or 'location' in c), None)
company_col = next((c for c in df_full.columns if 'company' in c or 'employer' in c), None)

with st.sidebar:
    st.markdown("### 💼 Job Market Pulse")
    st.markdown("---")
    page = st.radio("Navigation", ["📊 Market Overview", "💡 Key Insights"], label_visibility="collapsed")
    st.markdown("---")
    if role_col:
        roles = sorted(df_full[role_col].dropna().unique().tolist())
        st.markdown("**Filter by Role**")
        selected_role = st.selectbox("Role", ["All Roles"] + roles, label_visibility="collapsed")
    else:
        selected_role = "All Roles"
    st.markdown("---")
    st.markdown(f"<div style='font-size:11px;color:#555'>Total listings: {len(df_full):,}</div>", unsafe_allow_html=True)

df = df_full.copy()
if selected_role != "All Roles" and role_col:
    df = df[df[role_col] == selected_role]

if page == "📊 Market Overview":
    st.markdown('<div class="page-title">Job Market Pulse</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Live data job market analysis — India</div>', unsafe_allow_html=True)
    st.markdown('<div class="insight-banner">"Data job demand is concentrated in a few metro cities, with Business Analyst roles leading overall hiring."</div>', unsafe_allow_html=True)

    total_jobs = len(df)
    total_cities = df[city_col].nunique() if city_col else 0
    total_companies = df[company_col].nunique() if company_col else 0

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_jobs:,}</div><div class="kpi-label">Total Jobs</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_cities}</div><div class="kpi-label">Total Cities</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_companies:,}</div><div class="kpi-label">Total Companies</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="section-title">Top 10 Hiring Cities</div>', unsafe_allow_html=True)
        if city_col:
            top_cities = df[city_col].value_counts().head(10).sort_values(ascending=True)
            fig = go.Figure(go.Bar(x=top_cities.values, y=top_cities.index, orientation='h',
                marker_color=BAR_COLOR, text=top_cities.values, textposition='outside',
                textfont=dict(color='#cccccc', size=10)))
            fig.update_layout(**PLOTLY_THEME, height=380, margin=dict(l=10,r=40,t=10,b=30),
                xaxis_title="Job count", yaxis_title="Cities", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            top3_pct = df[city_col].value_counts().head(3).sum() / total_jobs * 100
            st.markdown(f"<div style='font-size:12px;color:#888;text-align:center'>Bangalore leads hiring. Top 3 cities = {top3_pct:.1f}% of listings.</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Jobs by Role Type</div>', unsafe_allow_html=True)
        if role_col:
            role_counts = df[role_col].value_counts().sort_values(ascending=True)
            fig2 = go.Figure(go.Bar(x=role_counts.values, y=role_counts.index, orientation='h',
                marker_color=BAR_COLOR, text=role_counts.values, textposition='outside',
                textfont=dict(color='#cccccc', size=10)))
            fig2.update_layout(**PLOTLY_THEME, height=380, margin=dict(l=10,r=40,t=10,b=30),
                xaxis_title="Job count", yaxis_title="Roles", showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
            top_role = role_counts.idxmax()
            st.markdown(f"<div style='font-size:12px;color:#888;text-align:center'>{top_role.title()} roles lead demand.</div>", unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="section-title">Top 10 Hiring Companies</div>', unsafe_allow_html=True)
        if company_col:
            top_companies = df[company_col].value_counts().head(10).sort_values(ascending=True)
            fig3 = go.Figure(go.Bar(x=top_companies.values, y=top_companies.index, orientation='h',
                marker_color=BAR_COLOR, text=top_companies.values, textposition='outside',
                textfont=dict(color='#cccccc', size=10)))
            fig3.update_layout(**PLOTLY_THEME, height=380, margin=dict(l=10,r=40,t=10,b=30),
                xaxis_title="Job count", yaxis_title="Companies", showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown("<div style='font-size:12px;color:#888;text-align:center'>Hiring spread across many companies, with a few dominating.</div>", unsafe_allow_html=True)

elif page == "💡 Key Insights":
    st.markdown('<div class="page-title">Key Insights & Conclusions</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if city_col:
        top_city = df[city_col].value_counts().index[0]
        top_city_pct = df[city_col].value_counts().iloc[0] / len(df) * 100
        top3_pct = df[city_col].value_counts().head(3).sum() / len(df) * 100
    else:
        top_city, top_city_pct, top3_pct = "Bangalore", 29.2, 66.0

    st.markdown(f"""
    <div class="headline-card">
        <div class="headline-main">{top_city} accounts for {top_city_pct:.1f}% of total job listings.</div>
        <div class="headline-sub">Revealing strong geographic concentration in metro cities.</div>
        <div class="headline-sub">Top 3 cities account for {top3_pct:.1f}% of listings.</div>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="insight-card">
            <div class="insight-card-title">📋 Key Findings</div>
            <div class="insight-item">Jobs are concentrated in metro cities, with <strong>Bangalore</strong> leading.</div>
            <div class="insight-item"><strong>Business Analyst</strong> roles slightly outnumber other data roles.</div>
            <div class="insight-item">A few top companies account for a large share of listings.</div>
            <div class="insight-item">~22% of listings lack location data ("Not Specified").</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="insight-card">
            <div class="insight-card-title">🔍 Implications</div>
            <div class="insight-item">Job seekers may need to focus on <strong>metro cities</strong> to access the majority of opportunities.</div>
            <div class="insight-item">Developing <strong>business-focused analytical skills</strong> can improve employability.</div>
            <div class="insight-item">Distributed hiring suggests opportunities across many types of organizations.</div>
            <div class="insight-item">High concentration may increase competition in major cities.</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="insight-card">
            <div class="insight-card-title">✅ Recommendations</div>
            <div class="insight-item">Focus skill development on <strong>Business Analyst</strong> and <strong>Data Analyst</strong> roles.</div>
            <div class="insight-item">Prioritize job search in <strong>Bangalore</strong> and <strong>Hyderabad</strong>.</div>
            <div class="insight-item">Build a diverse skill set combining technical and business knowledge.</div>
            <div class="insight-item">Monitor hiring trends over time to adapt to market dynamics.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if role_col:
        st.markdown('<div class="section-title">Role Distribution Summary</div>', unsafe_allow_html=True)
        role_counts = df[role_col].value_counts()
        fig = go.Figure(go.Bar(x=role_counts.index, y=role_counts.values, marker_color=BAR_COLOR,
            text=role_counts.values, textposition='outside', textfont=dict(color='#cccccc', size=11)))
        fig.update_layout(**PLOTLY_THEME, height=300, margin=dict(l=10,r=10,t=10,b=30),
            xaxis_title="Role", yaxis_title="Job Count", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

