var app = angular.module('solarsenseApp', ['navigation']);

app.config(['$interpolateProvider', function($interpolateProvider) {
  	$interpolateProvider.startSymbol('{a');
  	$interpolateProvider.endSymbol('a}');
}]);

app.controller('SensorsCtrl', function($scope,$http,$timeout){
		
		$scope.showLoader = true;
		$scope.sensors = [];
		$scope.fields = [];

		$scope.getSensors = function() {
			$http({
				method:'GET',
				url:'http://11.11.11.11/getSensors',
				headers: {
					'Access-Control-Allow-Origin': '*',
        			'Access-Control-Allow-Methods' : 'PUT,GET',
        			'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
				}
			}).then(function success(response){
				console.log(response.data);
				for (var i = 0; i < response.data.length; i++) {
					$scope.sensors.push(JSON.parse(response.data[i]));
				}
				$scope.showLoader = false;
				console.log($scope.sensors);
				$scope.getFields();
			}, function error(err){
				console.log(err);
				$scope.showLoader = false;
			});	
		}

		$scope.getFields = function () {
		$http({
			method:'GET',
			url:'http://11.11.11.11/getFields',
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

	$scope.getSensors();

	$scope.saveSensor = function(sensor) {

		$scope.sensorData = {
			'mac': sensor.mac,
			'field': sensor.field
		};

		$scope.showLoader = true;

		$http({
			method:'POST',
			url:'http://11.11.11.11/editSensor',
			headers: {
				'Access-Control-Allow-Origin': '*',
				'Access-Control-Allow-Methods' : 'POST',
				'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
			},
			data: $scope.sensorData
		}).then(function success(response){
			$scope.showLoader = false;
		}, function error(err){
			console.log(err);
			$scope.showLoader = false;
		});
	}

	$scope.save = function () {
		for (var i = 0; i < $scope.sensors.length; i++) {
			$scope.saveSensor($scope.sensors[i]);
		}
	}

});
