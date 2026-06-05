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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0d1117; color: #e0e0e0; }
    .stApp { background-color: #0d1117; }
    section[data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }

    .kpi-card {
        background: linear-gradient(135deg, #161b22 0%, #1c2333 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 28px 24px;
        text-align: center;
        transition: border-color 0.2s;
    }
    .kpi-card:hover { border-color: #58a6ff; }
    .kpi-value { font-size: 44px; font-weight: 700; color: #58a6ff; letter-spacing: -1px; }
    .kpi-label { font-size: 12px; color: #8b949e; margin-top: 6px; text-transform: uppercase; letter-spacing: 1px; font-weight: 500; }

    .hero-banner {
        background: linear-gradient(135deg, #0d1117 0%, #1c2333 50%, #0d1117 100%);
        border: 1px solid #30363d;
        border-radius: 14px;
        padding: 28px 32px;
        text-align: center;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .hero-quote {
        font-size: 18px;
        font-weight: 600;
        color: #ffffff;
        line-height: 1.5;
        margin-bottom: 8px;
    }
    .hero-sub { font-size: 13px; color: #8b949e; }

    .page-title { text-align: center; font-size: 26px; font-weight: 700; color: #ffffff; margin-bottom: 4px; letter-spacing: -0.5px; }
    .page-subtitle { text-align: center; font-size: 13px; color: #8b949e; margin-bottom: 20px; }

    .section-title { font-size: 14px; font-weight: 600; color: #c9d1d9; margin-bottom: 2px; letter-spacing: 0.2px; }
    .section-note { font-size: 11px; color: #6e7681; margin-top: 6px; text-align: center; font-style: italic; }

    .chart-card {
        background: linear-gradient(135deg, #161b22 0%, #1c2333 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 16px;
    }

    .insight-card {
        background: linear-gradient(135deg, #161b22 0%, #1c2333 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 22px;
        height: 100%;
    }
    .insight-card-title { font-size: 13px; font-weight: 600; color: #58a6ff; margin-bottom: 14px; text-transform: uppercase; letter-spacing: 0.5px; }
    .insight-item { font-size: 12px; color: #8b949e; margin-bottom: 10px; padding-left: 12px; border-left: 2px solid #21262d; line-height: 1.5; }
    .insight-item strong { color: #c9d1d9; }

    .headline-card {
        background: linear-gradient(135deg, #0d419d 0%, #1158c7 100%);
        border: 1px solid #388bfd;
        border-radius: 12px;
        padding: 24px 32px;
        text-align: center;
        margin-bottom: 24px;
    }
    .headline-main { font-size: 24px; font-weight: 700; color: #ffffff; margin-bottom: 8px; letter-spacing: -0.5px; }
    .headline-sub { font-size: 13px; color: #cae8ff; margin-top: 4px; }

    .stat-chip {
        display: inline-block;
        background: #21262d;
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 12px;
        color: #8b949e;
        margin: 4px;
    }

    div[data-baseweb="select"] > div { background-color: #21262d !important; border: 1px solid #30363d !important; border-radius: 8px !important; color: #ffffff !important; }
    div[data-baseweb="select"] span { color: #c9d1d9 !important; }
    div[data-baseweb="popover"] { background-color: #161b22 !important; border: 1px solid #30363d !important; }
    li[role="option"] { background-color: #161b22 !important; color: #c9d1d9 !important; }
    li[role="option"]:hover { background-color: #21262d !important; color: #ffffff !important; }

    .stRadio > div { gap: 8px; }
    .stRadio label { background: #21262d; border: 1px solid #30363d; border-radius: 8px; padding: 8px 14px; font-size: 13px; color: #c9d1d9; cursor: pointer; }

    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container { padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ── DB ──
@st.cache_resource
def get_engine():
    user     = os.getenv('RAILWAY_MYSQL_USER', 'root')
    password = os.getenv('RAILWAY_MYSQL_PASSWORD', '')
    host     = os.getenv('RAILWAY_MYSQL_HOST', 'localhost')
    port     = os.getenv('RAILWAY_MYSQL_PORT', '3306')
    database = os.getenv('RAILWAY_MYSQL_DATABASE', 'job_market')
    return sal.create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

@st.cache_data(ttl=3600)
def load_data():
    try:
        df = pd.read_sql("SELECT * FROM job_listings", get_engine())
        df.columns = [c.lower().strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

PLOTLY_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(22,27,34,0.8)',
    font_color='#8b949e',
    font_family='Inter',
    xaxis=dict(gridcolor='#21262d', linecolor='#30363d', tickfont=dict(color='#8b949e', size=10)),
    yaxis=dict(gridcolor='#21262d', linecolor='#30363d', tickfont=dict(color='#c9d1d9', size=10)),
)
BAR_COLOR = '#388bfd'
BAR_HOVER = '#58a6ff'

# ── LOAD ──
df_full = load_data()
if df_full.empty:
    st.warning("No data available. Check your database connection.")
    st.stop()

# Correct columns
role_col    = 'search_keyword'
city_col    = 'city'
company_col = 'company'

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("### 💼 Job Market Pulse")
    st.markdown("<div style='font-size:11px;color:#6e7681;margin-bottom:16px'>India's Data Job Landscape</div>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("", ["📊 Market Overview", "💡 Key Insights"], label_visibility="collapsed")
    st.markdown("---")

    roles = sorted(df_full[role_col].dropna().str.title().unique().tolist())
    st.markdown("<div style='font-size:12px;color:#8b949e;margin-bottom:6px;font-weight:500'>FILTER BY ROLE</div>", unsafe_allow_html=True)
    selected_role = st.selectbox("Role", ["All Roles"] + roles, label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"<div style='font-size:11px;color:#6e7681'>📋 {len(df_full):,} total listings</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:11px;color:#6e7681'>🏙️ {df_full[city_col].nunique()} cities</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:11px;color:#6e7681'>🏢 {df_full[company_col].nunique():,} companies</div>", unsafe_allow_html=True)

# ── FILTER ──
df = df_full.copy()
df[role_col] = df[role_col].str.title()
if selected_role != "All Roles":
    df = df[df[role_col] == selected_role]

# ── PAGE 1 ──
if page == "📊 Market Overview":
    st.markdown('<div class="page-title">Job Market Pulse</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Real-time analysis of India\'s data job market — powered by Adzuna API</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-banner">
        <div class="hero-quote">"Data job demand is concentrated in a few metro cities,<br>with Business Analyst roles leading overall hiring."</div>
        <div class="hero-sub">Based on 1,149 live job listings across 51 cities and 666 companies</div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    total_jobs      = len(df)
    total_cities    = df[city_col].nunique()
    total_companies = df[company_col].nunique()
    has_salary_pct  = (df['has_salary'].sum() / len(df) * 100) if 'has_salary' in df.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_jobs:,}</div><div class="kpi-label">Total Jobs</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_cities}</div><div class="kpi-label">Cities</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_companies:,}</div><div class="kpi-label">Companies</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{has_salary_pct:.0f}%</div><div class="kpi-label">With Salary</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    # Top Cities
    with col1:
        st.markdown('<div class="section-title">🏙️ Top 10 Hiring Cities</div>', unsafe_allow_html=True)
        top_cities = df[df[city_col] != 'Not Specified'][city_col].value_counts().head(10).sort_values(ascending=True)
        colors = [BAR_HOVER if i == len(top_cities)-1 else BAR_COLOR for i in range(len(top_cities))]
        fig = go.Figure(go.Bar(
            x=top_cities.values, y=top_cities.index, orientation='h',
            marker_color=colors,
            text=top_cities.values, textposition='outside',
            textfont=dict(color='#8b949e', size=10),
            hovertemplate='<b>%{y}</b><br>%{x} jobs<extra></extra>'
        ))
        fig.update_layout(**PLOTLY_THEME, height=380, margin=dict(l=10,r=50,t=10,b=30),
            xaxis_title="Job count", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        top3_pct = df[city_col].value_counts().head(3).sum() / total_jobs * 100
        st.markdown(f'<div class="section-note">Top 3 cities = {top3_pct:.1f}% of all listings</div>', unsafe_allow_html=True)

    # Jobs by Role
    with col2:
        st.markdown('<div class="section-title">💼 Jobs by Role Type</div>', unsafe_allow_html=True)
        role_counts = df[role_col].value_counts().sort_values(ascending=True)
        colors2 = [BAR_HOVER if i == len(role_counts)-1 else BAR_COLOR for i in range(len(role_counts))]
        fig2 = go.Figure(go.Bar(
            x=role_counts.values, y=role_counts.index, orientation='h',
            marker_color=colors2,
            text=role_counts.values, textposition='outside',
            textfont=dict(color='#8b949e', size=10),
            hovertemplate='<b>%{y}</b><br>%{x} listings<extra></extra>'
        ))
        fig2.update_layout(**PLOTLY_THEME, height=380, margin=dict(l=10,r=50,t=10,b=30),
            xaxis_title="Job count", showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
        top_role = role_counts.idxmax()
        st.markdown(f'<div class="section-note">{top_role} roles lead demand</div>', unsafe_allow_html=True)

    # Top Companies
    with col3:
        st.markdown('<div class="section-title">🏢 Top 10 Hiring Companies</div>', unsafe_allow_html=True)
        top_cos = df[company_col].value_counts().head(10).sort_values(ascending=True)
        colors3 = [BAR_HOVER if i == len(top_cos)-1 else BAR_COLOR for i in range(len(top_cos))]
        fig3 = go.Figure(go.Bar(
            x=top_cos.values, y=top_cos.index, orientation='h',
            marker_color=colors3,
            text=top_cos.values, textposition='outside',
            textfont=dict(color='#8b949e', size=10),
            hovertemplate='<b>%{y}</b><br>%{x} listings<extra></extra>'
        ))
        fig3.update_layout(**PLOTLY_THEME, height=380, margin=dict(l=10,r=50,t=10,b=30),
            xaxis_title="Job count", showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('<div class="section-note">Hiring spread across many companies</div>', unsafe_allow_html=True)

    # Contract type breakdown if available
    if 'contract_type' in df.columns:
        st.markdown("---")
        st.markdown('<div class="section-title">📋 Contract Type Distribution</div>', unsafe_allow_html=True)
        ct = df['contract_type'].value_counts()
        fig4 = go.Figure(go.Pie(
            labels=ct.index, values=ct.values, hole=0.5,
            marker_colors=['#388bfd','#3fb950','#f78166','#d2a8ff','#ffa657'],
            textfont=dict(color='#ffffff', size=11),
        ))
        fig4.update_layout(**PLOTLY_THEME, height=280, margin=dict(l=10,r=10,t=10,b=10),
            legend=dict(font=dict(color='#8b949e'), orientation='h', yanchor='bottom', y=1.02))
        st.plotly_chart(fig4, use_container_width=True)

# ── PAGE 2 ──
elif page == "💡 Key Insights":
    st.markdown('<div class="page-title">Key Insights & Conclusions</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">What the data tells us about India\'s data job market</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    top_city     = df[city_col].value_counts().index[0]
    top_city_pct = df[city_col].value_counts().iloc[0] / len(df) * 100
    top3_pct     = df[city_col].value_counts().head(3).sum() / len(df) * 100

    st.markdown(f"""
    <div class="headline-card">
        <div class="headline-main">{top_city} accounts for {top_city_pct:.1f}% of total job listings.</div>
        <div class="headline-sub">Revealing strong geographic concentration in metro cities.</div>
        <div class="headline-sub">Top 3 cities account for {top3_pct:.1f}% of all listings.</div>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="insight-card">
            <div class="insight-card-title">📋 Key Findings</div>
            <div class="insight-item">Jobs are concentrated in metro cities, with <strong>Bangalore</strong> leading significantly.</div>
            <div class="insight-item"><strong>Business Analyst</strong> roles slightly outnumber other data roles.</div>
            <div class="insight-item">A few top companies account for a disproportionately large share of listings.</div>
            <div class="insight-item">~22% of listings lack location data, listed as "Not Specified".</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="insight-card">
            <div class="insight-card-title">🔍 Implications</div>
            <div class="insight-item">Job seekers should focus on <strong>metro cities</strong> to access the majority of opportunities.</div>
            <div class="insight-item">Developing <strong>business-focused analytical skills</strong> improves employability significantly.</div>
            <div class="insight-item">Distributed company hiring suggests opportunities beyond just large tech firms.</div>
            <div class="insight-item">High geographic concentration increases competition in major cities.</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="insight-card">
            <div class="insight-card-title">✅ Recommendations</div>
            <div class="insight-item">Prioritize <strong>Business Analyst</strong> and <strong>Data Analyst</strong> skill development.</div>
            <div class="insight-item">Focus job search efforts in <strong>Bangalore</strong> and <strong>Hyderabad</strong>.</div>
            <div class="insight-item">Build a diverse skill set combining technical and business knowledge.</div>
            <div class="insight-item">Monitor hiring trends continuously to adapt to changing market dynamics.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-title">Role Distribution</div>', unsafe_allow_html=True)
        role_counts = df[role_col].value_counts()
        fig = go.Figure(go.Pie(
            labels=role_counts.index,
            values=role_counts.values,
            hole=0.55,
            marker_colors=['#388bfd','#3fb950','#d2a8ff','#ffa657','#f78166'],
            textfont=dict(color='#ffffff', size=12),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>%{value} listings (%{percent})<extra></extra>'
        ))
        fig.update_layout(**PLOTLY_THEME, height=320, margin=dict(l=10,r=10,t=10,b=10),
            legend=dict(font=dict(color='#8b949e', size=10), orientation='h', yanchor='bottom', y=1.02),
            annotations=[dict(text=f'{role_counts.sum():,}<br><span style="font-size:10px">listings</span>',
                x=0.5, y=0.5, font=dict(size=16, color='#ffffff'), showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="section-note">Each keyword fetched ~250 listings — distribution reflects data collection design</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-title">City Concentration (excl. Not Specified)</div>', unsafe_allow_html=True)
        city_filtered = df[df[city_col] != 'Not Specified'][city_col]
        top5 = city_filtered.value_counts().head(5)
        others_count = len(city_filtered) - top5.sum()
        not_specified_count = (df[city_col] == 'Not Specified').sum()
        labels = list(top5.index) + ['Others']
        values = list(top5.values) + [others_count]
        fig2 = go.Figure(go.Pie(
            labels=labels, values=values, hole=0.55,
            marker_colors=['#388bfd','#3fb950','#d2a8ff','#ffa657','#f78166','#8b949e'],
            textfont=dict(color='#ffffff', size=11),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>%{value} jobs (%{percent})<extra></extra>'
        ))
        fig2.update_layout(**PLOTLY_THEME, height=320, margin=dict(l=10,r=10,t=10,b=10),
            legend=dict(font=dict(color='#8b949e', size=10), orientation='h', yanchor='bottom', y=1.02))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(f'<div class="section-note">{not_specified_count} listings ({not_specified_count/len(df)*100:.1f}%) have no location data</div>', unsafe_allow_html=True)

