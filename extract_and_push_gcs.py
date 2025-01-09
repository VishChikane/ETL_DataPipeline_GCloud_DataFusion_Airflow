import faker
import csv
import random
from google.cloud import storage
import os

# Initialize the Faker generator
fake = faker.Faker()

# Number of dummy employee records to generate
num_records = 100

# List to hold employee data
employee_data = []

# Generate dummy employee data
for _ in range(num_records):
    employee = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "job_title": fake.job(),
        "department": random.choice(['HR', 'Engineering', 'Marketing', 'Sales', 'Finance']),
        #"address": fake.address(),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=65).strftime("%Y-%m-%d"),
        "hire_date": fake.date_this_decade().strftime("%Y-%m-%d"),
        "salary": round(random.uniform(40000, 120000), 2),  # Random salary between 40k and 120k
        "password": fake.password(length=8, special_chars=False, digits=True, upper_case=True),  # Random password
        "employee_id": fake.uuid4(),  # Random unique employee ID
        "credit_card_number": fake.credit_card_number()  # Credit Card Number (PII)
    }
    
    employee_data.append(employee)

# Save to CSV file
csv_file = 'employee_data.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    #writer = csv.DictWriter(file, fieldnames=employee_data[0].keys())
    writer = csv.DictWriter(file, fieldnames=employee_data[0].keys(), quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(employee_data)

# Function to upload file to GCS bucket
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    # Set environment variable for Google Cloud credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cloud-etl-project-446709-fa37b207b9e4.json"

    # Initialize a GCS client
    storage_client = storage.Client()
    
    # Get the GCS bucket
    bucket = storage_client.bucket(bucket_name)
    
    # Create a new blob and upload the file
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    
    print(f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}.")

# GCS bucket details
bucket_name = 'bkt-dev-employee-data'
source_file_name = 'employee_data.csv'
destination_blob_name = 'employee_data.csv'

# Upload the file to GCS bucket
upload_to_gcs(bucket_name, source_file_name, destination_blob_name)
