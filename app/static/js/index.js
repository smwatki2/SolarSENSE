/*
	Author: ASU CAPSTONE TEAM 2018
	Date: 11.08.2018
	Description: Controllers for Handling UI data binding and REST request
*/

var app = angular.module('solarsenseApp', []);

//let data = require('./urlendpoint.json');
import data from './urlendpoint.json';
const urlendpoint = data.urlendpoint;

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

app.controller('HomeCtrl', function($scope, $timeout, $http, $window) {

	angular.element(document).ready(function() {
		$scope.getValues();
	})

	$scope.notifications = [];
	// Temporary Variables, until we properly pull from databases
	$scope.statusWarnings = {
		"OK" : 0,
		"Caution" : 1,
		"Warning" : 2
	}
	$scope.cropName = "";
	$scope.temperatureStatus = 2; // OK (Green)
	$scope.sunlightStatus = 1; // Caution (Yellow)
	$scope.waterStatus = 0; // Warning (Red)

	// Debug Values (Most likely not to be used in final product)
	// $scope.temperature = 70.0;
	// $scope.sunlightTime = 4.0;
	// $scope.waterAmount = 10000.0;

	$scope.actualValues = {};
	$scope.goalValues = {};

	$scope.getValues = function() {
		$http({
			method:'GET',
			//url:'http://11.11.11.11/getValues',
			url: urlendpoint + '/getValues',
			headers: {
				'Access-Control-Allow-Origin': '*',
        		'Access-Control-Allow-Methods' : 'PUT,GET',
        		'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
			}
		}).then(function success(response){
			console.log(response.data);
			var resObj = response.data;
			$scope.cropName = resObj['CropName'];
			$scope.actualValues = resObj['ActualObj'];
			$scope.goalValues = resObj['GoalObj'];
			$scope.getFarmStatus();			
		}, function error(err){
			console.log(err);
		})		
	}

	$scope.getFarmStatus = function() {
		$scope.compareWater();
		$scope.compareTemp();
	}

	$scope.compareWater = function(){

		var waterVal = $scope.actualValues['WaterActual'];
		var waterGoal = $scope.goalValues['GoalEvo'];

		// If actual water values in a +- 0.1 range we can be considered good
		if (waterVal > waterGoal + 0.1 &&
			waterGoal < waterGoal - 0.1){
				$scope.waterStatus = $scope.statusWarnings['OK'];
		} else if (waterVal > waterGoal + 0.5 &&
			waterGoal < waterGoal - 0.5) {
			$scope.waterStatus = $scope.statusWarnings['Caution'];
		} else if (waterVal > waterGoal + 1.0 &&
			waterVal < waterGoal - 1.0) {
			$scope.waterStatus = $scope.statusWarnings['Warning'];
		}
	}

	$scope.compareTemp = function() {
		var tempMin = $scope.goalValues['GoalTempRange'][0];
		var tempMax = $scope.goalValues['GoalTempRange'][1];
		var tempActual = $scope.actualValues['TempActual'];

		if(tempActual > tempMin &&
			tempActual < tempMax) {
			$scope.temperatureStatus = $scope.statusWarnings['OK'];
		} else if(tempActual - tempMin  <= 3 ||  
			tempMax - tempActual <= 3){
			$scope.temperatureStatus = $scope.statusWarnings['Caution'];
		} else if(tempActual - tempMin  > 5 ||  
			tempMax - tempActual > 5){
			$scope.temperatureStatus = $scope.statusWarnings['Warning'];
		} 
	}

	$scope.buttonStatus = function(status, link){
		switch (status) {
            case 0:
                break;
            case 1:
            case 2:
                $window.location.href = link;
                break;
            default:
        }
	}



	// Function to check for notifications
	$scope.checkNotifications = function() {
		$http({
			method:'GET',
			//url:'http://11.11.11.11/notifications',
			url: urlendpoint + '/notifications',
			headers: {
				'Access-Control-Allow-Origin': '*',
        		'Access-Control-Allow-Methods' : 'PUT,GET',
        		'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
			}
		})
		.then(function success(response){
			console.log(response.data);
			for (var i = 0; i < response.data.length; i++) {
				$scope.notifications.push(JSON.parse(response.data[i]));
				console.log(response.data[i]);
			}
			console.log($scope.notifications);
		}, function error(err){
			console.log(err);
		});

	};

	$scope.checkNotifications();

	
});
