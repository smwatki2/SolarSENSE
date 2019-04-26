/*
	Author: ASU CAPSTONE TEAM 2018 - 2019
	Date: 03.22.2019
	Description: Displays the SolarSENSE Digital Library
*/

var env = {};

if(window){
	Object.assign(env, window.__env);
}

var app = angular.module('solarsenseApp', []);

app.constant("__env", env);

app.config(['$interpolateProvider', function($interpolateProvider) {
  	$interpolateProvider.startSymbol('{a');
  	$interpolateProvider.endSymbol('a}');
}]);

app.controller('LearnCtrl', function($scope, $timeout, $http) {
	$scope.url = __env.serverUrl + "/digital_library";
	// TODO: Finish adding ability to change which page is used on page load.
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
