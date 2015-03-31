"use strict";

angular.module('root', ['ngRoute', 'ui.bootstrap', 'services'])
    .config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        $routeProvider.when('/:campaign_key?/basic', {
            controller: 'BasicController',
            templateUrl: '/static/partials/basic.html'
        }).when('/:campaign_key/perks', {
            controller: 'PerksController',
            templateUrl: '/static/partials/perks.html'
        }).when('/:campaign_key/duration', {
            controller: 'DurationController',
            templateUrl: '/static/partials/duration.html'
        }).when('/:campaign_key/finished', {
            controller: 'FinishedController',
            templateUrl: '/static/partials/finished.html'
        }).otherwise({
            redirectTo: '/basic'
        });
    }])
    .controller("BasicController", ["$scope", '$location', '$routeParams', 'sharedModel',
        function($scope, $location, $routeParams, sharedModel) {
        sharedModel.loadData($routeParams.campaign_key);
        $scope.model = sharedModel;


        $scope.active_tab = 'basic';
        $scope.next = function () {
            if ($scope.basicForm.$valid) {

			}
            return false;
        };
        $scope.saveCampaign = function() {
            debugger;
            sharedModel.campaign.$save()
                .$then(function() {
                    sharedModel.basic_done = true;
                    $location.path('/' + $scope.model.campaign.key + '/perks');
                })
                .catch(function() {
                    alert("An error occured");
                });
        };
    }])
    .controller("PerksController", ['$scope', '$routeParams', '$location' ,'sharedModel', 'Perk',
        function($scope, $routeParams, $location, sharedModel, Perk) {
        sharedModel.loadData($routeParams.campaign_key);

        var DEFAULT_MODEL = {
            title: "test",
            amount: 0.0,
            state: 'OK',
            available: 0
        };

        Perk.query({campaign: $routeParams.campaign_key}, function(data) {
            sharedModel.perks = data;
            if (sharedModel.perks.length < 1) {
                $scope.model.perks.push(new Perk(DEFAULT_MODEL));
            }
        });
        $scope.model = sharedModel;
        $scope.active_tab = 'perks';

        $scope.add_perk = function() {
            $scope.model.perks.push(new Perk(DEFAULT_MODEL));
            return false;
        };
        $scope.delete_perk = function(index) {
            $scope.model.perks[index].state = 'DELETED';
            return false;
        };
        $scope.undelete_perk = function(index) {
            $scope.model.perks[index].state = 'OK';
            return false;
        };

        $scope.perks_sum = function() {
            var sum = 0.0;
            for(var i=0; i < $scope.model.perks.length; i++) {

                var perk = $scope.model.perks[i];
                if(perk.state == 'OK' || perk.state == 'EDITABLE') {
                    sum += parseFloat(perk.amount, 10) * parseInt(perk.available);
                }

            }
            return sum;
        };

        $scope.savePerks = function() {
            for (var i=0; i < $scope.model.perks.length; i++) {
                var perk = $scope.model.perks[i];
                if (perk.id !== undefined && perk.state == 'DELETED') {
                    perk.$delete();
                    continue;
                }

                perk.campaign = sharedModel.campaign.id;

                perk.$save()
                    .$then(function() {
                        $location.path('/' + $scope.model.campaign.key + '/duration');
                    })
                    .catch(function() {
                        alert("error");
                    });
            }
            sharedModel.perks_done = true;
        };

    }])
    .controller("DurationController", ['$scope', '$routeParams','sharedModel', function($scope, $routeParams, sharedModel) {
        sharedModel.loadData($routeParams.campaign_key);
        $scope.model = sharedModel;

        $scope.active_tab = 'duration';

        $scope.saveDuration = function() {
            sharedModel.campaign.$save().$then(function() {

            });
        };

        $scope.today = function () {
            sharedModel.campaign.start_date = new Date();
            sharedModel.campaign.end_date = new Date();
        };
        $scope.today();

        $scope.clear_start = function () {
            sharedModel.campaign.start_date = null;
        };

        $scope.clear_end = function () {
            sharedModel.campaign.end_date = null;
        };

        // Disable weekend selection
        $scope.disabled = function (date, mode) {
            return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );
        };

        $scope.toggleMin = function () {
            $scope.minDate = $scope.minDate ? null : new Date();
        };
        $scope.toggleMin();

        $scope.open_start = function ($event) {
            $event.preventDefault();
            $event.stopPropagation();

            $scope.opened_start = true;
        };

        $scope.open_end = function ($event) {
            $event.preventDefault();
            $event.stopPropagation();

            $scope.opened_end = true;
        };

        $scope.dateOptions = {
            formatYear: 'yy',
            startingDay: 1
        };

        $scope.initDate = new Date('2016-15-20');
        $scope.format = 'dd-MMMM-yyyy';


    }])
    .controller('FinishedController', ['$scope', '$routeParams', 'sharedModel', function($scope, $routeParams, sharedModel) {
        sharedModel.loadData($routeParams.campaign_key);
        $scope.model = sharedModel;

        $scope.active_tab = 'finished';
        sharedModel.finished_done = true;
    }]);

