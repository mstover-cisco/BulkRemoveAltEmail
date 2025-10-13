# BulkRemoveAltEmail
Python Script that removes Alternate Email addresses from users in Webex CI.

BulkRemoveAltEmail reads a CSV file of users that contains their primary email address and uses the SCIM-2 API to
remove the specified alternate email from that user's profile. The application will find each user by their 
primary email, used their SCIM ID, and remove the supplied, corresponding alternate email address from their account.

The application uses the CSV reader module, so it can identify the relevant columns in a complete bulk download of 
users from Webex Control Hub. By default, 

## References
[Webex Admin SCIM-2 Overview](https://developer.webex.com/admin/docs/scim-2-overview)
