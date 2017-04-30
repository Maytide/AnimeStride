var app = angular.module('statsApp', []);

// Required for csrf
// http://stackoverflow.com/questions/18156452/django-csrf-token-angularjs
app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.controller('statsController', function($scope, $http) {
  // $scope.testvar = window.location.protocol + '//' + window.location.hostname + '/stride_recommender/api/random/' + ' ' + window.location.href;
  $scope.genreModel = genreModel;
  numCols = 6;
  partitionSize = parseInt(Math.ceil(genreList.length/numCols));
  $scope.partitionedGenreList = partition(genreList, partitionSize);

  function partition(arr, size) {
    var partitionedList = [];
    for (var i = 0; i < arr.length; i+=size) {
      partitionedList.push(arr.slice(i, i+size));
    }
    return partitionedList;
  }


  $scope.formData = {'search_string': '', 'genre_obj': $scope.genreModel};

	$scope.getData = function () {
  $http.get(window.location.href + 'api/popularity/50').
      then(function(response) {
          $scope.shows = response.data;
          for (var i = 0; i < $scope.shows.length; i++) {

              // Trim underscores
              $scope.shows[i]['display_name'] = $scope.shows[i]['name'].slice(2,-2);
              // Aired is stored as a unix datetime. Display as "mon-year"
              $scope.shows[i]['aired'] = dateToMMYYYY($scope.shows[i]['aired']);
              // Add commas in number
              $scope.shows[i]['members'] = numberFormat($scope.shows[i]['members']);
              // $scope.shows[i]['name'] = makeURLCompatible($scope.shows[i]['name']);
              // Link to show's stats page.
              $scope.shows[i]['stride_url'] = window.location.href +'show/' + makeURLCompatible($scope.shows[i]['name']);
              // alert($scope.shows[i]['name'].replace('/', '&#47'));
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
  $scope.testvar = 'TEST';

  $scope.postData = function () {
    // Deep copy the data
    // alert($scope.formData['search_string']);
    var packagedFormData = JSON.parse(JSON.stringify($scope.formData));
    // alert(packagedFormData['genre_obj'][genreList[0]]);
    // alert(packagedFormData['genre_obj'][genreList[1]]);
    // alert(packagedFormData['genre_obj'][genreList[4]]);
    var genre_bit_sequence = '';
    $scope.testvar = genreList[0];

    if (packagedFormData['search_string'] === ''){
      // alert(packagedFormData['search_string']);
      packagedFormData['search_string'] = '[Query: Genres]';

    }
    // alert(typeof packagedFormData['search_string']);

    for (var i = 0; i < genreList.length; i++){
      // alert(packagedFormData['genre_obj'][genreList[i]] === true);
      // alert(packagedFormData['genre_obj'][genreList[i]]);
      // alert(i);
      // alert(packagedFormData['genre_obj'][genreList[4]]);


      if (packagedFormData['genre_obj'][genreList[i]] === true) {
        genre_bit_sequence += '1';
      } else {
        genre_bit_sequence += '0';
      }

    }
    packagedFormData['genre_obj'] = genre_bit_sequence;

    $http({
        url: window.location.href,
        method: 'POST',
        data: packagedFormData,
    }).
    then(function(response) {
        $scope.shows = response.data;
        for (var i = 0; i < $scope.shows.length; i++) {

            // Trim underscores
            $scope.shows[i]['display_name'] = $scope.shows[i]['name'].slice(2,-2);
            // Aired is stored as a unix datetime. Display as "mon-year"
            $scope.shows[i]['aired'] = dateToMMYYYY($scope.shows[i]['aired']);
            // Add commas in number
            $scope.shows[i]['members'] = numberFormat($scope.shows[i]['members']);
            // $scope.shows[i]['name'] = makeURLCompatible($scope.shows[i]['name']);
            // Link to show's stats page.
            $scope.shows[i]['stride_url'] = window.location.href +'show/' + makeURLCompatible($scope.shows[i]['name']);

            // $scope.shows[i]['stride_url'] = $scope.shows[i]['stride_url'].replace('/', '&#47');

            // Genres and studios contain multiple elements stored in string;
            // Convert to list and pop last element, because it is empty.
            $scope.shows[i]['genres'] = stringToJSON($scope.shows[i]['genres']);
            $scope.shows[i]['genres'].pop();
            $scope.shows[i]['studios'] = stringToJSON($scope.shows[i]['studios']);
            $scope.shows[i]['studios'].pop();
        }
    });
  }


});
