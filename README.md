# Email HackerNews

A Python script that scrapes the Hacker News homepage
and emails the content to specified recipients.
Designed to run automatically via GitHub Actions.

## Features

- Scrapes the latest stories from Hacker News (<https://news.ycombinator.com/news>)
- Converts relative URLs to absolute URLs
- Sends the HTML content via email
- Automated daily runs via GitHub Actions
- Retry logic for SMTP connection failures

## Requirements

- Python 3.13.2
- Dependencies listed in `requirements.txt`

## Setup

### Environment Variables

Configure the following environment variables in your GitHub repository secrets:

- `SENDER` - Sender email address
- `MAIL_PASSWORD` - Email account password/app password
- `SMTPSERVER` - SMTP server address (e.g., `smtp.gmail.com`)
- `RECIPIENT_1` - First recipient email address
- `RECIPIENT_2` - Second recipient email address (optional)

### Installation

- Clone the repository
- Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- Set the environment variables or run locally with:

```bash
export SENDER="your_email@example.com"
export MAIL_PASSWORD="your_password"
export SMTPSERVER="smtp.example.com"
export RECIPIENT_1="recipient1@example.com"
export RECIPIENT_2="recipient2@example.com"
python scrape_and_email.py
```

## Usage

The script runs automatically via GitHub Actions every day at 9:00 AM UTC.

To run manually:

```bash
python scrape_and_email.py
```

## GitHub Actions

The workflow is configured in `.github/workflows/send_email.yml` and triggers on:

- Push to the `master` branch
- Daily cron job at 9:00 AM UTC

## Dependencies

- `beautifulsoup4` - HTML parsing
- `requests` - HTTP requests
- `tenacity` - Retry logic for SMTP connections
- Standard library: `smtplib`, `email.mime`, `time`, `os`
