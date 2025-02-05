import os
import gspread
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

def trigger(sheet1_name, sheet1_worksheet, sheet2_name, sheet2_worksheet, no_of_days):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    # Get credentials from GitHub Secret
    service_account_info = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')

    # Convert credentials JSON from string to dictionary
    credentials = Credentials.from_service_account_info(eval(service_account_info), scopes=SCOPES)
    client = gspread.authorize(credentials)

    # Debugging: Print the loaded secret values
    print(f"Spreadsheet 1: {sheet1_name} | Worksheet 1: {sheet1_worksheet}")
    print(f"Spreadsheet 2: {sheet2_name} | Worksheet 2: {sheet2_worksheet}")

    # Open the spreadsheets and correct worksheets
    attendance_sheet = client.open(sheet1_name).worksheet(sheet1_worksheet)
    phone_sheet = client.open(sheet2_name).worksheet(sheet2_worksheet)

    # Convert data into pandas DataFrame
    attendance_data = pd.DataFrame(attendance_sheet.get_all_records())
    phone_data = pd.DataFrame(phone_sheet.get_all_records())

    attendance_data['Date'] = pd.to_datetime(attendance_data['Date'])
    attendance_data = attendance_data.sort_values(by=['Enter Last Name ', 'Date'])

    students_with_long_absences = []

    for _, group in attendance_data.groupby(['Enter First Name ', 'Enter Last Name ']):
        submission_dates = group['Date'].tolist()
        first_name = group['Enter First Name '].iloc[0]
        last_name = group['Enter Last Name '].iloc[0]

        i = len(submission_dates) - 1
        day_difference = (submission_dates[i] - submission_dates[i - 1]).days

        if day_difference >= no_of_days:
            phone_number = phone_data[
                (phone_data['First Name'] == first_name) & (phone_data['Last Name'] == last_name)
            ]['Phone'].values

            if phone_number.size > 0:
                students_with_long_absences.append({
                    "Name": f"{first_name} {last_name}",
                    "Phone Number": phone_number[0],
                    "Absent Days": day_difference
                })

    if students_with_long_absences:
        absences_df = pd.DataFrame(students_with_long_absences)
        output_file_path = 'Final_User_Data.csv'
        absences_df.to_csv(output_file_path, index=False)
        print(f"Report successfully written to {output_file_path}")
    else:
        print(f"No students were absent for more than {no_of_days} days.")

# Load secrets from GitHub environment variables
sheet1_name = os.getenv('SHEET1_NAME')
sheet1_worksheet = os.getenv('SHEET1_WORKSHEET')

sheet2_name = os.getenv('SHEET2_NAME')
sheet2_worksheet = os.getenv('SHEET2_WORKSHEET')

no_of_days = int(os.getenv('NO_OF_DAYS', '7'))  # Default is 7

trigger(sheet1_name, sheet1_worksheet, sheet2_name, sheet2_worksheet, no_of_days)
