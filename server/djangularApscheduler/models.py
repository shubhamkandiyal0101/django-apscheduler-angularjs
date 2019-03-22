from django.contrib.auth.models import User
from django.db import models

class emailData(models.Model):
	email_by = models.ForeignKey(User, on_delete=models.CASCADE)
	email_subject = models.CharField(max_length=255)
	email_content = models.CharField(max_length=1000)
	email_tags = models.CharField(max_length=1000)
	report_name = models.CharField(max_length=1000)

class emailCronTable(models.Model):
	cron_by = models.ForeignKey(User, on_delete=models.CASCADE)
	cron_value = models.CharField(max_length=255)
	cron_report_name = models.CharField(max_length=1000)
	cron_status = models.BooleanField(default=True)
	cron_email_relation = models.ForeignKey(emailData, on_delete=models.CASCADE)
	cron_id = models.CharField(max_length=255)
