// This implementation is referenced from:
// https://www.jvandemo.com/how-to-configure-your-angularjs-application-using-environment-variables/
// This is needed to move testing from local development to the server

(function(window){
	window.__env = window.__env || {};

	window.__env.serverUrl = "http://11.11.11.11";
	window.__env.enableDebug = true;
}(this));