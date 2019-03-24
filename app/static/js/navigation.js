/*
	Author: ASU CAPSTONE TEAM 2018
	Date: 11.08.2018
	Description: Controllers for UI Navigation
*/

var navigation = angular.module('navigation', []);

navigation.controller('LinkCtrl', function($scope, $window) {

	var fieldsLink = document.getElementById("fieldsLink"),
		learnLink = document.getElementById("learnLink"),
		configLink = document.getElementById("configLink"),
		sensorsLink = document.getElementById("sensorsLink");

	$scope.goToLearn = function () {
		$window.location.href = "/learn";
	}

	$scope.goToFields = function () {
		$window.location.href = "/";
	}

	$scope.goToSensors = function () {
		$window.location.href = "/sensors";
	}

	$scope.goToConfig = function () {
		$window.location.href = "/config";
	}

	angular.element(function() {
		var path = window.location.href;
		var processedPath = path.replace("http://11.11.11.11", "");
		console.log(path);
		console.log(processedPath);
		if (processedPath === '/') {
			configLink.classList.remove("active");
			learnLink.classList.remove("active");
			sensorsLink.classList.remove("active");
			fieldsLink.classList.add("active");
		} else if (processedPath === "/learn") {
			fieldsLink.classList.remove("active");
			configLink.classList.remove("active");
			sensorsLink.classList.remove("active");
			learnLink.classList.add("active");
		} else if (processedPath === "/config") {
			fieldsLink.classList.remove("active");
			learnLink.classList.remove("active");
			sensorsLink.classList.remove("active");
			configLink.classList.add("active");
		} else if (processedPath === "/sensors") {
			sensorsLink.classList.add("active");
			learnLink.classList.remove("active");
			fieldsLink.classList.remove("active");
			configLink.classList.remove("active");
		}
	});
});
