import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from openpyxl.styles import Font, PatternFill

def set_custom_style():
    # Add custom CSS
    st.markdown("""
        <style>
        .stApp {
            background-color: #f8f9fa;
        }
        .main {
            padding: 2rem;
        }
        .block-container {
            padding: 2rem;
            border-radius: 10px;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1E88E5;
            padding-bottom: 1rem;
            border-bottom: 2px solid #1E88E5;
        }
        h2 {
            color: #1976D2;
            margin-top: 2rem;
        }
        h3 {
            color: #1565C0;
        }
        .metric-card {
            background-color: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border-left: 4px solid #1E88E5;
        }
        .stButton>button {
            background-color: #1E88E5;
            color: white;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            border: none;
        }
        .stButton>button:hover {
            background-color: #1976D2;
        }
        .stProgress > div > div > div {
            background-color: #1E88E5;
        }
        .stExpander {
            border: 1px solid #E3F2FD;
            border-radius: 4px;
            margin-bottom: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

def create_campaign_scorecard():
    st.set_page_config(
        page_title="Campaign Scorecard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    set_custom_style()

    # Initialize session state
    if 'pre_scores' not in st.session_state:
        st.session_state.pre_scores = {}
    if 'post_scores' not in st.session_state:
        st.session_state.post_scores = {}
    if 'comments' not in st.session_state:
        st.session_state.comments = {}

    # Page Header with Campaign Information
    st.title("📊 Campaign Scorecard Dashboard")
    
    # Create tabs for different sections
    tabs = st.tabs(["📋 Campaign Info", "⚡ Pre-Campaign", "🎯 Post-Campaign", "📈 Analytics"])
    
    with tabs[0]:
        st.header("Campaign Information")
        col1, col2 = st.columns(2)
        with col1:
            campaign_name = st.text_input("Campaign Name", placeholder="Enter campaign name...")
        with col2:
            campaign_date = st.date_input("Campaign Date")

    # Metrics definitions and options remain the same as your original code
    # [Previous metrics definitions and options code here]

    # Pre-Campaign Section
    with tabs[1]:
        st.header("Pre-Campaign Scorecard")
        
        # Group metrics by category
        for category, metrics in pre_metrics.items():
            with st.expander(f"📌 {category}", expanded=True):
                st.markdown(f"<div class='metric-card'>", unsafe_allow_html=True)
                for metric in metrics:
                    key = f"pre_{category}_{metric}"
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{metric}**")
                        with st.expander("ℹ️ Learn more"):
                            st.write(metric_definitions[metric])
                    
                    with col2:
                        score = st.select_slider(
                            "Score",
                            options=[0, 3, 5],
                            format_func=lambda x: score_options[x],
                            key=f"score_{key}",
                            label_visibility="collapsed"
                        )
                        st.session_state.pre_scores[key] = score
                    
                    with col3:
                        comment = st.text_input(
                            "Comments",
                            key=f"comment_{key}",
                            placeholder="Add comments...",
                            label_visibility="collapsed"
                        )
                        st.session_state.comments[key] = comment
                st.markdown("</div>", unsafe_allow_html=True)

    # Post-Campaign Section
    with tabs[2]:
        st.header("Post-Campaign Scorecard")
        # Similar structure as pre-campaign section
        # [Post-campaign metrics code here]

    # Analytics Section
    with tabs[3]:
        st.header("Campaign Analytics")
        
        # Calculate and display summary metrics
        col1, col2 = st.columns(2)
        with col1:
            pre_total = sum(st.session_state.pre_scores.values())
            pre_max = len([metric for metrics in pre_metrics.values() for metric in metrics]) * 5
            st.metric(
                "Pre-Campaign Score",
                f"{pre_total}/{pre_max}",
                f"{(pre_total/pre_max*100):.1f}%"
            )
            st.progress(pre_total/pre_max if pre_max > 0 else 0)
        
        with col2:
            post_total = sum(st.session_state.post_scores.values())
            post_max = len([metric for metrics in post_metrics.values() for metric in metrics]) * 5
            st.metric(
                "Post-Campaign Score",
                f"{post_total}/{post_max}",
                f"{(post_total/post_max*100):.1f}%"
            )
            st.progress(post_total/post_max if post_max > 0 else 0)

        # Visualization options
        viz_type = st.radio(
            "Select Visualization Type",
            ["Category Performance", "Radar Chart", "Score Distribution", "Phase Comparison"],
            horizontal=True
        )

        # Enhanced visualizations with consistent styling
        if viz_type == "Category Performance":
            fig = px.bar(
                combined_df,
                x='Category',
                y='Average Score',
                color='Phase',
                barmode='group',
                title='Category Performance Comparison',
                color_discrete_sequence=['#1E88E5', '#90CAF9'],
                template='plotly_white'
            )
            fig.update_layout(
                plot_bgcolor='white',
                yaxis_range=[0, 5],
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

        # [Other visualization code with enhanced styling]

        # Export functionality
        st.markdown("### 📤 Export Report")
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Generate Excel Report", use_container_width=True):
                # [Excel generation code]
                pass

if __name__ == "__main__":
    create_campaign_scorecard()
