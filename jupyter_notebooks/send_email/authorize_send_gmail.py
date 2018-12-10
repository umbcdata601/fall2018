# python3 send_gmail.py

# sudo pip3 install --upgrade google-api-python-client
# sudo pip3 install --upgrade oauth2client 
# rm token.json

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
# see https://developers.google.com/gmail/api/auth/scopes
#SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
#SCOPES = 'https://www.googleapis.com/auth/gmail.send'
SCOPES = 'https://mail.google.com/'

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

if __name__ == '__main__':
    main()
