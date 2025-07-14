# Referral Dashboard Streamlit App

This Streamlit app converts your referral data analysis script into an interactive web application with file upload and download capabilities. The application is now modularly organized for better maintainability and scalability.

## 📁 Project Structure

```
📦 Weekly Referral Overview Automation
├── 📄 streamlit_app.py          # Main Streamlit application
├── 📄 data_processor.py         # Data processing and filtering functions
├── 📄 excel_generator.py        # Excel report generation and formatting
├── 📄 ui_components.py          # Streamlit UI components and helpers
├── 📄 script.py                 # Original Python script (for reference)
├── 📄 requirements.txt          # Python dependencies
├── 📄 README.md                 # This file
└── 📄 __init__.py              # Package initialization
```

## 🔧 Module Overview

### `streamlit_app.py`
- Main application entry point
- Coordinates between UI and data processing modules
- Handles the overall application flow

### `data_processor.py`
- **Functions**: Data cleaning, filtering, and processing
- `clean_and_convert_data()`: Data type conversions
- `filter_*()`: Various filtering functions for different categories
- `process_referral_data()`: Main processing orchestrator
- `create_summary_table()`: Summary statistics generation

### `excel_generator.py`
- **Functions**: Excel report creation and formatting
- `create_excel_report()`: Main Excel generation function
- `write_all_sheets()`: Data writing to Excel sheets
- `format_all_sheets()`: Styling and formatting application
- `format_headers_and_columns()`: Column width and header formatting

### `ui_components.py`
- **Functions**: Streamlit UI components and layouts
- `render_*()`: Various UI rendering functions
- `setup_page_config()`: Page configuration
- `show_*_message()`: User feedback functions

## Features

- 📊 **Interactive Dashboard**: Upload Excel files and view summary metrics
- 📥 **Excel Export**: Download formatted Excel reports with multiple sheets
- 📄 **CSV Export**: Download summary data as CSV
- ⚙️ **Date Override**: Use custom analysis date if needed
- 🔍 **Detailed Views**: Expandable sections for each metric category
- 🎨 **Modular Design**: Well-organized, maintainable code structure

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

1. Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

2. Open your browser and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

3. Upload your Excel file using the file uploader

4. View the dashboard and download the generated reports

## Expected File Format

Your Excel file should contain columns such as:
- `Pending Task/ Next Task`
- `Day(s) in Current Activity` or `Last Activity Date`
- `Number of Grocery Boxes Successfully Sent`
- `Payer Organization`
- `Referral Start Date`
- `Referral Created Date`
- `Re-authorization Status`
- `Last Activity Completed`
- `Number of Nutrition Counseling Sessions Completed`

## Output

The app generates:
1. **Interactive Dashboard**: Summary metrics and detailed breakdowns
2. **Excel Report**: Multi-sheet Excel file with formatted data and styling
3. **CSV Summary**: Summary table in CSV format

## Configuration

- Use the sidebar to set a custom analysis date
- View real-time metrics and summaries
- Expand detailed sections to see specific records

## Development

### Adding New Features

1. **Data Processing**: Add new functions to `data_processor.py`
2. **UI Components**: Add new rendering functions to `ui_components.py`
3. **Excel Features**: Extend `excel_generator.py` for new formatting options
4. **Main App**: Update `streamlit_app.py` to integrate new features

### Code Organization Benefits

- **Maintainability**: Each module has a specific responsibility
- **Testability**: Functions can be tested independently
- **Scalability**: Easy to add new features without cluttering main file
- **Reusability**: Functions can be imported and used in other projects
