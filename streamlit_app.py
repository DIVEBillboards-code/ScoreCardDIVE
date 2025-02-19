import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from openpyxl.styles import Font, PatternFill

def set_page_style():
    st.markdown("""
        <style>
        /* Main theme color: #0066ff */
        .main { background-color: #f8f9fa; }
        
        h1, h2, h3 { 
            color: #0066ff;
            padding: 0.5rem 0;
        }
        
        .metric-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 102, 255, 0.1);
            margin: 1rem 0;
            border-left: 4px solid #0066ff;
        }
        
        .stButton > button {
            background-color: #0066ff !important;
            color: white !important;
            border-radius: 6px !important;
        }
        
        .stProgress > div > div > div {
            background-color: #0066ff;
        }
        
        </style>
    """, unsafe_allow_html=True)

def display_metric_group(category, metrics, phase, definitions, score_options):
    """Helper function to display metric groups with consistent styling"""
    st.markdown(f"### {category}")
    
    for metric in metrics:
        key = f"{phase}_{category}_{metric}"
        
        col1, col2 = st.columns([3, 2])
        with col1:
            with st.expander(f"❓ {metric}", expanded=False):
                st.write(definitions.get(metric, "No definition available"))
        
        with col2:
            score = st.select_slider(
                "Score",
                options=list(score_options.keys()),
                format_func=lambda x: score_options[x],
                key=f"score_{key}"
            )
            if phase == 'pre':
                st.session_state.pre_scores[key] = score
            else:
                st.session_state.post_scores[key] = score
                
        comment = st.text_input(
            "Comments",
            key=f"comment_{key}",
            placeholder="Add comments...",
            label_visibility="collapsed"
        )
        st.session_state.comments[key] = comment
        st.markdown("---")

def create_campaign_scorecard():
    st.set_page_config(
        page_title="Campaign Scorecard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    set_page_style()
    
    # Initialize session state
    if 'pre_scores' not in st.session_state:
        st.session_state.pre_scores = {}
    if 'post_scores' not in st.session_state:
        st.session_state.post_scores = {}
    if 'comments' not in st.session_state:
        st.session_state.comments = {}

    # App Header
    st.title("📊 Campaign Performance Scorecard")
    
    # Campaign Information
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

    # Define metrics
    pre_metrics = {
        'Creative Readiness': [
            'Assets received on time',
            'Storyboard approvals met deadlines',
            'Creative meets format & resolution'
        ],
        'Production Timeline': [
            'Workback schedule followed',
            'Vendor deadlines met',
            'Final creative delivered on time'
        ]
    }

    post_metrics = {
        'Impressions & Reach': [
            'Actual impressions vs target',
            'Audience engagement rate',
            'Share of voice achieved'
        ],
        'Engagement & Awareness': [
            'Social media mentions increased',
            'Hashtag usage met expectations',
            'Earned media coverage'
        ]
    }

    # Definitions for tooltips
    metric_definitions = {
        'Assets received on time': 'Measures if all creative assets were delivered by the scheduled date.',
        'Storyboard approvals met deadlines': 'Checks if storyboard approvals were completed on time.',
        'Creative meets format & resolution': 'Ensures creative assets meet required formats and resolution standards.',
        'Workback schedule followed': 'Verifies if the production timeline was adhered to as planned.',
        'Vendor deadlines met': 'Confirms if external vendors met their deadlines.',
        'Final creative delivered on time': 'Ensures the final creative was delivered by the deadline.',
    }

    # Score options
    score_options = {
        0: "0 - No/Poor",
        3: "3 - Partial/Medium",
        5: "5 - Yes/Excellent"
    }

    # Create main tabs
    tabs = st.tabs([
        "📈 Pre-Campaign Metrics",
        "🎯 Post-Campaign Metrics",
        "📊 Analytics Dashboard"
    ])

    # Pre-Campaign Tab
    with tabs[0]:
        st.header("Pre-Campaign Scorecard")
        for category, metrics in pre_metrics.items():
            with st.expander(f"📌 {category}", expanded=True):
                display_metric_group(category, metrics, 'pre', metric_definitions, score_options)

    # Post-Campaign Tab
    with tabs[1]:
        st.header("Post-Campaign Performance")
        for category, metrics in post_metrics.items():
            with st.expander(f"📌 {category}", expanded=True):
                display_metric_group(category, metrics, 'post', metric_definitions, score_options)

    # Analytics Tab
    with tabs[2]:
        st.header("Campaign Analytics Dashboard")
        
        # Calculate totals
        pre_total = sum(st.session_state.pre_scores.values()) if st.session_state.pre_scores else 0
        post_total = sum(st.session_state.post_scores.values()) if st.session_state.post_scores else 0
        
        pre_max = len([metric for metrics in pre_metrics.values() for metric in metrics]) * 5
        post_max = len([metric for metrics in post_metrics.values() for metric in metrics]) * 5
        
        # Display summary metrics
        col1, col2 = st.columns(2)
        with col1:
            pre_percentage = (pre_total / pre_max * 100) if pre_max > 0 else 0
            st.metric("Pre-Campaign Score", f"{pre_percentage:.1f}%")
            st.progress(pre_percentage / 100)
            
        with col2:
            post_percentage = (post_total / post_max * 100) if post_max > 0 else 0
            st.metric("Post-Campaign Score", f"{post_percentage:.1f}%")
            st.progress(post_percentage / 100)

        # Add visualization
        if st.session_state.pre_scores or st.session_state.post_scores:
            # Create DataFrames for visualization
            def create_category_df(scores_dict, metrics_dict, phase):
                data = []
                for category, metrics in metrics_dict.items():
                    category_scores = [scores_dict.get(f"{phase}_{category}_{metric}", 0) for metric in metrics]
                    avg_score = np.mean(category_scores) if category_scores else 0
                    data.append({
                        'Category': category,
                        'Average Score': avg_score,
                        'Phase': 'Pre-Campaign' if phase == 'pre' else 'Post-Campaign'
                    })
                return pd.DataFrame(data)

            pre_df = create_category_df(st.session_state.pre_scores, pre_metrics, 'pre')
            post_df = create_category_df(st.session_state.post_scores, post_metrics, 'post')
            combined_df = pd.concat([pre_df, post_df])

            fig = px.bar(
                combined_df,
                x='Category',
                y='Average Score',
                color='Phase',
                barmode='group',
                title='Category Performance Comparison',
                color_discrete_sequence=['#0066ff', '#66a3ff']
            )
            
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                yaxis_range=[0, 5]
            )
            
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    create_campaign_scorecard()
