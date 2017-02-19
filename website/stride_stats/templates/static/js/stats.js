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
          for (var i = 0; i < $scope.shows.length; i++) {

              // Aired is stored as a unix datetime. Display as "mon-year"
              $scope.shows[i]['aired'] = dateToMMYYYY($scope.shows[i]['aired']);
              // Add commas in number
              $scope.shows[i]['members'] = numberFormat($scope.shows[i]['members']);
              // Link to show's stats page.
              $scope.shows[i]['stride_url'] = window.location.href +'show/' + $scope.shows[i]['name'];

              // Genres and studios contain multiple elements stored in string;
              // Convert to list and pop last element, because it is empty.
              $scope.shows[i]['genres'] = stringToJSON($scope.shows[i]['genres']);
              $scope.shows[i]['genres'].pop();
              $scope.shows[i]['studios'] = stringToJSON($scope.shows[i]['studios']);
              $scope.shows[i]['studios'].pop();
          }
      });
  };
  $scope.getData()

  $scope.postData = function () {

  }


});
