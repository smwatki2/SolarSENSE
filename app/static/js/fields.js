/*
	Author: ASU CAPSTONE TEAM 2018
	Date: 03.19.2019
	Description: Controller for Handling UI data binding and REST request
	             for Fields
*/

var app = angular.module('solarsenseApp', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  	$interpolateProvider.startSymbol('{a');
  	$interpolateProvider.endSymbol('a}');
}]);

app.controller('FieldsCtrl', function($scope, $timeout, $http, $window) {
	$scope.showLoader = true;
	$scope.fields = [];
	$scope.statusLight;
	$scope.statusTemperature;
	$scope.statusMoisture;

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

	$scope.statusWarnings = {
		"WarningHigh" : "-2",
		"CautionHigh" : "-1"
		"OK" : "0",
		"CautionLow" : "1",
		"WarningLow" : "2"
	}

	// dummy function, will load graphic based on status
	$scope.buttonStatus = function(status){
		switch (status) {
			case $scope.statusWarnings.WarningHigh:
				return "/static/img/arrows/+2.PNG";
                break;
			case $scope.statusWarnings.CautionHigh:
				return "/static/img/arrows/+1.PNG";
                break;
            case $scope.statusWarnings.OK:
            	return "/static/img/arrows/0.PNG";
                break;
            case $scope.statusWarnings.CautionLow:
            	return "/static/img/arrows/-1.PNG";
            	break;
            case $scope.statusWarnings.WarningLow:
            	return "/static/img/arrows/-2.PNG";
                break;
            default:
            	return "/static/img/arrows/0.PNG";
            	break;
        }
    }

	$scope.getFields();
});
