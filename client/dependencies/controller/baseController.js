var app = angular.module('apschedulerApp', []);
app.controller('apschedulerMainApp', function($scope,$http) {

	// common function for show messages
	toastr.options = {
        closeButton: true,
        newestOnTop: true,
        progressBar: true
    };
    $scope.toastrErrorMsg = function(title, message) {
		toastr.error(message, title)
	}
	$scope.toastrSuccessMsg = function(title, message) {
		toastr.success(message, title)
	}
    $scope.$on('parentToastrErrorMsg', function(evt, title, message) {
		toastr.error(message, title)
    })
    $scope.$on('parentToastrSuccessMsg', function(evt, title, message) {
    	console.log(title, message)
		toastr.success(message, title)
    })
	// ends here ~ common function for show messages

	// common http call function
	$scope.$on('httpFunction', function(evt, urlParam, payloadParam, callbackFuncAvail, callback){
		$http({
		    method: "POST",
		    url: urlParam,
		   	headers: {
		        'Content-Type': 'application/json; charset=UTF-8'
		    },
		    data: payloadParam
		  }).then(function success(response) {
		  		let ajaxResponseData =  response.data;
		  		if (ajaxResponseData.responseType == 'success') {
		  			if (callbackFuncAvail == false) {
		  				$scope.toastrSuccessMsg('success', ajaxResponseData.responseMessage)
		  			} else {
		  				callback(ajaxResponseData);
		  			}
		  		} else {
		  			$scope.toastrErrorMsg('Error', ajaxResponseData.responseMessage)
		  		}
		  }, function error(response) {
		  		console.log('error response',response)
		  });
	})
	// ends here ~ common http call function



});