from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timezone
import google.generativeai as genai
import re
from dotenv import load_dotenv
import os
import pickle
from google.auth.transport.requests import Request

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
skip_domain = ['@vanderbilt.edu']


def gmail_auth():
    creds = None
    # Token file stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token_file:
            creds = pickle.load(token_file)

    # If no valid credentials available, let user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for next run
        with open('token.pickle', 'wb') as token_file:
            pickle.dump(creds, token_file)

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_recent_emails(service, query = 'newer_than:1h'):
    print(f"🔍 Using query: {query}")
    print(f"Current UTC time: {datetime.now(timezone.utc)}")

    result = service.users().messages().list(userId='me', q=query).execute()
    messages = result.get('messages', [])
    return messages

def get_email_body(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    parts = msg['payload'].get('parts', [])
    for part in parts:
        if part['mimeType'] == 'text/plain':
            return part['body'].get('data', '')
    return ""

def classify_text(text):
    prompt = f"""
Classify the following email text into one of these categories:
- Spam - Scam/Phishing
- Spam - Offer/Advert
- NonSpam - Platform Notification
- NonSpam

Email:
{text}

Respond with just one of the three categories.
"""
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text.strip()


def apply_label(service, msg_id, label_name):
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    label_id = next((l['id'] for l in labels if l['name'] == label_name), None)

    if not label_id:
        label_obj = {'name': label_name, 'labelListVisibility': 'labelShow', 'messageListVisibility': 'show'}
        new_label = service.users().labels().create(userId='me', body=label_obj).execute()
        label_id = new_label['id']

    # Apply label
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'addLabelIds': [label_id]}
    ).execute()

def extract_email_address(sender_header):
    # Extract email address from formats like "Name <email@domain.com>"
    match = re.search(r'<(.+?)>', sender_header)
    return match.group(1) if match else sender_header


def main():
    print("🔧 Starting Gmail classification tool")
    service = gmail_auth()

    print("📥 Fetching emails from last hour...")
    messages = get_recent_emails(service, 'newer_than:2h')
    print(f"✅ Found {len(messages)} messages")

    for msg in messages:
        msg_id = msg['id']
        msg_data = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        headers = msg_data.get('payload', {}).get('headers', [])
        sender_raw = next((h['value'] for h in headers if h['name'].lower() == 'from'), '')
        sender = extract_email_address(sender_raw)

        if not msg_data:
            print("No Data Skipping")
            continue

        if any(sender.endswith(domain) for domain in skip_domain):
            print("Allowed Domain Skipping")
            continue

        classification = classify_text(msg_data)
        print(f'Classified as: {classification}')
        apply_label(service, msg['id'], classification)


if __name__ == '__main__':
    main()






