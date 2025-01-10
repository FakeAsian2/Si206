import json
import pandas as pd
from datetime import datetime, timedelta

# List of available files
files = ['expenses_1.json', 'expenses_2.json', 'expenses_3.json', 'expenses_4.json']

# Function to standardize dates
def standardize_date(date):
    if pd.isna(date):
        return None
    formats = ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%y']
    for fmt in formats:
        try:
            return datetime.strptime(date, fmt).date()
        except ValueError:
            continue
    return None  # Invalid date

# Function to clean and load data
def load_and_clean_data(file):
    with open(file, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)

    # Standardize dates
    df['Date'] = df['Date'].apply(standardize_date)

    # Fix category spelling errors
    category_corrections = {'Fod': 'Food', 'Utillties': 'Utilities'}
    df['Category'] = df['Category'].replace(category_corrections)

    # Handle invalid or missing amounts
    def clean_amount(amount):
        try:
            return float(amount) if amount is not None else None
        except ValueError:
            return None

    df['Amount'] = df['Amount'].apply(clean_amount)

    # Drop unnecessary or invalid data
    df.dropna(subset=['Date', 'Amount'], inplace=True)
    return df

# User chooses a file
print("Available files:")
for i, file in enumerate(files, start=1):
    print(f"{i}. {file}")

file_choice = int(input("Enter the number of the file you want to process: "))
selected_file = files[file_choice - 1]

# Load and clean the data
df = load_and_clean_data(selected_file)

# User provides a date or range
date_input = input("Enter a specific date (YYYY-MM-DD) or a range in days (e.g., '7' for the last 7 days): ")

if date_input.isdigit():
    # Handle range in days
    days = int(date_input)
    start_date = datetime.now().date() - timedelta(days=days)
    filtered_df = df[df['Date'] >= start_date]
else:
    # Handle specific date
    try:
        specific_date = datetime.strptime(date_input, '%Y-%m-%d').date()
        filtered_df = df[df['Date'] == specific_date]
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        exit()

# Group by category and calculate totals
if not filtered_df.empty:
    grouped = filtered_df.groupby('Category')['Amount'].sum()

    # Print results
    print("\nExpenses Breakdown:")
    print(grouped.to_string())
else:
    print("\nNo data found for the specified date or range.")