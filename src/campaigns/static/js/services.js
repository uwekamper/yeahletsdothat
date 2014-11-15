"use strict";
module = angular.module("services", ['djangoRESTResources']);

module.factory('Campaign', function (djResource) {
    var resource = djResource('/yeah/rest/campaigns/:key/ ', {key: '@key'});
    return resource;
});

module.factory('Perk', function (djResource) {
    var resource = djResource('/yeah/rest/perks/:id', {id: '@id'});
    return resource;
});

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
