"""
Streamlit UI components and helper functions
"""
import streamlit as st
import pandas as pd
from datetime import datetime


def setup_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Referral Dashboard Generator",
        page_icon="📊",
        layout="wide"
    )


def render_sidebar():
    """Render sidebar configuration options"""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Date override option
        use_custom_date = st.checkbox("Use custom date (instead of today)")
        if use_custom_date:
            custom_date = st.date_input("Select date for analysis", value=datetime.now().date())
            today = pd.to_datetime(custom_date).normalize()
        else:
            today = pd.to_datetime("today").normalize()
        
        st.info(f"Analysis date: {today.strftime('%Y-%m-%d')}")
        
        return today


def render_file_uploader():
    """Render file upload widget"""
    return st.file_uploader(
        "Upload Excel file", 
        type=['xlsx', 'xls'],
        help="Upload your Umoja Referral Overview Excel file"
    )


def render_summary_metrics(summary_data):
    """Render summary metrics in a grid layout"""
    st.header("📈 Summary Metrics")
    
    # Create columns for metrics
    cols = st.columns(4)
    
    for i, (_, row) in enumerate(summary_data.iterrows()):
        col_idx = i % 4
        with cols[col_idx]:
            st.metric(
                label=row['Category'],
                value=row['Number of Referrals'],
                help=row['Definition']
            )


def render_summary_table(summary_data):
    """Render detailed summary table"""
    st.subheader("📋 Detailed Summary")
    st.dataframe(
        summary_data,
        use_container_width=True,
        hide_index=True
    )


def render_detailed_analysis(data):
    """Render expandable sections for detailed analysis"""
    from data_processor import prepare_dataframe_for_display
    
    st.header("🔍 Detailed Analysis")
    
    sections = [
        ("Initial MTG Box Delivery", data['initial_mtg']),
        ("Ongoing MTG Box Delivery", data['ongoing_mtg']),
        ("Nutritional Assessment", data['nutritional_assessment']),
        ("Speak to Member", data['speak_to_member']),
        ("TAR Approval", data['tar_approval']),
        ("CCHP Nutrition Counseling", data['cchp_nutrition']),
        ("Reauthorization Pending", data['reauth_pending'])
    ]

    for title, df_section in sections:
        with st.expander(f"{title} ({len(df_section)} records)"):
            if len(df_section) > 0:
                display_df = prepare_dataframe_for_display(df_section)
                st.dataframe(display_df, use_container_width=True, hide_index=True)
            else:
                st.info("No records found for this category.")


def render_download_section(data, summary_data):
    """Render download buttons and functionality"""
    st.header("💾 Download Report")
    
    # Center the Excel download button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        render_excel_download_button(data)


def render_excel_download_button(data):
    """Render Excel download functionality"""
    from excel_generator import create_excel_report
    
    with st.spinner("Preparing Excel report..."):
        excel_data = create_excel_report(data, datetime.now())
        
        # Direct download button
        st.download_button(
            label="📥 Download Excel Report",
            data=excel_data,
            file_name=f"referral_dashboard_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )


def render_data_info(df, today):
    """Render data information section"""
    st.header("ℹ️ Data Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        st.metric("Analysis Date", today.strftime('%Y-%m-%d'))


def render_instructions():
    """Render instructions when no file is uploaded"""
    st.info("👆 Please upload an Excel file to get started.")
    
    # st.markdown("""
    # ### Expected File Format
    # Your Excel file must contain all of the following columns:
    # """)
    
    # # Display expected columns in a more readable format
    # expected_columns = [
    #     'Payer Organization', 'Implify Member ID', 'Zip Code', 'County',
    #     'Referral Created Date', 'Referral Start Date', 'Referral End Date',
    #     'ECM Enrollment', 'Condition', 'Service Type', 'Last Activity Completed',
    #     'Last Activity Date', 'Pending Task/ Next Task', 'Day(s) in Current Activity',
    #     'Date of Last Delivered box', 'Box Type', 'Number of Grocery Boxes Successfully Sent',
    #     'Outreach Attempt within 48 Hours of Referral', 'Number of Outreach Attempts by GGH',
    #     'Outreach Method', 'Number of Nutrition Counseling Sessions Completed',
    #     'Need TAR Submission', 'TAR Submission Status', 'Claims Submitted',
    #     'Outstanding Claims: CHW', 'Outstanding Claims: MTG/MTM',
    #     'Outstanding Claims: Nutritional Counseling', 'Ready for Re-authorization',
    #     'Re-authorization Status'
    # ]
    
    # # Display columns in a compact format
    # col1, col2 = st.columns(2)
    
    # with col1:
    #     for i, col in enumerate(expected_columns[:15]):
    #         st.write(f"• {col}")
    
    # with col2:
    #     for i, col in enumerate(expected_columns[15:]):
    #         st.write(f"• {col}")
    
    # st.markdown("""
    # ### Features
    # - 📊 **Interactive Dashboard**: View summary metrics and detailed breakdowns
    # - 📥 **Excel Export**: Download formatted Excel report with multiple sheets
    # - ⚙️ **Date Override**: Use custom analysis date if needed
    # - 🔍 **Detailed Views**: Expandable sections for each metric category
    # """)


def show_error_message(error):
    """Display error message with helpful information"""
    error_str = str(error)
    
    # Check if it's a validation error (contains column structure message)
    if "Invalid Column Structure" in error_str:
        st.error(error_str)
    else:
        st.error(f"❌ Error processing file: {error_str}")
        st.info("Please ensure your Excel file has the expected column structure and data types.")


def show_success_message():
    """Display success message"""
    st.success("✅ Data processed successfully!")
