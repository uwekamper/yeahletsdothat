
angular.module("root", ['ngRoute', 'services'])
    .config(['$routeProvider', function($routeProvider) {

        $routeProvider.when('/basic', {
            controller: 'BasicController',
            templateUrl: '/static/partials/basic.html'
        }).when('/perks', {
            controller: 'PerksController',
            templateUrl: '/static/partials/perks.html'
        }).when('/duration', {
            controller: 'DurationController',
            templateUrl: '/static/partials/duration.html'
        }).otherwise({
            redirectTo: '/basic'
        });

    }])
    .controller("BasicController", ["$scope", '$location', 'sharedModel', function($scope, $location, sharedModel) {
        $scope.model = sharedModel;
        $scope.active_tab = 'basic';
        $scope.next = function () {
            if ($scope.basicForm.$valid) {
                sharedModel.basic_done = true;
                $location.path('/perks');
			}
            return false;
        };
    }])
    .controller("PerksController", ['$scope', 'sharedModel', function($scope, sharedModel) {
        $scope.model = sharedModel;
        $scope.active_tab = 'perks';
        if (sharedModel.perks.length < 1) {
            sharedModel.perks.push({title: "test", amount: 42.0});
        }

        $scope.add_perk = function () {
             sharedModel.perks.push({title: "test", amount: 23.0});
        };
        $scope.delete_perk = function(index) {
            sharedModel.perks.pop(index);
        }
    }])
    .controller("DurationController", ['$scope', 'sharedModel', function($scope, sharedModel) {
        $scope.model = sharedModel;
        $scope.active_tab = 'duration';
    }]);

