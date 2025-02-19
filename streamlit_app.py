import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from openpyxl.styles import Font, PatternFill

# First, update the CSS for better UX
st.markdown("""
    <style>
    /* Modern color palette */
    :root {
        --primary: #0066ff;
        --primary-dark: #0052cc;
        --primary-light: #e6f0ff;
        --success: #28a745;
        --warning: #ffc107;
        --danger: #dc3545;
        --gray-100: #f8f9fa;
        --gray-200: #e9ecef;
        --gray-300: #dee2e6;
    }

    /* Base styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Card container improvements */
    .stContainer {
        border: 1px solid var(--gray-300);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 28px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        background-color: white;
        transition: all 0.3s ease;
    }
    .stContainer:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    /* Enhanced header with gradient */
    .stHeader {
        color: white;
        font-size: 1.6rem;
        font-weight: 600;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0, 102, 255, 0.15);
    }
    
    /* Improved subheader */
    .stSubheader {
        color: var(--primary-dark);
        font-size: 1.3rem;
        font-weight: 600;
        margin: 24px 0 16px;
        padding-bottom: 12px;
        border-bottom: 3px solid var(--primary);
        transition: color 0.2s ease;
    }
    .stSubheader:hover {
        color: var(--primary);
    }
    
    /* Enhanced metric tiles */
    .stMetric {
        background: linear-gradient(135deg, white, var(--gray-100));
        padding: 24px;
        border-radius: 12px;
        border: 1px solid var(--gray-300);
        transition: all 0.3s ease;
        margin-bottom: 16px;
    }
    .stMetric:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Modern button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        border-radius: 12px;
        padding: 16px 32px;
        border: none;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        font-size: 14px;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-dark) 0%, #004399 100%);
        box-shadow: 0 6px 12px rgba(0, 102, 255, 0.2);
        transform: translateY(-2px);
    }
    
    /* Enhanced progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--primary-dark) 100%);
        border-radius: 8px;
        height: 8px !important;
        transition: width 1s ease-in-out;
    }
    .stProgress {
        height: 8px !important;
    }
    
    /* Improved input styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid var(--gray-300);
        padding: 12px 16px;
        transition: all 0.3s ease;
        background-color: var(--gray-100);
    }
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1);
        background-color: white;
    }
    
    /* Enhanced expander styling */
    .st-emotion-cache-1fttcpj {
        color: var(--primary) !important;
        font-weight: 500;
    }
    .st-emotion-cache-1pwu5cb {
        color: var(--primary) !important;
        fill: var(--primary) !important;
    }
    .st-emotion-cache-1q1n0ol {
        color: var(--primary-dark) !important;
        background-color: var(--primary-light);
        padding: 16px;
        border-radius: 8px;
        margin-top: 8px;
    }
    
    /* Score indicators */
    .score-indicator {
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        text-align: center;
        margin-top: 8px;
    }
    .score-high {
        background-color: #e6ffe6;
        color: var(--success);
        border: 1px solid var(--success);
    }
    .score-medium {
        background-color: #fff9e6;
        color: var(--warning);
        border: 1px solid var(--warning);
    }
    .score-low {
        background-color: #ffe6e6;
        color: var(--danger);
        border: 1px solid var(--danger);
    }
    
    /* Improved dividers */
    hr {
        height: 2px;
        background: linear-gradient(to right, 
            transparent, 
            var(--gray-300), 
            transparent
        );
        border: none;
        margin: 24px 0;
    }
    
    /* Loading states */
    .stSpinner > div {
        border-color: var(--primary);
        border-top-color: transparent;
    }
    
    /* Tooltip improvements */
    .stTooltipIcon {
        color: var(--primary) !important;
        transition: transform 0.2s ease;
    }
    .stTooltipIcon:hover {
        transform: scale(1.1);
    }
    
    /* Chart customization */
    .js-plotly-plot .plotly .modebar {
        background: white !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
    }
    
    /* Improved table styling */
    table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    th, td {
        padding: 16px;
        background: white;
        border-bottom: 1px solid var(--gray-300);
    }
    th {
        background: var(--gray-100);
        font-weight: 600;
        color: var(--primary-dark);
    }
    tr:last-child td {
        border-bottom: none;
    }

    /* New style for Post-Campaign container */
    .stContainer-post {
        border: 1px solid var(--gray-300);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 28px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        background-color: #f0f0f0; /* Light gray background */
        transition: all 0.3s ease;
    }
    .stContainer-post:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }

    /* Ensure other styles don't override this */
    .stContainer {
        /* Original container style remains for Pre-Campaign */
        border: 1px solid var(--gray-300);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 28px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        background-color: white; /* Default white background for Pre-Campaign */
        transition: all 0.3s ease;
    }
    .stContainer:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    /* Animation for content loading */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stContainer {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
""", unsafe_allow_html=True)

# Update the visualization settings for better visual appeal
def update_plot_theme(fig):
    fig.update_layout(
        font_family="Inter, -apple-system, BlinkMacSystemFont, sans-serif",
        title_font_size=20,
        title_font_family="Inter, -apple-system, BlinkMacSystemFont, sans-serif",
        title_font_color="#0066ff",
        plot_bgcolor="rgba(248, 249, 250, 0.5)",
        paper_bgcolor="rgba(248, 249, 250, 0)",
        hovermode="closest",
        showlegend=True,
        legend=dict(
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="rgba(0, 0, 0, 0.1)",
            borderwidth=1,
            font=dict(size=12, color="#333333")
        ),
        margin=dict(t=50, b=50, l=50, r=50)
    )
    return fig

def create_campaign_scorecard():
    # Initialize session state for storing scores
    if 'pre_scores' not in st.session_state:
        st.session_state.pre_scores = {}
    if 'post_scores' not in st.session_state:
        st.session_state.post_scores = {}
    if 'comments' not in st.session_state:
        st.session_state.comments = {}

    # Campaign Information (in a box)
    with st.container():
        st.markdown('<div class="stContainer"><div class="stHeader">Campaign Information</div>', unsafe_allow_html=True)
        campaign_name = st.text_input("Campaign Name", key="campaign_name")
        start_date = st.date_input("Start Date", key="start_date")
        end_date = st.date_input("End Date", key="end_date")
        client_name = st.text_input("Client Name", key="client_name")
        country = st.text_input("Country", key="country")
        cities = st.text_input("Cities", key="cities", help="Enter cities separated by commas")
        st.markdown('</div>', unsafe_allow_html=True)

    # Create two columns for Pre and Post Campaign
    pre_col, post_col = st.columns(2)

    # Pre-Campaign Metrics (Updated with new parameters)
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
        ],
        'Placement & Inventory': [
            'Billboard locations confirmed',
            'Placement visibility',
            'Competitive share of voice'
        ],
        'Budget & Media': [
            'Budget fully utilized',
            'Number of spots booked vs planned'
        ],
        'Target Audience': [
            'Demographic match',
            'Estimated reach meets expectations'
        ],
        'Approval & Compliance': [
            'Legal/brand compliance approved',
            'Vendor tests & pre-launch checks done'
        ],
        'Moderation Guidelines': [
            'Pre-Defined Moderation Guidelines',
            'Approval Checklist'
        ],
        'Moderation Script': [
            'Pre-Moderation Review Process',
            'Compliance Script Execution'
        ],
        'Moderation Workback Schedule': [
            'Content Submission Date',
            'Moderation Review Deadline'
        ],
        'Influencer Assets': [
            'Influencer Content Submission',
            'Influencer Content Approval'
        ],
        'Clients Approvals': [
            'Client Content Submission',
            'Client Content Approval'
        ],
        'Creators Approvals': [
            'Creator Content Submission',
            'Creator Content Approval'
        ],
        'TikTok Approvals': [
            'TikTok Platform Compliance',
            'TikTok Ad Moderation Passed'
        ]
    }

    # Post-Campaign Metrics
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
        ],
        'Brand Sentiment': [
            'Positive sentiment shift',
            'UGC growth',
            'Influencer engagement'
        ],
        'Conversion & ROI': [
            'Website traffic increased',
            'Sales lift / conversion growth',
            'Cost per engagement met target'
        ],
        'Photography & Visibility': [
            'High-quality images captured',
            'Splash video created',
            'Social media features'
        ],
        'Campaign Learnings': [
            'Key wins identified',
            'Areas for improvement noted',
            'Optimization recommendations made'
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
        'Billboard locations confirmed': 'Verifies that billboard placements were secured and confirmed.',
        'Placement visibility': 'Evaluates the visibility and effectiveness of ad placements.',
        'Competitive share of voice': 'Measures the campaign’s visibility relative to competitors.',
        'Budget fully utilized': 'Checks if the entire allocated budget was used effectively.',
        'Number of spots booked vs planned': 'Compares booked ad spots to the planned number.',
        'Demographic match': 'Assesses if the target audience matches the intended demographics.',
        'Estimated reach meets expectations': 'Verifies if the campaign reached the expected audience size.',
        'Legal/brand compliance approved': 'Ensures all content complies with legal and brand standards.',
        'Vendor tests & pre-launch checks done': 'Confirms all pre-launch tests and checks by vendors were completed.',
        'Pre-Defined Moderation Guidelines': 'Refers to established rules for content moderation before launch.',
        'Approval Checklist': 'Lists required approvals for moderation processes.',
        'Pre-Moderation Review Process': 'Evaluates content before it goes live for compliance.',
        'Compliance Script Execution': 'Ensures scripts for compliance checks were correctly implemented.',
        'Content Submission Date': 'Tracks when content was submitted for moderation.',
        'Moderation Review Deadline': 'Sets the deadline for completing moderation reviews.',
        'Influencer Content Submission': 'Monitors when influencers submit their content.',
        'Influencer Content Approval': 'Tracks approval of influencer-submitted content.',
        'Client Content Submission': 'Records when clients submit their content for review.',
        'Client Content Approval': 'Confirms client content has been approved.',
        'Creator Content Submission': 'Logs when creators submit their content.',
        'Creator Content Approval': 'Verifies approval of content from creators.',
        'TikTok Platform Compliance': 'Ensures content meets TikTok’s platform-specific rules.',
        'TikTok Ad Moderation Passed': 'Confirms TikTok ads passed moderation checks.',
        'Actual impressions vs target': 'Compares actual ad impressions to the set target.',
        'Audience engagement rate': 'Measures how audiences interacted with the campaign.',
        'Share of voice achieved': 'Evaluates the campaign’s market presence post-launch.',
        'Social media mentions increased': 'Tracks growth in social media mentions.',
        'Hashtag usage met expectations': 'Checks if hashtag usage reached expected levels.',
        'Earned media coverage': 'Measures unsolicited media coverage gained.',
        'Positive sentiment shift': 'Assesses improvement in audience sentiment.',
        'UGC growth': 'Tracks growth in user-generated content related to the campaign.',
        'Influencer engagement': 'Measures interactions and impact from influencers.',
        'Website traffic increased': 'Evaluates if the campaign drove more website visits.',
        'Sales lift / conversion growth': 'Measures increase in sales or conversions.',
        'Cost per engagement met target': 'Checks if engagement costs were within targets.',
        'High-quality images captured': 'Ensures campaign visuals meet quality standards.',
        'Splash video created': 'Confirms a promotional video was produced.',
        'Social media features': 'Tracks use of social media features like stories or reels.',
        'Key wins identified': 'Highlights successful aspects of the campaign.',
        'Areas for improvement noted': 'Identifies aspects needing enhancement.',
        'Optimization recommendations made': 'Suggests ways to improve future campaigns.'
    }

    # Score options
    score_options = {
        0: "0 - No/Poor",
        3: "3 - Partial/Medium",
        5: "5 - Yes/Excellent"
    }

    # Pre-Campaign Section (in a box)
    with pre_col:
        with st.container():
            st.markdown('<div class="stContainer"><div class="stHeader">Pre-Campaign Scorecard</div>', unsafe_allow_html=True)
            for category, metrics in pre_metrics.items():
                st.markdown(f'<div class="stSubheader">{category}</div>', unsafe_allow_html=True)
                for metric in metrics:
                    key = f"pre_{category}_{metric}"
                    col1, col2 = st.columns([3, 2])
                    with col1:
                        with st.expander(f"❓ {metric}", expanded=False):
                            st.write(metric_definitions[metric])
                    with col2:
                        score = st.selectbox(
                            "Score",
                            options=list(score_options.keys()),
                            format_func=lambda x: score_options[x],
                            key=f"score_{key}"
                        )
                        st.session_state.pre_scores[key] = score
                    comment = st.text_area("Comments", key=f"comment_{key}", label_visibility="collapsed")
                    st.session_state.comments[key] = comment
                    st.markdown('<hr style="border: 1px solid #e0e0e0; margin: 10px 0;">', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

   # In the create_campaign_scorecard function, find the Post-Campaign Section and replace it with this:

    # Post-Campaign Section (with new background)
    with post_col:
        with st.container():
            st.markdown('<div class="stContainer-post"><div class="stHeader">Post-Campaign Scorecard</div>', unsafe_allow_html=True)
            for category, metrics in post_metrics.items():
                st.markdown(f'<div class="stSubheader">{category}</div>', unsafe_allow_html=True)
                for metric in metrics:
                    key = f"post_{category}_{metric}"
                    col1, col2 = st.columns([3, 2])
                    with col1:
                        with st.expander(f"❓ {metric}", expanded=False):
                            st.write(metric_definitions[metric])
                    with col2:
                        score = st.selectbox(
                            "Score",
                            options=list(score_options.keys()),
                            format_func=lambda x: score_options[x],
                            key=f"score_{key}"
                        )
                        st.session_state.post_scores[key] = score
                    comment = st.text_area("Comments", key=f"comment_{key}", label_visibility="collapsed")
                    st.session_state.comments[key] = comment
                    st.markdown('<hr style="border: 1px solid #e0e0e0; margin: 10px 0;">', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Calculate totals as percentages
    pre_total = sum(st.session_state.pre_scores.values()) if st.session_state.pre_scores else 0
    post_total = sum(st.session_state.post_scores.values()) if st.session_state.post_scores else 0
    pre_max = len([metric for metrics in pre_metrics.values() for metric in metrics]) * 5
    post_max = len([metric for metrics in post_metrics.values() for metric in metrics]) * 5

    # Convert to percentages (0 to 100)
    pre_percentage = (pre_total / pre_max * 100) if pre_max > 0 else 0
    post_percentage = (post_total / post_max * 100) if post_max > 0 else 0

    # Normalize for progress bar (0 to 1)
    pre_progress = pre_percentage / 100 if pre_max > 0 else 0
    post_progress = post_percentage / 100 if post_max > 0 else 0

    # Get unique categories from both pre and post metrics
    categories = list(set(list(pre_metrics.keys()) + list(post_metrics.keys())))

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
    combined_df = pd.concat([pre_df, post_df]).dropna()

    # Calculate improvements and declines (in percentages for consistency), only for categories with both pre and post data
    improvements = []
    declines = []
    
    common_categories = set(pre_df['Category']).intersection(set(post_df['Category']))
    
    for category in common_categories:
        try:
            pre_score = pre_df[pre_df['Category'] == category]['Average Score'].iloc[0] if not pre_df[pre_df['Category'] == category].empty else 0
            post_score = post_df[post_df['Category'] == category]['Average Score'].iloc[0] if not post_df[post_df['Category'] == category].empty else 0
            
            # Convert to percentages for comparison (scale 0-5 to 0-100%)
            pre_percent = (pre_score / 5) * 100 if pre_score > 0 else 0
            post_percent = (post_score / 5) * 100 if post_score > 0 else 0
            
            # Avoid division by zero or unrealistic declines
            if pre_percent == 0 and post_percent == 0:
                continue  # Skip if both are 0 (no change)
            elif pre_percent == 0 and post_percent > 0:
                improvements.append((category, post_percent))  # Full improvement if pre was 0
            else:
                diff = post_percent - pre_percent
                if diff > 0:
                    improvements.append((category, diff))
                elif diff < 0:
                    declines.append((category, abs(diff)))
        except (IndexError, KeyError):
            continue  # Skip if data is not available for this category

    # Display totals and visualizations (in a box)
    with st.container():
        st.markdown('<div class="stContainer"><div class="stHeader">Score Summary and Visualizations</div>', unsafe_allow_html=True)
        
        # Summary metrics as percentages
        col1, col2 = st.columns(2)
        with col1:
            with st.container():
                st.markdown('<div class="stMetric">', unsafe_allow_html=True)
                st.metric("Pre-Campaign Score", f"{pre_percentage:.1f}%")
                st.progress(pre_progress)
                st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            with st.container():
                st.markdown('<div class="stMetric">', unsafe_allow_html=True)
                st.metric("Post-Campaign Score", f"{post_percentage:.1f}%")
                st.progress(post_progress)
                st.markdown('</div>', unsafe_allow_html=True)

        # Visualization Section
        st.subheader("Data Visualizations")
        
        # Select visualization type
        viz_type = st.selectbox(
            "Select Visualization Type",
            ["Category Performance", "Radar Chart", "Score Distribution", "Phase Comparison"],
            key="viz_type_select"
        )

        if viz_type == "Category Performance" and not combined_df.empty:
            # Bar chart comparing pre and post campaign scores by category
            fig = px.bar(
                combined_df,
                x='Category',
                y='Average Score',
                color='Phase',
                barmode='group',
                title='Category Performance Comparison',
                height=500
            )
            fig.update_layout(yaxis_range=[0, 5], plot_bgcolor='#f5f5f5', paper_bgcolor='#f5f5f5')
            st.plotly_chart(fig, use_container_width=True)

        elif viz_type == "Radar Chart" and not pre_df.empty and not post_df.empty:
            # Radar chart showing category scores
            categories = list(pre_metrics.keys())
            pre_scores = pre_df['Average Score'].tolist()
            post_scores = post_df['Average Score'].tolist()

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=pre_scores,
                theta=categories,
                fill='toself',
                name='Pre-Campaign'
            ))
            fig.add_trace(go.Scatterpolar(
                r=post_scores,
                theta=categories,
                fill='toself',
                name='Post-Campaign'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 5], color="#003399")),
                showlegend=True,
                title='Radar Chart: Category Scores',
                plot_bgcolor='#f5f5f5',
                paper_bgcolor='#f5f5f5'
            )
            st.plotly_chart(fig, use_container_width=True)

        elif viz_type == "Score Distribution" and (st.session_state.pre_scores or st.session_state.post_scores):
            # Histogram of score distribution
            all_pre_scores = list(st.session_state.pre_scores.values()) if st.session_state.pre_scores else []
            all_post_scores = list(st.session_state.post_scores.values()) if st.session_state.post_scores else []
            
            fig = go.Figure()
            if all_pre_scores:
                fig.add_trace(go.Histogram(
                    x=all_pre_scores,
                    name='Pre-Campaign',
                    nbinsx=3,
                    marker_color='#0066ff',
                    opacity=0.7
                ))
            if all_post_scores:
                fig.add_trace(go.Histogram(
                    x=all_post_scores,
                    name='Post-Campaign',
                    nbinsx=3,
                    marker_color='#003399',
                    opacity=0.7
                ))
            fig.update_layout(
                barmode='overlay',
                title='Score Distribution',
                xaxis_title='Score',
                yaxis_title='Count',
                plot_bgcolor='#f5f5f5',
                paper_bgcolor='#f5f5f5'
            )
            st.plotly_chart(fig, use_container_width=True)

        elif viz_type == "Phase Comparison" and not combined_df.empty:
            # Scatter plot comparing pre vs post scores
            fig = px.scatter(
                combined_df,
                x='Category',
                y='Average Score',
                color='Phase',
                title='Pre vs Post Campaign Score Comparison',
                height=500
            )
            
            # Update trace to set marker color
            fig.update_traces(marker=dict(color='#0066ff'), selector=dict(type='scatter'))
            
            fig.update_layout(
                xaxis_tickangle=-45,
                yaxis_range=[0, 5],
                showlegend=True,
                plot_bgcolor='#f5f5f5',
                paper_bgcolor='#f5f5f5'
            )
            st.plotly_chart(fig, use_container_width=True)

        # Add insights based on the data (in a box)
        with st.container():
            st.markdown('<div class="stContainer"><div class="stHeader">Key Insights</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Top Improvements:**")
                if improvements:
                    improvements.sort(key=lambda x: x[1], reverse=True)
                    for category, diff in improvements[:3]:
                        st.write(f"• {category}: +{diff:.1f}%")
                else:
                    st.write("No improvements detected")

            with col2:
                st.markdown("**Areas for Focus:**")
                if declines:
                    declines.sort(key=lambda x: x[1], reverse=True)
                    for category, diff in declines[:3]:
                        st.write(f"• {category}: -{diff:.1f}%")
                else:
                    st.write("No declines detected")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Create Excel download (in a box)
    with st.container():
        st.markdown('<div class="stContainer">', unsafe_allow_html=True)
        if st.button("Generate Report", key="generate_report", help="Download the scorecard as an Excel file"):
            # Create DataFrame for Excel
            data = []
            
            # Add campaign info with new fields
            data.append(["Campaign Information", "", "", ""])
            data.append(["Campaign Name", campaign_name, "", ""])
            data.append(["Campaign Date", campaign_date.strftime("%Y-%m-%d"), "", ""])
            data.append(["Start Date", start_date.strftime("%Y-%m-%d"), "", ""])
            data.append(["End Date", end_date.strftime("%Y-%m-%d"), "", ""])
            data.append(["Client Name", client_name, "", ""])
            data.append(["Country", country, "", ""])
            data.append(["Cities", cities, "", ""])
            data.append(["", "", "", ""])
            
            # Add Pre-Campaign data
            data.append(["Pre-Campaign Scorecard", "", "", ""])
            data.append(["Category", "Metric", "Score", "Comments"])
            for category, metrics in pre_metrics.items():
                for metric in metrics:
                    key = f"pre_{category}_{metric}"
                    data.append([
                        category,
                        metric,
                        st.session_state.pre_scores.get(key, 0),
                        st.session_state.comments.get(key, "")
                    ])
            
            # Add Post-Campaign data
            data.append(["", "", "", ""])
            data.append(["Post-Campaign Scorecard", "", "", ""])
            data.append(["Category", "Metric", "Score", "Comments"])
            for category, metrics in post_metrics.items():
                for metric in metrics:
                    key = f"post_{category}_{metric}"
                    data.append([
                        category,
                        metric,
                        st.session_state.post_scores.get(key, 0),
                        st.session_state.comments.get(key, "")
                    ])
            
            # Add totals as percentages
            data.append(["", "", "", ""])
            data.append(["Score Summary", "", "", ""])
            data.append(["Pre-Campaign Score", f"{pre_percentage:.1f}%", "", ""])
            data.append(["Post-Campaign Score", f"{post_percentage:.1f}%", "", ""])
            
            # Create DataFrame and Excel file
            df = pd.DataFrame(data)
            excel_file = f"campaign_scorecard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            # Create Excel writer
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False)
                
                # Get workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['Sheet1']
                
                # Add some styling
                header_fill = PatternFill(start_color='CCCCCC', end_color='CCCCCC', fill_type='solid')
                
                # Style headers
                for cell in worksheet['1:1']:
                    cell.font = Font(bold=True)
                    cell.fill = header_fill
            
            # Create download button
            with open(excel_file, 'rb') as f:
                st.download_button(
                    label="Download Excel Report",
                    data=f,
                    file_name=excel_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_button"
                )
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    create_campaign_scorecard()
