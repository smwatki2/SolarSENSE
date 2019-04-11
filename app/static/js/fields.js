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
				var thisField = JSON.parse(response.data[i]);
				thisField.light = Math.round(thisField.light);
				thisField.moisture = Math.round(thisField.moisture);
				thisField.temperature = Math.round(thisField.temperature);
				$scope.fields.push(thisField);
			}
			$scope.showLoader = false;
			console.log($scope.fields);
		}, function error(err){
			console.log(err);
			$scope.showLoader = false;
		});
	}

	$scope.getFields();
});
