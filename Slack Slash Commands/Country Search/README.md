Complete Setup Guide: Slack Travel Checker

Part 1: Set Up Your Google Spreadsheet
Step 1: Create your spreadsheet

Go to sheets.google.com
Create a new blank spreadsheet
Name it something like "Travel Permissions"
Set up your data like this:

Column A (Country)Column B (Status)
Nigeria                 no
Canada                  yes
Brazil                  restricted
China                   no
France                  yes

Make sure row 1 has your headers, and data starts in row 2
Note your spreadsheet ID from the URL - it's the long string between /d/ and /edit. For example, in https://docs.google.com/spreadsheets/d/1aBcDeFgHiJkLmNoPqRsTuVwXyZ/edit, the ID is 1aBcDeFgHiJkLmNoPqRsTuVwXyZ


Part 2: Set Up Google Cloud
Step 2: Create a Google Cloud Project

Go to console.cloud.google.com
If you don't have a Google Cloud account, create one (there's a free tier with generous allowances)
Click the project dropdown at the top of the page (it might say "Select a project")
Click "New Project"
Give it a name like "slack-travel-checker"
Click "Create"
Wait a moment for it to create, then make sure your new project is selected in the dropdown

Step 3: Enable the Required APIs

In the Google Cloud Console, click the search bar at the top
Search for "Google Sheets API"
Click on "Google Sheets API" in the results
Click the blue "Enable" button
Go back to the search bar and search for "Cloud Functions API"
Click on it and click "Enable"
Search for "Cloud Build API"
Click on it and click "Enable"

Step 4: Create a Service Account

In the left sidebar, click "IAM & Admin"
Click "Service Accounts"
Click "Create Service Account" at the top
For "Service account name," enter "sheets-reader"
The "Service account ID" will auto-fill
Click "Create and Continue"
For "Grant this service account access to project," skip this by clicking "Continue"
For "Grant users access to this service account," skip this by clicking "Done"

Step 5: Create and Download the Key File

In the Service Accounts list, click on "sheets-reader" (the one you just created)
Click the "Keys" tab at the top
Click "Add Key"
Click "Create new key"
Make sure "JSON" is selected
Click "Create"
A JSON file will automatically download to your computer - save this somewhere safe
Go back to the "Details" tab and copy the service account email address (it looks like sheets-reader@slack-travel-checker.iam.gserviceaccount.com)

Step 6: Share Your Google Sheet with the Service Account

Go back to your Google Sheet
Click the "Share" button in the top right
Paste the service account email address you copied
Set the permission to "Viewer"
Uncheck "Notify people"
Click "Share"


Part 3: Create and Deploy the Cloud Function
Step 7: Create the Cloud Function

Go back to the Google Cloud Console
In the search bar, search for "Cloud Functions"
Click on "Cloud Functions"
If prompted to enable any APIs, click "Enable"
Click "Create Function"
Configure the basics:

Environment: 2nd gen
Function name: canigo
Region: Choose one close to you (e.g., us-central1)


Under "Trigger," make sure "HTTPS" is selected
Check the box for "Allow unauthenticated invocations"
Click "Next"

Step 8: Add the Code
(see code file)

Step 9: Upload Your Service Account Key

In the file editor, click the "+" button to add a new file
Name it exactly service-account.json
Open the JSON key file you downloaded earlier in a text editor
Copy the entire contents
Paste it into the service-account.json file in the Cloud Functions editor

Step 10: Update the Spreadsheet ID

In main.py, find the line that says SPREADSHEET_ID = "YOUR_SPREADSHEET_ID_HERE"
Replace YOUR_SPREADSHEET_ID_HERE with your actual spreadsheet ID (keep the quotes)

Step 11: Add the Slack Signing Secret (We'll get this in Part 4)

Before deploying, scroll down to "Runtime, build, connections and security settings"
Click to expand it
Click on "Runtime environment variables"
Click "Add variable"
Set Name to SLACK_SIGNING_SECRET
Leave Value blank for now (we'll come back to this)
Click "Deploy"
Wait for the deployment to complete (this can take 1-2 minutes)
Once deployed, copy the URL shown - it will look like https://us-central1-slack-travel-checker.cloudfunctions.net/canigo


Part 4: Set Up the Slack App
Step 12: Create a Slack App

Go to api.slack.com/apps
Click "Create New App"
Click "From scratch"
For "App Name," enter "Travel Checker"
Select your workspace from the dropdown
Click "Create App"

Step 13: Get Your Signing Secret

You should now be on the "Basic Information" page
Scroll down to "App Credentials"
Find "Signing Secret" and click "Show"
Copy this value

Step 14: Add the Signing Secret to Your Cloud Function

Go back to the Google Cloud Console
Go to Cloud Functions
Click on your canigo function
Click "Edit"
Click "Next" to get to the code section
Scroll down to "Runtime, build, connections and security settings"
Click to expand it
Under "Runtime environment variables," find SLACK_SIGNING_SECRET
Paste your signing secret as the value
Click "Deploy"
Wait for it to redeploy

Step 15: Create the Slash Command

Go back to your Slack app settings at api.slack.com/apps
Click on your "Travel Checker" app
In the left sidebar, click "Slash Commands"
Click "Create New Command"
Fill in the form:

Command: /canigo
Request URL: Paste your Cloud Function URL (e.g., https://us-central1-slack-travel-checker.cloudfunctions.net/canigo)
Short Description: Check if you can travel to a country
Usage Hint: [country name]


Click "Save"

Step 16: Install the App to Your Workspace

In the left sidebar, click "Install App"
Click "Install to Workspace"
Review the permissions and click "Allow"


Part 5: Test Your Setup
Step 17: Test the Command

Open Slack
Go to any channel or direct message
Type /canigo Canada
Press Enter
You should see a response like "✅ Yes, you're able to travel to Canada."

Step 18: Test Other Countries
Try these commands to make sure everything works:

/canigo Nigeria (should show "No")
/canigo Brazil (should show "restricted")
/canigo Narnia (should show "not found")


Troubleshooting
If you get a timeout error:

Go to your Cloud Function in Google Cloud Console
Click "Edit"
Under "Runtime, build, connections and security settings," increase the timeout to 60 seconds
Redeploy

If you get "dispatch_failed":

Make sure your Cloud Function URL is correct in the Slack slash command settings
Make sure "Allow unauthenticated invocations" is checked on your Cloud Function

If you get no response:

Go to your Cloud Function in Google Cloud Console
Click on the "Logs" tab
Look for error messages that might explain what went wrong

If you get "unauthorized":

Double-check that your Slack signing secret is correct in the Cloud Function environment variables
Make sure there are no extra spaces when you copied it