'use strict';

var AppDispatcher = require('../dispatcher/AppDispatcher');
var EditConstants = require('../constants/EditConstants');
var EditStore = require('../stores/EditStore');
var MessageStore = require('../stores/MessageStore');

// Show a message on top of the UI.
function _showMessage(type, message) {
  AppDispatcher.handleViewAction({
    actionType: EditConstants.SHOW_MESSAGE,
    type: type,
    message: message
  });
}

function _hideMessage() {
  AppDispatcher.handleViewAction({
    actionType: EditConstants.HIDE_MESSAGE
  });
}

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

  uneditPerk: function(index, data) {
    AppDispatcher.handleViewAction({
      actionType: EditConstants.UNEDIT_PERK,
      index: index,
      data: data
    });
  },

  deletePerk: function(index) {
    AppDispatcher.handleViewAction({
      actionType: EditConstants.DELETE_PERK,
      index: index
    });
  },

  undeletePerk: function(index) {
    AppDispatcher.handleViewAction({
      actionType: EditConstants.UNDELETE_PERK,
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

  // Save the whole campaing object to the REST backend.
  saveCampaign: function() {
    console.log('Saving campaign...');

    var url = 'http://localhost:8000/yeah/rest/campaigns/p655SzwbICQ33UfR';
    var save_data = EditStore.getCampaign();
    delete save_data.perks;
    $.ajax({
      url: url,
      method: 'PUT',
      dataType: 'json',
      contentType: "application/json",
      data: JSON.stringify(save_data),
      success: function(data) {
        AppDispatcher.handleViewAction({
          actionType: EditConstants.UPDATE_REST,
          data: data
        });
        _showMessage('success', 'Your changes were saved.');
        setTimeout(_hideMessage, 5000);
      },
      error: function(e) {
        alert("SAVE ERROR: " + e);
        _showMessage('danger', 'Error saving.')
      }
    });
  },

  // Show a message on top of the UI.
  showMessage: _showMessage,

  // Show a message on top of the UI.
  hideMessage: _hideMessage

};
