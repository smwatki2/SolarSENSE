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

app.controller('HomeCtrl', function($scope, $timeout, $http, $window) {
	$scope.showStatuses = "status";
	$scope.growthStage = "germination";

	$scope.temperatureStatus = "";
	$scope.waterStatus = "";


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
			// url: 'http://localhost:5000/getValues',
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
            case status.statusWarnings.OK:
                break;
            case status.statusWarnings.Caution:
            case status.statusWarnings.Warning:
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
			// url: 'http://localhost:5000/notifications',
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
			// url:'http://localhost:5000/changeStage',
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
			//url: 'http://localhost:5000/data',
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
			url:'http://11.11.11.11/data',
			//url: 'http://localhost:5000/data',
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

	$scope.getLat = function(region) {
		for(var i = 0; i < $scope.regions.length; i++){
			if(region === $scope.regions[i].name){
				return $scope.regions[i].lat_direction;
			}
		}
	}

	$scope.getDegree = function(region) {
		for(var i = 0; i < $scope.regions.length; i++){
			if(region === $scope.regions[i].name){
				return $scope.regions[i].degree;
			}
		}
	}

	$scope.getRegion = function() {
		$http({
			method: 'GET',
			url: 'http://11.11.11.11/getRegions',
			// url: 'http://localhost:5000/getRegions',
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
			"cfCollection" : $scope.getRegionCFCollection(region),
			"latDir" : $scope.getLat(region),
			"deg" : $scope.getDegree(region)
		};

		console.log(constraintObj);

		$http({
			method: 'POST',
			url: 'http://11.11.11.11/saveConstraints',
			// url:'http://localhost:5000/saveConstraints',
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
