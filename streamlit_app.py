import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from openpyxl.styles import Font, PatternFill

def set_page_style():
    # Custom CSS with #0066ff branding
    st.markdown("""
        <style>
        /* Main theme color: #0066ff */
        .main {
            background-color: #f8f9fa;
        }
        
        /* Header Styling */
        .stApp header {
            background-color: #0066ff !important;
        }
        
        h1, h2, h3 {
            color: #0066ff;
            padding: 0.5rem 0;
        }
        
        /* Card styling */
        .metric-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 102, 255, 0.1);
            margin: 1rem 0;
            border-left: 4px solid #0066ff;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #0066ff !important;
            color: white !important;
            border-radius: 6px !important;
            padding: 0.5rem 1.5rem !important;
            font-weight: 500 !important;
            border: none !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            background-color: #0052cc !important;
            box-shadow: 0 4px 8px rgba(0, 102, 255, 0.2);
        }
        
        /* Progress bar */
        .stProgress > div > div > div {
            background-color: #0066ff;
        }
        
        /* Selectbox and input styling */
        .stSelectbox, .stTextInput {
            border-radius: 6px;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: #f8f9fa;
            border-radius: 6px;
            border: 1px solid rgba(0, 102, 255, 0.2);
        }
        
        .streamlit-expanderContent {
            border: 1px solid rgba(0, 102, 255, 0.2);
            border-top: none;
            border-radius: 0 0 6px 6px;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
            border-bottom: 1px solid #0066ff;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #0066ff;
            border-radius: 4px 4px 0 0;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #0066ff !important;
            color: white !important;
        }
        
        /* Tooltip styling */
        .tooltip {
            position: relative;
            display: inline-block;
            cursor: help;
        }
        
        .tooltip .tooltiptext {
            visibility: hidden;
            background-color: #0066ff;
            color: white;
            text-align: center;
            padding: 5px;
            border-radius: 6px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        </style>
    """, unsafe_allow_html=True)

def create_campaign_scorecard():
    st.set_page_config(
        page_title="Campaign Scorecard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    set_page_style()
    
    # Initialize session state
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 0
    if 'pre_scores' not in st.session_state:
        st.session_state.pre_scores = {}
    if 'post_scores' not in st.session_state:
        st.session_state.post_scores = {}
    if 'comments' not in st.session_state:
        st.session_state.comments = {}

    # App Header with Campaign Stats
    st.title("📊 Campaign Performance Scorecard")
    
    # Create main navigation tabs
    tabs = st.tabs([
        "📋 Campaign Overview",
        "📈 Pre-Campaign Metrics",
        "🎯 Post-Campaign Metrics",
        "📊 Analytics Dashboard"
    ])
    
    # Campaign Overview Tab
    with tabs[0]:
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            campaign_name = st.text_input(
                "Campaign Name",
                placeholder="Enter campaign name...",
                help="Enter the name of your campaign"
            )
        with col2:
            campaign_date = st.date_input(
                "Start Date",
                help="Select campaign start date"
            )
        with col3:
            end_date = st.date_input(
                "End Date",
                help="Select campaign end date"
            )
        
        # Quick Stats Cards
        st.markdown("### Campaign Quick Stats")
        quick_stats_cols = st.columns(4)
        with quick_stats_cols[0]:
            st.markdown("""
                <div class="metric-card">
                    <h4>Pre-Campaign Score</h4>
                    <h2 style="color: #0066ff;">85%</h2>
                    <p>Campaign Readiness</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Add more quick stat cards...

    # Pre-Campaign Metrics Tab
    with tabs[1]:
        st.header("Pre-Campaign Scorecard")
        
        # Create category tabs for better organization
        metric_tabs = st.tabs([
            "Creative & Production",
            "Media & Placement",
            "Compliance & Approvals"
        ])
        
        with metric_tabs[0]:
            # Creative & Production metrics
            for category in ['Creative Readiness', 'Production Timeline']:
                with st.expander(f"📌 {category}", expanded=True):
                    display_metric_group(category, pre_metrics[category], 'pre')
        
        # Similarly organize other metric tabs...

    # Post-Campaign Metrics Tab
    with tabs[2]:
        st.header("Post-Campaign Performance")
        
        # Create category tabs for better organization
        post_metric_tabs = st.tabs([
            "Reach & Engagement",
            "Brand Impact",
            "ROI & Conversions"
        ])
        
        # Similar organization as pre-campaign...

    # Analytics Dashboard Tab
    with tabs[3]:
        st.header("Campaign Analytics Dashboard")
        
        # Filters and Controls
        col1, col2 = st.columns([2,2])
        with col1:
            viz_type = st.radio(
                "Select Visualization",
                ["Performance Overview", "Category Comparison", "Trend Analysis"],
                horizontal=True
            )
        
        # Enhanced visualizations with consistent branding
        if viz_type == "Performance Overview":
            fig = create_performance_overview()
            st.plotly_chart(fig, use_container_width=True)
        
        # Add more visualization options...

def display_metric_group(category, metrics, phase):
    """Helper function to display metric groups with consistent styling"""
    for metric in metrics:
        key = f"{phase}_{category}_{metric}"
        
        st.markdown(f"""
            <div class="metric-card">
                <h4>{metric}</h4>
                {create_metric_content(key, metric)}
            </div>
        """, unsafe_allow_html=True)

def create_performance_overview():
    """Create a performance overview visualization with branded colors"""
    fig = go.Figure()
    
    # Add traces with branded colors
    fig.add_trace(go.Bar(
        name="Pre-Campaign",
        x=categories,
        y=pre_scores,
        marker_color="#0066ff"
    ))
    
    fig.add_trace(go.Bar(
        name="Post-Campaign",
        x=categories,
        y=post_scores,
        marker_color="#66a3ff"
    ))
    
    # Update layout with consistent branding
    fig.update_layout(
        title="Campaign Performance Overview",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#333333"),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

# Additional helper functions and main execution...

if __name__ == "__main__":
    create_campaign_scorecard()
