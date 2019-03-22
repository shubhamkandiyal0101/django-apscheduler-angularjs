# import required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from . import settings
from .models import emailData, emailCronTable
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import uuid 
from datetime import datetime


# from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

# required on load variables
# jobstores = {
#     'default': SQLAlchemyJobStore(url="mysql+pymysql://root:XXXXX@localhost/XXXX",tablename='apscheduler_jobs')
# }
# executors = {
#     'default': ThreadPoolExecutor(20),
#     'processpool': ProcessPoolExecutor(5)
# }
# job_defaults = {
#     'coalesce': False,
#     'max_instances': 3
# }

# sched = BackgroundScheduler(jobstores=jobstores,executors=executors,job_defaults=job_defaults)
# sched.start()

# sched = BackgroundScheduler()
# sched.start()

jobstores = {
    'default': SQLAlchemyJobStore(url="postgresql://postgres:rootdb@localhost/djangularApschedulerDb",tablename='apscheduler_jobs')
}

sched = BackgroundScheduler(jobstores=jobstores)
sched.start()

# ends here ~ required on load variables


# for login signup
def loginSignup(request):
	return render(request, 'render/loginSignup.html')

# for signup user
@csrf_exempt
def signupUser(request):
	try:
		# read request data
		requestData = request.body;
		requestDataDecode = requestData.decode('utf8').replace("'", '"');
		requestDataJson = json.loads(requestDataDecode)
		# ends here ~ read request data

		# assign data to variable from dict 
		userEmail = requestDataJson['email'];
		userFullName = requestDataJson['fullname'];
		userPassword = requestDataJson['password'];
		# ends here ~ assign data to variable from dict

		# filter user table data
		userFilterData = User.objects.filter(email=userEmail)
		# ends here ~ filter user table data

		if len(userFilterData) == 0:
			# create user
			User.objects.create(email=userEmail,password=make_password(userPassword));
			messageData = {'responseType':'success','responseMessage':'Account Created Successfully'}
			# ends here ~ create user
		else:
			messageData = {'responseType':'error','responseMessage':'Account Already Exists. Please Login'}

		# return response
		return HttpResponse(json.dumps(messageData))
		# ends here ~ return response

	except Exception as e:
		print('error while user registration ',e)

# for signin user
@csrf_exempt
def signinUser(request):
	try:
		# read request data
		requestData = request.body;
		requestDataDecode = requestData.decode('utf8').replace("'", '"');
		requestDataJson = json.loads(requestDataDecode)
		# ends here ~ read request data

		# assign data to variable from dict 
		userEmail = requestDataJson['email'];
		userPassword = requestDataJson['password'];
		# ends here ~ assign data to variable from dict

		try:
			userFilterData = User.objects.get(email=userEmail)
			verifyUserPassword = userFilterData.check_password(userPassword)
			if verifyUserPassword == True:
				login(request, userFilterData)
				messageData = {'responseType':'success','responseMessage':'Successfully Login. Please wait Redirecting you to Next Page'}
			else:
				messageData = {'responseType':'error','responseMessage':'Password is mismatch with provided id. Please enter Correct Password'}
		except Exception as e:
			# account not exists
			messageData = {'responseType':'error','responseMessage':'Account not Exists with this Email. Please signup and then try to login again'}
			# ends here ~ account not exists

		# return response
		return HttpResponse(json.dumps(messageData))
		# ends here ~ return response

	except Exception as e:
		print('error while user login ',e)

# function for render dashboard
@csrf_exempt
def dashboard(request):
	try:
		if request.user == 'AnonymousUser':
			print('user is not logged in')
		else:
			print('i am here')
			return render(request, 'render/index.html')
	except Exception as e:
		print('facing error in dashboard function: ',e)

# ends here ~ function for render dashboard

# function for send bulk email
@csrf_exempt
def instantEmailSend(request):
	try:
		# read request data
		requestData = request.body;
		requestDataDecode = requestData.decode('utf8').replace("'", '"');
		requestDataJson = json.loads(requestDataDecode)
		# ends here ~ read request data

		# extract data from request json
		instantEmailSubject =  requestDataJson['subject']
		instantEmailContent = requestDataJson['content']
		instantEmailAddress = requestDataJson['email']
		# ends here ~ extract data from request json

		# send email
		send_mail(
		    instantEmailSubject,
		    instantEmailContent,
		    settings.EMAIL_HOST_USER,
		    instantEmailAddress,
		)
		# ends here ~ send email

		messageData = {'responseType':'success','responseMessage':'Bulk Email Sent Successfully'}
		# return response
		return HttpResponse(json.dumps(messageData))
		# ends here ~ return response

	except Exception as e:
		print('facing error in instantEmailSend function: ',e)
# ends here ~ function for send bulk email

# function for save email content data
@csrf_exempt
def saveEmailReport(request):
	try:
		# read request data
		requestData = request.body;
		requestDataDecode = requestData.decode('utf8').replace("'", '"');
		requestDataJson = json.loads(requestDataDecode)
		# ends here ~ read request data

		# extract data from request json
		emailSubject =  requestDataJson['subject']
		emailContent = requestDataJson['content']
		emailAddress = requestDataJson['email']
		emailReportName = requestDataJson['reportName']
		# ends here ~ extract data from request json

		# filter user table data
		emailDataFilterContent = emailData.objects.filter(report_name=emailReportName)
		# ends here ~ filter user table data
		if len(emailDataFilterContent) == 0:
			# create report or store email record
			emailData.objects.create(email_by_id=request.user.id,email_subject=emailSubject,email_content=emailContent,email_tags=emailAddress,report_name=emailReportName);
			messageData = {'responseType':'success','responseMessage':'Email Saved Successfully for Scheduling'}
			# ends here ~ create report or store email record
		else:
			messageData = {'responseType':'error','responseMessage':'Same Report is Already Created for Scheduling. Please Assign Unique Name'}


		
		# return response
		return HttpResponse(json.dumps(messageData))
		# ends here ~ return response

	except Exception as e:
		print('facing error in instantEmailSend function: ',e)

# ends here ~ function for save email content data

# fetch all email data
@csrf_exempt
def fetchAllEmailReports(request):
	try:
		if request.user == 'AnonymousUser':
			print('user is not logged in')
		else:
			try:
				emailDataFilterContent = emailData.objects.filter(email_by_id=request.user.id)
				if len(emailDataFilterContent) == 0:
					messageData = {'responseType':'error','responseMessage':'No Email Data Found for Scheduling'}
				else:
					emailReportList = []
					emailReportDict = {'subject':'','content':'','email':'','reportName':'','user_id':''}
					for emailReportData in emailDataFilterContent:
						emailReportDict['subject'] = emailReportData.email_subject
						emailReportDict['content'] = emailReportData.email_content
						emailReportDict['email'] = emailReportData.email_tags
						emailReportDict['reportName'] = emailReportData.report_name
						emailReportDict['user_id'] = request.user.id
						emailReportList.append(emailReportDict.copy())
					messageData = {'responseType':'success','responseMessage':'Reload All Email Reports','responseData':emailReportList}
				# return response
				return HttpResponse(json.dumps(messageData))
				# ends here ~ return response

			except Exception as e:
				print('facing error while fetching data from table: ',e)
	except Exception as e:
		print('facing error in dashboard function: ',e)
# ends here ~ fetch all email data

# delete email report function
@csrf_exempt
def deleteCurrentEmailReport(request):
	try:
		# read request data
		requestData = request.body;
		requestDataDecode = requestData.decode('utf8').replace("'", '"');
		requestDataJson = json.loads(requestDataDecode)
		# ends here ~ read request data

		# extract data from request
		reportName = requestDataJson['reportName']
		emailData.objects.filter(email_by_id=request.user.id,report_name=reportName).delete()
		# ends here ~ extract data from request

		messageData = {'responseType':'success','responseMessage':'Delete Report Successfully'}
		# return response
		return HttpResponse(json.dumps(messageData))
		# ends here ~ return response

		print(requestDataJson)
	except Exception as e:
		print('facing error in deleteCurrentEmailReport function: ',e)
# ends here ~ delete email report function

# send email function
def sendEmailFunc(emailSubjectParam, emailSubjectContent, emailSubjectAddress):
	send_mail(
	    emailSubjectParam,
	    emailSubjectContent,
	    settings.EMAIL_HOST_USER,
	    emailSubjectAddress,
	)
# ends here ~ send email function

# send email cron function
def sendEmailCron(cronJobId):
	try:
		emailCronTableResult = emailCronTable.objects.get(cron_id=cronJobId)
		emailCronTableEmailRelId = emailCronTableResult.cron_email_relation_id
		emailDataResult = emailData.objects.get(id=emailCronTableEmailRelId)
		
		# extract data from email
		emailSubjectVal = emailDataResult.email_subject
		emailContentVal = emailDataResult.email_content
		emailAddressVal = eval(emailDataResult.email_tags)
		# ends here ~ extract data from email

		# print(type(eval(emailAddressVal)))

		# send email code
		sendEmailFunc(emailSubjectVal,emailContentVal,emailAddressVal)
		# ends here 
		print('Email is Sent Successfully')

	except Exception as e:
		print('facing error in sendEmailCron function: ',e)
# ends here ~ send email cron function 

# schedule cron
def scheduleCron(cronParam):
	schedJobData = sched.add_job(sendEmailCron, CronTrigger.from_crontab(cronParam))
	# schedJobData.id
	sched.print_jobs()
# ends here ~ schedule cron

# function for schedule current email report
@csrf_exempt
def scheduleCurrentEmailReport(request):
	try:
		# read request data
		requestData = request.body;
		requestDataDecode = requestData.decode('utf8').replace("'", '"');
		requestDataJson = json.loads(requestDataDecode)
		# ends here ~ read request data

		userId = requestDataJson['user_id']
		cronValue = requestDataJson['cronValue']
		reportName = requestDataJson['reportName']

		emailDataInstance = emailData.objects.get(email_by_id=request.user.id,report_name=reportName)
		
		uniqueUuid = uuid.uuid4().hex[:6].lower()
		stringTimestamp = str(int(datetime.now().timestamp()))
		uniqueCronId = uniqueUuid+stringTimestamp

		schedJobData = sched.add_job(sendEmailCron, CronTrigger.from_crontab(cronValue), id=uniqueCronId, args=[uniqueCronId])
		schedJobDataId = schedJobData.id
		
		emailCronTable.objects.create(cron_by_id=request.user.id,cron_value=cronValue,cron_report_name=reportName,cron_email_relation=emailDataInstance,cron_id=schedJobDataId)

		messageData = {'responseType':'success','responseMessage':'Email Report is Successfully Schedule'}
		# return response
		return HttpResponse(json.dumps(messageData))

	except Exception as e:
		print('facing error in scheduleCurrentEmailReport function: ',e)
# ends here ~ function for schedule current email report


# get all schedule email
@csrf_exempt
def getAllScheduleEmail(request):
	try:
		listAllCronJob = emailCronTable.objects.filter(cron_by_id=request.user.id)
		cornList = []
		listCronDict = {'cronReportName':'','cronValue':'','cronUserId':'','cronId':'','cronStatus':''}
		for cronJob in listAllCronJob:
			listCronDict['cronReportName'] = cronJob.cron_report_name
			listCronDict['cronValue'] = cronJob.cron_value
			listCronDict['cronUserId'] = cronJob.cron_by_id
			listCronDict['cronId'] = cronJob.cron_id
			listCronDict['cronStatus'] = cronJob.cron_status
			cornList.append(listCronDict.copy())

		messageData = {'responseType':'success','responseMessage':'Get All Email Report Successfully','responseData':cornList}
		# return response
		return HttpResponse(json.dumps(messageData))

	except Exception as e:
		print('facing error in getAllScheduleEmail function: ',e)
# ends here ~ get all schedule email

# code for pause Delete Schedule Email function
@csrf_exempt
def pauseDeleteScheduleEmail(request):
	try:
		# read request data
		requestData = request.body;
		requestDataDecode = requestData.decode('utf8').replace("'", '"');
		requestDataJson = json.loads(requestDataDecode)
		# ends here ~ read request data
		print(requestDataJson)

		requiredCronId = requestDataJson['cronId']
		cronRequiredAction = requestDataJson['requiredAction']

		if (cronRequiredAction == 'pauseCronSchedule'):
			emailCronTable.objects.filter(cron_id=requiredCronId).update(cron_status=False)
			sched.pause_job(requiredCronId)
			returnResponseMessage = 'Pause Job Successfully'
			returnResponseData = ''
		elif (cronRequiredAction == 'resumeCronSchedule'):
			emailCronTable.objects.filter(cron_id=requiredCronId).update(cron_status=True)
			sched.resume_job(requiredCronId)
			returnResponseMessage = 'Resume Job Successfully'
			returnResponseData = ''
		elif (cronRequiredAction == 'deleteCronSchedule'):
			emailCronTable.objects.filter(cron_id=requiredCronId).delete()
			sched.remove_job(requiredCronId)
			returnResponseMessage = 'Delete Job Successfully'
			returnResponseData = ''

		messageData = {'responseType':'success','responseMessage':returnResponseMessage,'responseData':returnResponseData}
		print(messageData)
		# return response
		return HttpResponse(json.dumps(messageData))

	except Exception as e:
		print('facing error in pauseDeleteScheduleEmail function: ',e)
# ends here ~ code for pause Delete Schedule Email function

# # test function
# def myfunc():
	# print('soemthing new')
# scheduler.add_job(myfunc, 'interval', seconds=5)
# sched.add_job(myfunc, CronTrigger.from_crontab('27,30 8 * * *'))
# # ends here ~ test function 