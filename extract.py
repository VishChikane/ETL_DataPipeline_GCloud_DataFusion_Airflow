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
    print(f"Created File {csv_file} Succesfully.")


