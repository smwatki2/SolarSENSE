/*
	Author: ASU CAPSTONE TEAM 2018
	Date: 11.08.2018
	Description: Controllers for Handling UI data binding and REST request
*/

var app = angular.module('solarsenseApp', ['ui.bootstrap']);

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
	$scope.showStatuses = "status";
	$scope.growthStage = "seed";


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
	$scope.temperatureStatus = 0; // OK (Green)
	$scope.sunlightStatus = 2; // Caution (Yellow)
	$scope.waterStatus = 0; // Warning (Red)

	// Debug Values (Most likely not to be used in final product)
	// $scope.temperature = 70.0;
	// $scope.sunlightTime = 4.0;
	// $scope.waterAmount = 10000.0;

	// Units for data, TODO: add option to toggle unit type
	$scope.temperatureUnits = "°C";
	$scope.sunlightTimeUnits = "Hours";
	$scope.waterAmountUnits = "mm/Day";

	$scope.actualValues = {};
	$scope.goalValues = {};

	$scope.getValues = function() {
		$http({
			method:'GET',
			//url:'http://11.11.11.11/testingAlgorithm',
			url: 'http://localhost:5000/testingAlgorithm',
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

	// $scope.gettingAlgorithmFromSensors = function() {
	// 	$http({
	// 		method:'GET',
	// 		// url:'http://11.11.11.11/testingAlgorithmFromSensors',
	// 		url: 'http://localhost:5000/testingAlgorithmFromSensors',
	// 		headers: {
	// 			'Access-Control-Allow-Origin': '*',
 //        		'Access-Control-Allow-Methods' : 'PUT,GET',
 //        		'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
	// 		}
	// 	}).then(function success(response){
	// 		console.log(response.data);
	// 	}, function error(err){
	// 		console.log(err);
	// 	})
	// }

	$scope.getActualValues = function() {
		$http({
			method: 'GET',
			//url: 'http://11.11.11.11/getActualValues',
			url: 'http://localhost:5000/getActualValues',
			headers:{
				'Access-Control-Allow-Origin': '*',
        		'Access-Control-Allow-Methods' : 'PUT,GET',
        		'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'				
			}
		}).then(function success(response){
			// console.log(response.data);
			$scope.actualValues = response.data;
			console.log($scope.actualValues);
			$scope.getFarmStatus()
		}, function error(err){
			console.log(err);
		});


	};

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
			url: 'http://localhost:5000/notifications',
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
			//url:'http://11.11.11.11/data',
			url: 'http://localhost:5000/data',
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

app.controller('ScanCtrl', function($scope, $timeout, $http) {
  $scope.percent = 0;
  $timeout(function(){
        for(var i = 0; i < 100; i++){
          $scope.percent+=10;
        }
      },1000);
});

app.controller('LearnCtrl', function($scope, $timeout, $http) {
	$scope.goHome = function () {
		$window.location.href = "/"; 
	}
});

app.controller('StatusCtrl', function($scope, $timeout, $http) {
	
	$scope.soilData = [];
	$scope.historicData = [];
	$scope.percent = 0;

	$scope.dataRequestSensor = function() {
		console.log("Calling Sensor Data Object");
		$http({
			method:'GET',
			// When using on development machine, use http://localhost:5000/data
			// When using and deploying on pi, use http://11.11.11.11/data
			//url:'http://11.11.11.11/data',
			url: 'http://localhost:5000/data',
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
			console.log("There was an error getting the Sensor data");
		});
	};
});

app.controller('ConfigCtrl', function($scope,$http,$timeout){

	// $scope.regions = ['Hawaii', 'Rwanda', 'AZTestRegion'];
	$scope.regions = []
	$scope.seasons = ['Spring', 'Summer', 'Winter', 'Fall'];
	$scope.regionCrops = ['Cotton', 'Wheat', 'Alfalfa'];

	$scope.saveSuccessful = false;
	$scope.saveMessage = "";

	let regionSelect = document.getElementById('region');
	let seasonSelect = document.getElementById('season');
	let cropSelect = document.getElementById('crops');

	$scope.didSave = function() {
		if($scope.saveSuccessful){
			return true;
		} else {
			return false;
		}
	}


	$scope.resetSaveAlert = function() {
		$scope.saveSuccessful = false;
	}

	$scope.getRegionCFCollection = function(region) {

		for(var i = 0; i < $scope.regions.length; i++){
			if(region === $scope.regions[i].name){
				console.log($scope.regions[i])
				return $scope.regions[i].cfCollection;
			}
		}

	}

	$scope.getRegion = function() {
		$http({
			method: 'GET',
			//url: 'http://11.11.11.11/getRegions',
			url: 'http://localhost:5000/getRegions',
			headers: {
				'Access-Control-Allow-Origin': '*',
        		'Access-Control-Allow-Methods' : 'GET',
        		'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
			}
		}).then(function success(response){
			console.log(response.data);
			for(var i = 0; i < response.data.length; i++){
				$scope.regions.push(JSON.parse(response.data[i]));
				console.log(response.data[i]);
			}
		}, function error(resposne){
			console.log("There was an error");
		})
	
	}

	$scope.saveConstraints = function() {

		var region = regionSelect.options[regionSelect.selectedIndex].value;
		var season = seasonSelect.options[seasonSelect.selectedIndex].value;
		var crop = cropSelect.options[cropSelect.selectedIndex].value;
		var date = document.getElementById('selected_date').value;

		var constraintObj = {
			"region": region,
			"season": season,
			"crop": crop,
			"date": date,
			"cfCollection" : $scope.getRegionCFCollection(region)
		};

		console.log(constraintObj);

		$http({
			method: 'POST',
			//url: 'http://11.11.11.11/saveConstraints',
			url:'http://localhost:5000/saveConstraints',
			data: constraintObj,
			headers: {
				'Access-Control-Allow-Origin': '*',
        		'Access-Control-Allow-Methods' : 'PUT',
        		'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With',
        		'Content-Type' : 'application/json'
			}
		}).then(function success(response){
			console.log(response.data);
			$scope.saveMessage = 'Save Successful';
			$scope.saveSuccessful = true;
			console.log('Save Successful');
		}, function error(response){
			$scope.saveMessage = 'Error in Saving Settings. Please Try Again.';
			console.log('There was an error saving constraints');
		});
	};
});
