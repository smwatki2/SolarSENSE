/*
	Author: ASU CAPSTONE TEAM 2018
	Date: 11.08.2018
	Description: Controllers for Handling UI data binding and REST request
*/

var app = angular.module('solarsenseApp', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  	$interpolateProvider.startSymbol('{a');
  	$interpolateProvider.endSymbol('a}');
}]);

app.controller('LinkCtrl', function($scope, $window) {

  	$scope.startCollection = function () {
		$window.location.href = "instant";
	}

	$scope.test = function(){
		$scope.gettingAlgorithm();
		$scope.gettingAlgorithmFromSensors();
	}

	$scope.scanSensors = function () {
		$window.location.href = "scan";
	}

	$scope.goToLearn = function () {
		$window.location.href = "learn";
	}

	$scope.goToFarmStatus = function () {
		$window.location.href = "/";
	}

	$scope.openConfig = function () {
		$window.location.href = "config";
	}
});

app.controller('InstantCtrl', function($scope,$http,$timeout){

	$scope.test = "This is a Test";
	$scope.soilData = [];
	$scope.percent = 0;

	$scope.showData = function() {
		if($scope.percent === 100){
			return true;
		}
		return false;
	};

	$scope.showProgress = function() {
		if($scope.percent === 100) {
			return false;
		}
		return true;
	};

	$scope.dataRequest = function() {
		console.log("Calling Data Object");
		$http({
			method:'GET',
			// When using on development machine, use http://localhost:5000/data
			// When using and deploying on pi, use http://11.11.11.11/data
			url:'http://11.11.11.11/data',
			// url: 'http://localhost:5000/data',
			headers: {
				'Access-Control-Allow-Origin': '*',
        		'Access-Control-Allow-Methods' : 'PUT,GET',
        		'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
			}
		})
		.then(function success(response){
			$scope.response = response.data;
			var percentVal = 100 / $scope.response.length;
			for(var i = 0; i < $scope.response.length; i++){		
				var soilObj = JSON.parse($scope.response[i]);
				$scope.soilData.push(soilObj);
			}

			$timeout(function(){
				for(var i = 0; i < 100; i++){
					$scope.percent++;
				}
			},5000);
		}, function error(response){
			console.log("There was an error getting the data");
		});

	};

});