'use strict';

var AppDispatcher = require('../dispatcher/AppDispatcher');
var EditConstants = require('../constants/EditConstants');
var EditStore = require('../stores/EditStore');

module.exports = {

  switchTab: function(tabName) {
    AppDispatcher.handleViewAction({
      actionType: EditConstants.SWITCH_TAB,
      tabName: tabName
    })
  },

  addPerk: function() {
    AppDispatcher.handleViewAction({
      actionType: EditConstants.ADD_PERK
    });
  },

  editPerk: function(index) {
    AppDispatcher.handleViewAction({
      actionType: EditConstants.EDIT_PERK,
      index: index
    });
  },

  uneditPerk: function(index) {
    AppDispatcher.handleViewAction({
      actionType: EditConstants.UNEDIT_PERK,
      index: index
    });
  },

  saveItem: function(text) {
    AppDispatcher.handleViewAction({
      actionType: EditConstants.SAVE_ITEM,
      text: text
    });
  },

  removeItem: function(index) {
    AppDispatcher.handleViewAction({
      actionType: EditConstants.REMOVE_ITEM,
      index: index
    });
  },

  updateCampaign: function(data) {
    AppDispatcher.handleViewAction({
      actionType: EditConstants.UPDATE_CAMPAIGN,
      data: data
    });
  },

  updateREST: function(data) {
    AppDispatcher.handleServerAction({
      actionType: EditConstants.UPDATE_REST,
      data: data
    });
  },

  saveCampaign: function() {
    console.log('Saving campaign...');

    var url = 'http://localhost:8000/yeah/rest/campaigns/p655SzwbICQ33UfR';
    $.ajax({
      url: url,
      method: 'PUT',
      dataType: 'json',
      contentType: "application/json",
      data: JSON.stringify(EditStore.getCampaign()),
      success: function(data) {
        AppDispatcher.handleViewAction({
          actionType: EditConstants.UPDATE_REST,
          data: data
        });
      },
      error: function(e) {
        alert("SAVE ERROR: " + e)
      }
    });
  }

};
