/*
	Author: ASU CAPSTONE TEAM 2018
	Date: 11.08.2018
	Description: Controllers for Handling UI data binding and REST request
*/

var app = angular.module('solarsenseApp', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  	$interpolateProvider.startSymbol('{a');
  	$interpolateProvider.endSymbol('a}');
  	//$locationProvider.html5Mode(true);
  	//$sceProvider.enabled(false);
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

app.controller('LearnCtrl', function($scope, $timeout, $http) {
	$scope.url = "http://11.11.11.11/digital_library";
	/*
	$scope.hash = $window.location.hash.substring(1);

 	$scope.getURL = function() {
		if (window.location.hash)
			$scope.url = $scope.url + "/" + $scope.hash + ".html";
		else
			$scope.url = $scope.url + "/index.html"
	}
	*/
	$scope.goHome = function () {
		$window.location.href = "/"; 
	}
});
