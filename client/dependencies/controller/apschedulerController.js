app.controller('apschedulerDashboardApp', function($scope,$http) {

	// on load tagify js
	let emailTagsInput = document.querySelector('input[name=emailTags]');
	let emailTagifyData = new Tagify(emailTagsInput);
	let instantEmailTagsInput = document.querySelector('input[name=instantEmailTags]');
	let instantEmailTagifyData = new Tagify(instantEmailTagsInput);
	// ends here ~ on load tagify js

	// save email content
	$scope.saveEmailContent = function() {
		let requiredPayload = {'subject':$scope.emailSubject,'content':$scope.emailContent,'reportName':$scope.reportName,'email':[]}
		let emailTagifyDataValue = emailTagifyData.value;
		requiredPayload.email = []
		for(let i=0; i<emailTagifyDataValue.length; i++) {
			requiredPayload.email.push(emailTagifyDataValue[i].value)
		}
		let requiredPayloadJson = JSON.stringify(requiredPayload) 
		$scope.$emit('httpFunction', '/save-email-report/', requiredPayloadJson, true,function(parentFuncReturnResp){
			if (parentFuncReturnResp.responseType == 'success') {
				$scope.$emit('parentToastrSuccessMsg', 'Success', parentFuncReturnResp.responseMessage)
			}
		})
	}
	// ends here ~ save email content

	// function for send email immediately
	$scope.instantBulkEmailSendFunc = function() {
		let requiredPayload = {'subject':$scope.instantEmailSubject,'content':$scope.instantEmailContent,'email':[]}
		let instantEmailTagifyDataValue = instantEmailTagifyData.value;
		requiredPayload.email = []
		for(let i=0; i<instantEmailTagifyDataValue.length; i++) {
			requiredPayload.email.push(instantEmailTagifyDataValue[i].value)
		}
		let requiredPayloadJson = JSON.stringify(requiredPayload) 
		$scope.$emit('httpFunction', '/instant-email-send/', requiredPayloadJson, true,function(parentFuncReturnResp){
			if (parentFuncReturnResp.responseType == 'success') {
				$scope.$emit('parentToastrSuccessMsg', 'Success', parentFuncReturnResp.responseMessage)
			}
		})
	}
	// ends here ~ function for send email immediately

	// load cron tabs UI 
	$scope.showCronTabsUi = function() {
		$scope.cronTabsUiVal = $('.cronTabsUi').jqCron({
	        enabled_minute: true,
	        multiple_dom: true,
	        multiple_month: true,
	        multiple_mins: true,
	        multiple_dow: true,
	        multiple_time_hours: true,
	        multiple_time_minutes: true,
	        bind_to: $('.cronTabsUi-input'),
	        bind_method: {
	            set: function($element, value) {
	                $element.val(value);
	            }
	        },
	        no_reset_button: false,
	        lang: 'en'
	    }).jqCronGetInstance();;
	}
	// ends here ~ load cron tabs UI 

	// fetch all reports
	$scope.fetchAllEmailReports = function() {
		$scope.$emit('httpFunction', '/fetch-all-email-reports/', '', true,function(parentFuncReturnResp){
			if (parentFuncReturnResp.responseType == 'success') {
				$scope.emailAssignReportData = parentFuncReturnResp.responseData;
				console.log($scope.emailAssignReportData)
				$scope.$emit('parentToastrSuccessMsg', 'Success', parentFuncReturnResp.responseMessage)
			}
		})
	}
	// ends here ~ fetch all reports

	// function for delete current report
	$scope.deleteSelectedEmailReport = function (selectedReportData) {
		let deleteReportPayload = {'reportName':selectedReportData}
		let deleteReportPayloadJson = JSON.stringify(deleteReportPayload)
		$scope.$emit('httpFunction', '/delete-current-email-report/', deleteReportPayloadJson, true,function(parentFuncReturnResp){
			if (parentFuncReturnResp.responseType == 'success') {
				$scope.$emit('parentToastrSuccessMsg', 'Success', parentFuncReturnResp.responseMessage)
				for(let i=0; i<$scope.emailAssignReportData.length; i++) {
					if ($scope.emailAssignReportData[i].reportName == selectedReportData) {
						$scope.emailAssignReportData.splice(i,1);
						break;
					}
				}
			}
		})
	}
	// ends here ~ function for delete current report


	// schedule email function
	$scope.scheduleEmailFunc = function(){
		let schedulePayload = Object.assign({},$scope.selectedEmailAssignReportData,{'cronValue':$scope.cronTabsUiVal.getCron()})
		delete schedulePayload['$$hashKey'];
		delete schedulePayload['email'];
		delete schedulePayload['content'];
		let schedulePayloadJson = JSON.stringify(schedulePayload);
		$scope.$emit('httpFunction', '/schedule-current-email-report/', schedulePayloadJson, false)
	}
	// ends here ~ schedule email function

	// get all schedule email report
	$scope.getAllScheduleEmail = function() {
		$scope.$emit('httpFunction', '/get-all-schedule-email/', '', true, function(scheduleEmailResponse){
			if(scheduleEmailResponse.responseType = 'success') {
				$scope.emailCronSchedule = scheduleEmailResponse.responseData;
				$scope.$emit('parentToastrSuccessMsg', 'Success', scheduleEmailResponse.responseMessage)
			}
		})
	}
	// ends here ~ get all schedule email report

	// pause or delete email schedule
	$scope.pauseDeleteSchedule = function(cronJobDataParam, actionPerformed) {
		let payloadData = cronJobDataParam;
		payloadData['requiredAction'] = actionPerformed;
		let payloadJsonData = JSON.stringify(payloadData)
		$scope.$emit('httpFunction', '/pause-delete-schedule-email/', payloadJsonData, true, function(scheduleEmailResponse){
			console.log(scheduleEmailResponse)
		})
		
	}
	// ends here ~ pause or delete email schedule 

});