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

app.controller('HomeCtrl', function($scope, $timeout, $http, $window) {

	$scope.startCollection = function () {
		$window.location.href = "instant"; 
	}

	$scope.scanSensors = function () {
		$window.location.href = "scan"; 
	}
	
});

app.controller('InstantCtrl', function($scope,$http){

	$scope.test = "This is a Test";
	$scope.soilData = [];

	$scope.dataRequest = function() {
		console.log("Calling Data Object");
		$http({
			method:'GET',
			// When using on development machine, use http://localhost:5000/data
			// When using and deploying on pi, use http://11.11.11.11/data
			url:'http://11.11.11.11/data',
			headers: {
				'Access-Control-Allow-Origin': '*',
        		'Access-Control-Allow-Methods' : 'PUT,GET',
        		'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
			}
		})
		.then(function success(response){
			$scope.response = response.data;
			for(var i = 0; i < $scope.response.length; i++){
				var soilObj = JSON.parse($scope.response[i]);
				$scope.soilData.push(soilObj);
			}
		}, function error(response){
			console.log("There was an error getting the data");
		});

	};

});

app.controller('ScanCtrl', function($scope, $timeout, $http) {
	
});
