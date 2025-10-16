# webex_scim_client.py

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


import requests
import json
import os
import time

class WebexScimClient:
    """
    A Python client for the Webex SCIM 2.0 API, with built-in rate limit handling.
    """
    def __init__(self, org_id: str, bearer_token: str):
        if not org_id or not bearer_token:
            raise ValueError("Organization ID and Bearer Token are required.")
            
        self.base_url = f"https://webexapis.com/identity/scim/{org_id}/v2"
        self._headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }


    def _make_request(self, method, endpoint, payload=None):
        """
        Helper method to make the actual API requests. It includes provisions to handle
        automatic retry on rate limiting from the Webex API service.
        """
        url = f"{self.base_url}{endpoint}"

        while True: # Loop to allow for retries
            try:
                if payload:
                    response = requests.request(method, url, headers=self._headers, data=json.dumps(payload))
                else:
                    response = requests.request(method, url, headers=self._headers)
                
                # This will raise an HTTPError for 4xx/5xx responses
                response.raise_for_status()
                
                if response.status_code == 204:
                    return None # Success with no content
                return response.json() # Success with content
            
            except requests.exceptions.HTTPError as e:
                # Check specifically for the rate limit status code
                if e.response.status_code == 429:
                    # Get the Retry-After header value, default to 5 seconds if not present
                    retry_after = int(e.response.headers.get("Retry-After", 5))
                    print(f"--- Rate limit hit. Waiting for {retry_after} seconds before retrying. ---")
                    time.sleep(retry_after)
                    continue # Retry the request by continuing the while loop
                else:
                    # For any other HTTP error, print it and re-raise the exception
                    print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
                    raise e
            
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                raise e

    # All SCIM methods in this client (create_user, list_users, etc.) automatically 
    # benefit from the rate-limiting logic.
    
    def list_users(self, filter_query: str):
        """
        Lists (searches for) users using a filter. 
        Currently simplified for this use case, which should find a single user based
        on their unique email address that Webex uses as Primary User Id.
        """
        endpoint = f"/Users?filter={filter_query}"
        url = f"{self.base_url}{endpoint}"
        # This GET request does not use the payload
        return self._make_request("GET", endpoint)

    def remove_email_from_user(self, user_id: str, email_to_remove: str):
        """Removes a specific email address from an existing user."""
        path_expression = f'emails[value eq "{email_to_remove}"]'
        patch_data = {
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
            "Operations": [
                {
                    "op": "remove",
                    "path": path_expression
                }
            ]
        }
        return self._make_request("PATCH", f"/Users/{user_id}", payload=patch_data)

