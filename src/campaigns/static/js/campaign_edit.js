"use strict";

var app = angular.module('root', ['services', 'ngToast']);

app.config(function($interpolateProvider) {
      $interpolateProvider.startSymbol('{$');
      $interpolateProvider.endSymbol('$}');
});

app.config(['$httpProvider', function($httpProvider) {
    var token = $('[name=csrfmiddlewaretoken]').val();
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.post['X-CSRFToken'] = token;
}]);

app.controller('EditController', ['$scope', '$window', 'ngToast', 'Campaign', 'Perk',
function($scope, $window, ngToast, Campaign, Perk) {
    var self = this;

    // Initialize models with data passed through in the HTML template.
    self.campaign = new Campaign($window.init);
    self.perks = [];
    self.perksPristine = true;
    for(var i = 0; i < $window.perks.length; i++) {
        self.perks.push( new Perk($window.perks[i]) );
    }
    self.currencies = $window.currencies;

    // default values for a new Perk instance when added
    var DEFAULT_PERK = {
        title: "test",
        amount: 0.0,
        state: 'OK',
        available: 0
    };

    self.getCurrencyDisplay = function() {
        return self.currencies[self.campaign.currency];
    };

    /**
     * Disables the save button while saving is in progress.
     */
    self.startSaving = function() {
        $('#saveButton').attr('value', 'Saving …');
        self.isSaving = true;
    };

    /**
     * Enables the save button after saving was finished.
     */
    self.stopSaving = function() {
        $('#saveButton').attr('value', 'Save');
        self.isSaving = false;
    };

    /**
     * Helper function that saves changes to the perks list.
     */
    self.savePerks = function() {
        for (var i=0; i < self.perks.length; i++) {
            var perk = self.perks[i];
            if (perk.id !== undefined && perk.state == 'DELETED') {
                perk.$delete();
                continue;
            }

            perk.campaign = self.campaign.key;

            if(perk.id !== undefined) {
                perk.$update().catch(function() {
                    alert("error");
                });
            }
            else {
                perk.$save().catch(function () {
                    alert("error");
                });
            }

        }
    };

    /**
     * Called when the user wants to save changes.
     */
    self.onSaveButtonClick = function() {
        self.startSaving();
        self.campaign.$update()
            .then(function() {
                self.stopSaving();
                self.savePerks();
                $scope.editCampaignForm.$setPristine();
                ngToast.create('<span class="glyphicon glyphicon-ok"></span> <strong>Yay!</strong> You changes have been saved.');
            })
            .catch(function() {
                self.stopSaving();
                alert("There was an error. Please try again.")
            });
    };


    self.add_perk = function() {
        self.perks.push(new Perk(DEFAULT_PERK));
        return false;
    };
    self.delete_perk = function(index) {
        self.perks[index].state = 'DELETED';
        return false;
    };
    self.undelete_perk = function(index) {
        self.perks[index].state = 'OK';
        return false;
    };


    /**
     * Returns true when all there are changes to be saved. Used to enable/disable the
     * save button.
     */
    self.isUnsaved = function() {
        if(self.isSaving) {
            return true;
        }

        return $scope.editCampaignForm.$pristine && self.perksPristine;
    };

}]);