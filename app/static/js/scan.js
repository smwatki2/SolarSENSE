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

app.controller('ScanCtrl', function($scope, $timeout, $http) {
  $scope.percent = 0;
  $timeout(function(){
        for(var i = 0; i < 100; i++){
          $scope.percent+=10;
        }
      },1000);
});