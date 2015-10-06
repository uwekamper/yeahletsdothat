'use strict';

var AppDispatcher = require('../dispatcher/AppDispatcher');
var EditConstants = require('../constants/EditConstants');

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
  }

};
