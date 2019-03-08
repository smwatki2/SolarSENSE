
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

app.controller('LinkCtrl', function($scope, $window) {

  	$scope.startCollection = function () {
		$window.location.href = "instant";
	}

	$scope.test = function(){
		$scope.gettingAlgorithm();
		$scope.gettingAlgorithmFromSensors();
	}

	$scope.scanSensors = function () {
		$window.location.href = "scan";
	}

	$scope.goToLearn = function () {
		$window.location.href = "http://11.11.11.11/digital_library";
	}

	$scope.goToFarmStatus = function () {
		$window.location.href = "/";
	}

	$scope.goToFieldStatus = function () {
		$window.location.href = "field";
	}


	$scope.openConfig = function () {
		$window.location.href = "config";
	}
});

// TODO: refactor which config options we are still using
app.controller('ConfigCtrl', function($scope,$http,$timeout){

	// $scope.regions = ['Hawaii', 'Rwanda', 'AZTestRegion'];
	$scope.regions = []
	$scope.seasons = ['Spring', 'Summer', 'Winter', 'Fall'];
	$scope.regionCrops = [];

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
	// Update which constraints are saved after refactor
	$scope.saveConstraints = function() {

		var region = regionSelect.options[regionSelect.selectedIndex].value;
		var season = seasonSelect.options[seasonSelect.selectedIndex].value;
		var crop = cropSelect.options[cropSelect.selectedIndex].value;
		var date = document.getElementById('selected_date').value;

		//If the user left one of the required fields blank, don't save
		if (region == "" || season == "" || crop ==  "") {
			return;
		}

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
			// TODO: Make sure error is displayed to the end user so they know it did not save
			$scope.saveMessage = 'Error in Saving Settings. Please Try Again.';
			console.log('There was an error saving constraints');
		});
	};

	$(function() {
		var region_select = $('#region');
		var crop_select = $('#crops');
		region_select.on('change', function() {
			console.log("Region has changed. Updating the Crop List.");
			crop_select.attr('disabled', true);
			crop_select.empty();
			$http({
				method:'GET',
				url:'http://11.11.11.11/getCrops',
				// url: 'http://localhost:5000/getCrops',
				params: {'region': region_select.val()},
				headers: {
					'Access-Control-Allow-Origin': '*',
	        		'Access-Control-Allow-Methods' : 'PUT,GET',
	        		'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
				}
			}).then(function success(response){
				console.log(response.data);
				if (response.data.length == 0) {
					crop_select.append($("<option value disabled selected></option>").text("No Crops Available for this Region"));
				} else {
					crop_select.append($("<option value disabled selected></option>").text("Select a Crop"));
				}
				response.data.forEach(function(element) {
					crop_select.append($("<option></option>").attr("value",element).text(element)); 
				});
				crop_select.attr('disabled', false);
			}, function error(err){
				console.log(err);
			})	
		})
	});
});
