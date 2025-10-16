# BulkRemoveAltEmail.py

# Copyright (c) 2025 Cisco and/or its affiliates.
#
# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.1 (the "License"). You may obtain a copy of the
# License at
#
#     https://developer.cisco.com/docs/licenses
#
# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.


import csv
import os
import argparse
from webex_scim_client import WebexScimClient # Assumes the class is in this file in an accessible path

def process_users_from_csv(client: WebexScimClient, csv_path: str, primary_col: str, alternate_col: str):
    """
    Reads a CSV, finds each user by their primary email, and removes the
    corresponding alternate email address from their account.

    Args:
        client: An initialized WebexScimClient instance.
        csv_path: Path to the input CSV file.
        primary_col: The name of the column containing the user's primary email.
        alternate_col: The name of the column containing the alternate email to remove.
    """
    print(f"Starting processing for file: {csv_path}")
    print(f"Reading primary email from '{primary_col}' column and alternate email from '{alternate_col}' column.\n")

    try:
        with open(csv_path, mode='r', encoding='utf-8') as csvfile:
            # Using DictReader to handle columns by name
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader, 1):
                user_primary_email = row.get(primary_col)
                email_to_remove = row.get(alternate_col)

                # --- Input Validation for each row ---
                if not user_primary_email:
                    print(f"SKIPPING row {i}: Primary email column '{primary_col}' is empty.\n")
                    continue
                if not email_to_remove:
                    print(f"SKIPPING row {i} for user '{user_primary_email}': Alternate email column '{alternate_col}' is empty.\n")
                    continue

                print(f"--- Processing user: {user_primary_email} ---")

                try:
                    # 1. Find the user by their primary email to get their SCIM ID
                    print(f"Step 1: Looking up SCIM ID for '{user_primary_email}'...")
                    filter_q = f'userName eq "{user_primary_email}"'
                    found_users = client.list_users(filter_query=filter_q)

                    if not found_users or found_users.get('totalResults', 0) == 0:
                        print(f"WARNING: User '{user_primary_email}' not found in Webex. Skipping.")
                        continue
                    
                    user_id = found_users['Resources'][0]['id']
                    print(f"Step 1: Found SCIM ID: {user_id}")

                    # 2. Use PATCH to remove the specific alternate email from this row
                    print(f"Step 2: Sending PATCH to remove '{email_to_remove}'...")
                    client.remove_email_from_user(user_id=user_id, email_to_remove=email_to_remove)
                    print(f"SUCCESS: Request to remove email for '{user_primary_email}' was successful.\n")

                except Exception as e:
                    # Catches errors like 400 Bad Request (e.g., if the alternate email doesn't exist on the user)
                    print(f"ERROR processing user '{user_primary_email}': {e}\n")
                    continue # Move to the next user

    except FileNotFoundError:
        print(f"FATAL ERROR: The file '{csv_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk remove specific alternate email addresses from Webex users based on a CSV file.")
    parser.add_argument("--csv-file", required=True, help="Path to the CSV file containing user data.")
    parser.add_argument("--primary-column", default="primary_email", help="Name of the column with the user's primary email for lookup.")
    parser.add_argument("--alternate-column", default="alternate_email", help="Name of the column with the alternate email to be removed.")
    
    args = parser.parse_args()

    # Load credentials from environment variables for security
    ORG_ID = os.getenv("WEBEX_ORG_ID")
    BEARER_TOKEN = os.getenv("WEBEX_SCIM_TOKEN")

    if not ORG_ID or not BEARER_TOKEN:
        print("FATAL ERROR: Please set WEBEX_ORG_ID and WEBEX_SCIM_TOKEN environment variables.")
    else:
        # Initialize the client
        scim_client = WebexScimClient(org_id=ORG_ID, bearer_token=BEARER_TOKEN)
        # Run the main processing function with the new arguments
        process_users_from_csv(
            client=scim_client,
            csv_path=args.csv_file,
            primary_col=args.primary_column,
            alternate_col=args.alternate_column
        )
        
    
