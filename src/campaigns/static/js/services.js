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