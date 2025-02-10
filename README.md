# Absence Detection System

## Overview
The Absence Detection System is a Python-based solution that automates the process of monitoring student attendance recorded in Google Sheets. The system identifies students with prolonged absences and generates a report containing their details. It integrates with Google Sheets via the Google Sheets API and is designed to run on GitHub Actions as a scheduled workflow.

## Features
- **Automated Attendance Monitoring**: Fetches attendance data from Google Sheets.
- **Absence Detection**: Identifies students absent for a specified number of consecutive days.
- **Report Generation**: Creates a CSV file (`Final_User_Data.csv`) listing students with prolonged absences along with their phone numbers.
- **Integration with GitHub Actions**: Runs the script automatically every 24 hours.

## Project Structure
```
|-- .github/workflows/monitor.yml   # GitHub Actions workflow
|-- Trigger.py                      # Main script for absence detection
|-- requirements.txt                 # Dependencies
|-- README.md                        # Project documentation
```

## Prerequisites
- Python 3.8+
- Google Sheets API credentials (stored in GitHub Secrets)
- Google Sheets with attendance and contact details

## Installation
1. **Clone the repository**:
   ```
   git clone https://github.com/your-repo/absence-detection.git
   cd absence-detection
   ```
2. **Create a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Usage
### Running Locally
1. Set environment variables in a `.env` file:
   ```
   GOOGLE_APPLICATION_CREDENTIALS_JSON=<your_credentials_json>
   SHEET1_NAME=<Attendance_Sheet_Name>
   SHEET1_WORKSHEET=<Attendance_Worksheet_Name>
   SHEET2_NAME=<Phone_Sheet_Name>
   SHEET2_WORKSHEET=<Phone_Worksheet_Name>
   NO_OF_DAYS=7  # Adjust as needed
   ```
2. Run the script:
   ```
   python Trigger.py
   ```

### Running on GitHub Actions
The script runs automatically using a scheduled GitHub Actions workflow (`.github/workflows/monitor.yml`). The workflow:
- Installs dependencies
- Runs `Trigger.py`
- Uses GitHub Secrets for credentials and configurations

## Configuration
### Environment Variables (GitHub Secrets)
The following secrets must be set in your GitHub repository:
- `GOOGLE_APPLICATION_CREDENTIALS_JSON` - Google Sheets API credentials
- `SHEET1_NAME` - Name of the attendance spreadsheet
- `SHEET1_WORKSHEET` - Name of the attendance worksheet
- `SHEET2_NAME` - Name of the phone number spreadsheet
- `SHEET2_WORKSHEET` - Name of the phone number worksheet
- `NO_OF_DAYS` - Threshold for detecting long absences (default: 7)

## Output
If students have been absent for more than the specified days, a CSV file `Final_User_Data.csv` is generated with their names, phone numbers, and absence duration.

## Dependencies
Dependencies are listed in `requirements.txt` and installed via:
```
pip install -r requirements.txt
```

## License
This project is licensed under the MIT License.

## Author
[Ganesh Kambli](https://github.com/Ganesh-403)

