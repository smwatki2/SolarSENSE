var app = angular.module('solarsenseApp', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  	$interpolateProvider.startSymbol('{a');
  	$interpolateProvider.endSymbol('a}');
}]);

app.controller('LinkCtrl', function($scope, $window) {

	$scope.openSensors = function () {
		$window.location.href = "/sensors";
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

app.controller('SensorsCtrl', function($scope,$http,$timeout){
		
		$scope.showLoader = true;
		$scope.sensors = [];
		$scope.fields = [];

		$scope.getSensors = function() {
			$http({
				method:'GET',
				url:'http://0.0.0.0:5000/getSensors',
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
			url:'http://0.0.0.0:5000/getFields',
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

});
