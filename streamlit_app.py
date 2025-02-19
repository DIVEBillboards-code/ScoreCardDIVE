import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

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

    # Pre-Campaign Metrics
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
                    st.write(metric)
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
                    st.write(metric)
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
    pre_total = sum(st.session_state.pre_scores.values())
    post_total = sum(st.session_state.post_scores.values())
    pre_max = len([metric for metrics in pre_metrics.values() for metric in metrics]) * 5
    post_max = len([metric for metrics in post_metrics.values() for metric in metrics]) * 5

    # Display totals and visualizations
    st.header("Score Summary and Visualizations")
    
    # Summary metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Pre-Campaign Total", f"{pre_total}/{pre_max}")
        st.progress(pre_total/pre_max)
    with col2:
        st.metric("Post-Campaign Total", f"{post_total}/{post_max}")
        st.progress(post_total/post_max)

    # Create DataFrames for visualization
    def create_category_df(scores_dict, metrics_dict, phase):
        data = []
        for category, metrics in metrics_dict.items():
            category_scores = [scores_dict.get(f"{phase}_{category}_{metric}", 0) for metric in metrics]
            avg_score = np.mean(category_scores)
            data.append({
                'Category': category,
                'Average Score': avg_score,
                'Phase': 'Pre-Campaign' if phase == 'pre' else 'Post-Campaign'
            })
        return pd.DataFrame(data)

    pre_df = create_category_df(st.session_state.pre_scores, pre_metrics, 'pre')
    post_df = create_category_df(st.session_state.post_scores, post_metrics, 'post')
    combined_df = pd.concat([pre_df, post_df])

    # Visualization Section
    st.subheader("Data Visualizations")
    
    # Select visualization type
    viz_type = st.selectbox(
        "Select Visualization Type",
        ["Category Performance", "Radar Chart", "Score Distribution", "Phase Comparison"]
    )

    if viz_type == "Category Performance":
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

    elif viz_type == "Radar Chart":
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

    elif viz_type == "Score Distribution":
        # Histogram of score distribution
        all_pre_scores = list(st.session_state.pre_scores.values())
        all_post_scores = list(st.session_state.post_scores.values())
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=all_pre_scores,
            name='Pre-Campaign',
            nbinsx=3,
            opacity=0.7
        ))
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

    elif viz_type == "Phase Comparison":
        # Scatter plot comparing pre vs post scores
        categories = list(pre_metrics.keys())
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
        pre_score = pre_df[pre_df['Category'] == category]['Average Score'].iloc[0]
        post_score = post_df[post_df['Category'] == category]['Average Score'].iloc[0]
        diff = post_score - pre_score
        if diff > 0:
            improvements.append((category, diff))
        elif diff < 0:
            declines.append((category, abs(diff)))

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
            from openpyxl.styles import Font, PatternFill
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
