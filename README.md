# BulkRemoveAltEmail
Python Script that removes Alternate Email addresses from users in Webex CI.

BulkRemoveAltEmail reads a CSV file of users that contains their primary email address and uses the SCIM-2 API to remove the specified alternate email from that user's profile. The application will find each user by their primary email, identify the SCIM ID associated wither their account, and remove the supplied, corresponding alternate email address from their account. If you need to remove more than one alternate email from a Webex account, the script can be run additional times for those alternate emails. 

Note that the script will successfully execute even if the alternate email has already been removed. The PATCH operation used will only remove the specified alternate_email, so any other email addresses assoicated with the user will not be removed unless they match.

The application uses the CSV reader module, so it can identify the relevant columns in a complete bulk download of users from Webex Control Hub. By default, the script will look for the primary email address in a column named **primary_email** with the corresponding alternate email address in a column named **alternate_email**. You can edit your CSV file to match or supply the column names on the command line. The script can handle _empty_ rows with an empty primary_email or rows that lack an alternate_email.

Webex Org ID and Admin Bearer Tokens are read from environment variables to prevent tokens from being stored. For one-off usage, a bearer token can be created using the [Webex Developer Website](https://developer.webex.com) where an admin can find their **Org.Id** and a temporary **Bearer** token for authorization. A future improvement is to include the workflow to create an OAuth Token for an Admin Account with the requried API scope.

The script should accomodate a busy condition with the Webex API server by honoring the 429 Retry-After header. It will automatically retry the current operation after the number of seconds specified in that header and resume processing the remainder of the CSV file. Any other errors will cause an exception that should be investigated. 

## Usage
The application runs from a terminal / command window: 

`python BulkRremoveAltEmail.py --csv-file users_to_process.csv`

Since there are provided default values for the column names (primary_email and alternate_email), you only need to specify them if your CSV headers are different. If, for example, your CSV headers are 'main_id' and 'email_to_delete', the command line would be:

`python process_csv.py --csv-file users_to_process.csv --primary-column "main_id" --alternate-column "email_to_delete"`

## Dependencies
* Supported [Python 3](https://www.python.org/downloads/) version (any non-end-of-life version)
* [Python Requests Package](https://pypi.org/project/requests/)

## References
By way of background, below are some reference pages that provide some details around the specific APIs being used:

* [Webex Admin SCIM-2 Overview](https://developer.webex.com/admin/docs/scim-2-overview)
* [Webex SCIM  Users API](https://developer.webex.com/admin/docs/api/v1/scim-2-users)
* [Webex Admin Authentication](https://developer.webex.com/admin/docs/authentication)
