// Useful link:
// http://stackoverflow.com/questions/14693815/how-to-reload-refresh-model-data-from-the-server-programmatically

var app = angular.module('displayApp', []);

// Required for csrf
// http://stackoverflow.com/questions/18156452/django-csrf-token-angularjs
app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.controller('displayController', function($scope, $http) {
  $scope.testvar = window.location.protocol + '//' + window.location.hostname + '/stride_recommender/api/random/' + ' ' + window.location.href;

	$scope.getData = function () {
  $http.get(window.location.href + 'stride_recommender/api/random/').
	// $http.get('http://127.0.0.1:8000/stride_recommender/api/random/').
      then(function(response) {
          $scope.shows = response.data;
      });
  };
  $scope.getData()




});
