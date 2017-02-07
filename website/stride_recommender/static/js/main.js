// Useful link:
// http://stackoverflow.com/questions/14693815/how-to-reload-refresh-model-data-from-the-server-programmatically

var app = angular.module('recommenderApp', []);

// Required for csrf
// http://stackoverflow.com/questions/18156452/django-csrf-token-angularjs
app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.controller('recommenderController', function($scope, $http) {
	
    $scope.formData = {'url': ''};

    // $http.get('https://maytide.github.io/').
	// TODO: Remove hard coded URL
    // Is this function even being used?
	$scope.getData = function () {
	$http.get('http://127.0.0.1:8000/stride_recommender/api/random/').
        then(function(response) {
            $scope.shows = response.data;
        });
    };
    $scope.postData = function () {
        $http({
            // url: "http://127.0.0.1:8000/stride_recommender/",
            url: window.location.href,
            method: 'POST',
            // data: {'url': '00'},
            data: $scope.formData, 
        }).
        then(function(response) {
            $scope.shows = response.data;
        });
    };
    $scope.getData()




});