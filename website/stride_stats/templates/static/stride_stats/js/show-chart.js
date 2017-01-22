var app = angular.module('statsApp', []);

// Required for csrf
// http://stackoverflow.com/questions/18156452/django-csrf-token-angularjs
app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.controller('statsController', function($scope, $http) {

	$scope.test_variable = 0;
	$scope.axis_labels = [0, 0, 0, 0, 0, 0];
	$scope.values = [12, 19, 3, 5, 2, 3];

	// http://stackoverflow.com/questions/13272406/javascript-string-to-array-conversion
	$scope.getData = function () {
	$scope.current_href = window.location.href.toString()
	// Following convention of /stride_stats/show/(show name here)/
	$scope.path_name = window.location.pathname.toString().split('/')[3]
	// TODO: Remove hard coded url
	// http://stackoverflow.com/questions/1034621/get-current-url-in-web-browser
	$http.get('http://127.0.0.1:8000/stride_stats/show/api/' + $scope.path_name + '/').
        then(function(response) {
        	// http://stackoverflow.com/questions/16830967/variable-keeps-its-old-value-after-exit-jquery-function
        	// Inner function variables passed byval; 
        	// They do not retain value after exiting function
        	// Fix is to call drawChart() within this function
            $scope.show_data = response.data;
            $scope.axis_labels = JSON.parse($scope.show_data['axis_labels']);
            $scope.values = JSON.parse($scope.show_data['values']);
            // $scope.axis_labels = [$scope.path_name, 100, 100, 100, 100, 100];
            $scope.drawChart()
            
        });
        // $scope.axis_labels = [100, 100, 100, 100, 100, 100];
    };

    $scope.getData();

    $scope.drawChart = function () {
		var ctx = document.getElementById("myChart");
		var myChart = new Chart(ctx, {
		    type: 'line',
		    data: {
		        // labels: [0, 1, 2, 3, 4, 5],
		        labels: $scope.axis_labels,
		        datasets: [{
		            label: '# of Votes',
		            // data: [12, 19, 3, 5, 2, 3],
		            data: $scope.values,
		        }]
		    },
		    options: {
		        scales: {
		            yAxes: [{
		                ticks: {
		                    beginAtZero: true
		                }
		            }]
		        }
		    },
		});
	};

    // $scope.drawChart();
});