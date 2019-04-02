var app = angular.module('solarsenseApp', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  	$interpolateProvider.startSymbol('{a');
  	$interpolateProvider.endSymbol('a}');
}]);


app.controller('SensorsCtrl', function($scope,$http,$timeout){
		
		$scope.showLoader = true;
		$scope.sensors = [];

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
			}, function error(err){
				console.log(err);
				$scope.showLoader = false;
			});	
		}

		$scope.getSensors();

});
