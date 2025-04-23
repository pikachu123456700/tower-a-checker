import requests
from bs4 import BeautifulSoup
import datetime
import smtplib
from email.mime.text import MIMEText
import os

# ========== 參數設定 ==========
url = 'https://globalvillage.icho.osaka-u.ac.jp/tsukumodai-en/application.html'
keywords = ['Tower A', 'application', 'open', 'New']
line_notify_token = os.getenv('LINE_NOTIFY_TOKEN')
gmail_user = os.getenv('GMAIL_USER')
gmail_pass = os.getenv('GMAIL_PASS')
receiver_email = os.getenv('GMAIL_RECEIVER')

# ========== 爬蟲 ==========
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

now = datetime.datetime.now()
print(f"Checked at {now.strftime('%Y-%m-%d %H:%M:%S')}")

found_msgs = []

for tag in soup.find_all(['h2', 'h3', 'p', 'li']):
    text = tag.get_text(strip=True)
    if any(keyword.lower() in text.lower() for keyword in keywords):
        found_msgs.append(text)

if found_msgs:
    message = "Tower A update found:\n" + "\n".join(found_msgs)
    print(message)
    
    # LINE Notify
    if line_notify_token:
        requests.post(
            'https://notify-api.line.me/api/notify',
            headers={'Authorization': f'Bearer {line_notify_token}'},
            data={'message': message}
        )

    # Gmail
    if gmail_user and gmail_pass and receiver_email:
        msg = MIMEText(message)
        msg['Subject'] = 'Tower A Update Found'
        msg['From'] = gmail_user
        msg['To'] = receiver_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(gmail_user, gmail_pass)
            smtp.send_message(msg)
else:
    print("No Tower A related updates found.")
