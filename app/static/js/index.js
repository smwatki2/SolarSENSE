/*
	Author: ASU CAPSTONE TEAM 2018
	Date: 11.08.2018
	Description: Controllers for Handling UI data binding and REST request
*/

var app = angular.module('solarsenseApp', ['navigation']);

app.config(['$interpolateProvider', function($interpolateProvider) {
  	$interpolateProvider.startSymbol('{a');
  	$interpolateProvider.endSymbol('a}');
}]);

app.controller('HomeCtrl', function($scope, $timeout, $http, $window) {
	$scope.showLoader = false;

	angular.element(document).ready(function() {

	})

	$scope.notifications = [];
	
});
