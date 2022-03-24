import logging
import os
import smtplib
import pickle

# Gmail API utils
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

# for encoding/decoding messages in base64
import base64

# Our Own Config File, for logging and smtp
import cfg

logger = logging.getLogger(cfg.g_logname)
logger.setLevel(cfg.g_loglevel)
logger.info('start ' + __file__)

# API scope required by Google (must match Oauth token setup on Google Cloud portal)
SCOPES = ['https://mail.google.com/']


def gmail_initialise_token():
    """
     1. Obtain a credentials.json file from within a Google Cloud Platform account [Oauth2 Desktop] prior to running
     2. On first run prompts for End User Google Account authorisation (GUI - browser required)
     3. Upon authentication, obtains a API access token with refresh characteristics, from Google's
        'credentials.json' and stores this as 'token.json'

     Recommended to use a Google Workspace gmail account with 'Internal' app designation
    """

    logging.info("In gmail_authenticate, converting credentials.json --> token.json , as required")
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            logger.info("GOOGLE REQUIRES REAUTHENTICATION - run this step on a machine with GUI Browser")
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # OPTIONAL TEST CODE
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


def gmail_authenticate():
    """
    Refreshes the OAUTH token as required
    """
    logging.info("In gmail_authenticate, refreshing token.json as needed")
    creds: Credentials = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time

    # set working directory in crontab
    if os.path.exists("token.pickle"):
        # if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            logger.info("reading creds from pickle")
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("running creds.refresh(Request())")
            creds.refresh(Request())
        else:
            logger.info("creating flow, creating server")
            logger.info("GOOGLE REQUIRES REAUTHENTICATION - run this step on a machine with GUI Browser")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        # with open("token.pickle", "wb") as token:
        with open("token.pickle", "wb") as token:
            logging.info("save the credentials for the next run")
            pickle.dump(creds, token)
    logger.info(creds)
    return creds.token  # we only need token for smtp
    # return build('gmail', 'v1', credentials=creds) #original form


def send_smtp_oauth(self, recipient, subject, content):
    """
    Sends typical SMTP request, additionally with the latest OAUTH bearer token information inserted within the Header
    """

    logger.info("In sendmailoauth, attempting gmail authenticate")
    token = gmail_authenticate()
    logger.info("gmail_authenticate completed")

    # Create Headers
    headers = ["From: " + cfg.SMTP_EMAIL, "Subject: " + subject, "To: " + recipient,
               "MIME-Version: 1.0", "Content-Type: text/html"]
    headers = "\r\n".join(headers)

    # Connect to Gmail Server
    logger.info("Creating smtp session")
    session = smtplib.SMTP(cfg.SMTP_SERVER, cfg.SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()

    auth_string = b'user=' + bytes(f"{cfg.SMTP_EMAIL}", 'ascii') + b'\1auth=Bearer ' + token.encode() + b'\1\1'
    logger.info("Sending auth string")
    code, msg = session.docmd('AUTH', 'XOAUTH2 ' + (base64.b64encode(auth_string)).decode('ascii'))

    # Send Email & Exit
    logger.info("Sending email")
    session.sendmail(cfg.SMTP_EMAIL, recipient, headers + "\r\n\r\n" + content)
    session.quit


if __name__ == '__main__':
    gmail_initialise_token()
    gmail_authenticate()
    send_smtp_oauth(cfg.SMTP_EMAIL, cfg.SMTP_EMAIL, "Test Subject", "Test Body")  # Send smtp to oursevles
