import logging
import os, sys
import requests
import azure.functions as func
from typing import *
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

def main(myReq: func.HttpRequest):
    playbook_url = extract_url("https://www.politico.eu/newsletter/brussels-playbook/", ".front-list > li:nth-child(1) > article:nth-child(1) > div:nth-child(2) > article:nth-child(1) > div:nth-child(1) > header:nth-child(1) > h3:nth-child(1) > a:nth-child(1)", 'href')
    audio_url = extract_url(playbook_url, "#amazon-polly-audio-play > source:nth-child(1)", "src")
    send_us_playbook_url(audio_url)
    logging.info('Python HTTP triggered function processed ok!')

def extract_content(url) -> str:
    req = requests.get(url, headers = {"user-agent":"Azure Cloud @ GitHub"}).text
    return req

def extract_url(url, selector, attribute) -> str:
    soup = BeautifulSoup(extract_content(url), 'html.parser')
    tag = soup.select(selector)[0]
    url = tag.attrs[attribute]
    return url

def send_us_playbook_url(url) -> str:
    sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    message = Mail(from_email=From(os.environ.get('OUTLOOK_EMAIL'), 'My Outlook email'),
            to_emails=To(os.environ.get('SEZNAM_EMAIL'), 'My seznam email'),
            subject=Subject('Politico Brussels Podcast URL Direct Link'),
            plain_text_content=PlainTextContent('Brussels Playbook Podcast: ' + url))
    try:
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
