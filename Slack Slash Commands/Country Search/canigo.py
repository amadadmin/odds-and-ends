import hashlib
import hmac
import time
import os
import functions_framework
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID_HERE"  # Replace with your actual spreadsheet ID
RANGE_NAME = "Sheet1!A:B"  # Adjust if your sheet has a different name
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET", "")

def verify_slack_request(request):
    """Verify that the request actually came from Slack."""
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    signature = request.headers.get("X-Slack-Signature", "")
    
    # Check if timestamp is too old (more than 5 minutes)
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False
    
    # Create the signature base string
    sig_basestring = f"v0:{timestamp}:{request.get_data(as_text=True)}"
    
    # Create our own signature
    my_signature = "v0=" + hmac.new(
        SLACK_SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures
    return hmac.compare_digest(my_signature, signature)

def get_sheets_service():
    """Create and return a Google Sheets service instance."""
    credentials = service_account.Credentials.from_service_account_file(
        "service-account.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    return build("sheets", "v4", credentials=credentials)

def lookup_country(country_name):
    """Look up a country in the spreadsheet and return its travel status."""
    service = get_sheets_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()
    
    rows = result.get("values", [])
    
    # Search for the country (case-insensitive)
    for row in rows:
        if len(row) >= 2 and row[0].lower() == country_name.lower():
            return {"country": row[0], "status": row[1].lower()}
    
    return None

@functions_framework.http
def canigo(request):
    """Main function that handles the /canigo slash command."""
    
    # Verify the request is from Slack
    if SLACK_SIGNING_SECRET and not verify_slack_request(request):
        return "Unauthorized", 401
    
    # Get the country from the slash command
    country = request.form.get("text", "").strip()
    
    if not country:
        return "Please specify a country. Usage: `/canigo [country name]`"
    
    # Look up the country
    result = lookup_country(country)
    
    if not result:
        return f"Sorry, I couldn't find *{country}* in the travel list. Please check the spelling or contact your travel administrator."
    
    # Format the response based on status
    status = result["status"]
    country_name = result["country"]
    
    if status == "yes":
        return f"✅ *Yes*, you're able to travel to *{country_name}*."
    elif status == "no":
        return f"🚫 *No*, you're unable to travel to *{country_name}*."
    elif status == "restricted":
        return f"⚠️ Travel to *{country_name}* is allowed *with restrictions*. Please contact your travel administrator for details."
    else:
        return f"The status for *{country_name}* is: {status}"
```

4. Click on `requirements.txt` in the file list on the left
5. Replace the contents with:
```
functions-framework==3.*
google-auth==2.*
google-api-python-client==2.*