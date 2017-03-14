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

  rec_type_msg = {'empty' : 'No shows found.', 'nonempty' : 'Displaying recommended shows:',
                  'random' : 'Displaying random shows', 'random-popular' : 'Displaying random popular shows. This may occur if user has not rated many shows.',
                  'popular' : 'Displaying popular shows. This may occur if user has not rated many shows.'}

	$scope.getData = function () {
	$http.get(window.location.href + 'api/random/').
        then(function(response) {
            $scope.all = response.data;
            $scope.shows = $scope.all['rec_list'];
            $scope.rec_type = rec_type_msg[$scope.all['rec_type']];
            for (var i = 0; i < $scope.shows.length; i++) {
                $scope.shows[i]['genres'] = stringToJSON($scope.shows[i]['genres']);
                $scope.shows[i]['genres'].pop();
                $scope.shows[i]['studios'] = stringToJSON($scope.shows[i]['studios']);
                $scope.shows[i]['studios'].pop();

                stats_url = window.location.href.toString().split('/');
                stats_url.pop();
                stats_url.pop();
                stats_url = stats_url.join('/') + '/stride_stats/show/' + makeURLCompatible($scope.shows[i]['name']);
                $scope.shows[i]['stride_url'] = stats_url;

            }
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
            $scope.all = response.data;
            $scope.shows = $scope.all['rec_list'];
            $scope.rec_type = rec_type_msg[$scope.all['rec_type']];

            for (var i = 0; i < $scope.shows.length; i++) {
              $scope.shows[i]['genres'] = stringToJSON($scope.shows[i]['genres']);
              $scope.shows[i]['genres'].pop();
              $scope.shows[i]['studios'] = stringToJSON($scope.shows[i]['studios']);
              $scope.shows[i]['studios'].pop();

              stats_url = window.location.href.toString().split('/');
              stats_url.pop();
              stats_url.pop();
              stats_url = stats_url.join('/') + '/stride_stats/show/' + makeURLCompatible($scope.shows[i]['name']);
              $scope.shows[i]['stride_url'] = stats_url;
            }


        });
    };
    $scope.getData()




});
