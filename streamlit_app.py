import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from openpyxl.styles import Font, PatternFill

def create_campaign_scorecard():
    st.set_page_config(page_title="Campaign Scorecard", layout="wide")
    st.title("Campaign Scorecard Dashboard")

    # Initialize session state for storing scores
    if 'pre_scores' not in st.session_state:
        st.session_state.pre_scores = {}
    if 'post_scores' not in st.session_state:
        st.session_state.post_scores = {}
    if 'comments' not in st.session_state:
        st.session_state.comments = {}

    # Campaign Information
    st.header("Campaign Information")
    campaign_name = st.text_input("Campaign Name")
    campaign_date = st.date_input("Campaign Date")

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

    # Pre-Campaign Section
    with pre_col:
        st.subheader("Pre-Campaign Scorecard")
        for category, metrics in pre_metrics.items():
            st.markdown(f"**{category}**")
            for metric in metrics:
                key = f"pre_{category}_{metric}"
                col1, col2 = st.columns([3, 2])
                with col1:
                    # Use button for expander with explanation
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
                st.markdown("---")

    # Post-Campaign Section
    with post_col:
        st.subheader("Post-Campaign Scorecard")
        for category, metrics in post_metrics.items():
            st.markdown(f"**{category}**")
            for metric in metrics:
                key = f"post_{category}_{metric}"
                col1, col2 = st.columns([3, 2])
                with col1:
                    # Use button for expander with explanation
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
                st.markdown("---")

    # Calculate totals
    pre_total = sum(st.session_state.pre_scores.values()) if st.session_state.pre_scores else 0
    post_total = sum(st.session_state.post_scores.values()) if st.session_state.post_scores else 0
    pre_max = len([metric for metrics in pre_metrics.values() for metric in metrics]) * 5
    post_max = len([metric for metrics in post_metrics.values() for metric in metrics]) * 5

    # Display totals and visualizations
    st.header("Score Summary and Visualizations")
    
    # Summary metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Pre-Campaign Total", f"{pre_total}/{pre_max}")
        st.progress(pre_total/pre_max if pre_max > 0 else 0)
    with col2:
        st.metric("Post-Campaign Total", f"{post_total}/{post_max}")
        st.progress(post_total/post_max if post_max > 0 else 0)

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

    # Visualization Section
    st.subheader("Data Visualizations")
    
    # Select visualization type
    viz_type = st.selectbox(
        "Select Visualization Type",
        ["Category Performance", "Radar Chart", "Score Distribution", "Phase Comparison"]
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
        fig.update_layout(yaxis_range=[0, 5])
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
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=True,
            title='Radar Chart: Category Scores'
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
                opacity=0.7
            ))
        if all_post_scores:
            fig.add_trace(go.Histogram(
                x=all_post_scores,
                name='Post-Campaign',
                nbinsx=3,
                opacity=0.7
            ))
        fig.update_layout(
            barmode='overlay',
            title='Score Distribution',
            xaxis_title='Score',
            yaxis_title='Count'
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
        fig.update_layout(
            xaxis_tickangle=-45,
            yaxis_range=[0, 5],
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)

    # Add insights based on the data
    st.subheader("Key Insights")
    
    # Calculate improvements and declines
    improvements = []
    declines = []
    
    for category in categories:
        try:
            pre_score = pre_df[pre_df['Category'] == category]['Average Score'].iloc[0] if not pre_df[pre_df['Category'] == category].empty else 0
            post_score = post_df[post_df['Category'] == category]['Average Score'].iloc[0] if not post_df[post_df['Category'] == category].empty else 0
            
            diff = post_score - pre_score
            if diff > 0:
                improvements.append((category, diff))
            elif diff < 0:
                declines.append((category, abs(diff)))
        except (IndexError, KeyError):
            continue  # Skip if data is not available for this category

    # Display insights
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Top Improvements:**")
        if improvements:
            improvements.sort(key=lambda x: x[1], reverse=True)
            for category, diff in improvements[:3]:
                st.write(f"• {category}: +{diff:.1f} points")
        else:
            st.write("No improvements detected")

    with col2:
        st.markdown("**Areas for Focus:**")
        if declines:
            declines.sort(key=lambda x: x[1], reverse=True)
            for category, diff in declines[:3]:
                st.write(f"• {category}: -{diff:.1f} points")
        else:
            st.write("No declines detected")

    # Create Excel download
    if st.button("Generate Report"):
        # Create DataFrame for Excel
        data = []
        
        # Add campaign info
        data.append(["Campaign Information", "", "", ""])
        data.append(["Campaign Name", campaign_name, "", ""])
        data.append(["Campaign Date", campaign_date.strftime("%Y-%m-%d"), "", ""])
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
        
        # Add totals
        data.append(["", "", "", ""])
        data.append(["Score Summary", "", "", ""])
        data.append(["Pre-Campaign Total", f"{pre_total}/{pre_max}", "", ""])
        data.append(["Post-Campaign Total", f"{post_total}/{post_max}", "", ""])
        
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
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    create_campaign_scorecard()
