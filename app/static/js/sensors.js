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

app.controller('SensorsCtrl', function($scope,$http,$timeout){
		
		$scope.showLoader = true;
		$scope.currentSensors = [];
		$scope.sensors = [];
		$scope.fields = [];
		$scope.disabledNames = [];
		$scope.savedSensor = false;
		$scope.saveMsg = "";

		$scope.getSensors = function() {
			$http({
				method:'GET',
				url: __env.serverUrl + '/getSensors',
				headers: {
					'Access-Control-Allow-Origin': '*',
        			'Access-Control-Allow-Methods' : 'PUT,GET',
        			'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
				}
			}).then(function success(response){
				console.log(response.data);
				for (var i = 0; i < response.data.length; i++) {
					sensorInfo = JSON.parse(response.data[i]);
					$scope.sensors.push(sensorInfo);
					$scope.disabledNames.push(sensorInfo['field'])
					console.log(sensorInfo);
				}
				$scope.showLoader = false;
				console.log("Scope Sensors: "+JSON.stringify($scope.sensors));
				$scope.getFields();
			}, function error(err){
				console.log(err);
				$scope.showLoader = false;
			});	
		}

		$scope.getFields = function () {
		$http({
			method:'GET',
			url: __env.serverUrl + '/getSensorFields',
			headers: {
				'Access-Control-Allow-Origin': '*',
				'Access-Control-Allow-Methods' : 'PUT,GET',
				'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
			}
		}).then(function success(response){
			console.log(response.data);
			for (var i = 0; i < response.data.length; i++) {
				$scope.fields.push(JSON.parse(response.data[i]));
			}
			$scope.showLoader = false;
			console.log($scope.fields);

		}, function error(err){
			console.log(err);
			$scope.showLoader = false;
		});
	}

	$scope.disableNamesOnLoad = function() {

		for(var i = 0; i < $scope.sensors; i++){
			$scope.disabledNames.push($scope.sensors[i]['field']);
		}
		console.log("disabled names" + $scope.disabledNames);
	}

	$scope.getSensors();
	$scope.disableNamesOnLoad();


	$scope.saveSensor = function(sensors) {

		// $scope.sensorData = {
		// 	'mac': sensor.mac,
		// 	'field': sensor.field
		// };
		sensorsData = {
			"sensors" : sensors
		}

		$scope.showLoader = true;

		// for(var i = 0; i < $scope.sensors.length; i++){
		// 	console.log("Current Field Settings: " + $scope.sensors);
		// }

		$http({
			method:'POST',
			url: __env.serverUrl + '/editSensor',
			headers: {
				'Access-Control-Allow-Origin': '*',
				'Access-Control-Allow-Methods' : 'POST',
				'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
			},
			data: sensorsData
		}).then(function success(response){
			$scope.showLoader = false;
			// console.log(response.data);
			// alert(response.data);
			$scope.saveMsg = response.data;
			$scope.savedSensor = true;
		}, function error(err){
			console.log(err);
			$scope.showLoader = false;
			$scope.saveMsg = err.data;
			$scope.savedSensor = true;
		});
	}

	$scope.closeSaveMsg = function(index){
		$scope.savedSensor = false;
	}

	$scope.save = function () {
		console.log("Current Sensors: " + JSON.stringify($scope.currentSensors));
		saveMsg = "You are about to assign Fields to Sensors.\nBy doing so any current field data associated with the sensors will be removed.\nContinue?";
		if(confirm(saveMsg)){
			// for (var i = 0; i < $scope.sensors.length; i++) {
			// 	$scope.saveSensor($scope.sensors[i]);
			// }
			$scope.saveSensor($scope.sensors);
		}
	}

});
