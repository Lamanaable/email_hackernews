import requests

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from bs4 import BeautifulSoup
import os
from tenacity import retry, stop_after_attempt, wait_fixed


def main() -> None:
    html = get_page_content()

    email_page_content(html)


def get_page_content() -> bytes:
    response = requests.get("https://news.ycombinator.com/news")

    return response.content


def email_page_content(page_html: bytes):
    soup = BeautifulSoup(page_html, "html.parser")

    for tag in soup.find_all(["a", "link", "img"]):
        if tag.get("href"):
            href = str(tag["href"])
            if "/" not in href:
                tag["href"] = f"https://news.ycombinator.com{href}"
            
        elif tag.get("src"):
            src = str(tag["src"])
            if "/" not in src:
                tag["src"] = f"https://news.ycombinator.com{src}"
            
    raw_html = str(soup)

    server = init_server()

    recipients = [os.getenv("RECIPIENT_1", ""), os.getenv("RECIPIENT_2", "")]

    msg = build_message(raw_html, recipients)

    server.sendmail(os.getenv("SENDER", ""), recipients, msg.as_string())

    server.quit()


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def init_server() -> smtplib.SMTP:
    username = os.getenv("SENDER", "")

    password = os.getenv("MAIL_PASSWORD", "")

    server = smtplib.SMTP(os.getenv("SMTPSERVER", ""), 587)

    server.starttls()
    server.login(username, password)

    return server


def build_message(raw_html: str, recipients: list) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    today = time.strftime("%Y-%m-%d")
    msg["Subject"] = f"HackerNews {today}"

    msg["From"] = os.getenv("SENDER", "")

    msg["To"] = ", ".join(recipients)

    msg_body = MIMEText(raw_html, "html")

    msg.attach(msg_body)

    return msg


if __name__ == "__main__":
    main()
