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