# GitHub Actions Setup Guide - Phase 4c

Complete setup instructions for automated daily forecast delivery via GitHub Actions.

## Overview

The GitHub Actions workflow runs automatically every day at 6:00 AM Israel time (3:00 AM UTC during DST) and sends the daily weather forecast via email.

**Workflow Features:**
- ✅ Automated daily execution
- ✅ Manual trigger for testing
- ✅ Dry-run mode support
- ✅ Artifact uploads (images + logs)
- ✅ Comprehensive workflow summaries

---

## Prerequisites

Before setting up GitHub Actions, ensure you have:

1. ✅ **Local workflow working** - Test `python forecast_workflow.py` successfully
2. ✅ **Gmail App Password** - 16-character app password generated
3. ✅ **Repository pushed to GitHub** - Code available in GitHub repository
4. ✅ **GitHub account access** - Admin/write permissions on the repository

---

## Step 1: Generate Gmail App Password

If you haven't already generated an App Password for Gmail:

1. **Enable 2-Step Verification:**
   - Go to: https://myaccount.google.com/security
   - Find "2-Step Verification" and enable it

2. **Generate App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - App name: "IMS Weather Forecast Automation"
   - Click "Generate"
   - Copy the 16-character password (spaces will be removed automatically)
   - **IMPORTANT:** Save this password - you can't view it again!

---

## Step 2: Add GitHub Secrets

GitHub Secrets are encrypted environment variables that are only exposed to workflow runs. They're never visible in logs or to unauthorized users.

### How to Add Secrets

1. **Navigate to Repository Settings:**
   - Go to your GitHub repository
   - Click **Settings** (top-right navigation)
   - In the left sidebar, click **Secrets and variables** → **Actions**

2. **Add the following 5 secrets:**

Click "New repository secret" for each of these:

### Required Secrets

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `EMAIL_ADDRESS` | Gmail account sending the forecast | `mws430170@gmail.com` |
| `EMAIL_PASSWORD` | Gmail App Password (16 chars) | `abcdefghijklmnop` |
| `RECIPIENTS_LIST` | **Multi-recipient list** (one per line) | See below |
| `SMTP_SERVER` | SMTP server address | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port (TLS) | `587` |

### Detailed Instructions for Each Secret

#### 1. EMAIL_ADDRESS
```
Name: EMAIL_ADDRESS
Value: your-gmail@gmail.com
```
- This is the Gmail account that will **send** the forecast emails
- Must be a valid Gmail address
- Must have 2-Step Verification enabled

#### 2. EMAIL_PASSWORD
```
Name: EMAIL_PASSWORD
Value: your-16-char-app-password
```
- **NOT your regular Gmail password**
- Must be a 16-character App Password
- Generate at: https://myaccount.google.com/apppasswords
- Example format: `abcdefghijklmnop` (no spaces)

#### 3. RECIPIENTS_LIST (Multi-Recipient Support)
```
Name: RECIPIENTS_LIST
Value:
user1@example.com
user2@gmail.com
team@company.com
```
- **One email address per line** (GitHub preserves line breaks)
- Can include multiple recipients (as many as needed)
- Empty lines and lines starting with `#` are ignored (comments)
- Example multi-recipient value:
  ```
  noamw2703@gmail.com
  weissno@ims.gov.il
  sassona@ims.gov.il
  # weather-team@ims.gov.il (commented out)
  ```
- **Important:** Copy your local `recipients.txt` content directly into this secret

#### 4. SMTP_SERVER
```
Name: SMTP_SERVER
Value: smtp.gmail.com
```
- SMTP server address for Gmail
- Always `smtp.gmail.com` for Gmail accounts
- For other providers, use their SMTP server

#### 5. SMTP_PORT
```
Name: SMTP_PORT
Value: 587
```
- SMTP port for TLS encryption
- Always `587` for Gmail (TLS)
- Alternative: `465` for SSL (not recommended)

---

## Step 3: Verify Secrets

After adding all secrets:

1. **Check the Secrets Page:**
   - Go to: Settings → Secrets and variables → Actions
   - You should see all 5 secrets listed:
     - ✅ EMAIL_ADDRESS
     - ✅ EMAIL_PASSWORD
     - ✅ RECIPIENTS_LIST
     - ✅ SMTP_SERVER
     - ✅ SMTP_PORT

2. **Security Notes:**
   - ✅ Secrets are encrypted by GitHub
   - ✅ Secret values are never displayed after creation
   - ✅ Only visible to workflow runs
   - ✅ Not visible in logs (replaced with ***)

---

## Step 4: Test the Workflow (Manual Trigger)

Before relying on the automated daily schedule, test the workflow manually:

### Test with Dry-Run Mode

1. **Navigate to Actions:**
   - Go to your GitHub repository
   - Click **Actions** tab (top navigation)

2. **Find the Workflow:**
   - In the left sidebar, click "IMS Daily Weather Forecast"

3. **Run Workflow (Dry-Run):**
   - Click the **Run workflow** button (right side)
   - Select branch: `feature/phase-4-v2-email-delivery` (or `main`)
   - Set "Dry run mode" to: **true**
   - Click **Run workflow**

4. **Monitor Execution:**
   - Click on the running workflow (orange dot)
   - Expand each step to see logs
   - Verify all steps complete successfully
   - **Expected:** Configuration validated, but NO email sent

### Test with Real Email Send

After dry-run succeeds:

1. **Run Workflow Again:**
   - Click **Run workflow** button
   - Set "Dry run mode" to: **false**
   - Click **Run workflow**

2. **Verify Success:**
   - ✅ All steps complete (green checkmarks)
   - ✅ Email received at recipient address
   - ✅ Image attached to email (Instagram-ready)
   - ✅ Hebrew RTL formatting correct

---

## Step 5: Enable Automated Daily Runs

Once manual testing succeeds:

### Schedule Configuration

The workflow is already configured to run daily at 6:00 AM Israel time:

```yaml
schedule:
  - cron: '0 3 * * *'  # 3:00 AM UTC = 6:00 AM Israel (DST)
```

**No additional configuration needed!** The workflow will automatically run every day.

### Monitoring Automated Runs

1. **View Workflow Runs:**
   - Go to: Actions → IMS Daily Weather Forecast
   - See history of all runs (manual + scheduled)

2. **Check Email Delivery:**
   - Recipient should receive email daily at ~6:00 AM Israel time
   - If no email received, check workflow logs

3. **Review Artifacts:**
   - Each run uploads forecast image + logs
   - Available for 90 days (images) and 30 days (logs)
   - Download from: Actions → [Workflow Run] → Artifacts

---

## Troubleshooting

### Workflow Fails: "Missing environment variable"

**Cause:** GitHub Secret not set or named incorrectly

**Solution:**
1. Go to: Settings → Secrets and variables → Actions
2. Verify all 5 secrets exist with EXACT names (case-sensitive):
   - `EMAIL_ADDRESS`
   - `EMAIL_PASSWORD`
   - `RECIPIENTS_LIST`
   - `SMTP_SERVER`
   - `SMTP_PORT`
3. Re-run workflow

### Workflow Fails: "SMTP Authentication Failed"

**Cause:** Incorrect App Password or 2-Step Verification not enabled

**Solution:**
1. Verify 2-Step Verification enabled: https://myaccount.google.com/security
2. Generate new App Password: https://myaccount.google.com/apppasswords
3. Update `EMAIL_PASSWORD` secret with new password
4. Re-run workflow

### Email Not Received (But Workflow Succeeds)

**Cause:** Email in spam folder or recipient address incorrect

**Solution:**
1. Check spam/junk folder for all recipients
2. Verify `RECIPIENTS_LIST` secret value (check email addresses)
3. Add sender to safe senders list
4. Check Gmail "Sent" folder (if sender is Gmail)
5. Verify recipients.txt was created correctly in workflow logs

### Workflow Doesn't Run Automatically

**Cause:** GitHub Actions disabled or repository inactive

**Solution:**
1. Go to: Settings → Actions → General
2. Verify "Actions permissions" allows workflows
3. Check: Actions → IMS Daily Weather Forecast → Enable workflow
4. Repository must have activity in last 60 days (scheduled workflows pause on inactive repos)

---

## Security Best Practices

### ✅ DO:
- Use temporary Gmail account for testing
- Generate separate App Password for this workflow
- Keep secrets encrypted in GitHub (never in code)
- Rotate App Password periodically
- Review workflow logs for unauthorized access

### ❌ DON'T:
- Commit `.env` file to repository
- Share App Password in plain text
- Use personal Gmail password (always use App Password)
- Enable "Less secure app access" (deprecated)
- Store credentials in workflow files

---

## Workflow Features

### Dry-Run Mode

Test workflow without sending email:

```bash
# Local testing
python forecast_workflow.py --dry-run

# GitHub Actions
Actions → Run workflow → Dry run mode: true
```

### Manual Trigger (workflow_dispatch)

Run workflow on-demand without waiting for schedule:

1. Go to: Actions → IMS Daily Weather Forecast
2. Click "Run workflow"
3. Select branch and dry-run mode
4. Click "Run workflow"

### Artifacts

Each workflow run uploads:

- **Forecast Image** (90-day retention)
  - Instagram story (1080x1920px)
  - All 15 cities with weather data
  - Download from: Artifacts → `forecast-image-{run_number}`

- **Logs** (30-day retention)
  - Complete workflow execution logs
  - Troubleshooting information
  - Download from: Artifacts → `logs-{run_number}`

### Workflow Summary

Each run generates a summary with:
- Run number and trigger type
- Execution mode (dry-run vs production)
- Step status (all 4 phases)
- Quick links to artifacts

View at: Actions → [Workflow Run] → Summary

---

## Next Steps: Phase 5

After Phase 4c completes successfully:

- **Phase 5:** Production server deployment
  - Transition from GitHub Actions to IMS production servers
  - Linux compatibility validation
  - IT team handoff and training
  - Production monitoring and alerting

---

## Quick Reference

### Essential Links

- **Add GitHub Secrets:** Settings → Secrets and variables → Actions
- **Generate App Password:** https://myaccount.google.com/apppasswords
- **View Workflow Runs:** Actions → IMS Daily Weather Forecast
- **Workflow File:** `.github/workflows/daily-forecast.yml`
- **Documentation:** `docs/GITHUB_ACTIONS_SETUP.md` (this file)

### Required Secrets Checklist

- [ ] `EMAIL_ADDRESS` - Gmail sender
- [ ] `EMAIL_PASSWORD` - 16-char App Password
- [ ] `RECIPIENTS_LIST` - Multi-recipient list (one per line)
- [ ] `SMTP_SERVER` - smtp.gmail.com
- [ ] `SMTP_PORT` - 587

### Testing Checklist

- [ ] Local workflow works: `python forecast_workflow.py`
- [ ] Dry-run succeeds: Actions → Run workflow (dry-run: true)
- [ ] Real email sent: Actions → Run workflow (dry-run: false)
- [ ] Email received with correct formatting
- [ ] Scheduled run successful (after 6:00 AM Israel time)

---

**Phase 4c Status:** Complete ✅
**Automated Daily Runs:** Enabled ✅
**Next Phase:** Phase 5 (Production Deployment)
