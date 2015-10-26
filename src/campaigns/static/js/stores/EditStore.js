'use strict';

var AppDispatcher = require('../dispatcher/AppDispatcher');
var EditConstants = require('../constants/EditConstants');
var ObjectAssign = require('object-assign');
var EventEmitter = require('events').EventEmitter;

var CHANGE_EVENT = 'change';

// This function creates a new perk object with the default contents.
function getEmptyPerk() {
  return {
    title: 'No title',
    ui_state: 'OK',
    amount: 0.0,
    currency: 'EUR',
    available: 0
  };
}

// Define the store as an empty array
var _store = {
  activeTab: 'basic',
  goal: 0.0,
  list: [],
  editing: false,
  is_pristine: true
};

var _campaign = {
  title: 'Title not loaded',
  perks: []
};

function updateCampaign(data) {
  for (var key in data) {
    if(typeof data[key] != 'undefined') {
      _campaign[key] = data[key];
    }
  }
  _store.is_pristine = false;
}

// Define the public event listeners and getters that
// the views will use to listen for changes and retrieve
// the store
var EditStore = ObjectAssign( {}, EventEmitter.prototype, {

  addChangeListener: function(cb) {
    this.on(CHANGE_EVENT, cb);
  },

  removeChangeListener: function(cb) {
    this.removeListener(CHANGE_EVENT, cb);
  },

  getPerks: function() {
    return _campaign.perks;
  },

  getActiveTab: function() {
    return _store.activeTab;
  },

  getTitle: function() {
    return _campaign.title
  },

  getCampaign: function() {
    return _campaign;
  },

  getIsPristine: function() {
    return _store.is_pristine;
  }

});

AppDispatcher.register(function(payload) {

  var action = payload.action;

  switch(action.actionType) {

    case EditConstants.SWITCH_TAB:
      // Add the data defined in the TodoActions
      // which the View will pass as a payload
      _store.activeTab = action.tabName;
      EditStore.emit(CHANGE_EVENT);
      break;

    case EditConstants.ADD_PERK:
      _campaign.perks.push(getEmptyPerk());
      _store.is_pristine = false;
      EditStore.emit(CHANGE_EVENT);
      break;

    case EditConstants.EDIT_PERK:
      _campaign.perks[action.index].ui_state = 'EDITABLE';
      EditStore.emit(CHANGE_EVENT);
      break;

    case EditConstants.UNEDIT_PERK:
      _campaign.perks[action.index] = ObjectAssign(_campaign.perks[action.index], action.data);
      _campaign.perks[action.index].ui_state = 'OK';
      _store.is_pristine = false;
      EditStore.emit(CHANGE_EVENT);
      break;

    case EditConstants.DELETE_PERK:
      _campaign.perks[action.index].ui_state = 'DELETED';
      _store.is_pristine = false;
      EditStore.emit(CHANGE_EVENT);
      break;

    case EditConstants.UNDELETE_PERK:
      _campaign.perks[action.index].ui_state = 'OK';
      _store.is_pristine = false;
      EditStore.emit(CHANGE_EVENT);
      break;

    case EditConstants.UPDATE_CAMPAIGN:
      updateCampaign(action.data);
      EditStore.emit(CHANGE_EVENT);
      break;

    case EditConstants.UPDATE_REST:
      _campaign = action.data;
      for (var i = 0; i < _campaign.perks.length; i++) {
        _campaign.perks[i].ui_state = 'OK';
      }
      console.log('_CAMPAIGN' + _campaign);
      _store.is_pristine = true;
      EditStore.emit(CHANGE_EVENT);
      break;

    default:
      return true;

  }

});

module.exports = EditStore;
