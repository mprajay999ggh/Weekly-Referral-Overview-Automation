import streamlit as st
import pandas as pd
from datetime import datetime
import warnings

# Suppress pandas and pyarrow warnings
warnings.filterwarnings('ignore', category=UserWarning, module='pyarrow')
warnings.filterwarnings('ignore', category=FutureWarning, module='pandas')

# Import custom modules
from data_processor import process_referral_data
from ui_components import (
    setup_page_config, render_sidebar, render_file_uploader,
    render_summary_metrics, render_summary_table, render_detailed_analysis,
    render_download_section, render_data_info, render_instructions,
    show_error_message, show_success_message
)

# Set page config
setup_page_config()

def main():
    st.title("📊 Referral Dashboard Generator")
    st.markdown("Upload your referral data Excel file to generate a comprehensive dashboard with pending tasks analysis.")

    # Sidebar for configuration
    today = render_sidebar()

    # File upload
    uploaded_file = render_file_uploader()

    if uploaded_file is not None:
        try:
            # Load data
            with st.spinner("Loading and processing data..."):
                df = pd.read_excel(uploaded_file, engine='openpyxl', keep_default_na=False)
                
                # Process data
                data = process_referral_data(df, today)

            show_success_message()

            # Download section
            render_download_section(data, data['summary'])

            # Display summary metrics
            render_summary_metrics(data['summary'])

            # Display summary table
            render_summary_table(data['summary'])

            # Expandable sections for detailed views
            render_detailed_analysis(data)

            # Data info
            render_data_info(df, today)

        except Exception as e:
            show_error_message(e)
            st.info("💡 **Tip**: This error might be due to data format issues. Please ensure your Excel file has the expected column structure and data types.")

    else:
        # Show instructions
        render_instructions()


if __name__ == "__main__":
    main()
