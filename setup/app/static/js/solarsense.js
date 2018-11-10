/*
	Author: ASU CAPSTONE TEAM 2018
	Date: 11.08.2018
	Description: Controllers for Handling UI data binding and REST request
*/

var app = angular.module('solarsenseApp', []);

app.controller('HomeCtrl', function($scope, $timeout, $http, $window) {

	$scope.startCollection = function () {
		$window.location.href = "instant"; 
	}

	$scope.scanSensors = function () {
		$window.location.href = "scan"; 
	}
	
});

app.controller('InstantCtrl', function($scope, $timeout, $http, $window) {
	
});

app.controller('ScanCtrl', function($scope, $timeout, $http) {
	
});