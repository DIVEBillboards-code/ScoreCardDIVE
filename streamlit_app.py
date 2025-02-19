import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# Initial page config
st.set_page_config(page_title="Campaign Scorecard", layout="wide")

# Custom styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0066ff;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Campaign Scorecard")

# Campaign Information
col1, col2 = st.columns(2)
with col1:
    campaign_name = st.text_input("Campaign Name")
with col2:
    campaign_date = st.date_input("Campaign Date")

# Initialize session state
if 'scores' not in st.session_state:
    st.session_state.scores = {}
if 'comments' not in st.session_state:
    st.session_state.comments = {}

# Basic metrics structure
metrics = {
    'Creative Readiness': [
        'Assets received on time',
        'Creative meets format'
    ],
    'Production Timeline': [
        'Deadlines met',
        'Final delivery on time'
    ]
}

# Score options
score_options = {
    0: "0 - Poor",
    3: "3 - Medium",
    5: "5 - Excellent"
}

# Create tabs
tab1, tab2 = st.tabs(["Pre-Campaign", "Post-Campaign"])

# Pre-Campaign Section
with tab1:
    st.header("Pre-Campaign Metrics")
    
    for category, category_metrics in metrics.items():
        st.subheader(category)
        for metric in category_metrics:
            key = f"pre_{category}_{metric}"
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(metric)
            with col2:
                score = st.select_slider(
                    "Score",
                    options=list(score_options.keys()),
                    format_func=lambda x: score_options[x],
                    key=f"score_{key}"
                )
                st.session_state.scores[key] = score
            
            comment = st.text_input("Comments", key=f"comment_{key}")
            st.session_state.comments[key] = comment
            st.markdown("---")

# Post-Campaign Section
with tab2:
    st.header("Post-Campaign Metrics")
    
    for category, category_metrics in metrics.items():
        st.subheader(category)
        for metric in category_metrics:
            key = f"post_{category}_{metric}"
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(metric)
            with col2:
                score = st.select_slider(
                    "Score",
                    options=list(score_options.keys()),
                    format_func=lambda x: score_options[x],
                    key=f"score_{key}"
                )
                st.session_state.scores[key] = score
            
            comment = st.text_input("Comments", key=f"comment_{key}")
            st.session_state.comments[key] = comment
            st.markdown("---")

# Calculate and display totals
if st.session_state.scores:
    st.header("Summary")
    
    pre_scores = {k: v for k, v in st.session_state.scores.items() if k.startswith('pre_')}
    post_scores = {k: v for k, v in st.session_state.scores.items() if k.startswith('post_')}
    
    col1, col2 = st.columns(2)
    with col1:
        pre_total = sum(pre_scores.values())
        pre_max = len(pre_scores) * 5
        if pre_max > 0:
            st.metric("Pre-Campaign Score", f"{(pre_total/pre_max*100):.1f}%")
            st.progress(pre_total/pre_max)
    
    with col2:
        post_total = sum(post_scores.values())
        post_max = len(post_scores) * 5
        if post_max > 0:
            st.metric("Post-Campaign Score", f"{(post_total/post_max*100):.1f}%")
            st.progress(post_total/post_max)
