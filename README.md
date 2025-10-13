# BulkRemoveAltEmail
Python Script that removes Alternate Email addresses from users in Webex CI.

BulkRemoveAltEmail reads a CSV file of users that contains their primary email address and uses the SCIM-2 API to
remove the specified alternate email from that user's profile. The application will find each user by their 
primary email, used their SCIM ID, and remove the supplied, corresponding alternate email address from their account.

The application uses the CSV reader module, so it can identify the relevant columns in a complete bulk download of 
users from Webex Control Hub. By default, 

Webex Org ID and Admin Bearer Tokens are read from environment variables to prevent tokens from being stored. For 
one-off usage, a bearer token can be created using the [Webex Developer Website](https://developer.webex.com) where
and admin can find their OrgID and a temporary authorization token. A future improvement is to include workflow 
to create an OAuth Token for an Admin Account with the requried scope.

## References
[Webex Admin SCIM-2 Overview](https://developer.webex.com/admin/docs/scim-2-overview)
