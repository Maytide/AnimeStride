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
  $http.get(window.location.href + 'stride_stats/api/frontpage/').
	// $http.get('http://127.0.0.1:8000/stride_recommender/api/random/').
      then(function(response) {
          shows_all = response.data;

          for (var key in shows_all){
            if (shows_all.hasOwnProperty(key)) {
              for (var i = 0; i < shows_all[key].length; i++) {
                shows_all[key][i]['genres'] = stringToJSON(shows_all[key][i]['genres']);
                shows_all[key][i]['genres'].pop();
              }
            }
          }

          $scope.shows_random = shows_all['show_list_random'];
          $scope.shows_recent = shows_all['show_list_recent'];
          $scope.shows_recent_popular = shows_all['show_list_recent_popular'];

      });
  };
  $scope.getData()




});
