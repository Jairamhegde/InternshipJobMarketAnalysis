import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from queries.analysis import roles,noOfopportunities,roles_trends, TopSkillsOfRole, jobCount, topSkills, topLocations, commonRoles, last_scraped_time
import pandas as pd
import logging


# Page configuration
st.set_page_config(
    page_title="Job Market Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

     
def load_dashboard():
    st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color:none;
        text:black;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 10px;
        border-bottom: 3px solid #1f77b4;
    }
    h2 {
        color: #2c3e50;
        margin-top: 20px;
    }
    h3 {
        color: #34495e;
    }
    .section-divider {
        margin: 30px 0;
        border-top: 2px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
    # @st.cache_data(ttl=3600)
    def load_all_data():
        return {
            'roles': roles(),
            'skills': topSkills(),
            'locations': topLocations(),
            'common_roles': commonRoles(),
            'opportunity':noOfopportunities()
        }
  
    data = load_all_data()
    df_roles = data['roles']
    df_skills = data['skills']
    df_locations = data['locations']
    df_common_roles = data['common_roles']
   

    #SIDEBAR
    with st.sidebar:
        st.title("Navigation")
        
        page = st.radio(
            "Select View",
            ["Overall Market Trends", "Role-Specific Analysis", "Comparative Analysis","Trends Over Time"],
            index=0
        )
      
        total_job_count = data['opportunity']
       
        
       
    st.title("Internship Job Market Analysis ")


    # PAGE: OVERALL MARKET TRENDS
    if page == "Overall Market Trends":
        # st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Key Metrics Row
        st.subheader("Market Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Opportunities",
                value=f"{total_job_count:,}",
                delta="Active Postings"
            )
        
        with col2:
            st.metric(
                label="Top Role",
                value=df_roles.iloc[0]['J_title'][:20] + "..." if len(df_roles.iloc[0]['J_title']) > 20 else df_roles.iloc[0]['J_title'],
                delta=f"{df_roles.iloc[0]['demand']} jobs"
            )
        
        with col3:
            st.metric(
                label="Most Demanded Skill",
                value=df_skills.iloc[0]['name'],
                delta=f"{df_skills.iloc[0]['demand']} mentions"
            )
        
        with col4:
            st.metric(
                label="Top Location",
                value=df_locations.iloc[0]['location'],
                delta=f"{df_locations.iloc[0]['count']} jobs"
            )
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Main Charts Section
        st.subheader("Market Demand Analysis")
        
        # Two columns for roles and skills
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("Top 10 In-Demand Roles")
            
            # Enhanced bar chart for roles
            fig_roles = px.bar(
                df_roles,
                x='demand',
                y='J_title',
                orientation='h',
                color='demand',
                color_continuous_scale='Blues',
                text='demand',
                labels={'demand': 'Number of Postings', 'J_title': 'Job Title'}
            )
            fig_roles.update_traces(texttemplate='%{text}', textposition='outside')
            fig_roles.update_layout(
                height=500,
                showlegend=False,
                xaxis_title="Number of Job Postings",
                yaxis_title="",
                yaxis={'categoryorder': 'total ascending'},
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig_roles, use_container_width=True)
        
        with col2:
            st.markdown("Top 10 In-Demand Skills")
            
            
            fig_skills = px.bar(
                df_skills,
                x='demand',
                y='name',
                orientation='h',
                color='demand',
                color_continuous_scale='Greens',
                text='demand',
                labels={'demand': 'Mentions Across Jobs', 'name': 'Skill'}
            )
            
            fig_skills.update_traces(texttemplate='%{text}', textposition='outside')
            fig_skills.update_layout(
                height=500,
                showlegend=False,
                xaxis_title="count",
                yaxis_title="",
                yaxis={'categoryorder': 'total ascending'},
                margin=dict(l=0, r=0, t=30, b=0))
            st.markdown("<div class=section-divider' stryle='background-color:red'> are the most commonly mentioned skills</div>", unsafe_allow_html=True)
            st.plotly_chart(fig_skills, use_container_width=True)
        # st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Location and Distribution Analysis
        st.subheader("Geographic Distribution & Insights")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Locations bar chart
            fig_locations = px.bar(
                df_locations,
                x='location',
                y='count',
                color='count',
                color_continuous_scale='Oranges',
                text='count',
                labels={'count': 'Number of Jobs', 'location': 'Location'}
            )
            fig_locations.update_traces(texttemplate='%{text}', textposition='outside')
            fig_locations.update_layout(
                title="Top 10 Job Locations",
                height=400,
                showlegend=False,
                xaxis_tickangle=-45,
                margin=dict(l=0, r=0, t=40, b=100)
            )
            st.plotly_chart(fig_locations, use_container_width=True)
        
        with col2:
            # Pie chart for role distribution
            fig_pie = px.pie(
                df_roles.head(8),
                values='demand',
                names='J_title',
                title='Market Share by Top Roles',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(height=400, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Common Skills Across Top Roles
        if not df_common_roles.empty:
            st.subheader("Cross-Functional Skills")
            st.markdown("##### Skills required across multiple top roles (versatile skills)")
            
            fig_common = px.bar(
                df_common_roles.head(15),
                x='total_occurrences',
                y='skill',
                orientation='h',
                color='role_count',
                color_continuous_scale='Purples',
                text='total_occurrences',
                labels={
                    'total_occurrences': 'Total Occurrences',
                    'skill': 'Skill',
                    'role_count': 'Role Count'
                }
            )
            fig_common.update_traces(texttemplate='%{text}', textposition='outside')
            fig_common.update_layout(
                height=500,
                yaxis={'categoryorder': 'total ascending'},
                margin=dict(l=0, r=0, t=10, b=0)
            )
            st.plotly_chart(fig_common, use_container_width=True)
        
        # Data tables in expander
        with st.expander("View Detailed Data Tables"):
            tab1, tab2, tab3 = st.tabs(["Roles Data", "Skills Data", "Locations Data"])
            
            with tab1:
                st.dataframe(df_roles, use_container_width=True, height=400)
            
            with tab2:
                st.dataframe(df_skills, use_container_width=True, height=400)
            
            with tab3:
                st.dataframe(df_locations, use_container_width=True, height=400)

    # PAGE: ROLE-SPECIFIC ANALYSIS 
    elif page == "Role-Specific Analysis":
     
        st.subheader("Select a Role to Analyze")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_role = st.selectbox(
                "Choose from available roles:",
                df_roles['J_title'].tolist(),
                key="role_selector"
            )
        
        with col2:
            # Show role rank
            role_rank = df_roles[df_roles['J_title'] == selected_role].index[0] + 1
            st.metric("Role Ranking", f"#{role_rank}", f"out of {len(df_roles)}")
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Fetch role-specific data
        df_role_skills = TopSkillsOfRole(selected_role)
        df_job_count = jobCount(selected_role)
        total_jobs = df_job_count.iloc[0]['no_of_jobs']
        
        # Role Overview
        st.markdown(f"{selected_role}")
        st.markdown(f"Detailed Analysis & Insights")
        
        # Key metrics for selected role
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Openings",
                value=f"{total_jobs}",
                delta="Active Positions"
            )
        
        with col2:
            market_share = (total_jobs / total_job_count) * 100
            st.metric(
                label="Market Share",
                value=f"{market_share:.1f}%",
                delta="of total market"
            )
        
        with col3:
            st.metric(
                label="Required Skills",
                value=f"{len(df_role_skills)}",
                delta="Unique skills"
            )
        
        with col4:
            avg_skills = df_role_skills['demand'].mean()
            st.metric(
                label="Avg. Skill Mentions",
                value=f"{avg_skills:.0f}",
                delta="per skill"
            )
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Skills visualization
        st.subheader("Skills Breakdown")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Horizontal bar chart for skills
            fig_role_skills = px.bar(
                df_role_skills,
                x='demand',
                y='name',
                orientation='h',
                color='demand',
                color_continuous_scale='Viridis',
                text='demand',
                labels={'demand': 'Frequency', 'name': 'Skill'}
            )
            fig_role_skills.update_traces(texttemplate='%{text}', textposition='outside')
            fig_role_skills.update_layout(
                title=f"Top Skills Required for {selected_role}",
                height=600,
                showlegend=False,
                yaxis={'categoryorder': 'total ascending'},
                margin=dict(l=0, r=0, t=40, b=0)
            )
            st.plotly_chart(fig_role_skills, use_container_width=True)
        
        with col2:
            # Pie chart for skill distribution
            fig_skill_pie = px.pie(
                df_role_skills.head(8),
                values='demand',
                names='name',
                title='Skill Distribution (Top 8)',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_skill_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_skill_pie.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_skill_pie, use_container_width=True)
            
            # Skill categories analysis
            st.markdown("Skill Priority")
            if len(df_role_skills) > 0:
                top_skill_pct = (df_role_skills.iloc[0]['demand'] / df_role_skills['demand'].sum()) * 100
                st.progress(top_skill_pct / 100)
                st.caption(f"**{df_role_skills.iloc[0]['name']}** appears in {top_skill_pct:.1f}% of skill requirements")
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Insights and recommendations
        st.subheader("Career Insights & Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("Must-Have Skills")
            must_have = df_role_skills.head(3)
            for idx, row in must_have.iterrows():
                percentage = (row['demand'] / total_jobs) * 100
                st.markdown(f"**{idx + 1}. {row['name']}** - Required in {percentage:.0f}% of postings")
        
        with col2:
            st.markdown("Emerging Skills")
            if len(df_role_skills) > 5:
                emerging = df_role_skills.tail(3)
                for idx, row in emerging.iterrows():
                    st.markdown(f"• **{row['name']}** - {row['demand']} mentions")
            else:
                st.info("Not enough data for emerging skills analysis")
        
        # Detailed data table
        with st.expander("View Complete Skills Data"):
            st.dataframe(df_role_skills, use_container_width=True, height=400)

    # PAGE: COMPARATIVE ANALYSIS
    elif page == "Comparative Analysis":
       
        
        st.subheader("Compare Multiple Roles")
        st.markdown("#### Analyze and compare different roles side by side")
        
        # Multi-select for roles
        selected_roles = st.multiselect(
            "Select 2-4 roles to compare:",
            df_roles['J_title'].tolist(),
            default=df_roles['J_title'].tolist()[:3],
            max_selections=4
        )
        
        if len(selected_roles) >= 2:
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            
            # Comparison metrics
            comparison_data = []
            for role in selected_roles:
                job_count = jobCount(role).iloc[0]['no_of_jobs']
                skills = TopSkillsOfRole(role)
                comparison_data.append({
                    'Role': role,
                    'Jobs': job_count,
                    'Unique Skills': len(skills),
                    'Avg Skill Demand': skills['demand'].mean() if len(skills) > 0 else 0
                })
            
            df_comparison = pd.DataFrame(comparison_data)
            
            # Display comparison table
            st.subheader("Role Comparison Table")
            st.dataframe(df_comparison, use_container_width=True, height=200)
            
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            
            # Comparative charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Job count comparison
                fig_comp_jobs = px.bar(
                    df_comparison,
                    x='Role',
                    y='Jobs',
                    color='Jobs',
                    color_continuous_scale='Blues',
                    text='Jobs',
                    title="Job Openings Comparison"
                )
                fig_comp_jobs.update_traces(texttemplate='%{text}', textposition='outside')
                fig_comp_jobs.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_comp_jobs, use_container_width=True)
            
            with col2:
                # Skills count comparison
                fig_comp_skills = px.bar(
                    df_comparison,
                    x='Role',
                    y='Unique Skills',
                    color='Unique Skills',
                    color_continuous_scale='Greens',
                    text='Unique Skills',
                    title="Unique Skills Required"
                )
                fig_comp_skills.update_traces(texttemplate='%{text}', textposition='outside')
                fig_comp_skills.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_comp_skills, use_container_width=True)
            
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

            import numpy as np

            # Skills comparison heatmap
            st.subheader("Skills Overlap Analysis")
            
            # Create skills comparison
            all_skills = set()
            role_skills_dict = {}
            
            for role in selected_roles:
                skills_df = TopSkillsOfRole(role)
                role_skills_dict[role] = set(skills_df['name'].tolist())
                all_skills.update(skills_df['name'].tolist())
            
            # Create matrix for heatmap
            matrix_data = []
            skill_list = sorted(list(all_skills))
            
            for skill in skill_list:
                row = {'Skill': skill}
                for role in selected_roles:
                    row[role] = 1 if skill in role_skills_dict[role] else 0
                matrix_data.append(row)
            
            df_matrix = pd.DataFrame(matrix_data)
            
            if len(df_matrix) > 0:
                # Display top common skills
                df_matrix['Total'] = df_matrix[selected_roles].sum(axis=1)
                df_matrix_sorted = df_matrix.sort_values('Total', ascending=False).head(20)
                
                fig_heatmap = px.imshow(
                    df_matrix_sorted[selected_roles].T,
                    labels=dict(x="Skills", y="Roles", color="Present"),
                    x=df_matrix_sorted['Skill'],
                    y=selected_roles,
                    color_continuous_scale='RdYlGn',
                    aspect='auto'
                )
                fig_heatmap.update_layout(
                    title="Top 20 Skills Presence Across Selected Roles",
                    height=400,
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)
                
                # Common skills
                common_skills = df_matrix[df_matrix['Total'] == len(selected_roles)]['Skill'].tolist()
                if common_skills:
                    st.success(f"**{len(common_skills)} skills** are common across all selected roles:")
                    st.write(", ".join(common_skills[:10]) + ("..." if len(common_skills) > 10 else ""))
        else:
            st.warning("Please select at least 2 roles to compare")
    elif page == "Trends Over Time":
        st.subheader("Treds over time")
        df = roles_trends()
        # df["month"]=pd.to_datetime(df["month"],format="%m")
        # df["month"]= df["month"].dt.strftime("%b")
        df = df.sort_values("month",ascending=False)
        fig=px.line(roles_trends(),x="month",y="jobCount",color="name",markers=True)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df)
        # st.dataframe(data)
    # Footer



       
load_dashboard()
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("---")
st.caption("Internship Job Market Analysis")
st.caption("Last scraped on :"+f"{last_scraped_time()}")

