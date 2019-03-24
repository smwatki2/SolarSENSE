/*
	Author: ASU CAPSTONE TEAM 2018
	Date: 11.08.2018
	Description: Controllers for UI Navigation
*/

var navigation = angular.module('navigation', []);

navigation.controller('LinkCtrl', function($scope, $window) {

	var homeLink = document.getElementById("homeLink"),
		learnLink = document.getElementById("learnLink"),
		configLink = document.getElementById("configLink");

	$scope.goToLearn = function () {
		$window.location.href = "/learn";
	}

	$scope.goToHome = function () {
		$window.location.href = "/";
	}

	$scope.goToConfig = function () {
		$window.location.href = "config";
	}

	angular.element(function() {
		var path = window.location.href;
		var processedPath = path.replace("http://11.11.11.11", "");
		console.log(path);
		console.log(processedPath);
		if (processedPath === '/') {
			configLink.classList.remove("active");
			learnLink.classList.remove("active");
			homeLink.classList.add("active");
		} else if (processedPath === "/learn") {
			homeLink.classList.remove("active");
			configLink.classList.remove("active");
			learnLink.classList.add("active");
		} else if (processedPath === "/config") {
			homeLink.classList.remove("active");
			learnLink.classList.remove("active");
			configLink.classList.add("active");
		}
	});

});
