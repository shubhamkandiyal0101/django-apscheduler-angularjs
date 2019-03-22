var app = angular.module('loginApp', []);
app.controller('loginController', function($scope,$http) {

	// regexp
	$scope.emailRegex = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
	$scope.nameRegex = /^[a-zA-Z\s]*$/;
	// ends here ~ regexp

	// on load toastr settings
	toastr.options = {
        closeButton: true,
        newestOnTop: true,
        progressBar: true
    };
	// ends here ~ on load toastr settings

	$scope.toastrErrorMsg = function(title, message) {
		toastr.error(message, title)
	}
	$scope.toastrSuccessMsg = function(title, message) {
		toastr.success(message, title)
	}

	// http call
	$scope.httpCall = function(urlParam, payloadParam, callbackFuncAvail, callback) {
		console.log(payloadParam)
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
	}
	// ends here ~ http call

	// dynamic function for check validation 
	$scope.checkValidation = function(regexpAvailable, regexVariable, angularModelVariable) {
		// declare global variable for this block
		let validationTest;
		// ends here ~ declare global variable for this block
		if(regexpAvailable == true) {
			validationTest = ($scope[regexVariable].test($scope[angularModelVariable]) == false || $scope[angularModelVariable] == '' || $scope[angularModelVariable] == undefined);
		} else {
			validationTest = ($scope[angularModelVariable] == '' || $scope[angularModelVariable] == undefined)
		}
		return validationTest;
	}
	// ends here ~ dynamic function for check validation

	// function for user signup
    $scope.userSignup = function() {
    	let signupPayload = {'fullname':$scope.signupFullname, 'email':$scope.signupEmail, 'password':$scope.signupPassword}

    	let fullnameCondition = $scope.checkValidation(true, 'nameRegex', 'signupFullname');
    	let emailCondition = $scope.checkValidation(true, 'emailRegex', 'signupEmail');
    	let pswdCondition = $scope.checkValidation(false, '', 'signupPassword');

    	if(fullnameCondition == true) {
    		$scope.toastrErrorMsg('Error','Name is not Valid. Please enter only Alphabets')
    	} else if (emailCondition == true) {
    		$scope.toastrErrorMsg('Error','Email is Incorrect')
    	} else if(pswdCondition == true) {
    		$scope.toastrErrorMsg('Error','Password is not be Empty')
    	} 
    	// ends here ~ check regex

    	// call http function
    	if(fullnameCondition == false && emailCondition == false && pswdCondition == false) {
    		let signupPayloadJson = JSON.stringify(signupPayload);
    		$scope.httpCall('/signup-user/',signupPayloadJson, false)
    	}
    	// ends here ~ call http function

    }
    // ends here ~ function for user signup

    // function for user signin
    $scope.userSignin = function() {
    	let signinPayload = {'email':$scope.loginEmail, 'password':$scope.loginPassword}

    	let emailCondition = $scope.checkValidation(true, 'emailRegex', 'loginEmail');
    	let pswdCondition = $scope.checkValidation(false, '', 'loginPassword');

    	if (emailCondition == true) {
    		$scope.toastrErrorMsg('Error','Email is not Valid')
    	} else if(pswdCondition == true) {
    		$scope.toastrErrorMsg('Error','Password is not be Empty')
    	}

    	// call http function
    	if(emailCondition == false && pswdCondition == false) {
    		let signinPayloadJson = JSON.stringify(signinPayload);
    		$scope.httpCall('/signin-user/',signinPayloadJson, true, function(returnAjaxResponse){
    			if(returnAjaxResponse.responseType == 'success') {
    				$scope.toastrSuccessMsg('success', returnAjaxResponse.responseMessage);
    				window.location = '/dashboard';
    			}
    		})
    	}
    	// ends here ~ call http function
    }
    // ends here ~ function for user signin
    
     

});