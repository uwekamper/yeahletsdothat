// var app = app || {};

$(function ($) {

    angular.module("root", [])
        .controller("new_campaign", ["$scope", function($scope) {

            $scope.basic_done = true;
            $scope.active_tab = 'basic';
            $scope.done = true;
        }]);

}(jQuery));