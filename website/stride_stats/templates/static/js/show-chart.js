var chartApp = angular.module('chartApp', []);

// Required for csrf
// http://stackoverflow.com/questions/18156452/django-csrf-token-angularjs
chartApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

chartApp.controller('chartController', function($scope, $http) {

	$scope.test_variable = 0;
	$scope.axis_labels = [0, 0, 0, 0, 0, 0];
	$scope.values = [12, 19, 3, 5, 2, 3];

	// function convert(date_array){
  //     for(var i = 0; i < date_array.length; i++){
  //         date_array[i] = moment(date_array[i], 'YYYY-MM-DD HH:mm:ss')
  //     }
  //     return date_array
  // }

	// http://stackoverflow.com/questions/13272406/javascript-string-to-array-conversion
	$scope.getData = function () {
  	$scope.current_href = window.location.href.toString().split('/');
    $scope.current_href.pop();
    $scope.current_href.pop();
  	// Following convention of /stride_stats/show/(show name here)/
  	$scope.path_name = window.location.pathname.toString().split('/')[3];
    $scope.api_path_stats = $scope.current_href.join('/') + '/api/1/' + $scope.path_name;
  	// TODO: Remove hard coded url
  	// http://stackoverflow.com/questions/1034621/get-current-url-in-web-browser
  	// $http.get('http://127.0.0.1:8000/stride_stats/show/api/1/' + $scope.path_name + '/').
    $http.get($scope.api_path_stats).
        then(function(response) {
        	// http://stackoverflow.com/questions/16830967/variable-keeps-its-old-value-after-exit-jquery-function
        	// Inner function variables passed byval;
        	// They do not retain value after exiting function
        	// Fix is to call drawChart() within this function
            $scope.show_data_stats = response.data;
            $scope.axis_labels = $scope.show_data_stats['axis_labels'];
            $scope.values = $scope.show_data_stats['values'];
            // $scope.axis_labels = [$scope.path_name, 100, 100, 100, 100, 100];
            $scope.drawChart()

        });
  };

  $scope.getData();

  $scope.drawChart = function () {
	var ctx = document.getElementById("myChart").getContext('2d');
	var myChart = new Chart(ctx, {
	    type: 'line',

	    data: {
	        // labels: [0, 1, 2, 3, 4, 5],
	        labels: dateToDetailedTime($scope.axis_labels['timestamp']),
	        datasets: [{
	            label: '# of Votes',
	            // data: [12, 19, 3, 5, 2, 3],
	            data: $scope.values['members'],
	        }]
	    },
	    options: {
          responsive: true,
          maintainAspectRatio: false,
	        scales: {
	          xAxes: [{
	          	// Why does having type: 'time', fail?
	          	// ANSWER: Have to declare moment script
	          	// before chart.js script in the
	          	// stats-wrapper.html
	            type: 'time',
	            time: {
	              displayFormats: {
	                'millisecond': 'MMM DD',
	                'second': 'MMM DD',
	                'minute': 'MMM DD',
	                'hour': 'MMM DD',
	                'day': 'MMM DD',
	                'week': 'MMM DD',
	                'month': 'MMM DD',
	                'quarter': 'MMM DD',
	                'year': 'MMM DD',
	              }
	            },
              ticks: {
                  autoSkip: true,
                  maxTicksLimit: 20
              },
	          }],
	        },
	      }
		});
	};

    // $scope.drawChart();
});

/////////////////////////////////////////////////////

var displayApp = angular.module('displayApp', []);

displayApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

displayApp.controller('displayController', function($scope, $http) {
  $scope.x = "asdasd";
  $scope.current_href = window.location.href.toString().split('/');
  $scope.current_href.pop();
  $scope.current_href.pop();
  // Following convention of /stride_stats/show/(show name here)/
  $scope.path_name = window.location.pathname.toString().split('/')[3];
  $scope.api_path_info = $scope.current_href.join('/') + '/api/2/' + $scope.path_name;

  $scope.getData2 = function () {
  $http.get($scope.api_path_info).
      then(function(response) {
          $scope.show = response.data;
      });
  }

  $scope.getData2();

});


// MUST include this wrapper, not just angular.bootstrap!:
// https://blog.mariusschulz.com/2014/10/22/asynchronously-bootstrapping-angularjs-applications-with-server-side-data
angular.element(document).ready(function() {
  angular.bootstrap(document.getElementById("idAppDisplay"), ['displayApp']);
});
