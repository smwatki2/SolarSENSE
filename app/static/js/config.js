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

	$scope.hasNumOfFields = false;
	$scope.numOfFields = "";
	$scope.fieldCount = 0;
	$scope.saveMessage = "";
	$scope.saveSuccessful = false;
	$scope.fields = [];

	$scope.showFields = function() {
		if ($scope.numOfFields > 0){
			$scope.hasNumOfFields = true;
		} 
	};

	$scope.displayFields = function(){

		if(parseInt($scope.numOfFields) !== 0
			&& parseInt($scope.numOfFields) < 100
			&& $scope.numOfFields !== undefined
			&& !isNaN(parseInt($scope.numOfFields))) {
			var fields = parseInt($scope.numOfFields,10);
			$scope.fieldCount = fields;
			$scope.hasNumOfFields = true;
			$scope.generateFieldEntries();
			console.log($scope.fields.length);
		} else {
			$scope.hasNumOfFields = false;
			$scope.fieldMax(parseInt($scope.numOfFields));
		}
	};

	$scope.generateFieldEntries = function(){
		$scope.fields = new Array($scope.fieldCount);
	};

	$scope.fieldMax = function(){
		if($scope.fieldCount > 100){
			$scope.maxMsg = "Number is not valid, must be less than 100!";
			return true;
		}
		return false;
	};

	$scope.resetMaxMsg = function(){
		$scope.maxMsg = "";
	};

	$scope.saveFieldSettings = function(){

		var saveFieldCount = $scope.fieldCount;
		var fieldNames = document.getElementsByName("fieldName");
		var saveArray = new Array();

		for(var i = 0; i < fieldNames.length; i++){
			var nameObj = {
				"fieldName" : fieldNames[i].value
			}
			saveArray.push(nameObj);
		}

		console.log(saveArray);

		var saveObj = {
			"numOfFields" : saveFieldCount,
			"fieldNames" : saveArray
		};

		$http({
			method: 'POST',
			url: 'http://11.11.11.11/saveFieldSettings',
			// url: 'http://localhost:5000/saveFieldSettings',
			data: saveObj,
			headers: {
				'Access-Control-Allow-Origin': '*',
        		'Access-Control-Allow-Methods' : 'POST',
        		'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
			}
		}).then(function success(response){
			var res = response.data;
			console.log(res);
			$scope.saveMessage = res['message'];
			$scope.saveSuccessful = true;
			$scope.numOfFields = "";
			$scope.hasNumOfFields = false;
		}, function error(resposne){
			console.log("There was an error");
		});
	};

	$scope.scanForSensors = function(){
		console.log("Scanning For New Sensors Yo")
		$http({
			method: 'GET',
			url: 'http://11.11.11.11/scanForSensors',
			// url: 'http://localhost:5000/scanForSensors',
			headers: {
				'Access-Control-Allow-Origin': '*',
        		'Access-Control-Allow-Methods' : 'POST',
        		'Access-Control-Allow-Headers' : 'Content-Type, Authorization, Content-Length, X-Requested-With'
			}
		}).then(function success(response){
			var res = response.data;
			console.log(res);
			$scope.saveMessage = res['message'];
			$scope.saveSuccessful = true;
			$scope.numOfFields = "";
			$scope.hasNumOfFields = false;
		}, function error(resposne){
			console.log("There was an error");
		});
	}

	$scope.didSave = function() {
		if($scope.saveSuccessful){
			return true;
		} else {
			return false;
		}
	};

	$scope.resetSaveAlert = function() {
		$scope.saveSuccessful = false;
	};
});
