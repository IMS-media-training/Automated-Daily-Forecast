# Deployment Guide

## GitHub Actions Automation

The project runs automatically via GitHub Actions.

### Scheduled Execution

- **Time:** Daily at 6:00 AM Israel time (3:00 AM UTC)
- **Workflow:** Download → Extract → Generate → Email

### Manual Execution

1. Go to: **Actions** → **IMS Daily Weather Forecast**
2. Click: **Run workflow**
3. Choose dry-run mode to test without sending email

## GitHub Secrets Configuration

Navigate to: **Repository Settings → Secrets and variables → Actions**

Add these secrets:

| Secret | Description | Example |
|--------|-------------|---------|
| `EMAIL_ADDRESS` | Sender email | forecasts@gmail.com |
| `EMAIL_PASSWORD` | App password | 16-char app password |
| `SMTP_SERVER` | SMTP server | smtp.gmail.com |
| `SMTP_PORT` | SMTP port | 587 |
| `RECIPIENTS_LIST` | Recipients (one per line) | user1@example.com<br>user2@example.com |

### Recipients Configuration

The `RECIPIENTS_LIST` secret supports multiple recipients:

```
user1@example.com
user2@gmail.com
team@company.com
```

GitHub preserves line breaks in secrets.

## Workflow Features

- **Timeout:** 15 minutes
- **Artifacts:** Images stored for 90 days, logs for 30 days
- **Notifications:** GitHub emails on workflow failures

## Monitoring

### View Runs
Actions tab → IMS Daily Weather Forecast → View run history

### Download Artifacts
Click on a workflow run → Download artifacts (images, logs)

### Failure Notifications
GitHub sends email notifications on workflow failures.

## Testing

### Dry-Run Test
1. Actions → Run workflow
2. Set "Dry run" to `true`
3. Validates configuration without sending email

### Production Test
1. Actions → Run workflow
2. Set "Dry run" to `false`
3. Verify all recipients receive email

## Troubleshooting

### Workflow Fails on Download
- Check IMS website availability
- Workflow will use archived XML if available

### Email Not Received
- Verify GitHub secrets are set correctly
- Check spam/junk folders
- Verify App Password (not regular Gmail password)

### Image Not Generated
- Check workflow logs for errors
- Verify all assets are present

---

*This documentation will be expanded as V2 development progresses.*
