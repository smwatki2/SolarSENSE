/*
	Author: ASU CAPSTONE TEAM 2018
	Date: 11.08.2018
	Description: Controllers for Handling UI data binding and REST request
*/

// TODO: Delete this file after it is transfered to index.js
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

	$scope.goToField = function () {
		$window.location.href = "field";
	}

	$scope.goToLearn = function () {
		$window.location.href = "http://11.11.11.11/digital_library";
	}

	$scope.goToFarmStatus = function () {
		$window.location.href = "/";
	}

	$scope.openConfig = function () {
		$window.location.href = "config";
	}
});

app.controller('FieldCtrl', function($scope, $timeout, $http, $window) {
	$scope.showLoader = true;
	$scope.showStatuses = "status";
	$scope.growthStage = "germination";

	$scope.temperatureStatus = "";
	$scope.waterStatus = "";
	$scope.field_num = 0;
	$scope.fields = [];


	angular.element(document).ready(function() {
		$scope.getValues();
	})

	$scope.notifications = [];
	// Temporary Variables, until we properly pull from databases
	$scope.statusWarnings = {
		"OK" : "0",
		"Caution" : "1",
		"Warning" : "2"
	}
	$scope.cropName = "";
	//$scope.temperatureStatus = 0; // OK (Green)
	//$scope.sunlightStatus = 1; // Caution (Yellow)
	//$scope.waterStatus = 2; // Warning (Red)

	// Debug Values (Most likely not to be used in final product)
	$scope.temperature;
	$scope.sunlightTime;
	$scope.waterAmount;

	// Units for data, TODO: add option to toggle unit type
	$scope.temperatureUnits = "°C";
	$scope.sunlightTimeUnits = "Hours";
	$scope.waterAmountUnits = "mm/Day";

	$scope.actualValues = {};
	$scope.goalValues = {};

	$scope.getValues = function() {
		$http({
			method:'GET',
			url:'http://11.11.11.11/getValues',
			//url: 'http://localhost:5000/getValues',
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
			$scope.showLoader = false;
		}, function error(err){
			console.log(err);
			$scope.showLoader = false;
		})	

	}

	$scope.getFields = function() {
		$scope.fields = [];
		$scope.field_num;
		for (var i = 0; i < $scope.field_num; i++) {
			console.log($scope.fields);
			$scope.fields.push(i);
		}
	}

	$scope.getFarmStatus = function() {
		$scope.compareWater();
		$scope.compareTemp();
		// $scope.compareSunlight();

		$scope.temperature = $scope.actualValues['TempActual'].toFixed(2);
		$scope.sunlightTime = 4.0; // temporary
		$scope.waterAmount = $scope.actualValues['WaterActual'].toFixed(2);
	}

	$scope.compareWater = function(){

		var waterVal = $scope.actualValues['WaterActual'];
		var waterGoal = $scope.goalValues['GoalEvo'];
		var waterMax = waterGoal + 0.2;
		var waterMin = waterGoal - 0.2;
		var waringVal = "";

		if(waterVal > waterMin &&
			waterVal < waterMax) {
			waringVal = $scope.statusWarnings['OK'];
		} else if (
			waterVal - waterMin <= 0.3 ||
			waterMax - waterVal > 0.3) {
			waringVal = $scope.statusWarnings['Caution'];
		} else {
			waringVal = $scope.statusWarnings['Warning'];
		}

		$scope.waterStatus = waringVal;

		console.log("Water Status: " + $scope.waterStatus);
	}

	$scope.compareTemp = function() {
		var tempMin = $scope.goalValues['GoalTempRange'][0];
		var tempMax = $scope.goalValues['GoalTempRange'][1];
		var tempActual = $scope.actualValues['TempActual'];

		var waringVal = "";

		if(tempActual > tempMin &&
			tempActual < tempMax) {
			waringVal = $scope.statusWarnings['OK'];
		} else if(tempActual - tempMin  <= 3 ||  
			tempMax - tempActual <= 3){
			waringVal= $scope.statusWarnings['Caution'];
		} else if(tempActual - tempMin  > 5 ||  
			tempMax - tempActual > 5){
			waringVal = $scope.statusWarnings['Warning'];
		}

		$scope.temperatureStatus = waringVal;

		console.log("Temp Status: " + $scope.temperatureStatus);
	}

	// Add all calls to initialization functions and data resets here
	$scope.reload = function () {
		//$scope.getFarmStatus();
		console.log($scope.growthStage);
		console.log($scope.showStatuses);

			$scope.showStatuses = "status";
			$scope.growthStage = "germination";
			$scope.actualValues = {};
			$scope.goalValues = {};

			$scope.getValues();
	}
	// // TODO: temporary dummy function, replace with actual calculations later
	// $scope.compareSunlight = function() {
	// 	$scope.temperatureStatus = $scope.statusWarnings["OK"];
	// }

	$scope.buttonStatus = function(status, link){
		switch (status) {
            case $scope.statusWarnings.OK:
                break;
            case $scope.statusWarnings.Caution:
            case $scope.statusWarnings.Warning:
                $window.location.href = link;
                break;
            default:
        }
	}



	// Function to check for notifications
	$scope.checkNotifications = function() {
		$http({
			method:'GET',
			url:'http://11.11.11.11/notifications',
			//url: 'http://localhost:5000/notifications',
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

	// $scope.viewStatuses = function () {
	// 	$scope.$apply(function() {
	// 		showStatuses = true;
	// 		console.log($scope.showStatuses);	
	// 	});
	// }
	// $scope.viewData = function () {
	// 	$scope.$apply(function() {
	// 		showStatuses = true;	
	// 		console.log($scope.showStatuses);
	// 	});
	// }

	// Function to switch between crop growth phases
	$scope.changeStage = function (stage) {
		$scope.growthStage = stage;

		var stage = {
			'stage' : stage
		}

		$http({
			method: 'POST',
			url: 'http://11.11.11.11/changeStage',
			//url:'http://localhost:5000/changeStage',
			data: stage,
			headers: {
				'Access-Control-Allow-Origin': '*',
        		'Access-Control-Allow-Methods' : 'POST',
        		'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With',
        		'Content-Type' : 'application/json'
			}
		}).then(function success(response){
			var resObj = response.data;
			$scope.cropName = resObj['CropName'];
			$scope.actualValues = resObj['ActualObj'];
			$scope.goalValues = resObj['GoalObj'];
			$scope.getFarmStatus();	

		}, function error(response){
			console.log("There was an error changing state")
		});
		console.log($scope.growthStage);
	}

	// Function to switch between different views
	$scope.changeView = function (view) {
		$scope.showStatuses = view;
		console.log($scope.showStatuses);
	}
});
