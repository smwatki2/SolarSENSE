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

});
