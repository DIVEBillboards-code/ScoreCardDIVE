import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from openpyxl.styles import Font, PatternFill

# Enhanced CSS for better UX/UI
st.markdown("""
    <style>
    /* Modern color palette with more depth */
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
        --shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    /* Base styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    body {
        background-color: var(--gray-100);
        padding: 20px;
        min-height: 100vh;
    }

    /* Container improvements with animation */
    .stContainer, .stContainer-post {
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: var(--shadow);
        background-color: white;
        transition: all 0.3s ease;
        overflow: hidden;
    }
    .stContainer:hover, .stContainer-post:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }

    /* Post-Campaign specific background */
    .stContainer-post {
        background-color: #f0f0f0; /* Light gray for distinction */
        border: 1px solid var(--gray-300);
    }

    /* Enhanced header with gradient and animation */
    .stHeader {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 28px;
        box-shadow: 0 6px 16px rgba(0, 102, 255, 0.2);
        animation: fadeInUp 0.5s ease-out;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Subheader with improved styling */
    .stSubheader {
        color: var(--primary-dark);
        font-size: 1.5rem;
        font-weight: 600;
        margin: 20px 0 16px;
        padding-bottom: 12px;
        border-bottom: 4px solid var(--primary);
        transition: color 0.3s ease, transform 0.3s ease;
        cursor: pointer;
    }
    .stSubheader:hover {
        color: var(--primary);
        transform: scale(1.02);
    }

    /* Metric tiles with enhanced design */
    .stMetric {
        background: linear-gradient(135deg, white, var(--gray-100));
        padding: 20px;
        border-radius: 12px;
        border: 1px solid var(--gray-300);
        box-shadow: var(--shadow);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .stMetric:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
    }

    /* Buttons with more polish */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        border-radius: 12px;
        padding: 14px 28px;
        border: none;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        font-size: 16px;
        box-shadow: var(--shadow);
        width: auto;
        margin: 10px 0;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-dark) 0%, #004399 100%);
        box-shadow: 0 8px 20px rgba(0, 102, 255, 0.3);
        transform: translateY(-2px);
    }

    /* Inputs and select boxes */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid var(--gray-300);
        padding: 12px 16px;
        transition: all 0.3s ease;
        background-color: var(--gray-100);
        font-size: 14px;
    }
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 4px var(--primary-light);
        background-color: white;
        outline: none;
    }

    /* Expander styling */
    .st-expander {
        border: 1px solid var(--gray-300);
        border-radius: 12px;
        margin-bottom: 16px;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    .st-expander:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    .st-expander-header {
        color: var(--primary-dark) !important;
        font-weight: 500;
        padding: 12px 16px;
    }
    .st-expander-content {
        padding: 16px;
        background-color: var(--gray-100);
        border-radius: 0 0 12px 12px;
    }

    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--primary-dark) 100%);
        border-radius: 8px;
        height: 10px !important;
        transition: width 0.5s ease-in-out;
    }
    .stProgress {
        height: 10px !important;
        margin: 10px 0;
    }

    /* Score indicators */
    .score-indicator {
        padding: 10px 20px;
        border-radius: 10px;
        font-weight: 600;
        text-align: center;
        margin-top: 12px;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
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
    .score-indicator:hover {
        transform: scale(1.05);
    }

    /* Dividers */
    hr {
        height: 2px;
        background: linear-gradient(to right, transparent, var(--gray-300), transparent);
        border: none;
        margin: 24px 0;
    }

    /* Tooltip improvements */
    .stTooltipIcon {
        color: var(--primary) !important;
        transition: transform 0.2s ease, color 0.2s ease;
        cursor: help;
    }
    .stTooltipIcon:hover {
        color: var(--primary-dark) !important;
        transform: scale(1.2);
    }

    /* Chart customization */
    .js-plotly-plot .plotly .modebar {
        background: white !important;
        box-shadow: var(--shadow);
        border-radius: 8px;
        padding: 8px;
    }
    .plotly-graph-div {
        border-radius: 12px;
        box-shadow: var(--shadow);
        margin-bottom: 24px;
    }

    /* Table styling */
    table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--shadow);
        background-color: white;
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
        border-top: 2px solid var(--primary);
    }
    tr:last-child td {
        border-bottom: none;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .stContainer, .stContainer-post {
            padding: 16px;
        }
        .stHeader {
            font-size: 1.5rem;
            padding: 16px;
        }
        .stSubheader {
            font-size: 1.2rem;
        }
        .stButton > button {
            padding: 12px 24px;
            font-size: 14px;
        }
    }

    /* Animation for all containers */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stContainer, .stContainer-post, .stMetric {
        animation: fadeInUp 0.5s ease-out;
    }
    </style>
""", unsafe_allow_html=True)

# Update the visualization settings
def update_plot_theme(fig):
    fig.update_layout(
        font_family="Inter, -apple-system, BlinkMacSystemFont, sans-serif",
        title_font_size=22,
        title_font_family="Inter, -apple-system, BlinkMacSystemFont, sans-serif",
        title_font_color="#0066ff",
        plot_bgcolor="rgba(248, 249, 250, 0.8)",
        paper_bgcolor="white",
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            bgcolor="white",
            bordercolor="rgba(0, 0, 0, 0.1)",
            borderwidth=1,
            font=dict(size=14, color="#333333")
        ),
        margin=dict(t=60, b=60, l=60, r=60),
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background for cleaner look
    )
    return fig

def create_campaign_scorecard():
    st.set_page_config(page_title="Campaign Scorecard", layout="wide", initial_sidebar_state="collapsed")

    # Initialize session state
    if 'pre_scores' not in st.session_state:
        st.session_state.pre_scores = {}
    if 'post_scores' not in st.session_state:
        st.session_state.post_scores = {}
    if 'comments' not in st.session_state:
        st.session_state.comments = {}

    # Sidebar for quick navigation
    with st.sidebar:
        st.markdown("<h2 style='color: var(--primary-dark);'>Navigation</h2>", unsafe_allow_html=True)
        if st.button("Jump to Summary"):
            st.session_state.jump_to_summary = True

    # Main content with tabs for better organization
    tab1, tab2, tab3 = st.tabs(["Campaign Info", "Scorecards", "Visualizations & Insights"])

    with tab1:
        with st.container():
            st.markdown('<div class="stContainer"><div class="stHeader">Campaign Information</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                campaign_name = st.text_input("Campaign Name", key="campaign_name", help="Enter the name of the campaign")
                start_date = st.date_input("Start Date", key="start_date")
                client_name = st.text_input("Client Name", key="client_name")
            with col2:
                end_date = st.date_input("End Date", key="end_date")
                country = st.text_input("Country", key="country")
                cities = st.text_input("Cities", key="cities", help="Enter cities separated by commas")
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        # Create two columns for Pre and Post Campaign with adjusted ratio
        pre_col, post_col = st.columns([1, 1.5])  # Slightly larger Post column

        # Pre-Campaign Metrics
        with pre_col:
            with st.container():
                st.markdown('<div class="stContainer"><div class="stHeader">Pre-Campaign Scorecard</div>', unsafe_allow_html=True)
                for category, metrics in pre_metrics.items():
                    with st.expander(f"{category}", expanded=False):
                        for metric in metrics:
                            key = f"pre_{category}_{metric}"
                            col1, col2, col3 = st.columns([2, 1, 1])
                            with col1:
                                st.write(metric)
                            with col2:
                                score = st.selectbox(
                                    "Score",
                                    options=list(score_options.keys()),
                                    format_func=lambda x: score_options[x],
                                    key=f"score_{key}",
                                    help="Rate the metric"
                                )
                                st.session_state.pre_scores[key] = score
                            with col3:
                                comment = st.text_area("Comments", key=f"comment_{key}", height=50, label_visibility="collapsed")
                                st.session_state.comments[key] = comment
                            st.markdown('<hr style="border: 1px solid var(--gray-300); margin: 10px 0;">', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # Post-Campaign Metrics
        with post_col:
            with st.container():
                st.markdown('<div class="stContainer-post"><div class="stHeader">Post-Campaign Scorecard</div>', unsafe_allow_html=True)
                for category, metrics in post_metrics.items():
                    with st.expander(f"{category}", expanded=False):
                        for metric in metrics:
                            key = f"post_{category}_{metric}"
                            col1, col2, col3 = st.columns([2, 1, 1])
                            with col1:
                                st.write(metric)
                            with col2:
                                score = st.selectbox(
                                    "Score",
                                    options=list(score_options.keys()),
                                    format_func=lambda x: score_options[x],
                                    key=f"score_{key}",
                                    help="Rate the metric"
                                )
                                st.session_state.post_scores[key] = score
                            with col3:
                                comment = st.text_area("Comments", key=f"comment_{key}", height=50, label_visibility="collapsed")
                                st.session_state.comments[key] = comment
                            st.markdown('<hr style="border: 1px solid var(--gray-300); margin: 10px 0;">', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        # Calculate totals
        pre_total = sum(st.session_state.pre_scores.values()) if st.session_state.pre_scores else 0
        post_total = sum(st.session_state.post_scores.values()) if st.session_state.post_scores else 0
        pre_max = len([metric for metrics in pre_metrics.values() for metric in metrics]) * 5
        post_max = len([metric for metrics in post_metrics.values() for metric in metrics]) * 5

        pre_percentage = (pre_total / pre_max * 100) if pre_max > 0 else 0
        post_percentage = (post_total / post_max * 100) if post_max > 0 else 0

        pre_progress = pre_percentage / 100 if pre_max > 0 else 0
        post_progress = post_percentage / 100 if post_max > 0 else 0

        # DataFrames for visualization
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

        # Improvements and declines
        improvements, declines = [], []
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

        # Visualizations and Insights
        with st.container():
            st.markdown('<div class="stContainer"><div class="stHeader">Score Summary & Visualizations</div>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="stMetric"><h3>Pre-Campaign Score</h3><h1>{pre_percentage:.1f}%</h1>', unsafe_allow_html=True)
                st.progress(pre_progress)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown(f'<div class="stMetric"><h3>Post-Campaign Score</h3><h1>{post_percentage:.1f}%</h1>', unsafe_allow_html=True)
                st.progress(post_progress)
                st.markdown('</div>', unsafe_allow_html=True)

            viz_type = st.selectbox(
                "Select Visualization",
                ["Category Performance", "Radar Chart", "Score Distribution", "Phase Comparison"],
                key="viz_type",
                help="Choose how to visualize the data"
            )

            if viz_type == "Category Performance" and not combined_df.empty:
                fig = px.bar(combined_df, x='Category', y='Average Score', color='Phase', barmode='group', title='Category Performance')
                fig = update_plot_theme(fig)
                st.plotly_chart(fig, use_container_width=True)

            elif viz_type == "Radar Chart" and not pre_df.empty and not post_df.empty:
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(r=pre_df['Average Score'], theta=pre_df['Category'], fill='toself', name='Pre-Campaign'))
                fig.add_trace(go.Scatterpolar(r=post_df['Average Score'], theta=post_df['Category'], fill='toself', name='Post-Campaign'))
                fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title='Radar Chart: Category Scores')
                fig = update_plot_theme(fig)
                st.plotly_chart(fig, use_container_width=True)

            elif viz_type == "Score Distribution" and (st.session_state.pre_scores or st.session_state.post_scores):
                all_scores = list(st.session_state.pre_scores.values()) + list(st.session_state.post_scores.values())
                fig = px.histogram(x=all_scores, nbins=5, title='Score Distribution')
                fig = update_plot_theme(fig)
                st.plotly_chart(fig, use_container_width=True)

            elif viz_type == "Phase Comparison" and not combined_df.empty:
                fig = px.scatter(combined_df, x='Category', y='Average Score', color='Phase', title='Pre vs Post Comparison')
                fig = update_plot_theme(fig)
                st.plotly_chart(fig, use_container_width=True)

            # Insights
            with st.expander("Key Insights", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Top Improvements")
                    if improvements:
                        for cat, diff in sorted(improvements, key=lambda x: x[1], reverse=True)[:3]:
                            st.success(f"{cat}: +{diff:.1f}%")
                    else:
                        st.info("No improvements detected")

                with col2:
                    st.subheader("Areas for Focus")
                    if declines:
                        for cat, diff in sorted(declines, key=lambda x: x[1], reverse=True)[:3]:
                            st.error(f"{cat}: -{diff:.1f}%")
                    else:
                        st.info("No declines detected")

            # Download Report
            if st.button("Generate & Download Report", key="download_report"):
                data = [
                    ["Campaign Information"],
                    ["Campaign Name", campaign_name],
                    ["Start Date", start_date.strftime("%Y-%m-%d")],
                    ["End Date", end_date.strftime("%Y-%m-%d")],
                    ["Client Name", client_name],
                    ["Country", country],
                    ["Cities", cities],
                    ["", ""],
                    ["Pre-Campaign Scorecard"],
                    ["Category", "Metric", "Score", "Comments"]
                ]

                for category, metrics in pre_metrics.items():
                    for metric in metrics:
                        key = f"pre_{category}_{metric}"
                        data.append([category, metric, st.session_state.pre_scores.get(key, 0), st.session_state.comments.get(key, "")])

                data.extend([["", ""], ["Post-Campaign Scorecard"], ["Category", "Metric", "Score", "Comments"]])

                for category, metrics in post_metrics.items():
                    for metric in metrics:
                        key = f"post_{category}_{metric}"
                        data.append([category, metric, st.session_state.post_scores.get(key, 0), st.session_state.comments.get(key, "")])

                data.extend([["", ""], ["Summary"], ["Pre-Campaign Score", f"{pre_percentage:.1f}%"], ["Post-Campaign Score", f"{post_percentage:.1f}%"]])

                df = pd.DataFrame(data)
                excel_file = f"campaign_scorecard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

                with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, header=False)
                    workbook = writer.book
                    worksheet = writer.sheets['Sheet1']

                    header_fill = PatternFill(start_color='CCCCCC', end_color='CCCCCC', fill_type='solid')
                    for row in [0, 8, 9, len(pre_metrics) + 10, len(pre_metrics) + len(post_metrics) + 11]:
                        for cell in worksheet[f'{row+1}:{row+1}']:
                            cell.font = Font(bold=True)
                            cell.fill = header_fill

                    for column in worksheet.columns:
                        max_length = 0
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(cell.value)
                            except:
                                pass
                        adjusted_width = (max_length + 2)
                        worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

                with open(excel_file, 'rb') as f:
                    st.download_button("Download Excel", data=f, file_name=excel_file, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            st.markdown('</div>', unsafe_allow_html=True)

    # Metrics and insights at the bottom for quick reference
    st.markdown(f"<h2 style='color: var(--primary-dark); text-align: center;'>Quick Summary</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Pre-Campaign", f"{pre_percentage:.1f}%")
    with col2:
        st.metric("Post-Campaign", f"{post_percentage:.1f}%")

if __name__ == "__main__":
    create_campaign_scorecard()
