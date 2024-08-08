import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import threading
import json

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_urls(urls, smtp_settings):
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"{time.ctime()}: {url} is up")
            else:
                print(f"{time.ctime()}: {url} is down")
                send_email(
                    subject=f"URL Down Alert: {url}",
                    body=f"The URL {url} is down with status code {response.status_code}.",
                    to_email=smtp_settings['to_email'],
                    from_email=smtp_settings['from_email'],
                    smtp_server=smtp_settings['smtp_server'],
                    smtp_port=smtp_settings['smtp_port'],
                    smtp_user=smtp_settings['smtp_user'],
                    smtp_password=smtp_settings['smtp_password']
                )
        except requests.exceptions.RequestException as e:
            print(f"{time.ctime()}: {url} is down")
            send_email(
                subject=f"URL Down Alert: {url}",
                body=f"The URL {url} is down. Exception: {e}",
                to_email=smtp_settings['to_email'],
                from_email=smtp_settings['from_email'],
                smtp_server=smtp_settings['smtp_server'],
                smtp_port=smtp_settings['smtp_port'],
                smtp_user=smtp_settings['smtp_user'],
                smtp_password=smtp_settings['smtp_password']
            )

def start_monitoring(file_path, smtp_settings):
    urls = read_urls_from_file(file_path)
    check_interval = 60  # Check every 60 seconds

    def monitor():
        while True:
            check_urls(urls, smtp_settings)
            time.sleep(check_interval)

    thread = threading.Thread(target=monitor)
    thread.daemon = True
    thread.start()
