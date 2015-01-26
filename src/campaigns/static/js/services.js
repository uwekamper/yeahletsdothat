"use strict";
var module = angular.module("services", ['ngResource']);

module.factory('Campaign', function ($resource) {
    var resource = $resource('/yeah/rest/campaigns/:key', {key: '@key'},
        {'update': {
            method: 'put'
        }}
    );
    return resource;
});

module.factory('Perk', function ($resource) {
    var resource = $resource('/yeah/rest/perks/:id', {id: '@id'},
        {'update':  {
            method: 'put'}
        }
    );
    return resource;
});

module.directive('dateTimePicker', [function() {
    function link(scope, element, attrs, controller) {
        var format = 'DD/MM/YYYY h:mm a';
        controller.$parsers.push(function (inputValue) {
            return moment(inputValue)
        });
        controller.$formatters.push(function (value) {
            return moment(value).format(format);
        });
        $(element).datetimepicker();
    }

    // put everything together
    return {
        restrict: 'A',
        require: 'ngModel',
        link: link
    };
}]);

var formatAsCurrency = function($locale){
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, element, attrs, controller) {
            var decimal, thousands;
            decimal = '.';
            thousands = ',';
            if ($locale.id.match(/^de/) !== null) {
                decimal = ',';
                thousands = '.';
            }
            controller.$parsers.push(function (inputValue) {
                var num;
                num = accounting.unformat(inputValue, decimal, thousands);
                return num;
            });
            controller.$formatters.push(function (modelValue) {
                var str;
                str = accounting.formatNumber(modelValue, 2, thousands, decimal);
                return str;
            });
            return element.bind('blur', function () {
                if (controller.$modelValue !== void 0) {
                    return element.val(accounting.formatNumber(controller.$modelValue, 2, thousands, decimal));
                }
            });
        }
    };
};

formatAsCurrency['$inject'] = ['$locale'];

module.directive('formatAsCurrency', ['$locale', formatAsCurrency]);

module.filter('currency', function() {

    return function(number) {
        return accounting.formatNumber(number, 2);
    };

});


/*

module.factory('sharedModel', function (Campaign) {
    var sharedModel = {
        campaign: undefined,
        basic_done: false,
        perks_done: false,
        duration_done: false,
        perks: [],
        goal: 23.42,
        currency: 'EUR',
        loadData: function(campaign_key) {
            if (campaign_key === undefined) {
                sharedModel.campaign = new Campaign({currency: 0, goal: 0.0, start_date: new Date(), end_date: new Date()});
            }
            else {
                if (sharedModel.campaign !== undefined && sharedModel.campaign.$resolved) {
                    return;
                }
                sharedModel.campaign = Campaign.get({key: campaign_key});

            }
        }
    };
    // sharedModel.loadData();
    return sharedModel;
});
*/