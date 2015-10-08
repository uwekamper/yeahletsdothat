var AppDispatcher = require('../dispatcher/AppDispatcher');
var EditConstants = require('../constants/EditConstants');
var ObjectAssign = require('object-assign');
var EventEmitter = require('events').EventEmitter;

var CHANGE_EVENT = 'change';

// This function creates a new perk object with the default contents.
function getEmptyPerk() {
  return {
    title: 'No title',
    state: 'OK',
    amount: 0.0,
    currency: 'EUR',
    available: 0,
  };
}

// Define the store as an empty array
var _store = {
  activeTab: 'basic',
  goal: 0.0,
  list: [],
  editing: false
};

var _campaign = {
  title: 'Title not loaded',
  perks: [],
};

function updateCampaign(data) {
  for (var key in data) {
    if(typeof data[key] != 'undefined') {
      _campaign[key] = data[key];
    }
  }
  console.log('Campaign updated');
  console.log(_campaign);
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
      EditStore.emit(CHANGE_EVENT);
      break;

    case EditConstants.EDIT_PERK:
      _campaign.perks[action.index].state = 'EDITABLE';
      EditStore.emit(CHANGE_EVENT);
      break;

    case EditConstants.UNEDIT_PERK:
      _campaign.perks[action.index].state = 'OK';
      EditStore.emit(CHANGE_EVENT);
      break;

    case EditConstants.UPDATE_CAMPAIGN:
      updateCampaign(action.data);
      EditStore.emit(CHANGE_EVENT);
      break;

    case EditConstants.UPDATE_REST:
      console.log('DATA: ', action.data);
      _campaign = action.data;
      _campaign.perks = [];
      for (var i = 0; i < _campaign.perks.length; i++) {
        _campaign.perks[i].state = 'OK';
      }
      console.log('_CAMPAIGN' + _campaign);
      EditStore.emit(CHANGE_EVENT);
      break;

//    case EditConstants.SAVE_CAMPAIGN:


    default:
      return true;

  }

});

module.exports = EditStore;
