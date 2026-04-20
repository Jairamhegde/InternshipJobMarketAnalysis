import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from queries.analysis import (
    roles, noOfopportunities, roles_trends, TopSkillsOfRole,
    jobCount, topSkills, topLocations, commonRoles, last_scraped_time
)
import pandas as pd
import numpy as np

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Internship Market Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊",
)

# ── Design tokens & global CSS ───────────────────────────────────────────────
BLUE   = "#378ADD"
TEAL   = "#1D9E75"
PURPLE = "#7F77DD"
CORAL  = "#D85A30"
AMBER  = "#BA7517"
GRAY   = "#888780"

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#444441"),
    margin=dict(l=0, r=10, t=36, b=0),
    showlegend=False,
)

def apply_global_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,600&family=Space+Mono:wght@400;700&display=swap');

    /* ── Reset & base ── */
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    .stApp { background: #000000; }

    /* ── Sticky top bar ── */
    .topbar {
        position: sticky; top: 0; z-index: 999;
        background: #fff;
        border-bottom: 1px solid #e2e0d8;
        padding: 12px 28px;
        display: flex; align-items: center; justify-content: space-between;
    }
    .topbar-title {
        font-family: 'Space Mono', monospace;
        font-size: 13px; font-weight: 700;
        letter-spacing: -0.5px; color: #2C2C2A;
    }
    .topbar-badge {
        font-size: 11px; font-weight: 500;
        background: #EAF3DE; color: #3B6D11;
        padding: 4px 12px; border-radius: 20px;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: #2C2C2A !important;
        border-right: none !important;
    }
    section[data-testid="stSidebar"] * { color: #B4B2A9 !important; }
    section[data-testid="stSidebar"] .stRadio label { font-size: 13px !important; }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #F1EFE8 !important; }
    section[data-testid="stSidebar"] .stRadio [role="radio"][aria-checked="true"] + div {
        color: #fff !important; font-weight: 600 !important;
    }

    /* ── Metric cards ── */
    [data-testid="stMetric"] {
        background: #fff;
        border: 1px solid #e2e0d8;
        border-radius: 12px;
        padding: 16px 18px !important;
    }
    [data-testid="stMetricLabel"] { font-size: 11px !important; color: #888780 !important; text-transform: uppercase; letter-spacing: 0.8px; }
    [data-testid="stMetricValue"] { font-family: 'Space Mono', monospace !important; font-size: 24px !important; color: #2C2C2A !important; }
    [data-testid="stMetricDelta"] { font-size: 11px !important; }

    /* ── Section headers ── */
    .section-header {
        font-size: 10px; font-weight: 600; color: #888780;
        text-transform: uppercase; letter-spacing: 1.4px;
        margin: 28px 0 14px; padding-left: 2px;
    }

    /* ── Chart cards ── */
    .chart-card {
        background: #fff;
        border: 1px solid #e2e0d8;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 14px;
    }
    .chart-card-title {
        font-size: 12px; font-weight: 600; color: #444441;
        margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.8px;
    }

    /* ── Skill progress bars ── */
    .skill-row { display: flex; align-items: center; gap: 10px; margin-bottom: 9px; }
    .skill-name { width: 130px; font-size: 12px; color: #5F5E5A; text-align: right; flex-shrink: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .skill-track { flex: 1; background: #F1EFE8; border-radius: 4px; height: 22px; overflow: hidden; }
    .skill-fill { height: 100%; border-radius: 4px; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; font-size: 11px; font-weight: 600; color: #fff; transition: width .5s ease; }

    /* ── Location table ── */
    .loc-table { width: 100%; border-collapse: collapse; font-size: 13px; }
    .loc-table th { font-size: 10px; font-weight: 600; color: #888780; text-transform: uppercase; letter-spacing: .8px; padding: 0 0 10px; border-bottom: 1px solid #e2e0d8; text-align: left; }
    .loc-table td { padding: 9px 0; border-bottom: 1px solid #F1EFE8; color: #5F5E5A; vertical-align: middle; }
    .loc-table tr:last-child td { border-bottom: none; }
    .loc-badge { display: inline-block; font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 20px; }
    .badge-up { background: #EAF3DE; color: #3B6D11; }
    .badge-flat { background: #F1EFE8; color: #888780; }

    /* ── Pill tags ── */
    .pill-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
    .pill { font-size: 11px; padding: 4px 11px; border-radius: 20px; font-weight: 500; }
    .pill-blue { background: #E6F1FB; color: #185FA5; }
    .pill-green { background: #EAF3DE; color: #3B6D11; }
    .pill-amber { background: #FAEEDA; color: #854F0B; }
    .pill-purple { background: #EEEDFE; color: #534AB7; }

    /* ── Divider ── */
    .divider { border: none; border-top: 1px solid #e2e0d8; margin: 24px 0; }

    /* ── Selectbox / multiselect ── */
    .stSelectbox > div, .stMultiSelect > div { border-radius: 8px !important; }
    .stSelectbox label, .stMultiSelect label { font-size: 12px !important; color: #888780 !important; text-transform: uppercase; letter-spacing: .8px; }

    /* ── Expander ── */
    .streamlit-expanderHeader { font-size: 12px !important; font-weight: 600 !important; color: #444441 !important; }

    /* ── Footer ── */
    .footer { font-size: 11px; color: #B4B2A9; text-align: right; padding: 12px 0 4px; }
    </style>
    """, unsafe_allow_html=True)


# ── Helpers ─────────────────────────────────────────────────────────────────

def skill_bars(df, col_name, col_demand, color=BLUE, max_bars=10):
    """Render animated HTML progress bars for skills."""
    df = df.head(max_bars).copy()
    max_val = df[col_demand].max()
    rows = ""
    for _, row in df.iterrows():
        pct = (row[col_demand] / max_val) * 100
        rows += f"""
        <div class="skill-row">
          <div class="skill-name">{row[col_name]}</div>
          <div class="skill-track">
            <div class="skill-fill" style="width:{pct:.0f}%;background:{color}">{int(row[col_demand])}</div>
          </div>
        </div>"""
    st.markdown(rows, unsafe_allow_html=True)


def location_table(df, max_rows=8):
    """Render a styled HTML table for locations."""
    rows = ""
    max_v = df['count'].max()
    for _, row in df.head(max_rows).iterrows():
        pct = (row['count'] / max_v) * 100
        badge_cls = "badge-up" if pct > 40 else "badge-flat"
        trend = "↑ hot" if pct > 70 else ("↑ rising" if pct > 40 else "stable")
        rows += f"""
        <tr>
          <td><b>{row['location']}</b></td>
          <td style="text-align:right;font-family:'Space Mono',monospace;color:#2C2C2A">{int(row['count'])}</td>
          <td style="text-align:right"><span class="loc-badge {badge_cls}">{trend}</span></td>
        </tr>"""
    st.markdown(f"""
    <table class="loc-table">
      <tr><th>City</th><th style="text-align:right">Jobs</th><th style="text-align:right">Trend</th></tr>
      {rows}
    </table>""", unsafe_allow_html=True)


def plotly_defaults(fig):
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig


def pill_tags(skills, colors=None):
    colors = colors or ["pill-blue", "pill-green", "pill-amber", "pill-purple"]
    tags = ""
    for i, s in enumerate(skills):
        cls = colors[i % len(colors)]
        tags += f'<span class="pill {cls}">{s}</span>'
    st.markdown(f'<div class="pill-wrap">{tags}</div>', unsafe_allow_html=True)


# ── Main dashboard ──────────────────────────────────────────────────────────

def load_dashboard():
    apply_global_css()

    # Top bar
    st.markdown("""
    <div class="topbar">
      <span class="topbar-title">📊 INTERNSHIP MARKET INTELLIGENCE</span>
      <span class="topbar-badge">Live data</span>
    </div>""", unsafe_allow_html=True)

    # ── Data loading ────────────────────────────────────────────────────────
    @st.cache_data(ttl=3600)
    def load_all():
        return {
            'roles':        roles(),
            'skills':       topSkills(),
            'locations':    topLocations(),
            'common_roles': commonRoles(),
            'opportunity':  noOfopportunities(),
        }

    data          = load_all()
    df_roles      = data['roles']
    df_skills     = data['skills']
    df_locations  = data['locations']
    df_common     = data['common_roles']
    total_jobs    = data['opportunity']

    # ── Sidebar ─────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## Navigation")
        page = st.radio(
            "",
            ["🌐  Market Trends", "🔍  Role Analysis", "⚖️  Compare Roles", "📈  Trends Over Time"],
            index=0,
        )
        st.markdown("---")
        st.markdown(f"**{total_jobs:,}** active postings")
        st.caption(f"Scraped: {last_scraped_time()}")

    # ════════════════════════════════════════════════════════════════════════
    # PAGE 1 — MARKET TRENDS
    # ════════════════════════════════════════════════════════════════════════
    if "Market Trends" in page:

        # Key metrics
        st.markdown('<div class="section-header">Market overview</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total opportunities", f"{total_jobs:,}", "active postings")
        with c2:
            top_role = df_roles.iloc[0]
            label = top_role['J_title'][:18] + "…" if len(top_role['J_title']) > 18 else top_role['J_title']
            st.metric("Top role", label, f"{top_role['demand']} jobs")
        with c3:
            st.metric("Top skill", df_skills.iloc[0]['name'], f"{df_skills.iloc[0]['demand']} mentions")
        with c4:
            st.metric("Hottest city", df_locations.iloc[0]['location'], f"{df_locations.iloc[0]['count']} jobs")

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # Roles + Skills bars side by side
        st.markdown('<div class="section-header">Demand analysis</div>', unsafe_allow_html=True)
        col_r, col_s = st.columns(2)

        with col_r:
            st.markdown('<div class="chart-card"><div class="chart-card-title">Top 10 roles</div>', unsafe_allow_html=True)
            skill_bars(df_roles.head(10), 'J_title', 'demand', color=BLUE)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_s:
            st.markdown('<div class="chart-card"><div class="chart-card-title">Top 10 skills</div>', unsafe_allow_html=True)
            skill_bars(df_skills.head(10), 'name', 'demand', color=TEAL)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # Geo + Role share
        st.markdown('<div class="section-header">Geographic & market share</div>', unsafe_allow_html=True)
        col_g, col_p = st.columns(2)

        with col_g:
            st.markdown('<div class="chart-card"><div class="chart-card-title">Job locations</div>', unsafe_allow_html=True)
            location_table(df_locations)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_p:
            fig_pie = px.pie(
                df_roles.head(8), values='demand', names='J_title',
                hole=0.55,
                color_discrete_sequence=[BLUE, TEAL, PURPLE, CORAL, AMBER, GRAY, "#5DCAA5", "#F0997B"],
            )
            fig_pie.update_traces(textposition='outside', textinfo='percent+label', textfont_size=11)
            fig_pie.update_layout(**PLOTLY_LAYOUT, title="Market share by role", title_font_size=12)
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # Cross-functional skills
        if not df_common.empty:
            st.markdown('<div class="section-header">Cross-functional skills</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-card"><div class="chart-card-title">Skills spanning multiple top roles</div>', unsafe_allow_html=True)
            skill_bars(df_common.head(12), 'skill', 'total_occurrences', color=PURPLE)
            st.markdown('</div>', unsafe_allow_html=True)

            top_common = df_common.head(8)['skill'].tolist()
            pill_tags(top_common)

        # Data tables
        with st.expander("📋  View raw data tables"):
            t1, t2, t3 = st.tabs(["Roles", "Skills", "Locations"])
            with t1: st.dataframe(df_roles, use_container_width=True)
            with t2: st.dataframe(df_skills, use_container_width=True)
            with t3: st.dataframe(df_locations, use_container_width=True)

    # ════════════════════════════════════════════════════════════════════════
    # PAGE 2 — ROLE ANALYSIS
    # ════════════════════════════════════════════════════════════════════════
    elif "Role Analysis" in page:

        col_sel, col_rank = st.columns([3, 1])
        with col_sel:
            selected_role = st.selectbox("Choose a role", df_roles['J_title'].tolist())
        with col_rank:
            rank = df_roles[df_roles['J_title'] == selected_role].index[0] + 1
            st.metric("Market rank", f"#{rank}", f"out of {len(df_roles)}")

        df_role_skills = TopSkillsOfRole(selected_role)
        role_job_count = jobCount(selected_role).iloc[0]['no_of_jobs']

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Role overview</div>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Total openings", f"{role_job_count:,}", "active")
        with c2: st.metric("Market share", f"{(role_job_count/total_jobs*100):.1f}%", "of total")
        with c3: st.metric("Unique skills", len(df_role_skills), "required")
        with c4: st.metric("Avg skill mentions", f"{df_role_skills['demand'].mean():.0f}", "per skill")

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Skills breakdown</div>', unsafe_allow_html=True)

        col_bars, col_donut = st.columns([3, 2])
        with col_bars:
            st.markdown('<div class="chart-card"><div class="chart-card-title">All required skills</div>', unsafe_allow_html=True)
            skill_bars(df_role_skills, 'name', 'demand', color=PURPLE, max_bars=15)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_donut:
            fig_d = px.pie(
                df_role_skills.head(7), values='demand', names='name', hole=0.6,
                color_discrete_sequence=[PURPLE, "#AFA9EC", BLUE, TEAL, CORAL, AMBER, GRAY],
            )
            fig_d.update_traces(textposition='outside', textinfo='percent+label', textfont_size=11)
            fig_d.update_layout(**PLOTLY_LAYOUT, title="Top 7 skill share", title_font_size=12)
            st.plotly_chart(fig_d, use_container_width=True)

            if len(df_role_skills) > 0:
                top_pct = (df_role_skills.iloc[0]['demand'] / df_role_skills['demand'].sum()) * 100
                st.progress(top_pct / 100)
                st.caption(f"**{df_role_skills.iloc[0]['name']}** = {top_pct:.0f}% of all skill mentions")

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Career insights</div>', unsafe_allow_html=True)

        col_must, col_emrg = st.columns(2)
        with col_must:
            st.markdown("**Must-have skills**")
            for i, (_, row) in enumerate(df_role_skills.head(3).iterrows()):
                pct = (row['demand'] / role_job_count) * 100
                st.markdown(f"`{i+1}.` **{row['name']}** — required in {pct:.0f}% of postings")
        with col_emrg:
            st.markdown("**Emerging / niche skills**")
            if len(df_role_skills) > 5:
                for _, row in df_role_skills.tail(4).iterrows():
                    st.markdown(f"→ **{row['name']}** · {row['demand']} mentions")

        with st.expander("📋  Full skills data"):
            st.dataframe(df_role_skills, use_container_width=True)

    # ════════════════════════════════════════════════════════════════════════
    # PAGE 3 — COMPARE ROLES
    # ════════════════════════════════════════════════════════════════════════
    elif "Compare" in page:

        selected_roles = st.multiselect(
            "Select 2–4 roles to compare",
            df_roles['J_title'].tolist(),
            default=df_roles['J_title'].tolist()[:3],
            max_selections=4,
        )

        if len(selected_roles) < 2:
            st.info("Select at least 2 roles to see the comparison.")
        else:
            comparison_data = []
            for role in selected_roles:
                jc     = jobCount(role).iloc[0]['no_of_jobs']
                skills = TopSkillsOfRole(role)
                comparison_data.append({
                    'Role':            role,
                    'Jobs':            jc,
                    'Unique Skills':   len(skills),
                    'Avg Skill Demand': round(skills['demand'].mean(), 1) if len(skills) else 0,
                    'Market Share %':  round((jc / total_jobs) * 100, 2),
                })
            df_cmp = pd.DataFrame(comparison_data)

            st.markdown('<div class="section-header">Side-by-side metrics</div>', unsafe_allow_html=True)
            st.dataframe(df_cmp.set_index('Role'), use_container_width=True)

            st.markdown('<hr class="divider">', unsafe_allow_html=True)

            colors_list = [BLUE, TEAL, PURPLE, CORAL]
            col_j, col_s = st.columns(2)

            with col_j:
                fig_j = px.bar(
                    df_cmp, x='Role', y='Jobs', text='Jobs',
                    color='Role', color_discrete_sequence=colors_list,
                )
                fig_j.update_traces(texttemplate='%{text}', textposition='outside')
                fig_j.update_layout(**PLOTLY_LAYOUT, title="Job openings", title_font_size=12)
                st.plotly_chart(fig_j, use_container_width=True)

            with col_s:
                fig_s = px.bar(
                    df_cmp, x='Role', y='Unique Skills', text='Unique Skills',
                    color='Role', color_discrete_sequence=colors_list,
                )
                fig_s.update_traces(texttemplate='%{text}', textposition='outside')
                fig_s.update_layout(**PLOTLY_LAYOUT, title="Unique skills required", title_font_size=12)
                st.plotly_chart(fig_s, use_container_width=True)

            # Skills heatmap
            st.markdown('<div class="section-header">Skills overlap heatmap</div>', unsafe_allow_html=True)
            all_skills = set()
            role_skills_dict = {}
            for role in selected_roles:
                s = TopSkillsOfRole(role)
                role_skills_dict[role] = set(s['name'].tolist())
                all_skills.update(s['name'].tolist())

            matrix = [
                {'Skill': sk, **{r: int(sk in role_skills_dict[r]) for r in selected_roles}}
                for sk in sorted(all_skills)
            ]
            df_mx = pd.DataFrame(matrix)
            df_mx['Total'] = df_mx[selected_roles].sum(axis=1)
            df_top = df_mx.sort_values('Total', ascending=False).head(20)

            fig_hm = px.imshow(
                df_top[selected_roles].T,
                x=df_top['Skill'].tolist(), y=selected_roles,
                color_continuous_scale=[[0, "#F1EFE8"], [1, BLUE]],
                aspect='auto',
            )
            fig_hm.update_layout(**PLOTLY_LAYOUT, title="Top 20 skills presence", title_font_size=12,
                                 xaxis_tickangle=-40, coloraxis_showscale=False)
            st.plotly_chart(fig_hm, use_container_width=True)

            common = df_mx[df_mx['Total'] == len(selected_roles)]['Skill'].tolist()
            if common:
                st.success(f"**{len(common)} skills** shared across ALL selected roles:")
                pill_tags(common[:12])

    # ════════════════════════════════════════════════════════════════════════
    # PAGE 4 — TRENDS OVER TIME
    # ════════════════════════════════════════════════════════════════════════
    elif "Trends" in page:

        st.markdown('<div class="section-header">Job count trends by role</div>', unsafe_allow_html=True)
        df_t = roles_trends().sort_values("month", ascending=True)

        fig_line = px.line(
            df_t, x="month", y="jobCount", color="name",
            markers=True, line_shape="spline",
            color_discrete_sequence=[BLUE, TEAL, PURPLE, CORAL, AMBER, GRAY, "#5DCAA5"],
        )
        fig_line.update_traces(line_width=2.5, marker_size=7)
        fig_line.update_layout(
            **PLOTLY_LAYOUT,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_title="", yaxis_title="Job count",
        )
        st.plotly_chart(fig_line, use_container_width=True)

        with st.expander("📋  View raw trend data"):
            st.dataframe(df_t, use_container_width=True)

    # Footer
    st.markdown(f'<div class="footer">Last scraped · {last_scraped_time()}</div>', unsafe_allow_html=True)


load_dashboard()
