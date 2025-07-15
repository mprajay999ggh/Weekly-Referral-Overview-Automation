"""
Data processing functions for referral dashboard
"""
import pandas as pd
import numpy as np
from datetime import timedelta


def validate_column_structure(df):
    """Validate that the DataFrame has the expected column structure"""
    # Clean column names first
    df = clean_column_names(df)
    
    expected_columns = [
        'Payer Organization',
        'Implify Member ID',
        'Zip Code',
        'County',
        'Referral Created Date',
        'Referral Start Date',
        'Referral End Date',
        'ECM Enrollment',
        'Condition',
        'Service Type',
        'Last Activity Completed',
        'Last Activity Date',
        'Pending Task/ Next Task',
        'Day(s) in Current Activity',
        'Date of Last Delivered box',
        'Box Type',
        'Number of Grocery Boxes Successfully Sent',
        'Outreach Attempt within 48 Hours of Referral',
        'Number of Outreach Attempts by GGH',
        'Outreach Method',
        'Number of Nutrition Counseling Sessions Completed',
        'Need TAR Submission',
        'TAR Submission Status',
        'Claims Submitted',
        'Outstanding Claims: CHW',
        'Outstanding Claims: MTG/MTM',
        'Outstanding Claims: Nutritional Counseling',
        'Ready for Re-authorization',
        'Re-authorization Status'
    ]
    
    # Check which expected columns are missing
    missing_columns = [col for col in expected_columns if col not in df.columns]
    
    if missing_columns:
        missing_list = '\n• '.join(missing_columns)
        raise ValueError(
            f"❌ **Invalid Column Structure**\n\n"
            f"The uploaded file does not have the expected column structure.\n\n"
            f"**Missing columns:**\n• {missing_list}\n\n"
            f"**Please ensure your Excel file contains all {len(expected_columns)} required columns.**"
        )
    
    return df  # Return the cleaned DataFrame


def clean_and_convert_data(df, today):
    """Clean and convert data columns to appropriate types"""
    df = df.copy()
    
    # Clean & Convert Date Columns
    date_columns = [
        'Referral Start Date', 
        'Referral Created Date', 
        'Last Activity Date',
        'Referral End Date',
        'Date of Last Delivered box'
    ]
    
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Calculate days in current activity
    df['Day(s) in Current Activity'] = (today - df['Last Activity Date']).dt.days
    
    # Clean numeric columns
    numeric_columns = [
        'Number of Grocery Boxes Successfully Sent',
        'Number of Nutrition Counseling Sessions Completed'
    ]
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Clean text columns to prevent mixed types
    text_columns = [
        'Pending Task/ Next Task',
        'Payer Organization',
        'Re-authorization Status',
        'Last Activity Completed'
    ]
    
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).replace('nan', '')
    
    # Fix mixed type columns that cause Arrow issues
    for col in df.columns:
        if df[col].dtype == 'object':
            # Check if column contains mixed types
            sample_vals = df[col].dropna().head(100)
            if len(sample_vals) > 0:
                # If it looks like it should be numeric but has strings, convert
                try:
                    pd.to_numeric(sample_vals)
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except:
                    # Keep as string but ensure consistent type
                    df[col] = df[col].astype(str).replace('nan', '')
    
    return df


def clean_column_names(df):
    """Clean column names by stripping leading and trailing spaces"""
    df.columns = df.columns.str.strip()
    return df


def filter_initial_mtg(df):
    """Filter records for initial MTG box delivery"""
    return df[
        (df['Pending Task/ Next Task'] == "MTG Box Delivery") &
        (df['Day(s) in Current Activity'] >= 4) &
        (df['Number of Grocery Boxes Successfully Sent'] == 0)
    ]


def filter_ongoing_mtg(df):
    """Filter records for ongoing MTG box delivery"""
    return df[
        (df['Pending Task/ Next Task'] == "MTG Box Delivery") &
        (df['Day(s) in Current Activity'] >= 8) &
        (df['Number of Grocery Boxes Successfully Sent'] != 0)
    ]


def filter_nutritional_assessment(df):
    """Filter records for nutritional assessment"""
    return df[
        (df['Pending Task/ Next Task'] == "Nutritional assessment") &
        (df['Day(s) in Current Activity'] >= 14)
    ]


def filter_speak_to_member(df):
    """Filter records for speak to member"""
    return df[
        (df['Pending Task/ Next Task'] == "Speak to Member") &
        (df['Day(s) in Current Activity'] >= 14)
    ]


def filter_tar_approval(df):
    """Filter records for TAR approval"""
    return df[
        (df['Pending Task/ Next Task'] == "TAR Approval") &
        (df['Day(s) in Current Activity'] >= 8)
    ]


def filter_cchp_nutrition(df, today):
    """Filter records for CCHP nutrition counseling"""
    return df[
        (df['Payer Organization'].str.upper() == "CCHP") &
        (df['Referral Created Date'] <= today - timedelta(days=49)) &
        (df['Number of Nutrition Counseling Sessions Completed'].isin([0,1])) &
        (~df['Pending Task/ Next Task'].astype(str).str.lower().str.contains("discontinued"))
    ]


def is_reauth_due(row, today):
    """Check if reauthorization is due for a specific row"""
    try:
        if str(row['Re-authorization Status']).strip().upper() != "NA":
            return False
        if str(row['Pending Task/ Next Task']).lower() in ["services discontinued", "service discontinued"]:
            return False
        if str(row.get('Last Activity Completed')).strip().lower() == "reauthorization approved":
            return False

        start_date = row['Referral Start Date']
        if pd.isnull(start_date):
            return False

        org = str(row['Payer Organization']).strip().upper()
        if org == "CCHP":
            return today >= start_date + timedelta(weeks=11)
        elif org == "CCAH":
            return today >= start_date + timedelta(weeks=15)
        elif org == "PHP":
            return today >= pd.to_datetime(start_date) + pd.DateOffset(months=5)
    except:
        return False
    return False


def filter_reauth_pending(df, today):
    """Filter records for pending reauthorization"""
    return df[df.apply(lambda row: is_reauth_due(row, today), axis=1)]


def create_summary_table(data_dict):
    """Create summary table with all metrics"""
    summary = pd.DataFrame({
        "Category": [
            "INITIAL MTG box delivery",
            "ONGOING MTG box delivery",
            "Nutritional assessment",
            "Speak to member",
            "TAR approval",
            "Nutritional counseling",
            "Reauth not submitted"
        ],
        "Number of Referrals": [
            len(data_dict['initial_mtg']),
            len(data_dict['ongoing_mtg']),
            len(data_dict['nutritional_assessment']),
            len(data_dict['speak_to_member']),
            len(data_dict['tar_approval']),
            len(data_dict['cchp_nutrition']),
            len(data_dict['reauth_pending'])
        ],
        "Definition": [
            "4 or more days pending delivery of initial box",
            "8 or more days pending delivery of follow-up boxes",
            "14 or more days pending nutritional assessment",
            "14 or more days pending speak to member status",
            "8 or more days pending TAR approval",
            "9 weeks from referral start date for CCHP",
            "CCHP - 11 weeks (out of 12)\nCCAH - 15 weeks (out of 17)\nPHP - 5 months (out of 6)"
        ]
    })
    return summary


def process_referral_data(df, today=None):
    """Main function to process referral data and generate all metrics"""
    if today is None:
        today = pd.to_datetime("today").normalize()
    
    # Validate column structure and clean column names
    df_cleaned = validate_column_structure(df)
    
    # Clean and convert data
    df_processed = clean_and_convert_data(df_cleaned, today)
    
    # Apply all filters
    initial_mtg = filter_initial_mtg(df_processed)
    ongoing_mtg = filter_ongoing_mtg(df_processed)
    nutritional_assessment = filter_nutritional_assessment(df_processed)
    speak_to_member = filter_speak_to_member(df_processed)
    tar_approval = filter_tar_approval(df_processed)
    cchp_nutrition = filter_cchp_nutrition(df_processed, today)
    reauth_pending = filter_reauth_pending(df_processed, today)
    
    # Create data dictionary
    data_dict = {
        'initial_mtg': initial_mtg,
        'ongoing_mtg': ongoing_mtg,
        'nutritional_assessment': nutritional_assessment,
        'speak_to_member': speak_to_member,
        'tar_approval': tar_approval,
        'cchp_nutrition': cchp_nutrition,
        'reauth_pending': reauth_pending,
        'processed_df': df_processed
    }
    
    # Create summary table
    summary = create_summary_table(data_dict)
    data_dict['summary'] = summary
    
    return data_dict


def prepare_dataframe_for_display(df):
    """Prepare DataFrame for Streamlit display to avoid Arrow serialization issues"""
    if df.empty:
        return df
    
    df_display = df.copy()
    
    # Convert datetime columns to strings for display
    for col in df_display.columns:
        if pd.api.types.is_datetime64_any_dtype(df_display[col]):
            df_display[col] = df_display[col].dt.strftime('%Y-%m-%d %H:%M:%S')
            df_display[col] = df_display[col].replace('NaT', '')
        elif df_display[col].dtype == 'object':
            # Ensure all object columns are strings
            df_display[col] = df_display[col].astype(str).replace('nan', '')
    
    return df_display
