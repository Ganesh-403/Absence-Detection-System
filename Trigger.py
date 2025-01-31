import os
import gspread
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

def trigger(sheet1_name, sheet2_name, no_of_days):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    # Get the service account credentials from environment variable
    service_account_info = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')

    # Load credentials from JSON stored in GitHub Secrets
    credentials = Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES)
    client = gspread.authorize(credentials)

    attendance_sheet = client.open(sheet1_name).sheet1
    phone_sheet = client.open(sheet2_name).sheet1

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
                (phone_data['First Name'] == first_name) &
                (phone_data['Last Name'] == last_name)
            ]['Phone'].values
            if phone_number.size > 0:
                students_with_long_absences.append({
                    "Name": f"{first_name} {last_name}",
                    "Phone Number": phone_number[0],
                    "Absent Days": day_difference
                })

    if students_with_long_absences:
        # Convert the list of dictionaries to a DataFrame
        absences_df = pd.DataFrame(students_with_long_absences)

        # Save to a CSV file in the GitHub Actions workspace
        output_file_path = 'Final_User_Data.csv'  # Relative path within GitHub Actions environment

        # Write the data to the file, appending if it already exists
        absences_df.to_csv(output_file_path, index=False)

        print(f"Report successfully written to {output_file_path}")
    else:
        print(f"No students were absent for more than {no_of_days} days.")

# Environment variables for sheet names and no_of_days
sheet1_name = os.getenv('SHEET1_NAME', 'Copy 2 of Attendance Form')  # Default to 'Copy 2 of Attendance Form'
sheet2_name = os.getenv('SHEET2_NAME', 'Whatsapp Trial')  # Default to 'Whatsapp Trial'
no_of_days = int(os.getenv('NO_OF_DAYS', '7'))  # Default to 7 days

trigger(sheet1_name, sheet2_name, no_of_days)
