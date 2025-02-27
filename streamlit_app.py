import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from openpyxl.styles import Font, PatternFill

# CSS for better UX (unchanged)
st.markdown("""
    <style>
    /* [CSS content remains unchanged] */
    </style>
""", unsafe_allow_html=True)

# Update the visualization settings (unchanged)
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
    # Initialize session state
    if 'pre_scores' not in st.session_state:
        st.session_state.pre_scores = {}
    if 'post_scores' not in st.session_state:
        st.session_state.post_scores = {}
    if 'comments' not in st.session_state:
        st.session_state.comments = {}

    # Define metric_definitions
    metric_definitions = {
        # Common Pre-Campaign Metrics (All Campaigns)
        'Assets received on time': 'Measures if all creative assets were delivered by the scheduled date.',
        'Storyboard approvals met deadlines': 'Checks if storyboard approvals were completed on time.',
        'Creative meets format & resolution': 'Ensures creative assets meet required formats and resolution standards.',
        'Workback schedule followed': 'Verifies if the production timeline was adhered to as planned.',
        'Vendor deadlines met': 'Confirms if external vendors met their deadlines.',
        'Final creative delivered on time': 'Ensures the final creative was delivered by the deadline.',
        'Billboard locations confirmed': 'Verifies that billboard placements were secured and confirmed.',
        'Vendor tests & pre-launch checks done': 'Confirms all pre-launch tests and checks by vendors were completed.',
        # Strategy Category (All Campaigns)
        'QR Code Added': 'Checks if a QR code was included in the campaign materials.',
        'Clear CTA': 'Ensures the campaign includes a clear Call-to-Action.',
        'Hashtag': 'Confirms a campaign-specific hashtag was created and implemented.',
        # TikTok-Only Pre-Campaign Metrics
        'TikTok Platform Compliance': 'Ensures content meets TikTok’s platform-specific rules.',
        'TikTok Ad Moderation Passed': 'Confirms TikTok ads passed moderation checks.',
        'TikTok Branded Mission': 'Verifies alignment with TikTok’s branded mission feature.',
        'TikTok Branded Effects': 'Confirms branded effects were implemented on TikTok.',
        'Creators Approval / responsiveness': 'Assesses responsiveness of creators during approvals.',
        'Client Approvals Responsiveness': 'Evaluates client responsiveness during approval processes.',
        'Creators UGC Approvals': 'Confirms approval of user-generated content from creators.',
        # Common Post-Campaign Metrics (All Campaigns)
        'High-quality images captured': 'Ensures campaign visuals meet quality standards.',
        'Splash video created': 'Confirms a promotional video was produced.',
        'Social media features': 'Tracks use of social media features like stories or reels.',
        'Key wins identified': 'Highlights successful aspects of the campaign.',
        'Areas for improvement noted': 'Identifies aspects needing enhancement.',
    }

    # Define recommendations for automated insights
    recommendations = {
        'Assets received on time': 'Set earlier internal deadlines or improve coordination with asset providers.',
        'Storyboard approvals met deadlines': 'Streamline the approval process with clearer timelines.',
        'Creative meets format & resolution': 'Review asset specifications with the creative team before submission.',
        'Workback schedule followed': 'Enhance timeline visibility with project management tools.',
        'Vendor deadlines met': 'Increase vendor oversight or negotiate stricter deadlines.',
        'Final creative delivered on time': 'Implement buffer periods or escalate delays earlier.',
        'Billboard locations confirmed': 'Confirm locations earlier in the planning phase.',
        'Vendor tests & pre-launch checks done': 'Schedule pre-launch checks earlier to catch issues.',
        'QR Code Added': 'Ensure QR code inclusion is part of the initial creative brief.',
        'Clear CTA': 'Test CTAs with a focus group to ensure clarity.',
        'Hashtag': 'Promote hashtag usage earlier in the campaign.',
        'TikTok Platform Compliance': 'Train team on TikTok guidelines or consult platform experts.',
        'TikTok Ad Moderation Passed': 'Submit ads earlier to allow time for revisions.',
        'TikTok Branded Mission': 'Align mission with TikTok trends for better traction.',
        'TikTok Branded Effects': 'Test effects with a small audience before full rollout.',
        'Creators Approval / responsiveness': 'Set clear response deadlines for creators.',
        'Client Approvals Responsiveness': 'Schedule regular check-ins to expedite client feedback.',
        'Creators UGC Approvals': 'Simplify UGC approval process with predefined criteria.',
        'High-quality images captured': 'Invest in better equipment or training for photography team.',
        'Splash video created': 'Plan video production earlier to ensure quality.',
        'Social media features': 'Experiment with additional features like polls or live streams.',
        'Key wins identified': 'Document wins in real-time during the campaign.',
        'Areas for improvement noted': 'Conduct a post-mortem meeting to identify gaps.'
    }

    score_options = {
        0: "0 - No/Poor",
        3: "3 - Partial/Medium",
        5: "5 - Yes/Excellent"
    }

    # Campaign Information with Category Filter
    with st.container():
        st.markdown('<div class="stContainer"><div class="stHeader">Campaign Information</div>', unsafe_allow_html=True)
        campaign_type = st.selectbox("Campaign Type", ["TikTok Campaign", "DIVE Campaign", "BYOB"], key="campaign_type")
        campaign_name = st.text_input("Campaign Name", key="campaign_name")
        start_date = st.date_input("Start Date", key="start_date")
        end_date = st.date_input("End Date", key="end_date")
        client_name = st.text_input("Client Name", key="client_name")
        country = st.text_input("Country", key="country")
        cities = st.text_input("Cities", key="cities", help="Enter cities separated by commas")
        
        # Define base metrics for filtering
        pre_metrics_base = {
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
                'Billboard locations confirmed'
            ],
            'Approval & Compliance': [
                'Vendor tests & pre-launch checks done'
            ],
            'Strategy': [
                'QR Code Added',
                'Clear CTA',
                'Hashtag'
            ],
            'TikTok Specific': [
                'TikTok Platform Compliance',
                'TikTok Ad Moderation Passed',
                'TikTok Branded Mission',
                'TikTok Branded Effects',
                'Creators Approval / responsiveness',
                'Client Approvals Responsiveness',
                'Creators UGC Approvals'
            ]
        }
        post_metrics_base = {
            'Photography & Visibility': [
                'High-quality images captured',
                'Splash video created',
                'Social media features'
            ],
            'Campaign Learnings': [
                'Key wins identified',
                'Areas for improvement noted'
            ]
        }

        # Interactive Metric Filtering
        all_pre_categories = [cat for cat in pre_metrics_base.keys() if cat != 'TikTok Specific' or campaign_type == "TikTok Campaign"]
        selected_pre_categories = st.multiselect(
            "Select Pre-Campaign Categories to Score",
            all_pre_categories,
            default=all_pre_categories,
            key="pre_category_filter"
        )
        all_post_categories = list(post_metrics_base.keys())
        selected_post_categories = st.multiselect(
            "Select Post-Campaign Categories to Score",
            all_post_categories,
            default=all_post_categories,
            key="post_category_filter"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Filter pre_metrics based on campaign type and user selection
    pre_metrics = {}
    for category, metrics in pre_metrics_base.items():
        if category in selected_pre_categories and (campaign_type != "TikTok Campaign" or category != 'TikTok Specific' or 'TikTok Specific' in selected_pre_categories):
            pre_metrics[category] = metrics

    # Filter post_metrics based on user selection
    post_metrics = {cat: post_metrics_base[cat] for cat in selected_post_categories if cat in post_metrics_base}

    # Pre-Campaign Section
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

    # Post-Campaign Section
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

    pre_percentage = (pre_total / pre_max * 100) if pre_max > 0 else 0
    post_percentage = (post_total / post_max * 100) if post_max > 0 else 0
    pre_progress = pre_percentage / 100 if pre_max > 0 else 0
    post_progress = post_percentage / 100 if post_max > 0 else 0

    # Get unique categories
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

    # Calculate improvements and declines
    improvements = []
    declines = []
    common_categories = set(pre_df['Category']).intersection(set(post_df['Category']))
    
    for category in common_categories:
        try:
            pre_score = pre_df[pre_df['Category'] == category]['Average Score'].iloc[0] if not pre_df[pre_df['Category'] == category].empty else 0
            post_score = post_df[post_df['Category'] == category]['Average Score'].iloc[0] if not post_df[post_df['Category'] == category].empty else 0
            pre_percent = (pre_score / 5) * 100 if pre_score > 0 else 0
            post_percent = (post_score / 5) * 100 if post_score > 0 else 0
            if pre_percent == 0 and post_percent == 0:
                continue
            elif pre_percent == 0 and post_percent > 0:
                improvements.append((category, post_percent))
            else:
                diff = post_percent - pre_percent
                if diff > 0:
                    improvements.append((category, diff))
                elif diff < 0:
                    declines.append((category, abs(diff)))
        except (IndexError, KeyError):
            continue

    # Display totals and visualizations
    with st.container():
        st.markdown('<div class="stContainer"><div class="stHeader">Score Summary and Visualizations</div>', unsafe_allow_html=True)
        
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

        st.subheader("Data Visualizations")
        viz_type = st.selectbox(
            "Select Visualization Type",
            ["Category Performance", "Radar Chart", "Score Distribution", "Phase Comparison"],
            key="viz_type_select"
        )

        if viz_type == "Category Performance" and not combined_df.empty:
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
            fig = px.scatter(
                combined_df,
                x='Category',
                y='Average Score',
                color='Phase',
                title='Pre vs Post Campaign Score Comparison',
                height=500
            )
            fig.update_traces(marker=dict(color='#0066ff'), selector=dict(type='scatter'))
            fig.update_layout(
                xaxis_tickangle=-45,
                yaxis_range=[0, 5],
                showlegend=True,
                plot_bgcolor='#f5f5f5',
                paper_bgcolor='#f5f5f5'
            )
            st.plotly_chart(fig, use_container_width=True)

        # Enhanced Key Insights with Automated Recommendations
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
                low_scores = [(key.split('_')[-1], score) for key, score in {**st.session_state.pre_scores, **st.session_state.post_scores}.items() if score < 3]
                if low_scores:
                    low_scores.sort(key=lambda x: x[1])  # Sort by score (lowest first)
                    for metric, score in low_scores[:3]:
                        st.write(f"• {metric} ({score_options[score]}): {recommendations.get(metric, 'Review process for improvement.')}")
                else:
                    st.write("No areas for focus detected")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Create Excel download
    with st.container():
        st.markdown('<div class="stContainer">', unsafe_allow_html=True)
        if st.button("Generate Report", key="generate_report", help="Download the scorecard as an Excel file"):
            data = []
            data.append(["Campaign Information", "", "", ""])
            data.append(["Campaign Type", campaign_type, "", ""])
            data.append(["Campaign Name", campaign_name, "", ""])
            data.append(["Start Date", start_date.strftime("%Y-%m-%d"), "", ""])
            data.append(["End Date", end_date.strftime("%Y-%m-%d"), "", ""])
            data.append(["Client Name", client_name, "", ""])
            data.append(["Country", country, "", ""])
            data.append(["Cities", cities, "", ""])
            data.append(["", "", "", ""])
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
            data.append(["", "", "", ""])
            data.append(["Score Summary", "", "", ""])
            data.append(["Pre-Campaign Score", f"{pre_percentage:.1f}%", "", ""])
            data.append(["Post-Campaign Score", f"{post_percentage:.1f}%", "", ""])
            
            df = pd.DataFrame(data)
            excel_file = f"{campaign_type.lower().replace(' ', '_')}_scorecard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False)
                workbook = writer.book
                worksheet = writer.sheets['Sheet1']
                header_fill = PatternFill(start_color='CCCCCC', end_color='CCCCCC', fill_type='solid')
                for cell in worksheet['1:1']:
                    cell.font = Font(bold=True)
                    cell.fill = header_fill
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
