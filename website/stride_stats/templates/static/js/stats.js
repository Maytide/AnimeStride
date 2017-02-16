var app = angular.module('statsApp', []);

// Required for csrf
// http://stackoverflow.com/questions/18156452/django-csrf-token-angularjs
app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.controller('statsController', function($scope, $http) {
  $scope.testvar = window.location.protocol + '//' + window.location.hostname + '/stride_recommender/api/random/' + ' ' + window.location.href;

	$scope.getData = function () {
  $http.get(window.location.href + 'api/popularity/50').
      then(function(response) {
          $scope.shows = response.data;
      });
  };
  $scope.getData()




});
