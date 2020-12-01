angular.module('IPSherlock', [])
    .controller('IPSherlockController', function($http, $timeout, $scope) {
        var sherlock = this;
        var load_promise;
        var load_time = 5000;
        sherlock.ip_info = [];

        var get_data = function() {
            $http.get('api/query')

            .then(function(res) {
                sherlock.ip_info = res.data;
                next_load();
            })

            .catch(function(res) {
                next_load();
            });
        };

        get_data();

        var cancel_next_load = function() {
            $timeout.cancel(load_promise);
        };

        var next_load = function(mill) {
            mill = mill || load_time;

            //Always make sure the last timeout is cleared before starting a new one
            cancel_next_load();
            load_promise = $timeout(get_data, mill);
        };

        //Always clear the timeout when the view is destroyed, otherwise it will keep polling and leak memory
        $scope.$on('$destroy', function() {
            cancel_next_load();
        });
  });