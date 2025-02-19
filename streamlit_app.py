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
        campaign_date = st.date_input("Campaign Date", key="campaign_date")
        start_date = st.date_input("Start Date", key="start_date")
        end_date = st.date_input("End Date", key="end_date")
        client_name = st.text_input("Client Name", key="client_name")
        country = st.text_input("Country", key="country")
        cities = st.text_input("Cities", key="cities", help="Enter cities separated by commas")
        st.markdown('</div>', unsafe_allow_html=True)

    # Rest of the function remains the same...
    # (Keep the pre_col, post_col, pre_metrics, post_metrics, metric_definitions, score_options, and all other sections unchanged)

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

    # Definitions for tooltips (unchanged)
    metric_definitions = {
        # ... (keep existing definitions as they are)
    }

    # Score options (unchanged)
    score_options = {
        0: "0 - No/Poor",
        3: "3 - Partial/Medium",
        5: "5 - Yes/Excellent"
    }

    # The rest of the function (Pre-Campaign Section, Post-Campaign Section, Calculate totals, Visualizations, Excel download) remains the same.
    # However, you'll also need to update the Excel report generation to include these new fields.

    # Update the Excel report generation to include new fields
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
            
            # Add Pre-Campaign data (unchanged)
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
            
            # Add Post-Campaign data (unchanged)
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
            
            # Add totals as percentages (unchanged)
            data.append(["", "", "", ""])
            data.append(["Score Summary", "", "", ""])
            data.append(["Pre-Campaign Score", f"{pre_percentage:.1f}%", "", ""])
            data.append(["Post-Campaign Score", f"{post_percentage:.1f}%", "", ""])
            
            # Create DataFrame and Excel file (unchanged)
            df = pd.DataFrame(data)
            excel_file = f"campaign_scorecard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            # Create Excel writer
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=False)
                
                # Get workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['Sheet1']
                
                # Add some styling (unchanged)
                header_fill = PatternFill(start_color='CCCCCC', end_color='CCCCCC', fill_type='solid')
                
                # Style headers
                for cell in worksheet['1:1']:
                    cell.font = Font(bold=True)
                    cell.fill = header_fill
            
            # Create download button (unchanged)
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
