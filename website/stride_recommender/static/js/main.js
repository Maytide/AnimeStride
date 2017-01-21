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
    // $http.post('http://127.0.0.1:8000/stride_recommender/api/url/').
	// $http.post('http://127.0.0.1:8000/stride_recommender/').
 //        then(function(response) {
 //            $scope.shows = response.data;
 //        });
 //    };
////////////////
        $http({
            url: "http://127.0.0.1:8000/stride_recommender/",
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

// $http.get('/api/random').then(function(result) {
//   angular.forEach(result.data, function(item) {
//     $scope.shows.push(item);
//   });

// var app = angular.module('myApp', []);
//     app.controller('cardsListController', function($scope, $http) {
//         $http.get("http://rest-service.guides.spring.io/greeting")
//                 .success(function(response) {
//                     $scope.shows = response.data;
//                 });
//     });

// var app = angular.module('myApp', []);
// app.controller('cardsListController', function($scope) {
// $scope.shows = []

// $http.get('/api/random').then(function(result) {
//   return angular.forEach(result.data, function(item) {
//     return $scope.shows.push(item);
//   });
// });


//         });