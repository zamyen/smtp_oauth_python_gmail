# smtp_oauth_python_gmail
Minimal viable SMTP Email send with Python, using Google Gmail OAUTH2

Google Gmail API Setup:
1. To enable SMTP sending with Google as of 2022, a Google Cloud Platform account is required.*
2. Enable the Gmail API within the account (under Enabled APIs and services)
3. Create an OAuth 2.0 Client ID (under Credentials-> click +Create Credentials)
4. Configure an (OAuth consent screen) , Adding the SCOPE 'https://mail.google.com/' as you will see matching SCOPES = ['https://mail.google.com/'] used later in Python code
5. Download the file to the project directory: similar to this client_secret_446754051945-g01ovfjitd9avog20ujqbu3shh3dbsa8.apps.googleusercontent.com.json
    and rename it to
    credentials.json
    
Python Code:
1. Ensure you have the credentials.json file in the project directory.
2. Install the Python3 dependencies in requirements.txt (ideally in a virtual environment)
3. Update email in the cfg.py file SMTP_EMAIL = "yourusername@example.com" to something relevant
4. Run main.py , Initial run needs to be on a machine with a GUI Browser, see next step..
5. Google will prompt you to Authorise the running app against your email account
6. If successful, you should see both token.json and token.pickle files created in the project directory, and a test smtp email sent to your configured email address.


*It is highly recommended to use a 'Google Workspace' account and flag the app as type 'INTERNAL' unless you plan to get the app fully certified for External users by Google. Private gmail address accounts can request tokens but they currently expire within 72 hours, unless the app undergoes a certification process with Google for External users. Google restricts the INTERNAL category to paid Workspace users apparently.

**Note prior to May 2022 there was an option to send via Gmail SMTP servers by enabling "Less-Secure Apps" in the gmail account being used. But this feature is slated for removal May 2022, requiring the OAUTH2 bearer token route, hence this repo.
