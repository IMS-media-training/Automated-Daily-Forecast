# Setup Guide

## Prerequisites

- Python 3.8+
- pip
- Git

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/noamweisss/Automated-Daily-Forecast.git
cd Automated-Daily-Forecast
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` with your SMTP credentials:

```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### 4. Configure Recipients

Create a `recipients.txt` file:

```bash
cp recipients.txt.example recipients.txt
```

Add recipient emails (one per line):

```
user1@example.com
user2@example.com
```

### 5. Test Installation

```bash
python forecast_workflow.py --dry-run
```

## Gmail App Password Setup

If using Gmail:

1. Enable 2-Step Verification on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Generate a 16-character App Password
4. Use this password in your `.env` file (not your regular Gmail password)

## Troubleshooting

### Common Issues

**ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**Hebrew text displays incorrectly**
Ensure XML encoding conversion is working. The download script handles this automatically.

**No cities extracted**
Check that the target date exists in the XML file. IMS provides 4-day forecasts.

---

*This documentation will be expanded as V2 development progresses.*
